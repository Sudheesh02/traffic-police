'use client'

import React, { useState } from 'react'
import {
  Shield,
  FileCheck,
  Download,
  Search,
  CheckCircle2,
  Lock,
  Radio,
  Sliders,
  Server,
  Sparkles,
} from 'lucide-react'
import { MetricsSection } from './metrics-section'
import { HeroPipelineSection } from './hero-pipeline-section'
import { StreamSection } from './stream-section'
import { RFRemote } from '../RFRemote'
import { CCTVStream } from '../CCTVStream'
import { AgenticCockpit } from '../AgenticCockpit'
import { AuditLedger } from '../AuditLedger'
import { CorridorMap } from '../CorridorMap'
import { JunctionTwin } from '../JunctionTwin'
import type { PreemptionStreamRow } from './data'
import {
  JunctionData,
  SignalPhase,
  LaneDirection,
  ANPRVehicleRecord,
  AuditBlock,
  AgentDecisionRecord,
} from '../../lib/types'

export type SharedViewProps = {
  junctions: JunctionData[]
  selectedJunctionId: string
  onSelectJunction: (id: string) => void
  phase: SignalPhase
  phaseTimer: number
  emergencyActive: boolean
  transitProgress: number
  activeLane: LaneDirection
  latencyMs: number
  vehicles: ANPRVehicleRecord[]
  auditBlocks: AuditBlock[]
  agentStates: AgentDecisionRecord[]
  onTriggerPreemption: (lane: LaneDirection) => void
  onCancelPreemption: () => void
  onAddYieldingCitizen: () => void
  customStreamRows: PreemptionStreamRow[]
}

