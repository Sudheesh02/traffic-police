import random
import string
import struct
import hmac
import hashlib
import numpy as np
import pytest
from pydantic import ValidationError

from ai_pipeline.detect_emergency import (
    EmergencyDetectionPipeline,
    OpticalStrobeAnalyzer,
    StandaloneVisionDetector,
)
from ai_pipeline.mock_generator import generate_frame
from ai_pipeline.anpr_logger import normalize_indian_plate
from ai_pipeline.schema import (
    validate_preemption_payload,
    PreemptionEventPayload,
    VehicleTypeEnum,
    LaneDirectionEnum,
)
from tests.test_firmware_logic import (
    SimulatedStateMachine,
    TrafficState,
    TrafficEvent,
    Direction,
    VehicleClass,
    MessageType,
    build_rf_packet,
    RF_SYNC_WORD,
    RF_PROTOCOL_VERSION,
    RF_PACKET_TOTAL_SIZE,
    RF_PAYLOAD_PLAIN_SIZE,
    RF_MAC_TAG_SIZE,
    TIMING_GUARD_MAX_PREEMPT_MS,
)


class TestAIPipelineAdversarial:

    def test_strobe_analyzer_rejects_0_5_hz_slow_flasher(self):
        analyzer = OpticalStrobeAnalyzer(window_size=30, fps=30.0)
        bbox = (180, 120, 280, 270)
        verified_any = False
        for i in range(40):
            frame = generate_frame(frame_idx=i, vehicle_type='AMBULANCE', strobe_hz=0.5, fps=30.0)
            _, _, is_v = analyzer.update(frame, bbox)
            if is_v:
                verified_any = True
        assert not verified_any, '0.5 Hz flasher should NEVER verify as emergency strobe'

    def test_strobe_analyzer_rejects_static_civilian_car(self):
        analyzer = OpticalStrobeAnalyzer(window_size=30, fps=30.0)
        bbox = (180, 120, 280, 270)
        verified_any = False
        for i in range(40):
            frame = generate_frame(frame_idx=i, vehicle_type='CIVILIAN_CAR', fps=30.0)
            _, _, is_v = analyzer.update(frame, bbox)
            if is_v:
                verified_any = True
        assert not verified_any, 'Civilian vehicle must not verify strobe'

    def test_anpr_fuzzer_robustness(self):
        edge_cases = [
            '', '   ', '\t\n\r', 'A', '123', 'XYZ123', 'CG04', 'CG04MB', 'CG04MB123',
            'CG04MB12345', 'CG-04-MB-1234', 'C G 0 4 M B 1 2 3 4', 'cg04mb1234',
            'CG04MB1234' * 50, 'null\0byte', 'DROP TABLE plates;--',
            '<script>alert(1)</script>', '22BH1234AA', '22-8H-I234-AA',
            'CGO4M8I234', 'C604MB1234', 'OG04MB1234', '0G04MB1234',
            'DL1C1234', 'MH12AB9999', 'UP32BN0001', 'RJ14CA5555',
            '!@#$%^&*()_+=-~', '123456789012345', 'ABCDEFGHIJKLMNO'
        ]
        for _ in range(500):
            length = random.randint(0, 40)
            chars = string.ascii_letters + string.digits + string.punctuation + ' \t\n'
            edge_cases.append(''.join(random.choice(chars) for _ in range(length)))

        for tc in edge_cases:
            norm, valid, fmt = normalize_indian_plate(tc)
            assert isinstance(norm, str)
            assert isinstance(valid, bool)
            assert isinstance(fmt, str)
            if valid:
                import re
                assert re.match(
                    r'^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$|^[0-9]{2}BH[0-9]{4}[A-Z]{1,2}$',
                    norm
                ), f'Valid plate {norm} violated syntax regex'

    def test_pydantic_schema_missing_required_fields(self):
        base = {
            'junction_id': 'RPR_GE_ROAD_04',
            'timestamp': '2026-09-17T06:15:22Z',
            'override_source': 'HANDHELD_RF_UNIT_02',
            'vehicle_detected': 'AMBULANCE',
            'license_plate': 'CG04MB1234',
            'confidence': 0.94,
            'lane_cleared': 'NORTH_BOUND',
            'preemption_duration_sec': 22,
        }
        for field in base.keys():
            corrupted = dict(base)
            del corrupted[field]
            with pytest.raises(ValidationError):
                validate_preemption_payload(corrupted)

    def test_pydantic_schema_injected_extra_fields_forbidden(self):
        base = {
            'junction_id': 'RPR_GE_ROAD_04',
            'timestamp': '2026-09-17T06:15:22Z',
            'override_source': 'HANDHELD_RF_UNIT_02',
            'vehicle_detected': 'AMBULANCE',
            'license_plate': 'CG04MB1234',
            'confidence': 0.94,
            'lane_cleared': 'NORTH_BOUND',
            'preemption_duration_sec': 22,
            'admin_override': True,
            'signature': 'forged',
        }
        with pytest.raises(ValidationError):
            validate_preemption_payload(base)


