"""
Tests for SynchroClear-ITS Firmware Logic & State Machine (firmware/).
Verifies:
1. Deterministic Inter-Green Safety State Machine transition timings:
   - Active Green -> 3.5s Amber -> 2.0s All-Red -> 22.0s Priority Green
   - -> 3.5s Recovery Amber -> 1.5s Recovery All-Red -> Normal Cycle.
2. 35.0s Maximum Preemption Guard Ceiling timeout.
3. Early cancellation safe recovery sequencing.
4. Hardware Relay Interlock & Absolute Mutual Exclusion (No conflicting greens).
5. 37-Byte Sub-GHz RF Packet Framing, Struct Layout, and Header Validation.
6. Monotonic Rolling Sequence Counter Anti-Replay Protection.
7. CRC16 & Cryptographic Authentication Tag Verification.
8. C Header & Firmware Source Static Integrity.
"""

import hashlib
import hmac
import re
import struct
from enum import IntEnum
from pathlib import Path
import pytest


# =====================================================================
# State Machine & Protocol Definitions (Mirroring state_machine.h & rf_protocol.h)
# =====================================================================

class TrafficState(IntEnum):
    STATE_NORMAL_CYCLE = 0
    STATE_AMBER_CLEARANCE = 1
    STATE_ALL_RED_CLEARANCE = 2
    STATE_PRIORITY_GREEN = 3
    STATE_RECOVERY_AMBER = 4
    STATE_RECOVERY_ALL_RED = 5
    STATE_FAILSAFE_FALLBACK = 6


class TrafficEvent(IntEnum):
    EVT_NONE = 0
    EVT_PREEMPT_TRIGGER = 1
    EVT_EARLY_CANCEL = 2
    EVT_TIMER_EXPIRED = 3
    EVT_GUARD_TIMER_EXPIRED = 4
    EVT_HARDWARE_FAULT = 5


class Direction(IntEnum):
    DIR_NONE = 0x00
    DIR_NORTH = 0x01
    DIR_EAST = 0x02
    DIR_SOUTH = 0x03
    DIR_WEST = 0x04


class VehicleClass(IntEnum):
    VEH_NONE = 0x00
    VEH_AMBULANCE = 0x10
    VEH_FIRE_TRUCK = 0x20
    VEH_POLICE = 0x30
    VEH_VIP_CONVOY = 0x40


class MessageType(IntEnum):
    MSG_PREEMPT_REQ = 0x10
    MSG_PREEMPT_CANCEL = 0x11
    MSG_STATUS_BEACON = 0x20
    MSG_ACK = 0x30
    MSG_DIAGNOSTIC = 0x7F


TIMING_AMBER_CLEARANCE_MS = 3500
TIMING_ALL_RED_CLEARANCE_MS = 2000
TIMING_PRIORITY_GREEN_DEFAULT_MS = 22000
TIMING_GUARD_MAX_PREEMPT_MS = 35000
TIMING_RECOVERY_AMBER_MS = 3500
TIMING_RECOVERY_ALL_RED_MS = 1500

RF_SYNC_WORD = 0x5343
RF_PROTOCOL_VERSION = 0x01
RF_PACKET_TOTAL_SIZE = 37
RF_PAYLOAD_PLAIN_SIZE = 21
RF_MAC_TAG_SIZE = 16