export function OverviewView(props: SharedViewProps) {
  const selectedJunction =
    props.junctions.find((j) => j.id === props.selectedJunctionId) || props.junctions[0]

  return (
    <div className="space-y-6 pb-12">
      {/* 4-Card Astrix Top Metrics */}
      <MetricsSection />

      {/* Astrix Hero Viewport (Pipeline / Twin / GIS) */}
      <HeroPipelineSection
        isPreempting={props.emergencyActive}
        phase={props.phase}
        phaseTimer={props.phaseTimer}
        transitProgress={props.transitProgress}
        onPreemptToggle={() => {
          if (props.emergencyActive) {
            props.onCancelPreemption()
          } else {
            props.onTriggerPreemption(props.activeLane)
          }
        }}
      />

      {/* Live Stream Table */}
      <StreamSection customRows={props.customStreamRows} />

      {/* Operational Cockpit Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-2">
        <div className="space-y-6">
          <RFRemote
            onTriggerPreemption={props.onTriggerPreemption}
            onCancelPreemption={props.onCancelPreemption}
            emergencyActive={props.emergencyActive}
            activeLane={props.activeLane}
            latencyMs={props.latencyMs}
          />
          <AgenticCockpit
            agents={props.agentStates}
            emergencyActive={props.emergencyActive}
          />
        </div>

        <div className="space-y-6">
          <CCTVStream
            vehicles={props.vehicles}
            onAddYieldingCitizen={props.onAddYieldingCitizen}
            emergencyActive={props.emergencyActive}
          />
          <AuditLedger blocks={props.auditBlocks} />
        </div>
      </div>
    </div>
  )
}

export function PreemptionView(props: SharedViewProps) {
  return (
    <div className="space-y-6 pb-12">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b border-border pb-4">
        <div>
          <h1 className="text-xl md:text-2xl font-bold tracking-tight text-foreground">
            Tactical Preemption & Edge-AI Stream
          </h1>
          <p className="text-xs md:text-sm text-muted-foreground mt-0.5">
            868.0 MHz Sub-GHz RF Dispatch · Multi-Camera Optical Strobe Verification (1.84 Hz)
          </p>
        </div>

        <button
          type="button"
          onClick={props.onAddYieldingCitizen}
          className="flex items-center gap-2 h-10 px-4 rounded-xl border border-primary/30 bg-primary/10 hover:bg-primary/20 text-xs font-semibold text-primary transition-colors"
        >
          <Sparkles className="size-4" />
          <span>Simulate Yielding Citizen</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-4 space-y-6">
          <RFRemote
            onTriggerPreemption={props.onTriggerPreemption}
            onCancelPreemption={props.onCancelPreemption}
            emergencyActive={props.emergencyActive}
            activeLane={props.activeLane}
            latencyMs={props.latencyMs}
          />
          <AgenticCockpit
            agents={props.agentStates}
            emergencyActive={props.emergencyActive}
          />
        </div>

        <div className="lg:col-span-8 space-y-6">
          <CCTVStream
            vehicles={props.vehicles}
            onAddYieldingCitizen={props.onAddYieldingCitizen}
            emergencyActive={props.emergencyActive}
          />
          <StreamSection customRows={props.customStreamRows} />
        </div>
      </div>
    </div>
  )
}

export function CorridorTwinView(props: SharedViewProps) {
  const selectedJunction =
    props.junctions.find((j) => j.id === props.selectedJunctionId) || props.junctions[0]

  return (
    <div className="space-y-6 pb-12">
      <div className="border-b border-border pb-4">
        <h1 className="text-xl md:text-2xl font-bold tracking-tight text-foreground">
          Corridor GIS & Physical Junction Twin
        </h1>
        <p className="text-xs md:text-sm text-muted-foreground mt-0.5">
          Great Eastern Road NH-53 Arterial (Telibandha → Jaistambh → Mekahara Hospital)
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <div className="rounded-2xl border border-border bg-card/60 p-4 space-y-3">
          <h2 className="text-sm font-bold text-foreground">
            Jaistambh Chowk 4-Way Physical Twin
          </h2>
          <JunctionTwin
            junction={selectedJunction}
            phase={props.phase}
            phaseTimer={props.phaseTimer}
            emergencyActive={props.emergencyActive}
          />
        </div>

        <div className="rounded-2xl border border-border bg-card/60 p-4 space-y-3">
          <h2 className="text-sm font-bold text-foreground">
            Arterial Green Wave Corridor Telemetry
          </h2>
          <CorridorMap
            junctions={props.junctions}
            selectedJunctionId={props.selectedJunctionId}
            onSelectJunction={props.onSelectJunction}
            emergencyActive={props.emergencyActive}
            transitProgress={props.transitProgress}
          />
        </div>
      </div>
    </div>
  )
}

export function AgenticView(props: SharedViewProps) {
  return (
    <div className="space-y-6 pb-12">
      <div className="border-b border-border pb-4">
        <h1 className="text-xl md:text-2xl font-bold tracking-tight text-foreground">
          Autonomous 6-Agent Consensus Engine
        </h1>
        <p className="text-xs md:text-sm text-muted-foreground mt-0.5">
          Multi-Agent Consensus · Strobe FFT Verification · IRC:SP:12 Deterministic Timing
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
        <div className="xl:col-span-7 space-y-6">
          <AgenticCockpit
            agents={props.agentStates}
            emergencyActive={props.emergencyActive}
          />
        </div>

        <div className="xl:col-span-5 space-y-6">
          <AuditLedger blocks={props.auditBlocks} />
        </div>
      </div>
    </div>
  )
}

export function GoodSamaritanView() {
  const [searchTerm, setSearchTerm] = useState('')

  const waivers = [
    {
      id: 'SAM-2026-0846',
      plate: 'CG-04-MB-2219',
      owner: 'A. K. Verma',
      vehicle: 'Maruti WagonR (White)',
      junction: 'Jaistambh Chowk (N)',
      action: 'Yielded past stop line for 108 Cardiac ICU',
      penaltyOriginal: '₹2,000',
      penaltyWaived: '₹0 (100% Waived)',
      section: 'MVA 1988 Sec 177 & 184',
      status: 'EXEMPTED',
      timestamp: '10:14:18 IST',
    },
    {
      id: 'SAM-2026-0844',
      plate: 'CG-04-NL-8841',
      owner: 'R. S. Dewangan',
      vehicle: 'Hyundai Creta (Silver)',
      junction: 'Ghadi Chowk (W)',
      action: 'Left-shoulder lane clearance for Fire Tender 03',
      penaltyOriginal: '₹1,000',
      penaltyWaived: '₹0 (100% Waived)',
      section: 'MVA 1988 Sec 177 & 184',
      status: 'EXEMPTED',
      timestamp: '10:08:39 IST',
    },
    {
      id: 'SAM-2026-0839',
      plate: 'CG-04-HX-4011',
      owner: 'P. K. Sahu',
      vehicle: 'Honda City (Grey)',
      junction: 'Telibandha Chowk',
      action: 'Advanced into pedestrian box to unblock ambulance',
      penaltyOriginal: '₹2,000',
      penaltyWaived: '₹0 (100% Waived)',
      section: 'MVA 1988 Sec 177 & 184',
      status: 'EXEMPTED',
      timestamp: '09:41:20 IST',
    },
  ]

  const filtered = waivers.filter(
    (w) =>
      w.plate.toLowerCase().includes(searchTerm.toLowerCase()) ||
      w.owner.toLowerCase().includes(searchTerm.toLowerCase()) ||
      w.junction.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="space-y-6 pb-12">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 border-b border-border pb-4">
        <div>
          <h1 className="text-xl md:text-2xl font-bold tracking-tight text-foreground">
            Good Samaritan Statutory Exemption Ledger
          </h1>
          <p className="text-xs md:text-sm text-muted-foreground mt-0.5">
            Motor Vehicles Act 1988 Sections 177 & 184 Legal Immunity Certification
          </p>
        </div>

        <button
          type="button"
          onClick={() => alert('Exporting Official Legal Immunity Certification CSV...')}
          className="flex items-center gap-2 h-10 px-4 rounded-xl border border-border bg-card hover:bg-secondary text-xs font-semibold text-foreground transition-colors"
        >
          <Download className="size-4 text-muted-foreground" />
          <span>Export Immunity Certificate</span>
        </button>
      </div>

      <div className="flex items-center gap-3">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-3 size-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search license plate, citizen name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full h-10 pl-9 pr-3 rounded-xl border border-border bg-secondary/60 text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-border bg-card/60">
        <table className="astrix-table min-w-[800px]">
          <thead>
            <tr>
              <th>Citizen Vehicle</th>
              <th>Yielding Incident</th>
              <th>Challan Waiver</th>
              <th>Statutory Law</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((w) => (
              <tr key={w.id}>
                <td>
                  <div className="space-y-0.5">
                    <p className="font-mono font-bold text-xs text-primary">{w.plate}</p>
                    <p className="text-xs text-foreground font-medium">{w.owner}</p>
                    <p className="text-[10px] text-muted-foreground">{w.vehicle}</p>
                  </div>
                </td>

                <td>
                  <div className="space-y-0.5">
                    <p className="text-xs text-foreground font-medium">{w.action}</p>
                    <p className="text-[10px] text-muted-foreground font-mono">{w.junction} · {w.timestamp}</p>
                  </div>
                </td>

                <td>
                  <div className="space-y-0.5">
                    <span className="text-xs font-bold text-emerald-400">{w.penaltyWaived}</span>
                    <p className="text-[10px] text-muted-foreground line-through">Fine: {w.penaltyOriginal}</p>
                  </div>
                </td>

                <td>
                  <span className="text-xs text-foreground font-medium">{w.section}</span>
                </td>

                <td>
                  <span className="inline-flex items-center gap-1 rounded-full bg-cyan-500/15 border border-cyan-500/30 px-2.5 py-1 text-xs font-bold text-cyan-400">
                    <Shield className="size-3" />
                    {w.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export function ReportsView() {
  return (
    <div className="space-y-6 pb-12">
      <div className="border-b border-border pb-4">
        <h1 className="text-xl md:text-2xl font-bold tracking-tight text-foreground">
          Statutory & Technical Compliance Reports
        </h1>
        <p className="text-xs md:text-sm text-muted-foreground mt-0.5">
          Raipur Police Commissionerate Traffic Audit & Legal Exemption Verification
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="rounded-2xl border border-border bg-card/60 p-5 space-y-3">
          <div className="size-9 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
            <CheckCircle2 className="size-5" />
          </div>
          <h3 className="font-bold text-sm text-foreground">IRC:SP:12 Clearance Buffer</h3>
          <p className="text-xs text-muted-foreground leading-relaxed">
            3.5s Yellow deceleration + 2.0s All-Red clearance mathematical verification. 100% adherence to Indian Road Congress guidelines, eliminating broadside cross-traffic collisions.
          </p>
          <button
            type="button"
            onClick={() => alert('Downloading IRC:SP:12 Compliance Certificate...')}
            className="w-full py-2 rounded-xl border border-border bg-secondary hover:bg-secondary/80 text-xs font-semibold text-foreground transition-colors"
          >
            Download Certificate
          </button>
        </div>

        <div className="rounded-2xl border border-border bg-card/60 p-5 space-y-3">
          <div className="size-9 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
            <Radio className="size-5" />
          </div>
          <h3 className="font-bold text-sm text-foreground">WPC Sub-GHz ISM 868.0 MHz</h3>
          <p className="text-xs text-muted-foreground leading-relaxed">
            Wireless Planning & Coordination (WPC) license-free Sub-GHz band conformity in India. Verified +14 dB link margin over 2.4GHz Wi-Fi across heavy vehicle queues.
          </p>
          <button
            type="button"
            onClick={() => alert('Downloading WPC RF Telemetry Audit...')}
            className="w-full py-2 rounded-xl border border-border bg-secondary hover:bg-secondary/80 text-xs font-semibold text-foreground transition-colors"
          >
            Download RF Audit
          </button>
        </div>

        <div className="rounded-2xl border border-border bg-card/60 p-5 space-y-3">
          <div className="size-9 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400">
            <Lock className="size-5" />
          </div>
          <h3 className="font-bold text-sm text-foreground">SHA-256 Cryptographic Audit Trail</h3>
          <p className="text-xs text-muted-foreground leading-relaxed">
            Append-only tamper-evident JSONL audit ledger. Each preemption event and Good Samaritan waiver is hash-chained to guarantee non-repudiation in court.
          </p>
          <button
            type="button"
            onClick={() => alert('Downloading SHA-256 Court Ledger...')}
            className="w-full py-2 rounded-xl border border-border bg-secondary hover:bg-secondary/80 text-xs font-semibold text-foreground transition-colors"
          >
            Export Hash Ledger
          </button>
        </div>
      </div>
    </div>
  )
}

export function SettingsView() {
  return (
    <div className="space-y-6 pb-12 max-w-4xl">
      <div className="border-b border-border pb-4">
        <h1 className="text-xl md:text-2xl font-bold tracking-tight text-foreground">
          System & Telemetry Settings
        </h1>
        <p className="text-xs md:text-sm text-muted-foreground mt-0.5">
          Configure Sub-GHz ISM radio frequencies, IRC:SP:12 timers, and Raipur ICCC MQTT brokers
        </p>
      </div>

      <div className="space-y-4">
        <div className="rounded-2xl border border-border bg-card/60 p-5 space-y-4">
          <h3 className="font-bold text-sm text-foreground flex items-center gap-2">
            <Radio className="size-4 text-cyan-400" />
            <span>Sub-GHz RF Configuration</span>
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-muted-foreground mb-1">Carrier Frequency (ISM)</label>
              <input
                type="text"
                disabled
                value="868.000 MHz (India License-Free)"
                className="w-full h-10 px-3 rounded-xl border border-border bg-secondary/50 text-foreground font-mono"
              />
            </div>
            <div>
              <label className="block text-muted-foreground mb-1">Hardware Ping Watchdog</label>
              <input
                type="text"
                disabled
                value="30 Seconds Auto-Reversion"
                className="w-full h-10 px-3 rounded-xl border border-border bg-secondary/50 text-foreground font-mono"
              />
            </div>
          </div>
        </div>

        <div className="rounded-2xl border border-border bg-card/60 p-5 space-y-4">
          <h3 className="font-bold text-sm text-foreground flex items-center gap-2">
            <Sliders className="size-4 text-emerald-400" />
            <span>IRC:SP:12 Deterministic Timing Buffers</span>
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-muted-foreground mb-1">Deceleration Amber (Yellow)</label>
              <input
                type="text"
                disabled
                value="3.5 Seconds Mandatory"
                className="w-full h-10 px-3 rounded-xl border border-border bg-secondary/50 text-foreground font-mono"
              />
            </div>
            <div>
              <label className="block text-muted-foreground mb-1">All-Red Clearance Interval</label>
              <input
                type="text"
                disabled
                value="2.0 Seconds Mandatory"
                className="w-full h-10 px-3 rounded-xl border border-border bg-secondary/50 text-foreground font-mono"
              />
            </div>
          </div>
        </div>

        <div className="rounded-2xl border border-border bg-card/60 p-5 space-y-4">
          <h3 className="font-bold text-sm text-foreground flex items-center gap-2">
            <Server className="size-4 text-primary" />
            <span>Raipur Smart City ICCC MQTT Broker</span>
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-muted-foreground mb-1">MQTT Broker Endpoint</label>
              <input
                type="text"
                disabled
                value="mqtt.raipurpolice.gov.in:8883 (TLS 1.3)"
                className="w-full h-10 px-3 rounded-xl border border-border bg-secondary/50 text-foreground font-mono"
              />
            </div>
            <div>
              <label className="block text-muted-foreground mb-1">Topic Prefix</label>
              <input
                type="text"
                disabled
                value="raipur/itms/ge_road/preempt"
                className="w-full h-10 px-3 rounded-xl border border-border bg-secondary/50 text-foreground font-mono"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
