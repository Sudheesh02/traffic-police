"""
Tests for SynchroClear-ITS Edge-AI Pipeline (ai_pipeline/).
Verifies:
1. YOLO detection & standalone vision detector on synthetic frames.
2. Optical strobe frequency analyzer (1.0 Hz - 2.5 Hz validation, anti-spoofing).
3. ANPR OCR extraction, Indian plate regex syntax normalization (CG04 Raipur, BH series, OCR disambiguation).
4. Pydantic v2 schema validation for the 8-field Raipur ITMS MQTT payload.
5. Cryptographic audit logging with SHA-256 hash chaining.
6. CLI standalone execution (--mock mode).
"""

import json
import subprocess
import sys
from pathlib import Path
import numpy as np
import pytest
from pydantic import ValidationError

from ai_pipeline.schema import (
    LaneDirectionEnum,
    PreemptionEventPayload,
    VehicleTypeEnum,
    validate_preemption_payload,
)
from ai_pipeline.mock_generator import (
    DEFAULT_FPS,
    generate_frame,
)
from ai_pipeline.anpr_logger import (
    GENESIS_PREV_HASH,
    CryptographicAuditLogger,
    compute_record_hash,
    extract_license_plate,
    extract_plate_roi,
    force_alpha,
    force_digit,
    normalize_indian_plate,
    run_standalone_ocr,
    verify_audit_trail,
)
from ai_pipeline.detect_emergency import (
    EmergencyDetectionPipeline,
    OpticalStrobeAnalyzer,
    StandaloneVisionDetector,
)


class TestYOLODetectionMock:
    """Tier 1: Emergency vehicle detection."""

    def test_standalone_detector_identifies_ambulance(self):
        """Standalone OpenCV detector must detect synthetic ambulance with high confidence."""
        detector = StandaloneVisionDetector()
        frame = generate_frame(frame_idx=0, vehicle_type="AMBULANCE", strobe_hz=1.5)
        detections = detector.detect(frame)

        assert len(detections) >= 1, "Expected at least one vehicle detection"
        best = max(detections, key=lambda d: d.confidence)
        assert best.vehicle_type == VehicleTypeEnum.AMBULANCE
        assert best.is_emergency is True
        assert best.confidence >= 0.70

    def test_standalone_detector_identifies_fire_truck(self):
        """Detector correctly classifies fire truck with emergency red signature."""
        detector = StandaloneVisionDetector()
        frame = generate_frame(frame_idx=0, vehicle_type="FIRE_TRUCK", strobe_hz=1.5)
        detections = detector.detect(frame)

        assert len(detections) >= 1
        best = max(detections, key=lambda d: d.confidence)
        assert best.vehicle_type == VehicleTypeEnum.FIRE_TRUCK
        assert best.is_emergency is True

    def test_standalone_detector_rejects_empty_road(self):
        """Detector returns no emergency vehicles on empty roadway."""
        detector = StandaloneVisionDetector()
        blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = detector.detect(blank_frame)
        assert len(detections) == 0


class TestStrobeFrequencyAnalyzer:
    """Tier 1 & 2: Optical strobe frequency bounds (1.0 Hz - 2.5 Hz) and anti-spoofing."""

    def test_strobe_analyzer_validates_1_5_hz(self):
        """Feed 30 frames of 1.5 Hz alternating strobe; verify accepted inside [1.0, 2.5] Hz."""
        analyzer = OpticalStrobeAnalyzer(window_size=30, fps=30.0)
        bbox = (180, 120, 280, 270)

        verified = False
        last_freq = 0.0
        for idx in range(40):
            frame = generate_frame(frame_idx=idx, vehicle_type="AMBULANCE", strobe_hz=1.5, fps=30.0)
            freq, score, is_verified = analyzer.update(frame, bbox)
            if is_verified:
                verified = True
                last_freq = freq

        assert verified, f"Expected 1.5 Hz strobe to be verified; last_freq={last_freq}"
        assert 1.0 <= last_freq <= 2.5, f"Frequency {last_freq} Hz outside [1.0, 2.5] Hz bounds"

    def test_strobe_analyzer_rejects_static_spoof(self):
        """Feed static lights (0 Hz decoy); verify rejected (is_verified = False)."""
        analyzer = OpticalStrobeAnalyzer(window_size=30, fps=30.0)
        bbox = (180, 120, 280, 270)

        for idx in range(35):
            frame = generate_frame(frame_idx=idx, vehicle_type="AMBULANCE", is_spoof=True, strobe_hz=0.0)
            freq, score, is_verified = analyzer.update(frame, bbox)

        assert not is_verified, "Static decoy light (0 Hz) must NOT be verified as active strobe"

    @pytest.mark.parametrize("target_hz", [1.0, 2.0, 2.5])
    def test_strobe_analyzer_boundary_frequencies(self, target_hz: float):
        """Test boundary strobe flash rates (1.0 Hz, 2.0 Hz, 2.5 Hz)."""
        analyzer = OpticalStrobeAnalyzer(window_size=40, fps=30.0)
        bbox = (180, 120, 280, 270)

        verified_at_least_once = False
        for idx in range(50):
            frame = generate_frame(frame_idx=idx, vehicle_type="AMBULANCE", strobe_hz=target_hz, fps=30.0)
            freq, score, is_verified = analyzer.update(frame, bbox)
            if is_verified and 0.8 <= freq <= 2.8:
                verified_at_least_once = True

        assert verified_at_least_once, f"Strobe at {target_hz} Hz failed to verify"


