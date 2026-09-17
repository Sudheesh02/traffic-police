'use client';

import React, { useState } from 'react';
import { Radio, Shield, Zap, Lock, Power, Compass, AlertCircle } from 'lucide-react';
import { LaneDirection } from '../lib/types';

interface RFRemoteProps {
  onTriggerPreemption: (lane: LaneDirection) => void;
  onCancelPreemption: () => void;
  emergencyActive: boolean;
  activeLane: LaneDirection;
  latencyMs: number;
}

export const RFRemote: React.FC<RFRemoteProps> = ({
  onTriggerPreemption,
  onCancelPreemption,
  emergencyActive,
  activeLane,
  latencyMs,
}) => {
  const [selectedLane, setSelectedLane] = useState<LaneDirection>('NORTH_BOUND');

  const lanes: { key: LaneDirection; label: string; desc: string }[] = [
    { key: 'NORTH_BOUND', label: 'NORTH', desc: 'From Pandri / Civil Lines' },
    { key: 'SOUTH_BOUND', label: 'SOUTH', desc: 'From Great Eastern Road' },
    { key: 'EAST_BOUND', label: 'EAST', desc: 'From Telibandha Link' },
    { key: 'WEST_BOUND', label: 'WEST', desc: 'From Sharda Chowk' },
  ];

  return (
    <div className="bg-c2-card border border-c2-border rounded-xl p-4 flex flex-col h-full shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-c2-border/70 pb-3 mb-3">
        <div className="flex items-center space-x-2.5">
          <div className="p-1.5 rounded-lg bg-police-navy border border-police-cyan/30">
            <Radio className="w-4 h-4 text-police-cyan" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-c2-textBright flex items-center gap-2">
              Constable Handheld RF Remote
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-c2-surface text-police-gold border border-c2-border">
                868 MHz Sub-GHz
              </span>
            </h2>
            <p className="text-xs text-c2-textDim">
              Industrial Semtech SX1262 Transceiver (1 km LOS)
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-c2-textBright">LINK ACTIVE</span>
        </div>
      </div>

      {/* Rugged Remote Enclosure Simulation */}
      <div className="flex-1 bg-c2-obsidian rounded-lg border-2 border-c2-border p-4 flex flex-col justify-between shadow-inner">
        {/* Top Status LCD Display */}
        <div className="bg-police-navy/40 border border-police-cyan/30 rounded p-2.5 font-mono text-xs mb-3">
          <div className="flex justify-between text-police-cyan text-[11px] mb-1">
            <span>TX_FREQ: 868.000 MHz</span>
            <span>RSSI: -68 dBm</span>
          </div>
          <div className="flex justify-between text-c2-textBright text-[11px]">
            <span>LATENCY: {latencyMs} ms</span>
            <span>AUTH: AES-128-GCM</span>
          </div>
          <div className="mt-1.5 pt-1.5 border-t border-c2-border text-[10px] text-c2-textDim flex items-center justify-between">
            <span>HARDWARE WATCHDOG:</span>
            <span className="text-police-gold font-bold">30.0s CEILING</span>
          </div>
        </div>

        {/* Directional Approach Selector */}
        <div className="mb-3">
          <label className="text-[11px] font-mono uppercase tracking-wider text-c2-textDim block mb-1.5">
            Select Approach Direction:
          </label>
          <div className="grid grid-cols-2 gap-2">
            {lanes.map((l) => {
              const isSelected = selectedLane === l.key;
              return (
                <button
                  key={l.key}
                  disabled={emergencyActive}
                  onClick={() => setSelectedLane(l.key)}
                  className={`p-2 rounded border text-left font-mono transition-all ${
                    isSelected
                      ? 'bg-police-navy border-police-cyan text-police-cyan font-bold shadow'
                      : 'bg-c2-surface border-c2-border text-c2-textDim hover:border-c2-borderLight'
                  } disabled:opacity-50`}
                >
                  <div className="text-xs font-bold">{l.label}</div>
                  <div className="text-[9px] truncate opacity-70">{l.desc}</div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Big Tactical Trigger Button */}
        <div>
          {emergencyActive ? (
            <button
              onClick={onCancelPreemption}
              className="w-full py-3.5 rounded-lg bg-c2-surface hover:bg-c2-hover border-2 border-signal-red text-signal-red font-mono font-bold text-sm tracking-wide transition-all shadow-lg flex items-center justify-center space-x-2"
            >
              <Power className="w-4 h-4" />
              <span>CANCEL PREEMPTION (RESTORE NORMAL)</span>
            </button>
          ) : (
            <button
              onClick={() => onTriggerPreemption(selectedLane)}
              className="w-full py-3.5 rounded-lg bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-c2-obsidian font-mono font-bold text-sm tracking-wide transition-all shadow-lg shadow-orange-500/20 flex items-center justify-center space-x-2 active:scale-[0.99]"
            >
              <Zap className="w-5 h-5 fill-current" />
              <span>TRANSMIT PREEMPTION OVERRIDE</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