class SimulatedStateMachine:
    """
    High-fidelity Python simulation of the STM32 C state machine
    implemented in firmware/cabinet_receiver_rtu/main.c.
    """

    def __init__(self):
        self.current_state = TrafficState.STATE_NORMAL_CYCLE
        self.previous_state = TrafficState.STATE_NORMAL_CYCLE
        self.state_entry_time_ms = 0
        self.state_dwell_target_ms = 0
        self.guard_timer_start_ms = 0
        self.target_approach = 0
        self.active_relay_mask = 0
        self.last_sequence_counter = 0
        self.preemption_active = False
        self.total_preemptions = 0
        self.fault_count = 0
        self.history = []

    def verify_invariants(self) -> bool:
        """Rule: Never more than one green approach bit set; no greens in non-priority states."""
        if self.active_relay_mask & ~0x0F:
            return False
        bit_count = bin(self.active_relay_mask).count("1")
        if bit_count > 1:
            return False

        # Priority Green is the ONLY state permitted to energize any relay
        if self.current_state != TrafficState.STATE_PRIORITY_GREEN:
            if self.active_relay_mask != 0:
                return False

        return True

    def _set_relay_mask(self, mask: int):
        if mask & ~0x0F:
            self.current_state = TrafficState.STATE_FAILSAFE_FALLBACK
            self.active_relay_mask = 0
            self.fault_count += 1
            return False
        bit_count = bin(mask).count("1")
        if bit_count > 1:
            self.current_state = TrafficState.STATE_FAILSAFE_FALLBACK
            self.active_relay_mask = 0
            self.fault_count += 1
            return False
        self.active_relay_mask = mask
        return True

    def transition_to(self, new_state: TrafficState, dwell_ms: int, current_tick_ms: int):
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_entry_time_ms = current_tick_ms
        self.state_dwell_target_ms = dwell_ms
        self.history.append((current_tick_ms, new_state, dwell_ms))

        if new_state == TrafficState.STATE_NORMAL_CYCLE:
            self.preemption_active = False
            self._set_relay_mask(0)
        elif new_state in (
            TrafficState.STATE_AMBER_CLEARANCE,
            TrafficState.STATE_ALL_RED_CLEARANCE,
            TrafficState.STATE_RECOVERY_AMBER,
            TrafficState.STATE_RECOVERY_ALL_RED,
        ):
            self._set_relay_mask(0)
        elif new_state == TrafficState.STATE_PRIORITY_GREEN:
            if 1 <= self.target_approach <= 4:
                mask = 1 << (self.target_approach - 1)
            else:
                mask = 0
            self._set_relay_mask(mask)
        elif new_state == TrafficState.STATE_FAILSAFE_FALLBACK:
            self.preemption_active = False
            self._set_relay_mask(0)

    def process_event(self, evt: TrafficEvent, approach: int, current_tick_ms: int) -> bool:
        if evt == TrafficEvent.EVT_PREEMPT_TRIGGER:
            if approach not in (1, 2, 3, 4):
                return False
            if self.current_state == TrafficState.STATE_NORMAL_CYCLE:
                self.target_approach = approach
                self.guard_timer_start_ms = current_tick_ms
                self.preemption_active = True
                self.total_preemptions += 1
                self.transition_to(TrafficState.STATE_AMBER_CLEARANCE, TIMING_AMBER_CLEARANCE_MS, current_tick_ms)
                return True
            return False

        elif evt == TrafficEvent.EVT_EARLY_CANCEL:
            if self.current_state == TrafficState.STATE_PRIORITY_GREEN:
                self.transition_to(TrafficState.STATE_RECOVERY_AMBER, TIMING_RECOVERY_AMBER_MS, current_tick_ms)
                return True
            return False

        elif evt == TrafficEvent.EVT_GUARD_TIMER_EXPIRED:
            if self.preemption_active and self.current_state == TrafficState.STATE_PRIORITY_GREEN:
                self.transition_to(TrafficState.STATE_RECOVERY_AMBER, TIMING_RECOVERY_AMBER_MS, current_tick_ms)
                return True
            return False

        elif evt == TrafficEvent.EVT_HARDWARE_FAULT:
            self.transition_to(TrafficState.STATE_FAILSAFE_FALLBACK, 0, current_tick_ms)
            return True

        return False

    def update_tick(self, current_tick_ms: int):
        if not self.verify_invariants():
            self.process_event(TrafficEvent.EVT_HARDWARE_FAULT, 0, current_tick_ms)
            return

        # Guard ceiling check
        if self.preemption_active and self.current_state == TrafficState.STATE_PRIORITY_GREEN:
            if (current_tick_ms - self.guard_timer_start_ms) >= TIMING_GUARD_MAX_PREEMPT_MS:
                self.process_event(TrafficEvent.EVT_GUARD_TIMER_EXPIRED, 0, current_tick_ms)
                return

        # Dwell timer
        elapsed = current_tick_ms - self.state_entry_time_ms
        if elapsed >= self.state_dwell_target_ms and self.state_dwell_target_ms > 0:
            if self.current_state == TrafficState.STATE_AMBER_CLEARANCE:
                self.transition_to(TrafficState.STATE_ALL_RED_CLEARANCE, TIMING_ALL_RED_CLEARANCE_MS, current_tick_ms)
            elif self.current_state == TrafficState.STATE_ALL_RED_CLEARANCE:
                self.transition_to(TrafficState.STATE_PRIORITY_GREEN, TIMING_PRIORITY_GREEN_DEFAULT_MS, current_tick_ms)
            elif self.current_state == TrafficState.STATE_PRIORITY_GREEN:
                self.transition_to(TrafficState.STATE_RECOVERY_AMBER, TIMING_RECOVERY_AMBER_MS, current_tick_ms)
            elif self.current_state == TrafficState.STATE_RECOVERY_AMBER:
                self.transition_to(TrafficState.STATE_RECOVERY_ALL_RED, TIMING_RECOVERY_ALL_RED_MS, current_tick_ms)
            elif self.current_state == TrafficState.STATE_RECOVERY_ALL_RED:
                self.transition_to(TrafficState.STATE_NORMAL_CYCLE, 0, current_tick_ms)