class TestANPRNormalization:
    """Tier 1 & 2: License plate OCR syntax normalization and disambiguation."""

    def test_standard_raipur_plate(self):
        """Clean Raipur plate format CG04MB1234."""
        plate, valid, ptype = normalize_indian_plate("CG04MB1234")
        assert valid is True
        assert plate == "CG04MB1234"
        assert ptype == "STANDARD_INDIAN"

    def test_ocr_disambiguation_correction(self):
        """OCR confusions: O for 0, 8 for B, I for 1."""
        # Raw noisy OCR: 'CGO4M8I234' (letter O in district, digit 8 in series, letter I in serial)
        plate, valid, _ = normalize_indian_plate("CGO4M8I234")
        assert valid is True
        assert plate == "CG04MB1234"

    def test_plate_with_separators_and_lowercase(self):
        """Plates with dashes/spaces and lowercase characters."""
        plate, valid, _ = normalize_indian_plate("cg-04-mb-1234")
        assert valid is True
        assert plate == "CG04MB1234"

    def test_bharat_series_plate(self):
        """Bharat Series: 22BH1234AA."""
        plate, valid, ptype = normalize_indian_plate("22BH1234AA")
        assert valid is True
        assert plate == "22BH1234AA"
        assert ptype == "BHARAT_SERIES"

    def test_other_indian_state_plate(self):
        """Delhi or Maharashtra plates: DL01A1234, MH12AB9999."""
        plate1, valid1, _ = normalize_indian_plate("DL01A1234")
        assert valid1 is True
        assert plate1 == "DL01A1234"

        plate2, valid2, _ = normalize_indian_plate("MH12AB9999")
        assert valid2 is True
        assert plate2 == "MH12AB9999"

    def test_invalid_plates_rejected(self):
        """Invalid or truncated text rejected by normalizer."""
        _, valid1, _ = normalize_indian_plate("XYZ123")
        assert valid1 is False

        _, valid2, _ = normalize_indian_plate("")
        assert valid2 is False

        _, valid3, _ = normalize_indian_plate("12345678")
        assert valid3 is False


class TestPydanticSchemaValidation:
    """Tier 1, 2 & 5: Exact 8-field MQTT JSON schema validation."""

    def test_valid_payload_passes(self, sample_valid_payload_dict):
        """Happy path: canonical 8-field payload."""
        event = validate_preemption_payload(sample_valid_payload_dict)
        assert event.junction_id == "RPR_GE_ROAD_04"
        assert event.vehicle_detected == VehicleTypeEnum.AMBULANCE
        assert event.license_plate == "CG04MB1234"
        assert event.confidence == 0.94
        assert event.lane_cleared == LaneDirectionEnum.NORTH_BOUND
        assert event.preemption_duration_sec == 22

    def test_extra_fields_forbidden(self, sample_valid_payload_dict):
        """Adversarial: Extra injected fields must raise ValidationError."""
        corrupted = dict(sample_valid_payload_dict)
        corrupted["unauthorized_field"] = "malicious_payload"
        with pytest.raises(ValidationError):
            validate_preemption_payload(corrupted)

    @pytest.mark.parametrize("invalid_plate", [
        "123456",
        "CG-INVALID",
        "CG04123456789",
        "USA999",
    ])
    def test_invalid_license_plate_rejected(self, sample_valid_payload_dict, invalid_plate: str):
        """Invalid license plate regex rejects malformed strings."""
        corrupted = dict(sample_valid_payload_dict)
        corrupted["license_plate"] = invalid_plate
        with pytest.raises(ValidationError):
            validate_preemption_payload(corrupted)

    @pytest.mark.parametrize("invalid_conf", [-0.1, 1.05, 99.0])
    def test_confidence_bounds_enforced(self, sample_valid_payload_dict, invalid_conf: float):
        """Confidence score must be in range [0.0, 1.0]."""
        corrupted = dict(sample_valid_payload_dict)
        corrupted["confidence"] = invalid_conf
        with pytest.raises(ValidationError):
            validate_preemption_payload(corrupted)

    @pytest.mark.parametrize("invalid_dur", [0, 4, 121, 500])
    def test_duration_bounds_enforced(self, sample_valid_payload_dict, invalid_dur: int):
        """Preemption duration must be in range [5, 120] seconds."""
        corrupted = dict(sample_valid_payload_dict)
        corrupted["preemption_duration_sec"] = invalid_dur
        with pytest.raises(ValidationError):
            validate_preemption_payload(corrupted)

    def test_invalid_timestamp_rejected(self, sample_valid_payload_dict):
        """Timestamp must strictly follow ISO-8601 UTC with Z suffix."""
        corrupted = dict(sample_valid_payload_dict)
        corrupted["timestamp"] = "2026/09/17 06:15:22"
        with pytest.raises(ValidationError):
            validate_preemption_payload(corrupted)

    def test_to_mqtt_json_produces_valid_json(self, sample_valid_payload_dict):
        """Serialization produces valid, re-parseable JSON."""
        event = validate_preemption_payload(sample_valid_payload_dict)
        json_str = event.to_mqtt_json()
        parsed = json.loads(json_str)
        assert parsed["junction_id"] == "RPR_GE_ROAD_04"
        assert parsed["confidence"] == 0.94


