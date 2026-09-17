"""
Unit tests for SynchroClear-ITS Agentic Preemption Layer.
Verifies all 6 agents and safety guardrails.
"""

import pytest
from ai_pipeline.agentic_layer import (
    AuditGovernanceAgent,
    CorridorPreemptionAgent,
    EmergencyVehicleVerificationAgent,
    GoodSamaritanWhitelistAgent,
    IRCSP12PolicyTimingAgent,
    MVAComplianceGuardrail,
    PreemptionDecisionOrchestrator,
)
from ai_pipeline.schema import LaneDirectionEnum


def test_emergency_verification_agent():
    agent = EmergencyVehicleVerificationAgent()
    # Verified ambulance with valid strobe
    res = agent.verify_vehicle("AMBULANCE", 0.92, True, 1.8)
    assert res["verified"] is True

    # Decoy vehicle with wrong strobe frequency
    res_spoof = agent.verify_vehicle("AMBULANCE", 0.92, True, 0.5)
    assert res_spoof["verified"] is False


def test_irc_policy_timing_agent():
    agent = IRCSP12PolicyTimingAgent()
    schedule = agent.compute_clearance_schedule(queue_pcu=20)
    assert schedule["yellow_sec"] == 3.5
    assert schedule["all_red_sec"] == 2.0
    assert 15 <= schedule["priority_green_sec"] <= 30
    assert schedule["total_inter_green_buffer_sec"] == 5.5


def test_mva_compliance_guardrail():
    guardrail = MVAComplianceGuardrail()
    # Safe clearance
    valid, err = guardrail.validate_safety_invariants(3.5, 2.0, 25, True)
    assert valid is True
    assert err is None

    # Violation: Missing yellow buffer
    invalid, err = guardrail.validate_safety_invariants(1.0, 2.0, 25, True)
    assert invalid is False
    assert "Yellow clearance" in err


def test_good_samaritan_whitelist_agent():
    agent = GoodSamaritanWhitelistAgent()
    plates = [
        {"plate": "CG04AB1234", "crossed_stop_line_red": True, "yielding_trajectory": True},
        {"plate": "CG04CD5678", "crossed_stop_line_red": False, "yielding_trajectory": False},
    ]
    whitelisted = agent.filter_yielding_vehicles(plates, preemption_active=True)
    assert whitelisted == ["CG04AB1234"]


def test_audit_governance_agent_hash_chain():
    agent = AuditGovernanceAgent()
    h1, rec1 = agent.generate_audit_record("J1", {"test": 1}, ["CG04A1"])
    h2, rec2 = agent.generate_audit_record("J1", {"test": 2}, ["CG04A2"])
    assert rec2["prev_hash"] == h1
    assert len(h1) == 64
    assert len(h2) == 64


def test_preemption_decision_orchestrator_e2e():
    orchestrator = PreemptionDecisionOrchestrator()
    decision = orchestrator.evaluate_preemption(
        junction_id="RPR_GE_ROAD_04",
        override_source="HANDHELD_RF_UNIT_02",
        vehicle_type="AMBULANCE",
        chassis_confidence=0.95,
        strobe_detected=True,
        target_lane=LaneDirectionEnum.NORTH_BOUND,
        detected_plates=[{"plate": "CG04MB1234", "crossed_stop_line_red": True, "yielding_trajectory": True}],
        queue_pcu=20,
    )
    assert decision.preemption_approved is True
    assert decision.inter_green_yellow_sec == 3.5
    assert decision.inter_green_all_red_sec == 2.0
    assert decision.whitelisted_plates == ["CG04MB1234"]
    assert decision.telemetry_payload is not None
    assert decision.telemetry_payload.junction_id == "RPR_GE_ROAD_04"