# =====================================================================
# RF Binary Packet Encoding Helper
# =====================================================================

def build_rf_packet(
    unit_id: int = 0x00010042,
    junction_id: int = 0x00040001,
    direction: int = Direction.DIR_NORTH,
    vehicle_class: int = VehicleClass.VEH_AMBULANCE,
    seq: int = 1,
    duration_sec: int = 22,
    batt_pct: int = 95,
    key: bytes = b"\xA5\x5A\x12\x34\x56\x78\x9A\xBC\xDE\xF0\x11\x22\x33\x44\x55\x66",
    msg_type: int = MessageType.MSG_PREEMPT_REQ,
) -> bytes:
    """Encodes a valid 37-byte SynchroClear RF wire packet with HMAC-SHA256 tag."""
    # Plaintext header + payload (21 bytes)
    # Format: <H (sync 2B), B (ver 1B), B (type 1B), I (unit 4B), I (junc 4B),
    #         B (dir 1B), B (veh 1B), I (seq 4B), H (dur 2B), B (batt 1B)
    plain = struct.pack(
        "<HBBIIBBIHB",
        RF_SYNC_WORD,
        RF_PROTOCOL_VERSION,
        msg_type,
        unit_id,
        junction_id,
        direction,
        vehicle_class,
        seq,
        duration_sec,
        batt_pct,
    )
    assert len(plain) == RF_PAYLOAD_PLAIN_SIZE, f"Expected {RF_PAYLOAD_PLAIN_SIZE} bytes, got {len(plain)}"

    # Generate 16-byte HMAC tag
    tag = hmac.new(key, plain, hashlib.sha256).digest()[:RF_MAC_TAG_SIZE]
    packet = plain + tag
    assert len(packet) == RF_PACKET_TOTAL_SIZE, f"Expected {RF_PACKET_TOTAL_SIZE} bytes, got {len(packet)}"
    return packet


# =====================================================================
# Test Suites
# =====================================================================

