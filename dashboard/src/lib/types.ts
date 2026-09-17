export type SignalPhase =
  | 'NORMAL_CYCLE'
  | 'ACTIVE_YELLOW'
  | 'ALL_RED_CLEARANCE'
  | 'PRIORITY_GREEN'
  | 'RECOVERY_YELLOW'
  | 'RECOVERY_ALL_RED';

export type LaneDirection = 'NORTH_BOUND' | 'SOUTH_BOUND' | 'EAST_BOUND' | 'WEST_BOUND';

export interface SignalHeadState {
  red: boolean;
  yellow: boolean;
  green: boolean;
  priorityOverlay: boolean;
}

export interface JunctionData {
  id: string;
  name: string;
  code: string;
  location: string;
  lat: number;
  lng: number;
  currentPhase: SignalPhase;
  phaseRemainingSec: number;
  queuePcu: number;
  averageDelaySec: number;
  emergencyActive: boolean;
  rfSignalDbm: number;
  linkLatencyMs: number;
  signals: Record<LaneDirection, SignalHeadState>;
}

export interface AgentDecisionRecord {
  agentName: string;
  agentRole: string;
  status: 'IDLE' | 'ACTIVE' | 'VERIFIED' | 'GUARDRAIL_BLOCKED';
  confidence: number;
  executionMs: number;
  actionSummary: string;
  evidence: string[];
}

export interface ANPRVehicleRecord {
  id: string;
  timestamp: string;
  plate: string;
  vehicleType: '108_AMBULANCE' | 'FIRE_TENDER' | 'POLICE_PATROL' | 'CITIZEN_CAR' | 'TWO_WHEELER' | 'BUS';
  confidence: number;
  speedKmh: number;
  crossedStopLineOnRed: boolean;
  yieldingToEmergency: boolean;
  status: 'COMPLIANT' | 'EXEMPT_GOOD_SAMARITAN' | 'VIOLATION_PENALIZED';
  challanAmountInr: number;
  exemptReason?: string;
  strobeFrequencyHz?: number;
}

export interface AuditBlock {
  blockHeight: number;
  timestamp: string;
  junctionId: string;
  overrideSource: string;
  vehicleClass: string;
  primaryPlate: string;
  preemptionDurationSec: number;
  whitelistedPlates: string[];
  prevHash: string;
  blockHash: string;
  isTamperProof: boolean;
}
