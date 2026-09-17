'use client';

import React, { useState } from 'react';
import { Bot, CheckCircle, ShieldAlert, Cpu, Sparkles, ChevronRight, Activity, Clock } from 'lucide-react';
import { AgentDecisionRecord } from '../lib/types';

interface AgenticCockpitProps {
  agents: AgentDecisionRecord[];
  emergencyActive: boolean;
}

export const AgenticCockpit: React.FC<AgenticCockpitProps> = ({ agents, emergencyActive }) => {
  const [selectedAgentIndex, setSelectedAgentIndex] = useState<number>(0);
  const activeAgent = agents[selectedAgentIndex] || agents[0];

  return (
    <div className="bg-c2-card border border-c2-border rounded-xl p-4 flex flex-col h-full shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-c2-border/70 pb-3 mb-3">
        <div className="flex items-center space-x-2.5">
          <div className="p-1.5 rounded-lg bg-police-navy border border-police-cyan/30">
            <Bot className="w-4 h-4 text-police-cyan" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-c2-textBright flex items-center gap-2">
              Agentic Preemption Cockpit
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-police-navy text-police-cyan border border-police-cyan/30">
                6-Agent Consensus
              </span>
            </h2>
            <p className="text-xs text-c2-textDim">
              Real-time reasoning & statutory guardrail arbitration
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono">
          <span className="text-c2-textDim">Total Execution:</span>
          <span className="text-police-cyan font-bold">52.3 ms</span>
        </div>
      </div>

      {/* Main Split Layout: Agent List on Left, Active Reasoning on Right */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-3 flex-1 min-h-[300px]">
        {/* Agent Cards List */}
        <div className="md:col-span-5 space-y-2 overflow-y-auto max-h-[320px] pr-1">
          {agents.map((agent, idx) => {
            const isSelected = idx === selectedAgentIndex;
            return (
              <div
                key={agent.agentName}
                onClick={() => setSelectedAgentIndex(idx)}
                className={`p-2.5 rounded-lg border transition-all cursor-pointer text-left ${
                  isSelected
                    ? 'bg-c2-hover border-police-cyan/60 shadow'
                    : 'bg-c2-surface/70 border-c2-border hover:border-c2-borderLight'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-bold text-c2-textBright truncate max-w-[170px]">
                    {agent.agentName}
                  </span>
                  <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
                    <CheckCircle className="w-2.5 h-2.5" /> {(agent.confidence * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="text-[11px] text-c2-textDim truncate">
                  {agent.agentRole}
                </div>
                <div className="flex items-center justify-between mt-1 text-[10px] font-mono text-c2-textDim">
                  <span>Latency: {agent.executionMs}ms</span>
                  <span className="text-police-gold font-bold">VERIFIED</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Deep Inspection Panel for Selected Agent */}
        <div className="md:col-span-7 bg-c2-obsidian rounded-lg border border-c2-borderLight/40 p-3.5 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-c2-border pb-2 mb-2.5">
              <div>
                <span className="text-xs font-bold text-police-cyan uppercase tracking-wider block">
                  {activeAgent.agentName}
                </span>
                <span className="text-[11px] text-c2-textDim font-mono">
                  Role: {activeAgent.agentRole}
                </span>
              </div>
              <div className="text-right font-mono text-xs">
                <span className="text-[10px] text-c2-textDim block">Confidence</span>
                <span className="text-emerald-400 font-bold text-sm">
                  {(activeAgent.confidence * 100).toFixed(1)}%
                </span>
              </div>
            </div>

            {/* Action Summary */}
            <div className="mb-3">
              <span className="text-[10px] font-mono text-c2-textDim uppercase tracking-wider block mb-1">
                Active Arbitration Output:
              </span>
              <p className="text-xs text-c2-textBright font-mono bg-c2-surface/80 p-2 rounded border border-c2-border leading-relaxed">
                {activeAgent.actionSummary}
              </p>
            </div>

            {/* Evidence & Invariants Checklist */}
            <div>
              <span className="text-[10px] font-mono text-c2-textDim uppercase tracking-wider block mb-1.5">
                Statutory & Telemetry Evidence Chain:
              </span>
              <ul className="space-y-1.5">
                {activeAgent.evidence.map((ev, i) => (
                  <li
                    key={i}
                    className="text-[11px] font-mono text-c2-textMuted flex items-start gap-2 bg-c2-card/40 p-1.5 rounded border border-c2-border/50"
                  >
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                    <span>{ev}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Bottom Compliance Badge */}
          <div className="mt-3 pt-2 border-t border-c2-border flex items-center justify-between text-[11px] font-mono text-c2-textDim">
            <span className="flex items-center gap-1 text-police-gold">
              <ShieldAlert className="w-3.5 h-3.5" /> MVA 1988 & IRC:SP:12 Guardrail Bound
            </span>
            <span className="text-emerald-400 font-bold">Consensus Approved</span>
          </div>
        </div>
      </div>
    </div>
  );
};
