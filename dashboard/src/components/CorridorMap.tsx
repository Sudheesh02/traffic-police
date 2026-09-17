'use client';

import React, { useState } from 'react';
import { MapPin, Navigation, Siren, Shield, AlertCircle, Clock, Zap, Gauge, Flame, TrendingDown } from 'lucide-react';
import { JunctionData } from '../lib/types';

interface CorridorMapProps {
  junctions: JunctionData[];
  selectedJunctionId: string;
  onSelectJunction: (id: string) => void;
  emergencyActive: boolean;
  transitProgress: number; // 0 to 100%
}

export const CorridorMap: React.FC<CorridorMapProps> = ({
  junctions,
  selectedJunctionId,
  onSelectJunction,
  emergencyActive,
  transitProgress = 35,
}) => {
  const [hoveredJunction, setHoveredJunction] = useState<string | null>(null);

  // Compute live ambulance position based on progress
  const ambX = 140 + (transitProgress / 100) * 600;
  const ambY = 155 - Math.sin((transitProgress / 100) * Math.PI) * 15;

  return (
    <div className="bg-c2-card border border-c2-border rounded-xl p-4 flex flex-col h-full shadow-lg relative overflow-hidden">
      {/* Card Header */}
      <div className="flex items-center justify-between border-b border-c2-border/70 pb-3 mb-3">
        <div className="flex items-center space-x-2.5">
          <div className="p-1.5 rounded-lg bg-police-navy border border-police-cyan/30">
            <Navigation className="w-4 h-4 text-police-cyan" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-c2-textBright flex items-center gap-2">
              Raipur GIS Arterial Corridor
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-c2-surface text-police-gold border border-c2-border">
                Great Eastern Road (NH-53)
              </span>
            </h2>
            <p className="text-xs text-c2-textDim">
              Lifeline route from Jaistambh Chowk to Dr. BR Ambedkar Memorial Hospital
            </p>
          </div>
        </div>

        {/* Live Corridor Stats & Tactical HUD */}
        <div className="flex items-center space-x-4 font-mono text-xs">
          <div className="text-right hidden sm:block">
            <span className="text-c2-textDim text-[10px] block uppercase">Queue Dissipation</span>
            <span className="text-emerald-400 font-bold text-xs flex items-center justify-end gap-1">
              <TrendingDown className="w-3 h-3 text-emerald-400" />
              {emergencyActive ? '42 ➔ 6 PCU (-85%)' : '42 PCU Peak'}
            </span>
          </div>
          <div className="text-right hidden md:block">
            <span className="text-c2-textDim text-[10px] block uppercase">Delay Reclaimed</span>
            <span className="text-signal-green font-bold text-sm">-68.4s / junc</span>
          </div>
          <div className="text-right">
            <span className="text-c2-textDim text-[10px] block uppercase">Corridor Status</span>
            <span className={`font-bold flex items-center justify-end gap-1 text-xs ${
              emergencyActive ? 'text-signal-amber animate-pulse' : 'text-emerald-400'
            }`}>
              <span className={`w-1.5 h-1.5 rounded-full ${emergencyActive ? 'bg-signal-amber' : 'bg-emerald-400'}`} />
              {emergencyActive ? 'GREEN WAVE ACTIVE' : 'OPTIMAL ROUND-ROBIN'}
            </span>
          </div>
        </div>
      </div>

      {/* Vector Interactive Map Canvas */}
      <div className="relative flex-1 min-h-[300px] w-full rounded-lg bg-c2-obsidian border border-c2-borderLight/30 tactical-grid flex items-center justify-center p-4 overflow-hidden">
        {/* Background Radar Scanner when preemption is active */}
        {emergencyActive && (
          <div className="absolute inset-0 radar-grid pointer-events-none animate-pulse" />
        )}

        {/* Raipur Great Eastern Road Vector Highway Spine */}
        <svg className="w-full h-full max-h-[360px]" viewBox="0 0 920 320" fill="none">
          <defs>
            <linearGradient id="roadGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#1E2B48" />
              <stop offset="50%" stopColor="#2A3D66" />
              <stop offset="100%" stopColor="#1E2B48" />
            </linearGradient>

            <linearGradient id="greenWaveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#10B981" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#06B6D4" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#10B981" stopOpacity="0.8" />
            </linearGradient>
          </defs>

          {/* Grid lines */}
          <line x1="40" y1="70" x2="880" y2="70" stroke="#1E2B48" strokeWidth="0.8" strokeDasharray="4 4" />
          <line x1="40" y1="250" x2="880" y2="250" stroke="#1E2B48" strokeWidth="0.8" strokeDasharray="4 4" />

          {/* Main Great Eastern Road Arterial Spine */}
          <path
            d="M 60 160 C 220 135, 380 185, 540 160 S 760 135, 840 150"
            stroke="url(#roadGrad)"
            strokeWidth="30"
            strokeLinecap="round"
          />

          {/* Road Center Dotted Marking */}
          <path
            d="M 60 160 C 220 135, 380 185, 540 160 S 760 135, 840 150"
            stroke="#64748B"
            strokeWidth="2"
            strokeDasharray="10 8"
          />

          {/* Active Preemption Green Wave Glow */}
          {emergencyActive && (
            <path
              d="M 60 160 C 220 135, 380 185, 540 160 S 760 135, 840 150"
              stroke="url(#greenWaveGrad)"
              strokeWidth="12"
              strokeLinecap="round"
              className="animate-pulse"
            />
          )}

          {/* Hospital Branch Line towards Mekahara */}
          <path
            d="M 690 150 C 715 110, 735 90, 780 65"
            stroke="#1E2B48"
            strokeWidth="18"
            strokeLinecap="round"
          />
          <path
            d="M 690 150 C 715 110, 735 90, 780 65"
            stroke={emergencyActive ? '#10B981' : '#64748B'}
            strokeWidth="2.5"
            strokeDasharray="6 6"
          />

          {/* Dr. BR Ambedkar Memorial Hospital (Mekahara) Terminal Node */}
          <g transform="translate(780, 65)">
            <circle cx="0" cy="0" r="24" fill="#0D1424" stroke="#EF4444" strokeWidth="2.5" />
            <rect x="-9" y="-3" width="18" height="6" fill="#EF4444" rx="1" />
            <rect x="-3" y="-9" width="6" height="18" fill="#EF4444" rx="1" />
            <text x="32" y="3" fill="#F8FAFC" fontSize="12" fontWeight="bold" fontFamily="sans-serif">
              Dr. BR Ambedkar Memorial
            </text>
            <text x="32" y="18" fill="#EF4444" fontSize="10" fontWeight="bold" fontFamily="monospace">
              MEKAHARA EMERGENCY TRAUMA
            </text>
            <text x="32" y="30" fill="#94A3B8" fontSize="9" fontFamily="monospace">
              ETA: {emergencyActive ? '2.4 min (Non-Stop)' : '8.6 min (Gridlock)'}
            </text>
          </g>

          {/* Moving 108 Ambulance Unit */}
          {emergencyActive ? (
            <g transform={`translate(${ambX}, ${ambY})`} className="transition-all duration-300">
              <circle cx="0" cy="0" r="30" fill="#F97316" fillOpacity="0.25" className="animate-ping" />
              <rect x="-20" y="-11" width="40" height="22" rx="4" fill="#F97316" stroke="#FFFFFF" strokeWidth="2" />
              <text x="-14" y="4" fill="#070A11" fontSize="11" fontWeight="bold" fontFamily="monospace">
                108
              </text>
              {/* Emergency Dual Strobes */}
              <circle cx="12" cy="-11" r="4.5" fill="#38BDF8" className="animate-pulse" />
              <circle cx="-12" cy="-11" r="4.5" fill="#EF4444" className="animate-pulse" />
              {/* Live HUD Tooltip */}
              <rect x="-70" y="-40" width="140" height="24" rx="4" fill="#070A11" stroke="#F97316" strokeWidth="1.2" />
              <text x="0" y="-27" fill="#F8FAFC" fontSize="9" fontWeight="bold" textAnchor="middle" fontFamily="monospace">
                108 AMBULANCE: 48 km/h
              </text>
              <text x="0" y="-18" fill="#38BDF8" fontSize="8" textAnchor="middle" fontFamily="monospace">
                CG-04-MB-1080 • STROBE ON
              </text>
            </g>
          ) : (
            <g transform="translate(90, 160)">
              <circle cx="0" cy="0" r="14" fill="#1E2B48" stroke="#64748B" strokeWidth="1.5" />
              <text x="0" y="4" fill="#94A3B8" fontSize="9" textAnchor="middle" fontFamily="monospace">
                PATROL
              </text>
            </g>
          )}

          {/* Junction 1: Jaistambh Chowk */}
          <g
            transform="translate(160, 150)"
            className="cursor-pointer group"
            onClick={() => onSelectJunction('RPR_GE_ROAD_01')}
            onMouseEnter={() => setHoveredJunction('RPR_GE_ROAD_01')}
            onMouseLeave={() => setHoveredJunction(null)}
          >
            <circle
              cx="0"
              cy="0"
              r={selectedJunctionId === 'RPR_GE_ROAD_01' ? 20 : 15}
              fill={selectedJunctionId === 'RPR_GE_ROAD_01' ? '#0F2B5C' : '#0D1424'}
              stroke={emergencyActive ? '#10B981' : '#E5A93C'}
              strokeWidth={selectedJunctionId === 'RPR_GE_ROAD_01' ? '3.5' : '2'}
            />
            <circle cx="0" cy="0" r="6" fill={emergencyActive ? '#10B981' : '#E5A93C'} />
            <text x="0" y="34" fill="#F8FAFC" fontSize="11" fontWeight="bold" textAnchor="middle" fontFamily="sans-serif">
              Jaistambh Chowk
            </text>
            <text x="0" y="48" fill="#94A3B8" fontSize="9" textAnchor="middle" fontFamily="monospace">
              JST-01 • {emergencyActive ? 'CLEARING' : '42 PCU'}
            </text>
          </g>

          {/* Junction 2: Ghadi Chowk */}
          <g
            transform="translate(420, 175)"
            className="cursor-pointer group"
            onClick={() => onSelectJunction('RPR_GE_ROAD_02')}
            onMouseEnter={() => setHoveredJunction('RPR_GE_ROAD_02')}
            onMouseLeave={() => setHoveredJunction(null)}
          >
            <circle
              cx="0"
              cy="0"
              r={selectedJunctionId === 'RPR_GE_ROAD_02' ? 20 : 15}
              fill={selectedJunctionId === 'RPR_GE_ROAD_02' ? '#0F2B5C' : '#0D1424'}
              stroke={emergencyActive ? '#10B981' : '#E5A93C'}
              strokeWidth={selectedJunctionId === 'RPR_GE_ROAD_02' ? '3.5' : '2'}
            />
            <circle cx="0" cy="0" r="6" fill={emergencyActive ? '#10B981' : '#E5A93C'} />
            <text x="0" y="34" fill="#F8FAFC" fontSize="11" fontWeight="bold" textAnchor="middle" fontFamily="sans-serif">
              Ghadi Chowk
            </text>
            <text x="0" y="48" fill="#94A3B8" fontSize="9" textAnchor="middle" fontFamily="monospace">
              GHD-02 • {emergencyActive ? 'NEXT WAVE' : '35 PCU'}
            </text>
          </g>

          {/* Junction 3: Telibandha Chowk */}
          <g
            transform="translate(680, 150)"
            className="cursor-pointer group"
            onClick={() => onSelectJunction('RPR_GE_ROAD_03')}
            onMouseEnter={() => setHoveredJunction('RPR_GE_ROAD_03')}
            onMouseLeave={() => setHoveredJunction(null)}
          >
            <circle
              cx="0"
              cy="0"
              r={selectedJunctionId === 'RPR_GE_ROAD_03' ? 20 : 15}
              fill={selectedJunctionId === 'RPR_GE_ROAD_03' ? '#0F2B5C' : '#0D1424'}
              stroke={emergencyActive ? '#10B981' : '#E5A93C'}
              strokeWidth={selectedJunctionId === 'RPR_GE_ROAD_03' ? '3.5' : '2'}
            />
            <circle cx="0" cy="0" r="6" fill={emergencyActive ? '#10B981' : '#E5A93C'} />
            <text x="0" y="34" fill="#F8FAFC" fontSize="11" fontWeight="bold" textAnchor="middle" fontFamily="sans-serif">
              Telibandha Chowk
            </text>
            <text x="0" y="48" fill="#94A3B8" fontSize="9" textAnchor="middle" fontFamily="monospace">
              TLB-03 • {emergencyActive ? 'ARMED' : '29 PCU'}
            </text>
          </g>
        </svg>

        {/* Tactical Legend & Speed Overlay */}
        <div className="absolute bottom-2 left-3 bg-c2-surface/90 border border-c2-border rounded-md px-3 py-1.5 text-[11px] font-mono flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-signal-green" />
            <span>Preempted Green Wave</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-police-gold" />
            <span>Fixed Cycle Phase</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-signal-red" />
            <span>Hospital Trauma Gate</span>
          </div>
        </div>
      </div>
    </div>
  );
};