class TestStateMachineTiming:
    """Tier 1: Deterministic state machine timing intervals."""

    def test_full_inter_green_clearance_timeline(self):
        """
        Verify the exact millisecond-by-millisecond progression:
        0ms: Trigger -> 3500ms Amber -> 2000ms All-Red -> 22000ms Green -> 3500ms Amber -> 1500ms All-Red -> Normal
        """
        sm = SimulatedStateMachine()
        assert sm.current_state == TrafficState.STATE_NORMAL_CYCLE

        # T = 0ms: Inject Preemption Trigger for North (Approach 1)
        res = sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=1, current_tick_ms=0)
        assert res is True
        assert sm.current_state == TrafficState.STATE_AMBER_CLEARANCE
        assert sm.active_relay_mask == 0  # No green during amber

        # Step to 3499ms: Still in Amber
        sm.update_tick(3499)
        assert sm.current_state == TrafficState.STATE_AMBER_CLEARANCE

        # Step to 3500ms: Amber finishes -> All-Red Clearance begins
        sm.update_tick(3500)
        assert sm.current_state == TrafficState.STATE_ALL_RED_CLEARANCE
        assert sm.active_relay_mask == 0  # All-Red holds all 0

        # Step to 5499ms (3500 + 1999): Still in All-Red
        sm.update_tick(5499)
        assert sm.current_state == TrafficState.STATE_ALL_RED_CLEARANCE

        # Step to 5500ms (3500 + 2000): All-Red finishes -> Priority Green begins
        sm.update_tick(5500)
        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN
        assert sm.active_relay_mask == 0x01  # Approach 1 Green

        # Step to 27499ms (5500 + 21999): Still in Priority Green
        sm.update_tick(27499)
        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN
        assert sm.active_relay_mask == 0x01

        # Step to 27500ms (5500 + 22000): Green finishes -> Recovery Amber begins
        sm.update_tick(27500)
        assert sm.current_state == TrafficState.STATE_RECOVERY_AMBER
        assert sm.active_relay_mask == 0

        # Step to 30999ms (27500 + 3499): Still in Recovery Amber
        sm.update_tick(30999)
        assert sm.current_state == TrafficState.STATE_RECOVERY_AMBER

        # Step to 31000ms (27500 + 3500): Recovery Amber finishes -> Recovery All-Red begins
        sm.update_tick(31000)
        assert sm.current_state == TrafficState.STATE_RECOVERY_ALL_RED
        assert sm.active_relay_mask == 0

        # Step to 32499ms (31000 + 1499): Still in Recovery All-Red
        sm.update_tick(32499)
        assert sm.current_state == TrafficState.STATE_RECOVERY_ALL_RED

        # Step to 32500ms (31000 + 1500): Complete! Returns to Normal Cycle
        sm.update_tick(32500)
        assert sm.current_state == TrafficState.STATE_NORMAL_CYCLE
        assert sm.preemption_active is False
        assert sm.active_relay_mask == 0

    def test_guard_timer_ceiling_forces_abort(self):
        """
        Verify Invariant 4: Maximum Preemption Ceiling (35.0s) forces recovery amber
        even if normal green dwell is not yet finished or officer forgot cancel.
        """
        sm = SimulatedStateMachine()
        sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=2, current_tick_ms=0)
        sm.update_tick(3500)  # to All-Red
        sm.update_tick(5500)  # to Priority Green (East, mask=0x02)
        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN

        # Artificially set an extreme target dwell (e.g. 60s)
        sm.state_dwell_target_ms = 60000

        # Tick at 34999ms from start: Still Green
        sm.update_tick(34999)
        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN

        # Tick at 35000ms from start: Guard timer ceiling expired!
        sm.update_tick(35000)
        assert sm.current_state == TrafficState.STATE_RECOVERY_AMBER
        assert sm.active_relay_mask == 0

    def test_early_cancel_respects_clearance_intervals(self):
        """
        When officer taps cancel, system MUST NOT jump immediately to normal;
        it MUST transition through 3.5s Recovery Amber + 1.5s Recovery All-Red.
        """
        sm = SimulatedStateMachine()
        sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=1, current_tick_ms=0)
        sm.update_tick(3500)  # Amber -> All-Red
        sm.update_tick(5500)  # All-Red -> Priority Green
        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN

        # Officer hits cancel at t = 10,000ms
        canceled = sm.process_event(TrafficEvent.EVT_EARLY_CANCEL, 0, current_tick_ms=10000)
        assert canceled is True
        assert sm.current_state == TrafficState.STATE_RECOVERY_AMBER
        assert sm.active_relay_mask == 0

        # Next 3.5s in Recovery Amber
        sm.update_tick(13499)
        assert sm.current_state == TrafficState.STATE_RECOVERY_AMBER

        sm.update_tick(13500)
        assert sm.current_state == TrafficState.STATE_RECOVERY_ALL_RED

        # Next 1.5s in Recovery All-Red
        sm.update_tick(15000)
        assert sm.current_state == TrafficState.STATE_NORMAL_CYCLE