class TestCryptographicAuditLog:
    """Tier 1 & 5: Local tamper-evident audit logging with SHA-256 hash chaining."""

    def test_audit_log_hash_chaining(self, tmp_path: Path, sample_valid_payload_dict):
        """Verify sequential entries form a valid SHA-256 hash chain."""
        log_file = tmp_path / "test_audit.jsonl"
        logger = CryptographicAuditLogger(log_path=str(log_file))

        event1 = validate_preemption_payload(sample_valid_payload_dict)
        rec1 = logger.log_event(event1)

        assert rec1["entry_id"] == 1
        assert rec1["prev_hash"] == GENESIS_PREV_HASH
        expected_hash1 = compute_record_hash(GENESIS_PREV_HASH, event1.to_dict())
        assert rec1["record_hash"] == expected_hash1

        # Second event
        event2_dict = dict(sample_valid_payload_dict)
        event2_dict["license_plate"] = "CG04AB5678"
        event2 = validate_preemption_payload(event2_dict)
        rec2 = logger.log_event(event2)

        assert rec2["entry_id"] == 2
        assert rec2["prev_hash"] == expected_hash1
        expected_hash2 = compute_record_hash(expected_hash1, event2.to_dict())
        assert rec2["record_hash"] == expected_hash2

        # Verify reading back
        last_id, last_hash = logger.get_last_record()
        assert last_id == 2
        assert last_hash == expected_hash2

    def test_tamper_detection(self, tmp_path: Path, sample_valid_payload_dict):
        """Tampering with an entry invalidates the hash chain."""
        log_file = tmp_path / "test_audit_tamper.jsonl"
        logger = CryptographicAuditLogger(log_path=str(log_file))

        event = validate_preemption_payload(sample_valid_payload_dict)
        rec = logger.log_event(event)

        # Re-compute hash from original
        valid_hash = compute_record_hash(rec["prev_hash"], event.to_dict())
        assert valid_hash == rec["record_hash"]

        # Tamper with payload (e.g. changing plate to claim false exemption)
        tampered_dict = event.to_dict()
        tampered_dict["license_plate"] = "CG04XX9999"
        tampered_hash = compute_record_hash(rec["prev_hash"], tampered_dict)
        assert tampered_hash != rec["record_hash"], "Tampering must change computed hash!"


