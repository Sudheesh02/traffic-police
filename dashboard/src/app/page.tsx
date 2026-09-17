'use client'

import React, { useState, useEffect } from 'react'
import {
  DashboardNavigationProvider,
  useDashboardNavigation,
} from '../components/astrix/navigation'
import { AstrixDashboardLayout } from '../components/astrix/dashboard-layout'
import {
  OverviewView,
  PreemptionView,
  CorridorTwinView,
  AgenticView,
  GoodSamaritanView,
  ReportsView,
  SettingsView,
} from '../components/astrix/workspace-views'
import { DispatchModal } from '../components/DispatchModal'
import { preemptionStreamData, type PreemptionStreamRow } from '../components/astrix/data'
import {
  RAIPUR_JUNCTIONS,
  INITIAL_ANPR_LOGS,
  INITIAL_AUDIT_BLOCKS,
  INITIAL_AGENT_STATES,
} from '../lib/mockData'
import {
  SignalPhase,
  LaneDirection,
  ANPRVehicleRecord,
  AuditBlock,
  AgentDecisionRecord,
} from '../lib/types'

function AstrixDashboardApp() {
  const { pathname } = useDashboardNavigation()

  // Preemption & Signal State Machine
  const [junctions, setJunctions] = useState(RAIPUR_JUNCTIONS)
  const [selectedJunctionId, setSelectedJunctionId] = useState<string>('RPR_GE_ROAD_01')
  const [emergencyActive, setEmergencyActive] = useState<boolean>(false)
  const [activeLane, setActiveLane] = useState<LaneDirection>('NORTH_BOUND')
  const [phase, setPhase] = useState<SignalPhase>('NORMAL_CYCLE')
  const [phaseTimer, setPhaseTimer] = useState<number>(24.0)
  const [latencyMs, setLatencyMs] = useState<number>(42)
  const [vehicles, setVehicles] = useState<ANPRVehicleRecord[]>(INITIAL_ANPR_LOGS)
  const [auditBlocks, setAuditBlocks] = useState<AuditBlock[]>(INITIAL_AUDIT_BLOCKS)
  const [agentStates, setAgentStates] = useState<AgentDecisionRecord[]>(INITIAL_AGENT_STATES)
  const [transitProgress, setTransitProgress] = useState<number>(15)
  const [audioEnabled, setAudioEnabled] = useState<boolean>(true)
  const [isDispatchModalOpen, setIsDispatchModalOpen] = useState<boolean>(false)
  const [streamRows, setStreamRows] = useState<PreemptionStreamRow[]>(preemptionStreamData)

  // Synthesize Web Audio API Tactical Radio / Beep
  const playTacticalBeep = (freq = 880, durationMs = 120) => {
    if (!audioEnabled || typeof window === 'undefined') return
    try {
      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext
      if (!AudioCtx) return
      const ctx = new AudioCtx()
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()
      osc.type = 'sine'
      osc.frequency.setValueAtTime(freq, ctx.currentTime)
      gain.gain.setValueAtTime(0.1, ctx.currentTime)
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + durationMs / 1000)
      osc.connect(gain)
      gain.connect(ctx.destination)
      osc.start()
      osc.stop(ctx.currentTime + durationMs / 1000)
    } catch {
      // Audio autoplay policy fallback
    }
  }

  // Preemption State Machine Loop
  useEffect(() => {
    const timer = setInterval(() => {
      if (emergencyActive) {
        setTransitProgress((prev) => (prev >= 95 ? 15 : prev + 0.8))
      }

      setPhaseTimer((prev) => {
        if (prev <= 0.1) {
          if (emergencyActive) {
            if (phase === 'ACTIVE_YELLOW') {
              playTacticalBeep(660, 200)
              setPhase('ALL_RED_CLEARANCE')
              return 2.0 // Mandatory 2.0s All-Red clearance
            } else if (phase === 'ALL_RED_CLEARANCE') {
              playTacticalBeep(1100, 300)
              setPhase('PRIORITY_GREEN')
              return 22.0 // 22.0s Priority Green corridor
            } else if (phase === 'PRIORITY_GREEN') {
              playTacticalBeep(550, 150)
              setPhase('RECOVERY_YELLOW')
              return 3.5
            } else if (phase === 'RECOVERY_YELLOW') {
              setPhase('RECOVERY_ALL_RED')
              return 1.5
            } else if (phase === 'RECOVERY_ALL_RED') {
              setPhase('NORMAL_CYCLE')
              setEmergencyActive(false)
              setTransitProgress(15)
              return 24.0
            }
          }
          return 24.0
        }
        return Math.max(0, Number((prev - 0.1).toFixed(1)))
      })
    }, 100)

    return () => clearInterval(timer)
  }, [emergencyActive, phase, audioEnabled])

  // Trigger Preemption Flow
  const handleTriggerPreemption = (lane: LaneDirection = 'NORTH_BOUND', durationSec = 22) => {
    playTacticalBeep(920, 250)
    setEmergencyActive(true)
    setActiveLane(lane)
    setLatencyMs(42)
    setPhase('ACTIVE_YELLOW')
    setPhaseTimer(3.5)
    setTransitProgress(20)

    const newRow: PreemptionStreamRow = {
      id: `PRE-2026-${Math.floor(1000 + Math.random() * 9000)}`,
      vehicle: '108 Ambulance · Advanced Life Support',
      vehicleType: 'Medical ALS',
      plateNumber: 'CG-04-TR-4912',
      junction: 'Jaistambh Chowk (North)',
      strobeFft: '1.84 Hz (Optical Strobe)',
      confidence: '99.4%',
      status: 'active',
      timestamp: new Date().toLocaleTimeString('en-IN', { hour12: false }) + ' IST',
      officer: 'Const. S. Verma (RF #12)',
    }
    setStreamRows((prev) => [newRow, ...prev])

    const newBlock: AuditBlock = {
      blockHeight: auditBlocks[0].blockHeight + 1,
      timestamp: new Date().toISOString(),
      junctionId: `Jaistambh Chowk (RPR_GE_ROAD_01)`,
      overrideSource: 'HANDHELD_RF_REMOTE_02',
      vehicleClass: '108_AMBULANCE',
      primaryPlate: 'CG-04-TR-4912',
      preemptionDurationSec: durationSec,
      whitelistedPlates: ['CG-04-MB-2219', 'CG-04-NL-8841'],
      prevHash: auditBlocks[0].blockHash,
      blockHash: '7c8a1e2f3d4b5c6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e',
      isTamperProof: true,
    }
    setAuditBlocks((prev) => [newBlock, ...prev])
  }

  // Cancel Preemption Flow
  const handleCancelPreemption = () => {
    playTacticalBeep(440, 150)
    setPhase('RECOVERY_YELLOW')
    setPhaseTimer(3.5)
  }

  // Handle CAD Dispatch from Modal
  const handleCustomDispatch = (
    vehicle: string,
    lane: LaneDirection,
    strobeValid: boolean,
    duration: number
  ) => {
    if (!strobeValid) {
      alert(
        'SECURITY ALERT: Strobe frequency out-of-band (<1.0 Hz). Decoy vehicle rejected by Agentic Layer.'
      )
      return
    }
    handleTriggerPreemption(lane, duration)
  }

  // Simulate Yielding Good Samaritan Citizen
  const handleSimulateYieldingCitizen = () => {
    playTacticalBeep(780, 80)
    const randomSuffix = Math.floor(1000 + Math.random() * 9000)
    const plate = `CG-04-TR-${randomSuffix}`

    const newCar: ANPRVehicleRecord = {
      id: `VEH-${Date.now().toString().slice(-4)}`,
      timestamp: new Date().toLocaleTimeString('en-IN', { hour12: false }),
      plate: plate,
      vehicleType: 'CITIZEN_CAR',
      confidence: 0.952,
      speedKmh: 14,
      crossedStopLineOnRed: true,
      yieldingToEmergency: true,
      status: 'EXEMPT_GOOD_SAMARITAN',
      challanAmountInr: 0,
      exemptReason: 'Yielded stop-line for emergency ambulance preemption (MVA Sec 177)',
    }
    setVehicles((prev) => [newCar, ...prev])

    const newRow: PreemptionStreamRow = {
      id: `PRE-2026-${Math.floor(1000 + Math.random() * 9000)}`,
      vehicle: `Citizen Car (${plate})`,
      vehicleType: 'Good Samaritan',
      plateNumber: plate,
      junction: 'Jaistambh Chowk (N)',
      strobeFft: 'Preempted Stop-Line Pass',
      confidence: '98.9%',
      status: 'exempted',
      timestamp: new Date().toLocaleTimeString('en-IN', { hour12: false }) + ' IST',
      officer: 'Automated ANPR AI',
    }
    setStreamRows((prev) => [newRow, ...prev])
  }

  // Active view switcher based on Astrix sidebar route
  let currentContent: React.ReactNode = null
  const sharedProps = {
    junctions,
    selectedJunctionId,
    onSelectJunction: setSelectedJunctionId,
    phase,
    phaseTimer,
    emergencyActive,
    transitProgress,
    activeLane,
    latencyMs,
    vehicles,
    auditBlocks,
    agentStates,
    onTriggerPreemption: handleTriggerPreemption,
    onCancelPreemption: handleCancelPreemption,
    onAddYieldingCitizen: handleSimulateYieldingCitizen,
    customStreamRows: streamRows,
  }

  switch (pathname) {
    case '/':
      currentContent = <OverviewView {...sharedProps} />
      break
    case '/preemption':
      currentContent = <PreemptionView {...sharedProps} />
      break
    case '/corridor':
      currentContent = <CorridorTwinView {...sharedProps} />
      break
    case '/agents':
      currentContent = <AgenticView {...sharedProps} />
      break
    case '/cctv':
      currentContent = <PreemptionView {...sharedProps} />
      break
    case '/whitelist':
      currentContent = <GoodSamaritanView />
      break
    case '/reports':
      currentContent = <ReportsView />
      break
    case '/settings':
      currentContent = <SettingsView />
      break
    default:
      currentContent = <OverviewView {...sharedProps} />
  }

  return (
    <AstrixDashboardLayout
      onOpenDispatch={() => setIsDispatchModalOpen(true)}
      onPreemptToggle={() => {
        if (emergencyActive) {
          handleCancelPreemption()
        } else {
          handleTriggerPreemption(activeLane)
        }
      }}
      isPreempting={emergencyActive}
      audioEnabled={audioEnabled}
      onToggleAudio={() => setAudioEnabled((prev) => !prev)}
    >
      {currentContent}

      {/* CAD Dispatch Modal */}
      <DispatchModal
        isOpen={isDispatchModalOpen}
        onClose={() => setIsDispatchModalOpen(false)}
        onDispatch={handleCustomDispatch}
      />
    </AstrixDashboardLayout>
  )
}

export default function Page() {
  return (
    <DashboardNavigationProvider>
      <AstrixDashboardApp />
    </DashboardNavigationProvider>
  )
}