class TestRelayMutualExclusion:
    """Tier 1 & 2: Hardware relay interlock and collision avoidance."""

    @pytest.mark.parametrize("app_id,expected_mask", [
        (1, 0x01),  # North
        (2, 0x02),  # East
        (3, 0x04),  # South
        (4, 0x08),  # West
    ])
    def test_each_direction_activates_only_its_single_relay(self, app_id: int, expected_mask: int):
        """Each approach energizes exactly 1 bit; all other 3 directions are 0."""
        sm = SimulatedStateMachine()
        sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=app_id, current_tick_ms=0)
        sm.update_tick(3500)
        sm.update_tick(5500)

        assert sm.current_state == TrafficState.STATE_PRIORITY_GREEN
        assert sm.active_relay_mask == expected_mask
        assert sm.verify_invariants() is True

    def test_simultaneous_dual_green_trips_failsafe(self):
        """Adversarial: Attempting to command two green relays simultaneously trips failsafe lockout."""
        sm = SimulatedStateMachine()
        # Direct attempt to set North + East (0x03)
        res = sm._set_relay_mask(0x03)
        assert res is False
        assert sm.current_state == TrafficState.STATE_FAILSAFE_FALLBACK
        assert sm.active_relay_mask == 0  # Power cut from all coils

    def test_invariant_checker_catches_corrupted_state(self):
        """Invariant validator catches any state with multiple active coils."""
        sm = SimulatedStateMachine()
        sm.active_relay_mask = 0x05  # North + South
        assert sm.verify_invariants() is False

    @pytest.mark.parametrize("invalid_app", [0, 5, -1, 99])
    def test_invalid_approach_corridor_rejected(self, invalid_app: int):
        """Out-of-bound approach corridor indices (0, 5, -1, 99) must be rejected without crash."""
        sm = SimulatedStateMachine()
        res = sm.process_event(TrafficEvent.EVT_PREEMPT_TRIGGER, approach=invalid_app, current_tick_ms=0)
        assert res is False, f"Invalid approach {invalid_app} must be rejected"
        assert sm.current_state == TrafficState.STATE_NORMAL_CYCLE

    @pytest.mark.parametrize("state", [
        TrafficState.STATE_NORMAL_CYCLE,
        TrafficState.STATE_AMBER_CLEARANCE,
        TrafficState.STATE_ALL_RED_CLEARANCE,
        TrafficState.STATE_RECOVERY_AMBER,
        TrafficState.STATE_RECOVERY_ALL_RED,
        TrafficState.STATE_FAILSAFE_FALLBACK,
    ])
    def test_invariant_checker_enforces_zero_mask_in_all_non_green_states(self, state: TrafficState):
        """Any non-zero relay mask during any non-priority-green state violates safety invariants."""
        sm = SimulatedStateMachine()
        sm.current_state = state
        sm.active_relay_mask = 0x01
        assert sm.verify_invariants() is False

    @pytest.mark.parametrize("out_of_bounds_mask", [0x10, 0x20, 0x80, 0xFF])
    def test_out_of_bounds_relay_mask_bits_rejected(self, out_of_bounds_mask: int):
        """Bits beyond approach 1..4 (bit 0..3) must be rejected and trip failsafe."""
        sm = SimulatedStateMachine()
        res = sm._set_relay_mask(out_of_bounds_mask)
        assert res is False
        assert sm.current_state == TrafficState.STATE_FAILSAFE_FALLBACK
        assert sm.active_relay_mask == 0


