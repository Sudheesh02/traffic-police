'use client';

import React, { useState } from 'react';
import { Camera, Eye, ShieldCheck, AlertOctagon, CheckCircle2, UserCheck, PlusCircle, Video, Sliders, Radio, Sparkles } from 'lucide-react';
import { ANPRVehicleRecord } from '../lib/types';

interface CCTVStreamProps {
  vehicles: ANPRVehicleRecord[];
  onAddYieldingCitizen: () => void;
  emergencyActive: boolean;
}

export const CCTVStream: React.FC<CCTVStreamProps> = ({
  vehicles,
  onAddYieldingCitizen,
  emergencyActive,
}) => {
  const [activeCam, setActiveCam] = useState<'CAM_04' | 'CAM_09' | 'CAM_14'>('CAM_04');
  const [visionMode, setVisionMode] = useState<'RGB' | 'IR_NIGHT' | 'HEATMAP'>('RGB');

  const cameras = [
    { id: 'CAM_04', name: 'CAM-04 Jaistambh N', pole: 'Pole #04 GE Rd' },
    { id: 'CAM_09', name: 'CAM-09 Ghadi W', pole: 'Pole #12 Raj Bhavan' },
    { id: 'CAM_14', name: 'CAM-14 Telibandha', pole: 'Pole #21 VIP Rd' },
  ];

  return (
    <div className="bg-c2-card border border-c2-border rounded-xl p-4 flex flex-col h-full shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-c2-border/70 pb-2.5 mb-2.5">
        <div className="flex items-center space-x-2.5">
          <div className="p-1.5 rounded-lg bg-police-navy border border-police-cyan/30">
            <Camera className="w-4 h-4 text-police-cyan" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-c2-textBright flex items-center gap-2">
              Edge CCTV & ANPR Feed
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-c2-surface text-signal-green border border-signal-green/30 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-signal-green animate-pulse" /> 30.2 FPS RTSP
              </span>
            </h2>
            <p className="text-xs text-c2-textDim">
              Smart City Optical Pole • Jetson Orin Edge Vision (33ms)
            </p>
          </div>
        </div>

        {/* Action button */}
        <button
          onClick={onAddYieldingCitizen}
          className="text-xs font-mono font-bold px-2.5 py-1 rounded bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 transition flex items-center gap-1.5 shadow"
        >
          <PlusCircle className="w-3.5 h-3.5" />
          <span>Simulate Yielding Citizen</span>
        </button>
      </div>

      {/* Camera Switcher Bar */}
      <div className="flex items-center justify-between gap-2 mb-2">
        <div className="flex items-center gap-1.5">
          {cameras.map((cam) => (
            <button
              key={cam.id}
              onClick={() => setActiveCam(cam.id as any)}
              className={`px-2 py-0.8 rounded text-[11px] font-mono transition ${
                activeCam === cam.id
                  ? 'bg-police-navy text-police-cyan border border-police-cyan/50 font-bold'
                  : 'bg-c2-surface text-c2-textDim hover:text-c2-textMuted border border-c2-border'
              }`}
            >
              {cam.name}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-1 font-mono text-[10px]">
          <button
            onClick={() => setVisionMode('RGB')}
            className={`px-1.5 py-0.5 rounded ${visionMode === 'RGB' ? 'bg-c2-hover text-c2-textBright border border-c2-borderLight' : 'text-c2-textDim'}`}
          >
            RGB
          </button>
          <button
            onClick={() => setVisionMode('IR_NIGHT')}
            className={`px-1.5 py-0.5 rounded ${visionMode === 'IR_NIGHT' ? 'bg-police-navy text-police-cyan border border-police-cyan' : 'text-c2-textDim'}`}
          >
            IR
          </button>
        </div>
      </div>

      {/* CCTV Camera Viewport Simulation */}
      <div className={`relative w-full h-[200px] rounded-lg border border-c2-borderLight/40 overflow-hidden flex items-center justify-center mb-2.5 ${
        visionMode === 'IR_NIGHT' ? 'bg-[#050D0A]' : 'bg-c2-obsidian'
      }`}>
        <svg className="w-full h-full" viewBox="0 0 500 200" fill="none">
          {/* Tarmac Background */}
          <rect width="500" height="200" fill={visionMode === 'IR_NIGHT' ? '#071A12' : '#0C121E'} />

          {/* Road Lanes */}
          <line x1="80" y1="200" x2="200" y2="0" stroke="#1E2B48" strokeWidth="2" strokeDasharray="8 6" />
          <line x1="420" y1="200" x2="300" y2="0" stroke="#1E2B48" strokeWidth="2" strokeDasharray="8 6" />
          <line x1="250" y1="200" x2="250" y2="0" stroke="#334155" strokeWidth="2" strokeDasharray="12 8" />

          {/* Physical Red Stop Line */}
          <line x1="100" y1="130" x2="400" y2="130" stroke="#EF4444" strokeWidth="4" />
          <text x="250" y="124" fill="#EF4444" fontSize="9" fontWeight="bold" textAnchor="middle" fontFamily="monospace">
            ITMS RED STOP-LINE [ANPR ENFORCEMENT]
          </text>

          {/* Ambulance In View (When emergency is active) */}
          {emergencyActive ? (
            <g transform="translate(190, 30)">
              {/* Bounding Box */}
              <rect x="0" y="0" width="120" height="85" fill="none" stroke="#F97316" strokeWidth="2" strokeDasharray="4 2" />
              {/* Tag Header */}
              <rect x="0" y="-18" width="120" height="18" fill="#F97316" />
              <text x="5" y="-5" fill="#070A11" fontSize="9" fontWeight="bold" fontFamily="monospace">
                108 AMBULANCE (98.4%)
              </text>
              {/* Strobe Tag */}
              <rect x="0" y="85" width="120" height="16" fill="#070A11" fillOpacity="0.85" stroke="#38BDF8" strokeWidth="1" />
              <text x="5" y="97" fill="#38BDF8" fontSize="8" fontWeight="bold" fontFamily="monospace">
                STROBE: 1.84 Hz VERIFIED
              </text>
            </g>
          ) : (
            <g transform="translate(200, 50)">
              <rect x="0" y="0" width="100" height="70" fill="none" stroke="#64748B" strokeWidth="1.5" />
              <rect x="0" y="-16" width="100" height="16" fill="#334155" />
              <text x="5" y="-4" fill="#F8FAFC" fontSize="9" fontWeight="bold" fontFamily="monospace">
                COMMERCIAL BUS (95%)
              </text>
            </g>
          )}

          {/* Citizen Yielding Vehicle Crossing Red Line */}
          <g transform="translate(320, 100)">
            <rect x="0" y="0" width="100" height="75" fill="none" stroke="#10B981" strokeWidth="2" />
            <rect x="0" y="-18" width="100" height="18" fill="#10B981" />
            <text x="5" y="-5" fill="#070A11" fontSize="8" fontWeight="bold" fontFamily="monospace">
              CG-04-NA-4492 [YIELDING]
            </text>
            <rect x="0" y="75" width="100" height="16" fill="#070A11" fillOpacity="0.85" stroke="#10B981" strokeWidth="1" />
            <text x="5" y="87" fill="#10B981" fontSize="8" fontWeight="bold" fontFamily="monospace">
              EXEMPT: MVA SEC 177
            </text>
          </g>
        </svg>

        {/* Camera OSD Overlays */}
        <div className="absolute top-2 left-2 text-[10px] font-mono text-signal-green bg-c2-obsidian/85 px-2 py-0.5 rounded border border-signal-green/30 flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-signal-green animate-pulse" />
          <span>{activeCam} [RAIPUR ITMS] 1080p</span>
        </div>

        <div className="absolute top-2 right-2 text-[10px] font-mono text-c2-textDim bg-c2-obsidian/85 px-2 py-0.5 rounded border border-c2-border">
          BANDWIDTH: 4.8 Mbps • H.265
        </div>

        {/* Rooftop Strobe Frequency Spectrum FFT analyzer */}
        <div className="absolute bottom-2 left-2 bg-c2-obsidian/90 border border-c2-border rounded px-2 py-1 font-mono text-[9px] text-c2-textDim flex items-center gap-2">
          <span>STROBE FFT:</span>
          <span className="text-police-cyan font-bold">{emergencyActive ? '1.84 Hz (PASS)' : '0.00 Hz (IDLE)'}</span>
        </div>
      </div>

      {/* ANPR Vehicle Exemption Table */}
      <div className="flex-1 overflow-y-auto max-h-[145px] border border-c2-border rounded-lg bg-c2-obsidian">
        <table className="w-full text-left font-mono text-[11px]">
          <thead className="bg-c2-surface text-c2-textDim text-[10px] sticky top-0 border-b border-c2-border">
            <tr>
              <th className="p-1.5">Plate</th>
              <th className="p-1.5">Type</th>
              <th className="p-1.5">Stop Line</th>
              <th className="p-1.5">Status</th>
              <th className="p-1.5">Fine</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-c2-border/40 text-c2-textBright">
            {vehicles.map((v) => (
              <tr key={v.id} className="hover:bg-c2-card/60 transition-colors">
                <td className="p-1.5 font-bold text-police-cyan">{v.plate}</td>
                <td className="p-1.5 text-c2-textMuted text-[10px]">{v.vehicleType}</td>
                <td className="p-1.5 text-[10px]">
                  {v.crossedStopLineOnRed ? (
                    <span className="text-amber-400">Crossed Red</span>
                  ) : (
                    <span className="text-emerald-400">Compliant</span>
                  )}
                </td>
                <td className="p-1.5">
                  {v.status === 'EXEMPT_GOOD_SAMARITAN' ? (
                    <span className="px-1.5 py-0.2 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1 w-fit text-[9px]">
                      <CheckCircle2 className="w-2.5 h-2.5" /> EXEMPTED
                    </span>
                  ) : v.status === 'VIOLATION_PENALIZED' ? (
                    <span className="px-1.5 py-0.2 rounded bg-red-500/10 text-red-400 border border-red-500/30 w-fit text-[9px]">
                      PENALTY
                    </span>
                  ) : (
                    <span className="text-c2-textDim text-[9px]">OK</span>
                  )}
                </td>
                <td className="p-1.5 font-bold text-[10px]">
                  {v.challanAmountInr === 0 ? (
                    <span className="text-emerald-400">₹0 (Waived)</span>
                  ) : (
                    <span className="text-red-400">₹{v.challanAmountInr}</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
