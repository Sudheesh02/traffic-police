'use client';

import React from 'react';
import { ShieldCheck, Cpu, AlertTriangle, Layers, Zap } from 'lucide-react';
import { JunctionData, SignalPhase } from '../lib/types';

interface JunctionTwinProps {
  junction: JunctionData;
  phase: SignalPhase;
  phaseTimer: number;
  emergencyActive: boolean;
}

export const JunctionTwin: React.FC<JunctionTwinProps> = ({
  junction,
  phase,
  phaseTimer,
  emergencyActive,
}) => {
  // Phase description helper
  const getPhaseBadge = () => {
    switch (phase) {
      case 'ACTIVE_YELLOW':
        return {
          label: '3.5s DECELERATION YELLOW',
          color: 'bg-amber-500/20 text-amber-400 border-amber-500',
        };
      case 'ALL_RED_CLEARANCE':
        return {
          label: '2.0s ALL-RED INTER-GREEN CLEARANCE',
          color: 'bg-red-500/20 text-red-400 border-red-500 animate-pulse',
        };
      case 'PRIORITY_GREEN':
        return {
          label: 'EMERGENCY PRIORITY GREEN (CORRIDOR OPEN)',
          color: 'bg-emerald-500/20 text-emerald-400 border-emerald-500 glow-emerald',
        };
      case 'RECOVERY_YELLOW':
      case 'RECOVERY_ALL_RED':
        return {
          label: 'SIGNAL RECOVERY CYCLE',
          color: 'bg-blue-500/20 text-blue-400 border-blue-500',
        };
      default:
        return {
          label: 'NORMAL ROUND-ROBIN FIXED CYCLE',
          color: 'bg-c2-border text-c2-textMuted border-c2-borderLight',
        };
    }
  };

  const badge = getPhaseBadge();

  return (
    <div className="bg-c2-card border border-c2-border rounded-xl p-4 flex flex-col h-full shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-c2-border/70 pb-3 mb-3">
        <div className="flex items-center space-x-2.5">
          <div className="p-1.5 rounded-lg bg-police-navy border border-police-gold/30">
            <Layers className="w-4 h-4 text-police-gold" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-c2-textBright flex items-center gap-2">
              Junction Physical Twin
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-c2-surface text-police-cyan border border-c2-border">
                {junction.name} ({junction.code})
              </span>
            </h2>
            <p className="text-xs text-c2-textDim">
              Form-C Relay Interlock & Signal State Machine
            </p>
          </div>
        </div>

        {/* Phase Countdown Timer */}
        <div className="flex items-center space-x-2 font-mono">
          <div className="text-right">
            <span className="text-c2-textDim text-[10px] block uppercase">Phase Time</span>
            <span className="text-lg font-bold text-c2-textBright leading-none">
              {phaseTimer.toFixed(1)}s
            </span>
          </div>
        </div>
      </div>

      {/* State Machine Status Bar */}
      <div className={`mb-3 px-3 py-1.5 rounded-lg border text-xs font-mono font-bold flex items-center justify-between ${badge.color}`}>
        <span>{badge.label}</span>
        <span>IRC:SP:12 STANDARDS</span>
      </div>

      {/* 2D/3D Top-Down Intersection Visualizer Canvas */}
      <div className="relative flex-1 min-h-[300px] w-full rounded-lg bg-c2-obsidian border border-c2-borderLight/30 flex items-center justify-center p-2 overflow-hidden">
        <svg className="w-full h-full max-h-[340px]" viewBox="0 0 400 340" fill="none">
          {/* Grass / Ground */}
          <rect width="400" height="340" fill="#0A0E17" />

          {/* North-South Road */}
          <rect x="150" y="0" width="100" height="340" fill="#131B2E" />
          {/* East-West Road */}
          <rect x="0" y="120" width="400" height="100" fill="#131B2E" />

          {/* Intersection Box Zone */}
          <rect x="150" y="120" width="100" height="100" fill="#1E2B48" fillOpacity="0.4" />
          {/* Yellow Box Junction Hatching */}
          <line x1="150" y1="120" x2="250" y2="220" stroke="#F59E0B" strokeWidth="1" strokeDasharray="6 6" />
          <line x1="150" y1="220" x2="250" y2="120" stroke="#F59E0B" strokeWidth="1" strokeDasharray="6 6" />

          {/* Road Markings - North */}
          <line x1="200" y1="0" x2="200" y2="110" stroke="#64748B" strokeWidth="2" strokeDasharray="8 6" />
          <line x1="150" y1="110" x2="250" y2="110" stroke="#FFFFFF" strokeWidth="3" /> {/* Stop Line North */}
          {/* Crosswalk North */}
          <rect x="155" y="112" width="12" height="6" fill="#FFFFFF" fillOpacity="0.4" />
          <rect x="175" y="112" width="12" height="6" fill="#FFFFFF" fillOpacity="0.4" />
          <rect x="195" y="112" width="12" height="6" fill="#FFFFFF" fillOpacity="0.4" />
          <rect x="215" y="112" width="12" height="6" fill="#FFFFFF" fillOpacity="0.4" />
          <rect x="235" y="112" width="12" height="6" fill="#FFFFFF" fillOpacity="0.4" />

          {/* Road Markings - South */}
          <line x1="200" y1="230" x2="200" y2="340" stroke="#64748B" strokeWidth="2" strokeDasharray="8 6" />
          <line x1="150" y1="230" x2="250" y2="230" stroke="#FFFFFF" strokeWidth="3" /> {/* Stop Line South */}

          {/* Road Markings - East */}
          <line x1="260" y1="170" x2="400" y2="170" stroke="#64748B" strokeWidth="2" strokeDasharray="8 6" />
          <line x1="250" y1="120" x2="250" y2="220" stroke="#FFFFFF" strokeWidth="3" /> {/* Stop Line East */}

          {/* Road Markings - West */}
          <line x1="0" y1="170" x2="140" y2="170" stroke="#64748B" strokeWidth="2" strokeDasharray="8 6" />
          <line x1="150" y1="120" x2="150" y2="220" stroke="#FFFFFF" strokeWidth="3" /> {/* Stop Line West */}

          {/* Traffic Signal Heads */}

          {/* North Signal Head (Top Right of Intersection) */}
          <g transform="translate(258, 70)">
            <rect x="0" y="0" width="14" height="34" rx="3" fill="#070A11" stroke="#2D3F66" strokeWidth="1.5" />
            <circle cx="7" cy="7" r="4" fill={phase === 'ALL_RED_CLEARANCE' || phase === 'NORMAL_CYCLE' ? '#EF4444' : '#2A1010'} />
            <circle cx="7" cy="17" r="4" fill={phase === 'ACTIVE_YELLOW' ? '#F59E0B' : '#2B2208'} />
            <circle cx="7" cy="27" r="4" fill={phase === 'PRIORITY_GREEN' ? '#10B981' : '#08251B'} className={phase === 'PRIORITY_GREEN' ? 'animate-pulse' : ''} />
          </g>

          {/* South Signal Head (Bottom Left of Intersection) */}
          <g transform="translate(128, 236)">
            <rect x="0" y="0" width="14" height="34" rx="3" fill="#070A11" stroke="#2D3F66" strokeWidth="1.5" />
            <circle cx="7" cy="7" r="4" fill={phase === 'ALL_RED_CLEARANCE' || phase === 'NORMAL_CYCLE' ? '#EF4444' : '#2A1010'} />
            <circle cx="7" cy="17" r="4" fill={phase === 'ACTIVE_YELLOW' ? '#F59E0B' : '#2B2208'} />
            <circle cx="7" cy="27" r="4" fill={phase === 'PRIORITY_GREEN' ? '#10B981' : '#08251B'} />
          </g>

          {/* East Signal Head (Top Right of Intersection horizontal) */}
          <g transform="translate(256, 100)">
            <rect x="0" y="0" width="34" height="14" rx="3" fill="#070A11" stroke="#2D3F66" strokeWidth="1.5" />
            <circle cx="7" cy="7" r="4" fill={phase === 'PRIORITY_GREEN' || phase === 'ALL_RED_CLEARANCE' ? '#EF4444' : '#2A1010'} />
            <circle cx="17" cy="7" r="4" fill={phase === 'ACTIVE_YELLOW' ? '#F59E0B' : '#2B2208'} />
            <circle cx="27" cy="7" r="4" fill={phase === 'NORMAL_CYCLE' ? '#10B981' : '#08251B'} />
          </g>

          {/* West Signal Head (Bottom Left of Intersection horizontal) */}
          <g transform="translate(110, 226)">
            <rect x="0" y="0" width="34" height="14" rx="3" fill="#070A11" stroke="#2D3F66" strokeWidth="1.5" />
            <circle cx="7" cy="7" r="4" fill={phase === 'PRIORITY_GREEN' || phase === 'ALL_RED_CLEARANCE' ? '#EF4444' : '#2A1010'} />
            <circle cx="17" cy="7" r="4" fill={phase === 'ACTIVE_YELLOW' ? '#F59E0B' : '#2B2208'} />
            <circle cx="27" cy="7" r="4" fill={phase === 'NORMAL_CYCLE' ? '#10B981' : '#08251B'} />
          </g>

          {/* Approaching Vehicles on South Approach */}
          {emergencyActive ? (
            /* Ambulance advancing through priority corridor */
            <g transform="translate(180, 250)">
              <rect x="-10" y="-20" width="20" height="36" rx="4" fill="#F97316" stroke="#FFFFFF" strokeWidth="1.5" />
              <text x="0" y="2" fill="#070A11" fontSize="9" fontWeight="bold" textAnchor="middle" fontFamily="monospace">
                108
              </text>
              <circle cx="0" cy="-14" r="3.5" fill="#38BDF8" className="animate-pulse" />
            </g>
          ) : (
            /* Queued citizen cars waiting at red stopline */
            <>
              <rect x="175" y="240" width="16" height="28" rx="3" fill="#334155" stroke="#64748B" strokeWidth="1" />
              <rect x="175" y="275" width="16" height="28" rx="3" fill="#475569" stroke="#64748B" strokeWidth="1" />
              <rect x="175" y="310" width="18" height="34" rx="3" fill="#E2E8F0" stroke="#94A3B8" strokeWidth="1" />
            </>
          )}

          {/* Active Crossing Traffic in East/West if normal */}
          {phase === 'NORMAL_CYCLE' && (
            <rect x="290" y="176" width="28" height="15" rx="3" fill="#38BDF8" stroke="#0284C7" strokeWidth="1" />
          )}
        </svg>

        {/* Form-C Hardware Relay Interlock Status Card */}
        <div className="absolute bottom-2 right-2 bg-c2-surface/95 border border-c2-border rounded-lg p-2 font-mono text-[11px] shadow-lg">
          <div className="flex items-center space-x-1.5 text-police-gold font-bold mb-1">
            <Cpu className="w-3.5 h-3.5 text-police-gold" />
            <span>Form-C Relay Interlock</span>
          </div>
          <div className="space-y-0.5 text-c2-textMuted text-[10px]">
            <div className="flex justify-between gap-4">
              <span>N-S Green Contacts:</span>
              <span className={phase === 'PRIORITY_GREEN' ? 'text-signal-green font-bold' : 'text-c2-textDim'}>
                {phase === 'PRIORITY_GREEN' ? 'ENERGIZED' : 'OPEN'}
              </span>
            </div>
            <div className="flex justify-between gap-4">
              <span>E-W Green Lockout:</span>
              <span className={phase === 'PRIORITY_GREEN' ? 'text-signal-red font-bold' : 'text-signal-green'}>
                {phase === 'PRIORITY_GREEN' ? 'PHYSICALLY BLOCKED' : 'NORMAL'}
              </span>
            </div>
            <div className="flex justify-between gap-4">
              <span>Collision Probability:</span>
              <span className="text-emerald-400 font-bold">0.000% (Hardware)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