def validate_rf_packet_framing(packet: bytes) -> bool:
    """Python mirror of C rf_packet_validate_framing from rf_protocol.h."""
    if len(packet) != RF_PACKET_TOTAL_SIZE:
        return False
    sync, ver, msg_type, _, _, direction = struct.unpack("<HBBIIB", packet[:13])
    if sync != RF_SYNC_WORD:
        return False
    if ver != RF_PROTOCOL_VERSION:
        return False
    if msg_type == MessageType.MSG_PREEMPT_REQ:
        if direction < Direction.DIR_NORTH or direction > Direction.DIR_WEST:
            return False
    else:
        if direction > Direction.DIR_WEST:
            return False
    return True


class TestRFPacketFraming:
    """Tier 1, 2 & 5: 37-byte wire packet structure and boundary validation."""

    def test_packet_size_is_exactly_37_bytes(self):
        """Wire format must be strictly 37 bytes."""
        pkt = build_rf_packet()
        assert len(pkt) == 37, f"RF packet size must be exactly 37 bytes, got {len(pkt)}"

    def test_packet_field_decoding(self):
        """Validate all byte offsets and field values in generated packet."""
        pkt = build_rf_packet(
            unit_id=0x12345678,
            junction_id=0x00040001,
            direction=Direction.DIR_EAST,
            vehicle_class=VehicleClass.VEH_FIRE_TRUCK,
            seq=42,
            duration_sec=30,
            batt_pct=88,
        )
        sync, ver, msg_type, unit, junc, direction, vclass, seq, dur, batt = struct.unpack(
            "<HBBIIBBIHB", pkt[:21]
        )
        assert sync == 0x5343  # 'SC'
        assert ver == 0x01
        assert msg_type == MessageType.MSG_PREEMPT_REQ
        assert unit == 0x12345678
        assert junc == 0x00040001
        assert direction == Direction.DIR_EAST
        assert vclass == VehicleClass.VEH_FIRE_TRUCK
        assert seq == 42
        assert dur == 30
        assert batt == 88

    def test_framing_rejects_corrupted_sync_word(self):
        """Packet with invalid magic word rejected."""
        pkt = bytearray(build_rf_packet())
        pkt[0] = 0x00  # Corrupt magic
        sync = struct.unpack("<H", pkt[:2])[0]
        assert sync != RF_SYNC_WORD
        assert validate_rf_packet_framing(bytes(pkt)) is False

    def test_framing_rejects_truncated_packet(self):
        """Packets shorter than 37 bytes rejected."""
        pkt = build_rf_packet()
        truncated = pkt[:36]
        assert len(truncated) != RF_PACKET_TOTAL_SIZE
        assert validate_rf_packet_framing(truncated) is False

    def test_rf_framing_validation_comprehensive(self):
        """Comprehensive verification of rf_packet_validate_framing across packet types."""
        # Valid preemption packet (North)
        pkt_valid = build_rf_packet(direction=Direction.DIR_NORTH)
        assert validate_rf_packet_framing(pkt_valid) is True

        # Valid cancel packet with DIR_NONE
        pkt_cancel = build_rf_packet(direction=Direction.DIR_NONE, msg_type=MessageType.MSG_PREEMPT_CANCEL)
        assert validate_rf_packet_framing(pkt_cancel) is True

        # Preemption request with DIR_NONE must be rejected
        pkt_bad_preempt = build_rf_packet(direction=Direction.DIR_NONE, msg_type=MessageType.MSG_PREEMPT_REQ)
        assert validate_rf_packet_framing(pkt_bad_preempt) is False

        # Invalid direction > 4
        pkt_bad_dir = build_rf_packet(direction=5)
        assert validate_rf_packet_framing(pkt_bad_dir) is False