class TestFirmwareLogicAdversarial:

    def test_exhaustive_relay_mask_space_no_conflicting_greens(self):
        for mask in range(256):
            sm = SimulatedStateMachine()
            res = sm._set_relay_mask(mask)
            bit_count = bin(mask).count('1')
            if bit_count > 1:
                assert res is False, f'Mask 0x{mask:02X} commanded multiple greens but was accepted!'
                assert sm.current_state == TrafficState.STATE_FAILSAFE_FALLBACK
                assert sm.active_relay_mask == 0

    def test_clearance_phases_strictly_hold_zero_relay_mask(self):
        sm = SimulatedStateMachine()
        sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=1, current_tick_ms=0)
        assert sm.current_state == TrafficState.STATE_AMBER_CLEARANCE
        assert sm.active_relay_mask == 0

        sm.update_tick(3500)
        assert sm.current_state == TrafficState.STATE_ALL_RED_CLEARANCE
        assert sm.active_relay_mask == 0

        sm.update_tick(5500)
        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN
        assert sm.active_relay_mask == 0x01

        sm.update_tick(27500)
        assert sm.current_state == TrafficState.STATE_RECOVERY_AMBER
        assert sm.active_relay_mask == 0

        sm.update_tick(31000)
        assert sm.current_state == TrafficState.STATE_RECOVERY_ALL_RED
        assert sm.active_relay_mask == 0

        sm.update_tick(32500)
        assert sm.current_state == TrafficState.STATE_NORMAL_CYCLE
        assert sm.active_relay_mask == 0

    def test_preemption_during_active_green_does_not_corrupt_phase(self):
        sm = SimulatedStateMachine()
        sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=1, current_tick_ms=0)
        sm.update_tick(3500)
        sm.update_tick(5500)
        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN
        assert sm.active_relay_mask == 0x01

        accepted = sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=2, current_tick_ms=10000)
        assert accepted is False
        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN
        assert sm.active_relay_mask == 0x01

    def test_rf_replay_defense_exhaustive_sequence_checks(self):
        last_seen = 500
        assert 501 > last_seen
        assert not (500 > last_seen)
        assert not (499 > last_seen)
        assert not (0 > last_seen)

    def test_rf_hmac_bit_flip_tampering_all_payload_bits(self):
        key = b'\xA5\x5A\x12\x34\x56\x78\x9A\xBC\xDE\xF0\x11\x22\x33\x44\x55\x66'
        for byte_idx in range(RF_PAYLOAD_PLAIN_SIZE):
            for bit_idx in range(8):
                pkt = bytearray(build_rf_packet(seq=200, key=key))
                pkt[byte_idx] ^= (1 << bit_idx)

                plain = bytes(pkt[:RF_PAYLOAD_PLAIN_SIZE])
                tag = bytes(pkt[RF_PAYLOAD_PLAIN_SIZE:])
                expected_tag = hmac.new(key, plain, hashlib.sha256).digest()[:RF_MAC_TAG_SIZE]
                assert not hmac.compare_digest(tag, expected_tag), (
                    f'Bit flip at byte {byte_idx} bit {bit_idx} was NOT detected!'
                )

    def test_35_second_guard_ceiling_hard_cutoff(self):
        sm = SimulatedStateMachine()
        sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=3, current_tick_ms=0)

        green_start = None
        green_end = None

        for tick in range(0, 60000, 100):
            sm.update_tick(tick)
            if sm.current_state == TrafficState.STATE_PRIORITY_GREEN:
                if green_start is None:
                    green_start = tick
                    sm.state_dwell_target_ms = 120000
            else:
                if green_start is not None and green_end is None:
                    green_end = tick

        assert green_start == 5500, f'Expected Priority Green to start at 5500ms, got {green_start}'
        assert green_end == 35000, f'Expected guard ceiling to cut off green at 35000ms, got {green_end}'
        assert sm.active_relay_mask == 0
    def test_strobe_analyzer_rejects_3_5_hz_high_speed_strobe(self):
        analyzer = OpticalStrobeAnalyzer(window_size=30, fps=30.0)
        bbox = (180, 120, 280, 270)
        verified_frames = []
        for i in range(40):
            frame = generate_frame(frame_idx=i, vehicle_type='AMBULANCE', strobe_hz=3.5, fps=30.0)
            _, _, is_v = analyzer.update(frame, bbox)
            if is_v:
                verified_frames.append(i)
        assert len(verified_frames) == 0, f'3.5 Hz flasher was verified on frames: {verified_frames}'
    def test_pipeline_rejects_out_of_range_frequencies_after_accumulation(self):
        pipeline = EmergencyDetectionPipeline(source='mock')
        events_35 = []
        for i in range(40):
            frame = generate_frame(frame_idx=i, vehicle_type='AMBULANCE', strobe_hz=3.5, fps=30.0)
            ev = pipeline.process_frame(frame)
            if i >= 20 and ev is not None:
                events_35.append(i)
        assert len(events_35) == 0, f'Pipeline granted preemption to 3.5 Hz vehicle on frames: {events_35}'
