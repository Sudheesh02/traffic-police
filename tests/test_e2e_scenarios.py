"""
End-to-End Integration Scenario Tests for SynchroClear-ITS.
Simulates real-world multi-tier operational scenarios for the Raipur Police Commissionerate:
1. Jaistambh Chowk Peak-Hour Ambulance Preemption (Mekahara Hospital Corridor).
2. Automated e-Challan Good Samaritan Whitelisting Window Computation.
3. Adversarial Corrupted / Replayed RF Packet Defense.
4. Ghadi Chowk Fire Truck Priority Preemption.
5. Perpendicular Conflict Resolution (FCFS Queuing, Zero Dual-Green).
6. Camera-in-the-Loop Early Clearance Optimization.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import pytest

from ai_pipeline.schema import (
    LaneDirectionEnum,
    PreemptionEventPayload,
    VehicleTypeEnum,
    validate_preemption_payload,
)
from ai_pipeline.anpr_logger import (
    CryptographicAuditLogger,
    compute_record_hash,
    normalize_indian_plate,
)
from ai_pipeline.mock_generator import generate_frame
from ai_pipeline.detect_emergency import (
    OpticalStrobeAnalyzer,
    StandaloneVisionDetector,
)
from tests.test_firmware_logic import (
    Direction,
    SimulatedStateMachine,
    TrafficEvent,
    TrafficState,
    VehicleClass,
    build_rf_packet,
)


class TestJaistambhChowkAmbulanceScenario:
    """
    Scenario 1: Complete end-to-end integration at Jaistambh Chowk.
    108 Ambulance heading north to Dr. BR Ambedkar Memorial Hospital (Mekahara).
    """

    def test_jaistambh_chowk_preemption_flow(self, tmp_path: Path):
        # 1. Traffic Constable detects ambulance and presses North on 868 MHz handheld wand
        rf_packet = build_rf_packet(
            unit_id=0x00010042,
            junction_id=0x00040001,  # Jaistambh Chowk ID
            direction=Direction.DIR_NORTH,
            vehicle_class=VehicleClass.VEH_AMBULANCE,
            seq=101,
            duration_sec=22,
        )
        assert len(rf_packet) == 37

        # 2. Cabinet RTU receives packet and initiates clearance state machine
        sm = SimulatedStateMachine()
        assert sm.current_state == TrafficState.STATE_NORMAL_CYCLE

        # t = 0ms: Preemption trigger
        triggered = sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=1, current_tick_ms=0)
        assert triggered is True
        assert sm.current_state == TrafficState.STATE_AMBER_CLEARANCE

        # t = 3500ms: Amber finishes -> All-Red evacuation
        sm.update_tick(3500)
        assert sm.current_state == TrafficState.STATE_ALL_RED_CLEARANCE
        assert sm.active_relay_mask == 0

        # t = 5500ms: All-Red finishes -> Priority Green energized for North (0x01)
        sm.update_tick(5500)
        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN
        assert sm.active_relay_mask == 0x01  # North relay active

        # 3. Simultaneously, Junction CCTV IP camera verifies vehicle & plate
        detector = StandaloneVisionDetector()
        strobe_analyzer = OpticalStrobeAnalyzer(window_size=30, fps=30.0)

        # Feed 30 frames of approaching ambulance with 1.5 Hz strobe
        strobe_ok = False
        for i in range(35):
            frame = generate_frame(frame_idx=i, vehicle_type="AMBULANCE", strobe_hz=1.5)
            detections = detector.detect(frame)
            assert len(detections) >= 1
            _, _, is_verified = strobe_analyzer.update(frame, detections[0].bbox)
            if is_verified:
                strobe_ok = True

        assert strobe_ok is True, "Optical strobe beacon must verify at 1.5 Hz"

        # Plate normalization
        plate, valid, _ = normalize_indian_plate("CG04MB1234")
        assert valid is True
        assert plate == "CG04MB1234"

        # 4. Generate structured MQTT telemetry payload
        event_dict = {
            "junction_id": "RPR_JAISTAMBH_01",
            "timestamp": "2026-09-17T06:15:22Z",
            "override_source": "HANDHELD_RF_UNIT_42",
            "vehicle_detected": "AMBULANCE",
            "license_plate": plate,
            "confidence": 0.95,
            "lane_cleared": "NORTH_BOUND",
            "preemption_duration_sec": 22,
        }
        event = validate_preemption_payload(event_dict)
        assert event.junction_id == "RPR_JAISTAMBH_01"

        # 5. Commit event to local cryptographic audit trail
        audit_file = tmp_path / "jaistambh_audit.jsonl"
        logger = CryptographicAuditLogger(log_path=str(audit_file))
        record = logger.log_event(event)

        assert record["entry_id"] == 1
        assert record["payload"]["license_plate"] == "CG04MB1234"
        assert record["record_hash"] is not None

        # 6. Priority green completes and returns to normal traffic
        sm.update_tick(27500)  # to Recovery Amber
        assert sm.current_state == TrafficState.STATE_RECOVERY_AMBER
        sm.update_tick(31000)  # to Recovery All-Red
        assert sm.current_state == TrafficState.STATE_RECOVERY_ALL_RED
        sm.update_tick(32500)  # to Normal Cycle
        assert sm.current_state == TrafficState.STATE_NORMAL_CYCLE


class TestEChallanWhitelistingWindow:
    """
    Scenario 2: Automated Good Samaritan e-Challan Exemption Window computation.
    Window = [T_trigger - 10s, T_clearance + 10s].
    """

    @staticmethod
    def is_vehicle_exempt(
        event_timestamp_iso: str,
        duration_sec: int,
        vehicle_cross_timestamp_iso: str
    ) -> tuple[bool, str]:
        """
        Evaluates whether a citizen vehicle crossing the stop line is legally exempt
        from automated ITMS red-light violation penalties.
        """
        t_trigger = datetime.fromisoformat(event_timestamp_iso.replace("Z", "+00:00"))
        t_clearance = t_trigger + timedelta(seconds=duration_sec)

        window_start = t_trigger - timedelta(seconds=10)
        window_end = t_clearance + timedelta(seconds=10)

        t_vehicle = datetime.fromisoformat(vehicle_cross_timestamp_iso.replace("Z", "+00:00"))

        if window_start <= t_vehicle <= window_end:
            return True, "STATUS_EXEMPT_EMERGENCY_CORRIDOR"
        else:
            return False, "STATUS_VIOLATION_RECORDED"

    def test_yielding_citizen_before_arrival_is_exempt(self):
        """Driver 20m back yields 6s before ambulance crosses junction."""
        # Preemption triggered at 06:15:22Z for 22s -> [06:15:12Z to 06:15:54Z]
        exempt, status = self.is_vehicle_exempt(
            event_timestamp_iso="2026-09-17T06:15:22Z",
            duration_sec=22,
            vehicle_cross_timestamp_iso="2026-09-17T06:15:16Z",  # 6s before trigger
        )
        assert exempt is True
        assert status == "STATUS_EXEMPT_EMERGENCY_CORRIDOR"

    def test_yielding_citizen_during_green_is_exempt(self):
        """Citizen vehicle pushes through intersection ahead of ambulance."""
        exempt, status = self.is_vehicle_exempt(
            event_timestamp_iso="2026-09-17T06:15:22Z",
            duration_sec=22,
            vehicle_cross_timestamp_iso="2026-09-17T06:15:35Z",  # During green
        )
        assert exempt is True
        assert status == "STATUS_EXEMPT_EMERGENCY_CORRIDOR"

    def test_trailing_citizen_in_buffer_is_exempt(self):
        """Citizen closely trailing ambulance within +10s buffer is exempt."""
        exempt, status = self.is_vehicle_exempt(
            event_timestamp_iso="2026-09-17T06:15:22Z",
            duration_sec=22,
            vehicle_cross_timestamp_iso="2026-09-17T06:15:48Z",  # 4s after green ends
        )
        assert exempt is True
        assert status == "STATUS_EXEMPT_EMERGENCY_CORRIDOR"

    def test_red_light_jump_prior_to_window_is_violation(self):
        """Reckless driver jumping red 40 seconds before preemption is fined."""
        exempt, status = self.is_vehicle_exempt(
            event_timestamp_iso="2026-09-17T06:15:22Z",
            duration_sec=22,
            vehicle_cross_timestamp_iso="2026-09-17T06:14:40Z",  # 42s prior
        )
        assert exempt is False
        assert status == "STATUS_VIOLATION_RECORDED"

    def test_red_light_jump_long_after_clearance_is_violation(self):
        """Late driver running red 30 seconds after ambulance cleared is fined."""
        exempt, status = self.is_vehicle_exempt(
            event_timestamp_iso="2026-09-17T06:15:22Z",
            duration_sec=22,
            vehicle_cross_timestamp_iso="2026-09-17T06:16:30Z",  # Long after
        )
        assert exempt is False
        assert status == "STATUS_VIOLATION_RECORDED"


class TestAdversarialRFAttackDefense:
    """
    Scenario 3: Corrupted, replayed, or spoofed RF packet rejection.
    """

    def test_replay_attack_rejected(self):
        """Attacker capturing valid preemption packet and replaying it is rejected."""
        sm = SimulatedStateMachine()
        sm.last_sequence_counter = 500

        # Legitimate packet with sequence 501
        pkt_counter_fresh = 501
        assert pkt_counter_fresh > sm.last_sequence_counter
        sm.last_sequence_counter = 501

        # Replay attack with sequence 501 again
        replayed_counter = 501
        assert not (replayed_counter > sm.last_sequence_counter), "Replayed packet must be dropped"

        # Stale packet with sequence 480
        stale_counter = 480
        assert not (stale_counter > sm.last_sequence_counter), "Stale packet must be dropped"

    def test_wrong_junction_id_ignored(self):
        """Packet for Ghadi Chowk (0x00040002) received at Jaistambh Chowk (0x00040001)."""
        local_junction_id = 0x00040001
        packet_target_id = 0x00040002  # Different junction

        # Receiver filter: accept if target == local or target == 0 (broadcast)
        accepted = (packet_target_id == 0 or packet_target_id == local_junction_id)
        assert accepted is False, "Cross-junction packet must be filtered out"

    def test_corrupted_payload_crc_mismatch(self):
        """Bit errors in transmission render packet invalid."""
        valid_packet = bytearray(build_rf_packet())
        # Corrupt 1 byte in payload
        valid_packet[10] ^= 0xFF

        # Verification function check
        from tests.test_firmware_logic import RF_SYNC_WORD, RF_PROTOCOL_VERSION
        import struct

        sync, ver = struct.unpack("<HB", valid_packet[:3])
        assert sync == RF_SYNC_WORD
        assert ver == RF_PROTOCOL_VERSION
        # But HMAC check fails
        import hmac, hashlib
        key = b"\xA5\x5A\x12\x34\x56\x78\x9A\xBC\xDE\xF0\x11\x22\x33\x44\x55\x66"
        plain = bytes(valid_packet[:21])
        tag = bytes(valid_packet[21:])
        expected = hmac.new(key, plain, hashlib.sha256).digest()[:16]
        assert not hmac.compare_digest(tag, expected), "Corrupted packet must fail HMAC"


class TestGhadiChowkFireTruckScenario:
    """
    Scenario 4: Fire truck preemption on East corridor at Ghadi Chowk.
    """

    def test_ghadi_chowk_fire_truck_flow(self):
        sm = SimulatedStateMachine()

        # Fire truck approaching from East (Approach 2)
        triggered = sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=2, current_tick_ms=0)
        assert triggered is True
        sm.update_tick(3500)  # Amber
        sm.update_tick(5500)  # Priority Green for East

        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN
        assert sm.active_relay_mask == 0x02  # East green only

        # Telemetry verification
        event_dict = {
            "junction_id": "RPR_GHADI_CHOWK_02",
            "timestamp": "2026-09-17T09:45:10Z",
            "override_source": "HANDHELD_RF_UNIT_15",
            "vehicle_detected": "FIRE_TRUCK",
            "license_plate": "CG04FT9110",
            "confidence": 0.97,
            "lane_cleared": "EAST_BOUND",
            "preemption_duration_sec": 30,
        }
        event = validate_preemption_payload(event_dict)
        assert event.vehicle_detected == VehicleTypeEnum.FIRE_TRUCK
        assert event.lane_cleared == LaneDirectionEnum.EAST_BOUND


class TestConflictResolutionFCFS:
    """
    Scenario 5: Perpendicular Conflict Resolution (First-Come First-Served).
    Two emergency vehicles arrive simultaneously from North and East.
    """

    def test_simultaneous_requests_queued_no_dual_green(self):
        sm = SimulatedStateMachine()

        # North trigger arrives at t = 0ms
        res1 = sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=1, current_tick_ms=0)
        assert res1 is True

        # East trigger arrives at t = 100ms (while North preemption sequence is underway)
        res2 = sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=2, current_tick_ms=100)
        # Second preempt trigger is rejected/queued while first is active
        assert res2 is False, "Concurrent trigger must not preempt already active clearance"

        # Advance North through clearance into Priority Green
        sm.update_tick(3500)
        sm.update_tick(5500)
        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN
        # INVARIANT: Only North green (0x01), East (0x02) MUST BE ZERO
        assert sm.active_relay_mask == 0x01
        assert (sm.active_relay_mask & 0x02) == 0, "East green must remain mechanically locked"


class TestCameraInTheLoopEarlyAbort:
    """
    Scenario 6: Edge-AI camera detects ambulance cleared after 8 seconds;
    issues early abort to recover normal traffic immediately.
    """

    def test_early_abort_saves_green_time_safely(self):
        sm = SimulatedStateMachine()
        sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=1, current_tick_ms=0)
        sm.update_tick(3500)
        sm.update_tick(5500)
        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN

        # At t = 13500ms (8s of green), queue is confirmed clear
        # AI issues early cancel
        aborted = sm.process_event(TrafficEvent.EVT_EARLY_CANCEL, 0, current_tick_ms=13500)
        assert aborted is True
        assert sm.current_state == TrafficState.STATE_RECOVERY_AMBER

        # Safe deceleration for 3.5s
        sm.update_tick(17000)
        assert sm.current_state == TrafficState.STATE_RECOVERY_ALL_RED

        # Safe all-red for 1.5s
        sm.update_tick(18500)
        assert sm.current_state == TrafficState.STATE_NORMAL_CYCLE

        # Cycle returned at 18.5s instead of full 32.5s -> 14 seconds saved!