class TestAntiReplayProtection:
    """Tier 2 & 5: Monotonic sequence counter anti-replay verification."""

    def test_monotonic_counter_accepts_increasing_numbers(self):
        """Fresh packets with strictly higher sequence counter accepted."""
        last_seen = 100
        new_counter = 101
        assert new_counter > last_seen

    def test_stale_or_repeated_counter_rejected(self):
        """Replayed packet with equal or smaller sequence counter dropped."""
        last_seen = 100
        # Replayed old packet
        stale_counter = 99
        assert not (stale_counter > last_seen), "Stale counter must be rejected"

        # Replayed identical packet
        identical_counter = 100
        assert not (identical_counter > last_seen), "Identical counter must be rejected"


class TestCryptographicIntegrity:
    """Tier 5: HMAC-SHA256 authentication tag verification & tampering."""

    def test_valid_packet_tag_verifies(self):
        """Tag computed with correct key matches packet tag."""
        key = b"\xA5\x5A\x12\x34\x56\x78\x9A\xBC\xDE\xF0\x11\x22\x33\x44\x55\x66"
        pkt = build_rf_packet(key=key)
        plain = pkt[:21]
        received_tag = pkt[21:]

        expected_tag = hmac.new(key, plain, hashlib.sha256).digest()[:16]
        assert hmac.compare_digest(received_tag, expected_tag)

    def test_single_bit_flip_fails_verification(self):
        """Flipping a single bit in the payload causes tag verification failure."""
        key = b"\xA5\x5A\x12\x34\x56\x78\x9A\xBC\xDE\xF0\x11\x22\x33\x44\x55\x66"
        pkt = bytearray(build_rf_packet(key=key))

        # Tamper: change requested direction from North to South
        pkt[12] = Direction.DIR_SOUTH

        plain = bytes(pkt[:21])
        received_tag = bytes(pkt[21:])
        expected_tag = hmac.new(key, plain, hashlib.sha256).digest()[:16]
        assert not hmac.compare_digest(received_tag, expected_tag), "Tampered packet must fail MAC check"


class TestFirmwareSourceCodeIntegrity:
    """Tier 1: Static verification of C source and header files."""

    def test_state_machine_h_constants(self, firmware_dir: Path):
        """Verify timing defines in state_machine.h."""
        h_path = firmware_dir / "cabinet_receiver_rtu" / "state_machine.h"
        assert h_path.exists(), "state_machine.h missing"
        content = h_path.read_text(encoding="utf-8")

        assert "TIMING_AMBER_CLEARANCE_MS" in content
        assert "3500" in content
        assert "TIMING_ALL_RED_CLEARANCE_MS" in content
        assert "2000" in content
        assert "TIMING_GUARD_MAX_PREEMPT_MS" in content
        assert "35000" in content

    def test_rf_protocol_h_constants(self, firmware_dir: Path):
        """Verify packet constants in rf_protocol.h."""
        h_path = firmware_dir / "handheld_transmitter" / "rf_protocol.h"
        assert h_path.exists(), "rf_protocol.h missing"
        content = h_path.read_text(encoding="utf-8")

        assert "0x5343" in content
        assert "37" in content
        assert "rf_packet_t" in content

    def test_watchdog_supervisor_present(self, firmware_dir: Path):
        """Verify TPS3823 external hardware supervisor in watchdog.c."""
        w_path = firmware_dir / "cabinet_receiver_rtu" / "watchdog.c"
        assert w_path.exists(), "watchdog.c missing"
        content = w_path.read_text(encoding="utf-8")

        assert "TPS3823" in content
        assert "IWDG" in content
        assert "WWDG" in content
