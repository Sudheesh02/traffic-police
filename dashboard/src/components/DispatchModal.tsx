'use client';

import React, { useState } from 'react';
import { X, Siren, ShieldAlert, Zap, Truck, Check, AlertTriangle, Radio } from 'lucide-react';
import { LaneDirection } from '../lib/types';

interface DispatchModalProps {
  isOpen: boolean;
  onClose: () => void;
  onDispatch: (vehicle: string, lane: LaneDirection, strobeValid: boolean, duration: number) => void;
}

export const DispatchModal: React.FC<DispatchModalProps> = ({
  isOpen,
  onClose,
  onDispatch,
}) => {
  if (!isOpen) return null;

  const [selectedVehicle, setSelectedVehicle] = useState<'108_AMBULANCE' | 'FIRE_TENDER' | 'POLICE_PATROL'>('108_AMBULANCE');
  const [selectedLane, setSelectedLane] = useState<LaneDirection>('NORTH_BOUND');
  const [strobeValid, setStrobeValid] = useState<boolean>(true);
  const [durationSec, setDurationSec] = useState<number>(22);

  const vehicles = [
    {
      id: '108_AMBULANCE',
      name: '108 Emergency Ambulance',
      plate: 'CG-04-MB-1080',
      dest: 'Dr. BR Ambedkar Memorial (Mekahara)',
      priority: 'CRITICAL (P1)',
    },
    {
      id: 'FIRE_TENDER',
      name: 'Raipur Fire Service Tender',
      plate: 'CG-04-A-1011',
      dest: 'Industrial Area Phase-2',
      priority: 'HIGH (P2)',
    },
    {
      id: 'POLICE_PATROL',
      name: 'Traffic Police Interceptor',
      plate: 'CG-04-TP-0044',
      dest: 'VIP Road Corridor Security',
      priority: 'PRIORITY (P3)',
    },
  ];

  const handleConfirm = () => {
    onDispatch(selectedVehicle, selectedLane, strobeValid, durationSec);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-c2-card border border-c2-border rounded-xl max-w-lg w-full p-5 shadow-2xl space-y-4">
        {/* Modal Header */}
        <div className="flex items-center justify-between border-b border-c2-border pb-3">
          <div className="flex items-center space-x-2">
            <div className="p-1.5 rounded-lg bg-signal-amber/20 border border-signal-amber/40">
              <Siren className="w-5 h-5 text-signal-amber" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-c2-textBright">
                Emergency Dispatch & Preemption Console
              </h3>
              <p className="text-xs text-c2-textDim font-mono">
                Raipur Commissionerate CAD Gateway
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-c2-hover text-c2-textDim hover:text-c2-textBright transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Vehicle Selection */}
        <div>
          <label className="text-xs font-mono uppercase tracking-wider text-c2-textDim block mb-2">
            Select Dispatch Unit:
          </label>
          <div className="space-y-2">
            {vehicles.map((v) => {
              const isSelected = selectedVehicle === v.id;
              return (
                <div
                  key={v.id}
                  onClick={() => setSelectedVehicle(v.id as any)}
                  className={`p-2.5 rounded-lg border transition-all cursor-pointer flex items-center justify-between ${
                    isSelected
                      ? 'bg-police-navy border-police-cyan text-c2-textBright'
                      : 'bg-c2-surface border-c2-border hover:border-c2-borderLight text-c2-textMuted'
                  }`}
                >
                  <div>
                    <div className="text-xs font-bold">{v.name}</div>
                    <div className="text-[11px] font-mono text-police-cyan">{v.plate} • {v.dest}</div>
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-c2-obsidian text-police-gold border border-c2-border">
                    {v.priority}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Optical Strobe Anti-Spoofing Simulator */}
        <div className="p-3 rounded-lg bg-c2-surface border border-c2-border space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-c2-textBright">Optical Strobe Verification</span>
            <button
              onClick={() => setStrobeValid(!strobeValid)}
              className={`px-2 py-0.5 rounded text-[11px] font-mono transition ${
                strobeValid
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500'
                  : 'bg-red-500/20 text-red-400 border border-red-500'
              }`}
            >
              {strobeValid ? '1.84 Hz (VERIFIED AUTHENTIC)' : '0.50 Hz (DECOY / REJECT)'}
            </button>
          </div>
          <p className="text-[11px] text-c2-textDim font-mono">
            {strobeValid
              ? 'Meets 1.0–2.5 Hz temporal frequency band. Preemption will be granted.'
              : 'Decoy/spoofed flasher simulated. Agentic layer will block preemption.'}
          </p>
        </div>

        {/* Duration Slider */}
        <div>
          <div className="flex justify-between text-xs font-mono mb-1">
            <span className="text-c2-textDim">Preemption Window Duration:</span>
            <span className="text-police-cyan font-bold">{durationSec} Seconds (Max 30s)</span>
          </div>
          <input
            type="range"
            min="15"
            max="30"
            value={durationSec}
            onChange={(e) => setDurationSec(Number(e.target.value))}
            className="w-full accent-police-cyan"
          />
        </div>

        {/* Action Button */}
        <div className="pt-2 border-t border-c2-border flex items-center justify-end space-x-2">
          <button
            onClick={onClose}
            className="px-3 py-1.5 rounded-lg border border-c2-border text-xs font-mono text-c2-textDim hover:text-c2-textBright"
          >
            Cancel
          </button>
          <button
            onClick={handleConfirm}
            className="px-4 py-2 rounded-lg bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-c2-obsidian font-mono font-bold text-xs shadow-lg transition flex items-center gap-1.5"
          >
            <Zap className="w-4 h-4 fill-current" />
            <span>DISPATCH MISSION & ENGAGE PREEMPTION</span>
          </button>
        </div>
      </div>
    </div>
  );
};