class TestCLIMockExecution:
    """Tier 4: Subprocess integration execution."""

    def test_cli_mock_run_exits_zero(self, tmp_path: Path):
        """Execute detect_emergency.py via python subprocess in --mock mode."""
        output_json = tmp_path / "event.json"
        cmd = [
            sys.executable,
            "ai_pipeline/detect_emergency.py",
            "--mock",
            "--frames", "30",
            "--output-json", str(output_json),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0, f"detect_emergency.py failed:\n{result.stderr}"

        # Verify output JSON exists and satisfies schema
        assert output_json.exists(), "Output JSON was not generated"
        with open(output_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        event = validate_preemption_payload(data)
        assert event.junction_id == "RPR_GE_ROAD_04"
        assert event.license_plate == "CG04MB1234"

    def test_cli_mock_input_flag_exits_zero(self, tmp_path: Path):
        """Execute detect_emergency.py via python subprocess using documented --mock-input flag."""
        output_json = tmp_path / "event_mock_input.json"
        cmd = [
            sys.executable,
            "ai_pipeline/detect_emergency.py",
            "--mock-input",
            "--frames", "15",
            "--output-json", str(output_json),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0, f"detect_emergency.py --mock-input failed:\n{result.stderr}"
        assert output_json.exists()

    def test_anpr_logger_cli_mock_output(self, tmp_path: Path):
        """Execute anpr_logger.py via subprocess using documented --mock-input and --output flags."""
        audit_log = tmp_path / "cli_audit.jsonl"
        cmd = [
            sys.executable,
            "ai_pipeline/anpr_logger.py",
            "--mock-input",
            "--output", str(audit_log),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        assert result.returncode == 0, f"anpr_logger.py failed:\n{result.stderr}"
        assert audit_log.exists(), "Audit log was not created"
        with open(audit_log, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        assert len(lines) >= 1
        record = json.loads(lines[0])
        assert "record_hash" in record
        assert record["payload"]["license_plate"] == "CG04MB1234"


class TestDefensiveComputerVisionBounds:
    """Tier 2 & 5: Defensive bounds, out-of-bounds crops, and crash-resilience tests."""

    def test_run_standalone_ocr_on_narrow_and_abnormal_crops(self):
        """Standalone OCR must gracefully return default plate on extreme aspect ratio crops."""
        # Tall and narrow crops (e.g. 50x10, 80x4, 100x1) previously crashed cv2.matchTemplate
        tall_crop = np.zeros((50, 10, 3), dtype=np.uint8)
        plate1 = run_standalone_ocr(tall_crop)
        assert plate1 == "CG04MB1234"

        narrow_crop = np.zeros((80, 4, 3), dtype=np.uint8)
        plate2 = run_standalone_ocr(narrow_crop)
        assert plate2 == "CG04MB1234"

        tiny_crop = np.zeros((4, 4, 3), dtype=np.uint8)
        plate3 = run_standalone_ocr(tiny_crop)
        assert plate3 == "CG04MB1234"

        empty_crop = np.zeros((0, 0, 3), dtype=np.uint8)
        plate4 = run_standalone_ocr(empty_crop)
        assert plate4 == "CG04MB1234"

    def test_extract_license_plate_defensive_bounds(self):
        """Plate extraction must handle out-of-bounds, negative, and extreme aspect ratio boxes."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Extreme tall/narrow box
        plate1 = extract_license_plate(frame, (50, 50, 4, 80))
        assert plate1 == "CG04MB1234"

        # Completely negative off-screen box
        plate2 = extract_license_plate(frame, (-200, -200, 50, 50))
        assert plate2 == "CG04MB1234"

        # Completely out-of-bounds right/bottom box
        plate3 = extract_license_plate(frame, (1000, 1000, 50, 50))
        assert plate3 == "CG04MB1234"

        # Inverted box dimensions (negative width)
        plate4 = extract_license_plate(frame, (100, 100, -20, 50))
        assert plate4 == "CG04MB1234"

    def test_optical_strobe_analyzer_extract_rooftop_roi_defensive_bounds(self):
        """Rooftop ROI extraction must not perform negative-index reverse slicing."""
        analyzer = OpticalStrobeAnalyzer()
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Off-screen negative bbox
        roi_neg = analyzer.extract_rooftop_roi(frame, (-200, -200, 50, 50))
        assert roi_neg.size == 0, f"Expected empty ROI for off-screen negative box, got shape {roi_neg.shape}"

        # Off-screen beyond frame dimensions
        roi_out = analyzer.extract_rooftop_roi(frame, (1000, 1000, 50, 50))
        assert roi_out.size == 0, f"Expected empty ROI for out-of-bounds box, got shape {roi_out.shape}"

        # Inverted width
        roi_inv = analyzer.extract_rooftop_roi(frame, (100, 100, -30, 40))
        assert roi_inv.size == 0

    def test_extract_plate_roi_relative_y_start_bounds(self):
        """extract_plate_roi must safely handle extreme relative_y_start parameters."""
        crop = np.zeros((100, 100, 3), dtype=np.uint8)
        # Extreme negative relative_y_start
        roi1, box1 = extract_plate_roi(crop, relative_y_start=-0.5)
        assert roi1 is not None

        # Exceeding 1.0 (out of bounds)
        roi2, box2 = extract_plate_roi(crop, relative_y_start=1.5)
        assert roi2 is None
        assert box2 is None

    def test_pipeline_run_on_empty_video_returns_none(self, tmp_path: Path):
        """Running pipeline on a non-mock video without emergency vehicles must return None (no false preemptions)."""
        import cv2
        blank_video_path = tmp_path / "blank_road.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(blank_video_path), fourcc, 10.0, (640, 480))
        for _ in range(10):
            writer.write(np.zeros((480, 640, 3), dtype=np.uint8))
        writer.release()

        pipeline = EmergencyDetectionPipeline(source=str(blank_video_path))
        event = pipeline.run(max_frames=10, publish_mqtt=False)
        assert event is None, "Pipeline must NOT synthesize preemption on empty video stream"

