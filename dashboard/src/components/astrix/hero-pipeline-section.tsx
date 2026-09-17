'use client'

import React, { useState } from 'react'
import {
  Plus,
  Minus,
  Maximize2,
  Minimize2,
  Zap,
  Radio,
  Eye,
  ShieldCheck,
  CheckCircle2,
  Layers,
  Cpu,
  Route,
} from 'lucide-react'
import { JunctionTwin } from '../JunctionTwin'
import { CorridorMap } from '../CorridorMap'
import { JunctionData, SignalPhase } from '../../lib/types'
import { RAIPUR_JUNCTIONS } from '../../lib/mockData'

type HeroPipelineProps = {
  isPreempting: boolean
  phase: SignalPhase
  phaseTimer: number
  transitProgress: number
  onPreemptToggle: () => void
}

export function HeroPipelineSection({
  isPreempting,
  phase,
  phaseTimer,
  transitProgress,
  onPreemptToggle,
}: HeroPipelineProps) {
  const [activeTab, setActiveTab] = useState<'pipeline' | 'twin' | 'corridor'>('pipeline')
  const [zoomLevel, setZoomLevel] = useState<number>(1)
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false)
  const [selectedJunctionId, setSelectedJunctionId] = useState<string>('RPR_GE_ROAD_01')

  const handleZoomIn = () => setZoomLevel((prev) => Math.min(prev + 0.15, 1.45))
  const handleZoomOut = () => setZoomLevel((prev) => Math.max(prev - 0.15, 0.75))

  const selectedJunction =
    RAIPUR_JUNCTIONS.find((j) => j.id === selectedJunctionId) || RAIPUR_JUNCTIONS[0]

  return (
    <section className="flex flex-col gap-3">
      {/* Top Header Row with Mode Switcher */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div className="flex items-center gap-2">
          <h2 className="text-base md:text-lg font-bold text-foreground tracking-tight">
            Live Signal Automation & Spatial Twin
          </h2>
          <span className="rounded-full bg-primary/10 border border-primary/20 px-2.5 py-0.5 text-[11px] font-semibold text-primary">
            GE Road Corridor
          </span>
        </div>

        {/* Tab switcher buttons */}
        <div className="flex items-center bg-secondary/80 p-1 rounded-xl border border-border shadow-sm">
          <button
            type="button"
            onClick={() => setActiveTab('pipeline')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'pipeline'
                ? 'bg-card text-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <Zap className="size-3.5 text-amber-500" />
            <span>Preemption Pipeline</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('twin')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'twin'
                ? 'bg-card text-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <Layers className="size-3.5 text-cyan-500" />
            <span>Jaistambh 4-Way Twin</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('corridor')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'corridor'
                ? 'bg-card text-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            <Route className="size-3.5 text-emerald-500" />
            <span>GIS Corridor Map</span>
          </button>
        </div>
      </div>

      {/* Astrix Signature Viewport with Pipeline Dots */}
      <div
        className={`relative overflow-hidden rounded-2xl border border-border bg-card/60 transition-all shadow-sm ${
          isFullscreen
            ? 'fixed inset-4 z-50 bg-background/95 backdrop-blur-xl h-auto'
            : 'min-h-[490px] h-[520px]'
        }`}
      >
        {/* Dot Matrix Background */}
        <div className="pipeline-dots absolute inset-0 pointer-events-none opacity-80" />

        {/* Live Pipeline Status Pill */}
        <div className="absolute top-4 left-4 z-30 flex items-center gap-2 flex-wrap">
          <div className="flex items-center gap-2 rounded-xl border border-border bg-card/90 px-3 py-1.5 shadow-sm backdrop-blur-md">
            <span className="relative flex size-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full size-2.5 bg-emerald-500" />
            </span>
            <span className="text-xs font-bold text-emerald-500">
              Live Pipeline
            </span>
            <span className="text-muted-foreground text-xs">|</span>
            <span className="text-xs font-mono text-muted-foreground">
              {activeTab === 'pipeline'
                ? 'Deterministic 6-Stage Flow'
                : activeTab === 'twin'
                ? 'Jaistambh Physical Interlocks'
                : 'Telibandha to Mekahara Lifeline'}
            </span>
          </div>

          {isPreempting && (
            <div className="flex items-center gap-2 rounded-xl border border-rose-500/40 bg-rose-950/80 px-3 py-1.5 shadow-sm animate-pulse backdrop-blur-md">
              <span className="size-2 rounded-full bg-rose-500" />
              <span className="text-xs font-mono font-bold text-rose-200">
                PREEMPTION ACTIVE: {phase} ({phaseTimer.toFixed(1)}s)
              </span>
            </div>
          )}
        </div>

        {/* Viewport Content */}
        <div
          className="w-full h-full flex items-center justify-center p-4 pt-14 pb-16 transition-transform duration-200 overflow-y-auto"
          style={{ transform: `scale(${zoomLevel})` }}
        >
          {activeTab === 'pipeline' && (
            <InteractivePipelineFlow
              isPreempting={isPreempting}
              phase={phase}
              onPreemptToggle={onPreemptToggle}
            />
          )}

          {activeTab === 'twin' && (
            <div className="w-full h-full flex items-center justify-center">
              <JunctionTwin
                junction={selectedJunction}
                phase={phase}
                phaseTimer={phaseTimer}
                emergencyActive={isPreempting}
              />
            </div>
          )}

          {activeTab === 'corridor' && (
            <div className="w-full h-full flex items-center justify-center">
              <CorridorMap
                junctions={RAIPUR_JUNCTIONS}
                selectedJunctionId={selectedJunctionId}
                onSelectJunction={setSelectedJunctionId}
                emergencyActive={isPreempting}
                transitProgress={transitProgress}
              />
            </div>
          )}
        </div>

        {/* Bottom-Left Zoom Controls */}
        <div className="absolute bottom-4 left-4 z-30 flex items-center rounded-xl border border-border bg-card/90 backdrop-blur-md overflow-hidden shadow-sm">
          <button
            type="button"
            onClick={handleZoomIn}
            className="p-2 text-muted-foreground hover:text-foreground hover:bg-secondary border-r border-border transition-colors"
            aria-label="Zoom in"
          >
            <Plus className="size-4" />
          </button>
          <span className="px-2.5 text-[11px] font-mono text-muted-foreground">
            {Math.round(zoomLevel * 100)}%
          </span>
          <button
            type="button"
            onClick={handleZoomOut}
            className="p-2 text-muted-foreground hover:text-foreground hover:bg-secondary border-l border-border transition-colors"
            aria-label="Zoom out"
          >
            <Minus className="size-4" />
          </button>
        </div>

        {/* Bottom-Right Fullscreen / Preview Toggle */}
        <div className="absolute bottom-4 right-4 z-30 flex items-center gap-2">
          <button
            type="button"
            onClick={() => setIsFullscreen((prev) => !prev)}
            className="flex items-center gap-1.5 h-9 px-3 rounded-xl border border-border bg-card/90 hover:bg-secondary text-xs font-semibold text-foreground backdrop-blur-md transition-colors shadow-sm"
          >
            {isFullscreen ? <Minimize2 className="size-4 text-primary" /> : <Maximize2 className="size-4 text-primary" />}
            <span>{isFullscreen ? 'Exit C2 Mode' : 'Full C2 Preview'}</span>
          </button>
        </div>
      </div>
    </section>
  )
}

function InteractivePipelineFlow({
  isPreempting,
  phase,
  onPreemptToggle,
}: {
  isPreempting: boolean
  phase: SignalPhase
  onPreemptToggle: () => void
}) {
  const nodes = [
    {
      step: '01',
      title: '868 MHz Sub-GHz RF',
      subtitle: 'Constable Handheld (42ms)',
      icon: Radio,
      active: isPreempting,
      color: 'border-cyan-500/60 bg-cyan-500/10 text-cyan-400',
    },
    {
      step: '02',
      title: 'Dual-Stage Optical AI',
      subtitle: 'YOLOv8 + 1.84Hz Strobe FFT',
      icon: Eye,
      active: isPreempting,
      color: 'border-amber-500/60 bg-amber-500/10 text-amber-400',
    },
    {
      step: '03',
      title: '6-Agent Consensus',
      subtitle: 'Autonomous Safety Engine',
      icon: Cpu,
      active: isPreempting,
      color: 'border-primary/60 bg-primary/10 text-primary',
    },
    {
      step: '04',
      title: 'IRC:SP:12 Inter-Green',
      subtitle: '3.5s Yellow + 2.0s All-Red',
      icon: ShieldCheck,
      active: isPreempting,
      color:
        phase === 'ACTIVE_YELLOW'
          ? 'border-yellow-500/80 bg-yellow-500/15 text-yellow-400'
          : phase === 'ALL_RED_CLEARANCE'
          ? 'border-red-500/80 bg-red-500/15 text-red-400'
          : 'border-border bg-card/80 text-muted-foreground',
    },
    {
      step: '05',
      title: 'Form-C Relay Interlock',
      subtitle: 'Priority Green (15-30s)',
      icon: CheckCircle2,
      active: phase === 'PRIORITY_GREEN',
      color:
        phase === 'PRIORITY_GREEN'
          ? 'border-emerald-500/80 bg-emerald-500/15 text-emerald-400 glow-emerald'
          : 'border-border bg-card/80 text-muted-foreground',
    },
    {
      step: '06',
      title: 'Good Samaritan OCR',
      subtitle: 'MVA 1988 ₹0 Auto-Waiver',
      icon: Layers,
      active: isPreempting,
      color: 'border-blue-500/60 bg-blue-500/10 text-blue-400',
    },
  ]

  return (
    <div className="w-full max-w-5xl py-2 px-2 flex flex-col items-center justify-center">
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 w-full">
        {nodes.map((n, idx) => {
          const Icon = n.icon
          return (
            <div
              key={n.step}
              className={`relative flex flex-col justify-between p-3.5 rounded-2xl border transition-all shadow-sm ${
                n.active
                  ? `${n.color} shadow-md scale-102 ring-1`
                  : 'border-border bg-card/90 text-muted-foreground hover:border-primary/30'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-mono font-bold tracking-wider text-primary">
                    STEP {n.step}
                  </span>
                  <Icon className="size-4 shrink-0" />
                </div>

                <p className="text-xs font-bold text-foreground leading-tight mb-1">
                  {n.title}
                </p>
                <p className="text-[11px] opacity-80 leading-snug">
                  {n.subtitle}
                </p>
              </div>

              {idx < nodes.length - 1 && (
                <div className="hidden lg:block absolute -right-2.5 top-1/2 -translate-y-1/2 z-20 text-muted-foreground/40 font-mono font-bold">
                  →
                </div>
              )}
            </div>
          )
        })}
      </div>

      <div className="mt-7 flex items-center justify-center gap-3">
        <button
          type="button"
          onClick={onPreemptToggle}
          className={`px-5 py-2.5 rounded-xl text-xs font-bold transition-all shadow-md ${
            isPreempting
              ? 'bg-rose-600 text-white hover:bg-rose-700 animate-pulse'
              : 'bg-primary text-primary-foreground hover:opacity-90 glow-primary'
          }`}
        >
          {isPreempting ? 'Simulate Corridor Passage Complete' : 'Trigger Handheld RF Test Stream (42ms)'}
        </button>
      </div>
    </div>
  )
}
