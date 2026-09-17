'use client';

import React, { useState, useEffect } from 'react';
import { Shield, Radio, Activity, Clock, AlertTriangle, CheckCircle2, Zap, Siren, Volume2, VolumeX, SlidersHorizontal, Bell } from 'lucide-react';

interface HeaderProps {
  emergencyActive: boolean;
  activeJunctionName: string;
  onSimulateEmergency: () => void;
  onResetNormal: () => void;
  latencyMs: number;
  audioEnabled: boolean;
  onToggleAudio: () => void;
  onOpenDispatchTool: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  emergencyActive,
  activeJunctionName,
  onSimulateEmergency,
  onResetNormal,
  latencyMs,
  audioEnabled,
  onToggleAudio,
  onOpenDispatchTool,
}) => {
  const [timeString, setTimeString] = useState<string>('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeString(
        now.toLocaleTimeString('en-IN', {
          hour12: false,
          timeZone: 'Asia/Kolkata',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
        }) + ' IST'
      );
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="border-b border-c2-border bg-c2-surface/95 backdrop-blur-md sticky top-0 z-50 shadow-md">
      <div className="max-w-[1750px] mx-auto px-4 py-2 flex flex-wrap items-center justify-between gap-3">
        {/* Left: Branding & Jurisdiction */}
        <div className="flex items-center space-x-3">
          <div className="relative flex items-center justify-center w-11 h-11 rounded-lg bg-police-navy border border-police-gold/40 shadow-inner">
            <Shield className="w-6 h-6 text-police-gold" />
            <div className="absolute -bottom-1 -right-1 w-3.5 h-3.5 rounded-full bg-emerald-500 border-2 border-c2-surface animate-pulse" />
          </div>

          <div>
            <div className="flex items-center space-x-2">
              <span className="text-[11px] font-bold uppercase tracking-wider text-police-gold bg-police-gold/10 px-2 py-0.5 rounded border border-police-gold/20">
                Raipur Police Commissionerate
              </span>
              <span className="text-[11px] font-mono text-c2-textDim hidden sm:inline">ITMS Smart Corridor C2</span>
              <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-c2-obsidian text-emerald-400 border border-c2-border">
                PORT 3000
              </span>
            </div>
            <h1 className="text-base font-bold text-c2-textBright tracking-tight flex items-center gap-2">
              SynchroClear-ITS
              <span className="text-xs font-mono px-1.5 py-0.5 rounded bg-c2-card text-police-cyan border border-c2-border">
                Tactical ATC Cockpit
              </span>
              <span className="text-xs font-normal text-c2-textMuted hidden lg:inline">
                | Great Eastern Road (NH-53 Lifeline)
              </span>
            </h1>
          </div>
        </div>

        {/* Center: Live Status & Preemption Banner */}
        <div className="flex items-center space-x-3">
          {emergencyActive ? (
            <div className="flex items-center space-x-2.5 bg-signal-amber/15 border border-signal-amber px-3 py-1.5 rounded-lg shadow-lg glow-amber animate-pulse">
              <Siren className="w-5 h-5 text-signal-amber animate-bounce" />
              <div>
                <div className="text-xs font-bold text-signal-amber uppercase tracking-wider flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-signal-amber animate-ping" />
                  EMERGENCY PREEMPTION ENGAGED
                </div>
                <div className="text-[11px] font-mono text-c2-textBright">
                  Green Corridor Active @ {activeJunctionName} • IRC:SP:12 Invariant Enforced
                </div>
              </div>
            </div>
          ) : (
            <div className="hidden lg:flex items-center space-x-2.5 bg-c2-card border border-c2-border px-3 py-1.5 rounded-lg text-xs font-mono text-c2-textMuted">
              <CheckCircle2 className="w-4 h-4 text-signal-green" />
              <span>Normal Round-Robin Active Across 4 Intersections (0% Gridlock)</span>
            </div>
          )}
        </div>

        {/* Right: Telemetry Health, Audio Toggle & Emergency Tools */}
        <div className="flex items-center space-x-3">
          {/* Audio Tactical Beep Toggle */}
          <button
            onClick={onToggleAudio}
            title={audioEnabled ? 'Mute Tactical Siren Tone' : 'Enable Tactical Siren Tone'}
            className={`p-2 rounded-lg border text-xs font-mono transition flex items-center gap-1.5 ${
              audioEnabled
                ? 'bg-police-navy border-police-cyan text-police-cyan'
                : 'bg-c2-card border-c2-border text-c2-textDim hover:text-c2-textMuted'
            }`}
          >
            {audioEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            <span className="text-[11px] hidden md:inline">{audioEnabled ? 'AUDIO ON' : 'MUTED'}</span>
          </button>

          {/* Emergency Vehicle Dispatcher Tool Trigger */}
          <button
            onClick={onOpenDispatchTool}
            className="px-2.5 py-1.5 rounded-lg bg-c2-surface hover:bg-c2-hover border border-c2-borderLight text-xs font-mono text-c2-textBright transition flex items-center gap-1.5 shadow"
          >
            <SlidersHorizontal className="w-3.5 h-3.5 text-police-gold" />
            <span className="hidden sm:inline">Dispatch Console</span>
          </button>

          {/* Sub-GHz RF telemetry */}
          <div className="hidden xl:flex flex-col items-end text-right font-mono text-xs">
            <div className="flex items-center space-x-1.5 text-police-cyan">
              <Radio className="w-3.5 h-3.5 animate-pulseFast" />
              <span>868.0 MHz Sub-GHz</span>
            </div>
            <span className="text-[11px] text-c2-textDim">{latencyMs}ms Latency • -68 dBm</span>
          </div>

          {/* Live Clock */}
          <div className="hidden 2xl:flex flex-col items-end text-right font-mono text-xs">
            <div className="flex items-center space-x-1 text-c2-textBright">
              <Clock className="w-3.5 h-3.5 text-c2-textDim" />
              <span>{timeString || '21:32:00 IST'}</span>
            </div>
            <span className="text-[10px] text-emerald-400 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> ICCC MQTT Sync
            </span>
          </div>

          {/* Main Action Button */}
          {emergencyActive ? (
            <button
              onClick={onResetNormal}
              className="px-3.5 py-1.5 text-xs font-bold rounded-lg bg-c2-border hover:bg-c2-borderLight text-c2-textBright border border-c2-border transition-all flex items-center space-x-1.5 shadow"
            >
              <Activity className="w-3.5 h-3.5 text-signal-green" />
              <span>Restore Normal</span>
            </button>
          ) : (
            <button
              onClick={onSimulateEmergency}
              className="px-3.5 py-1.5 text-xs font-bold rounded-lg bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 text-c2-obsidian font-mono shadow-lg shadow-orange-500/20 transition-all flex items-center space-x-1.5 active:scale-95"
            >
              <Zap className="w-3.5 h-3.5 text-c2-obsidian fill-current" />
              <span>Trigger 108 Preemption</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
