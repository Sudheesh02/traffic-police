import type { ElementType } from 'react'
import {
  LayoutDashboard,
  Zap,
  Route,
  Bot,
  Video,
  ShieldCheck,
  FileText,
  Settings,
} from 'lucide-react'
import type { DashboardRoutePath } from './navigation'

export type NavigationItem = {
  name: string
  href: DashboardRoutePath
  icon: ElementType
  badge?: string
}

export const workspaceNavigation: NavigationItem[] = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Live Preemption', href: '/preemption', icon: Zap, badge: '42ms' },
  { name: 'Corridor & Twin', href: '/corridor', icon: Route, badge: 'GE Road' },
  { name: 'Agentic Consensus', href: '/agents', icon: Bot, badge: '6 Nodes' },
  { name: 'CCTV & ANPR Vision', href: '/cctv', icon: Video, badge: '1.84 Hz' },
  { name: 'Good Samaritan Ledger', href: '/whitelist', icon: ShieldCheck, badge: '142' },
  { name: 'Statutory Reports', href: '/reports', icon: FileText, badge: 'MVA 1988' },
  { name: 'ISM 868MHz Settings', href: '/settings', icon: Settings, badge: 'WPC' },
]

export const currentUser = {
  name: 'Insp. R. K. Sharma',
  email: 'traffic.iccc@raipurpolice.gov.in',
  role: 'Chief Traffic Operations Officer',
  unit: 'Raipur Traffic Police',
  initials: 'RS',
  avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
}

export type NotificationItem = {
  id: string
  title: string
  description: string
  time: string
  severity: 'info' | 'success' | 'warning'
  type: 'preemption' | 'exemption' | 'failover' | 'audit'
}

export const notifications: NotificationItem[] = [
  {
    id: 'NOTIF-01',
    title: 'Preemption Granted · 108 Ambulance',
    description: 'CG-04-TR-4912 preemption active at Jaistambh Chowk North approach.',
    time: '2 mins ago',
    severity: 'success',
    type: 'preemption',
  },
  {
    id: 'NOTIF-02',
    title: 'Good Samaritan Auto-Whitelisted',
    description: 'CG-04-MB-2219 granted statutory immunity under MVA 1988 Sec 177 & 184 (₹0 Challan).',
    time: '6 mins ago',
    severity: 'info',
    type: 'exemption',
  },
  {
    id: 'NOTIF-03',
    title: 'Form-C Hardware Interlock Verified',
    description: 'Zero probability of conflicting green feeds at Ghadi Chowk controller.',
    time: '14 mins ago',
    severity: 'info',
    type: 'audit',
  },
  {
    id: 'NOTIF-04',
    title: 'Sub-GHz ISM Telemetry Link Steady',
    description: '868.0 MHz link margin +14 dB above noise floor. Latency 42ms.',
    time: '28 mins ago',
    severity: 'info',
    type: 'audit',
  },
]

export type DateRange = 'today' | 'last-24-hours' | 'peak-hours' | 'monthly'

export type DateRangeOption = {
  label: string
  value: DateRange
}

export const dateRangeOptions: DateRangeOption[] = [
  { label: 'Today (Shift A · 08:00 - 16:00)', value: 'today' },
  { label: 'Last 24 Hours Telemetry', value: 'last-24-hours' },
  { label: 'Peak Rush Hours (17:00 - 20:30)', value: 'peak-hours' },
  { label: 'Monthly Statutory Aggregates', value: 'monthly' },
]

export type MetricCard = {
  label: string
  value: string
  trend?: {
    value: string
    label: string
    tone: 'positive' | 'warning' | 'neutral'
  }
  footnote?: string
}

export const dashboardMetricsByRange: Record<DateRange, MetricCard[]> = {
  today: [
    {
      label: 'Ambulance Transit Delay',
      value: '-68.4%',
      trend: { value: '-48.2s', label: 'saved per junction', tone: 'positive' },
      footnote: '45,000+ PCU/day Great Eastern Road baseline',
    },
    {
      label: 'Sub-GHz RF Latency',
      value: '42 ms',
      trend: { value: '+14 dB', label: 'link margin vs 2.4GHz', tone: 'positive' },
      footnote: '868.0 MHz license-free ISM compliance in India',
    },
    {
      label: 'IRC:SP:12 Inter-Green Buffer',
      value: '5.5 s',
      trend: { value: '3.5s Y + 2.0s AR', label: 'clearance verified', tone: 'positive' },
      footnote: 'Form-C mechanical interlock zero conflict',
    },
    {
      label: 'Good Samaritan Waivers',
      value: '142 / 142',
      trend: { value: '100%', label: 'granted (₹0 challan)', tone: 'positive' },
      footnote: 'Sections 177 & 184 MVA 1988 statutory sync',
    },
  ],
  'last-24-hours': [
    {
      label: 'Ambulance Transit Delay',
      value: '-65.1%',
      trend: { value: '-44.7s', label: 'average corridor delay', tone: 'positive' },
      footnote: 'Across 4 junctions (Jaistambh to Mekahara)',
    },
    {
      label: 'Sub-GHz RF Latency',
      value: '44 ms',
      trend: { value: '99.98%', label: 'packet delivery ratio', tone: 'positive' },
      footnote: 'Adversarial RF drop recovery < 100ms',
    },
    {
      label: 'IRC:SP:12 Inter-Green Buffer',
      value: '5.5 s',
      trend: { value: '100%', label: 'safety clearance maintained', tone: 'positive' },
      footnote: 'Zero broadside collisions recorded',
    },
    {
      label: 'Good Samaritan Waivers',
      value: '286 / 286',
      trend: { value: '₹2,86,000', label: 'false fines prevented', tone: 'positive' },
      footnote: '100% automated OCR & SHA-256 ledger proof',
    },
  ],
  'peak-hours': [
    {
      label: 'Ambulance Transit Delay',
      value: '-72.9%',
      trend: { value: '-62.0s', label: 'during 2,200 PCU/hr queue', tone: 'positive' },
      footnote: 'Corridor green wave dissipation activated',
    },
    {
      label: 'Sub-GHz RF Latency',
      value: '41 ms',
      trend: { value: '42ms', label: 'line-of-sight response', tone: 'positive' },
      footnote: 'Penetrates heavy bus and commercial truck queues',
    },
    {
      label: 'IRC:SP:12 Inter-Green Buffer',
      value: '5.5 s',
      trend: { value: 'Deterministic', label: 'hardware enforced', tone: 'positive' },
      footnote: 'Pedestrian & cross-traffic safely held',
    },
    {
      label: 'Good Samaritan Waivers',
      value: '89 / 89',
      trend: { value: '100%', label: 'instant exemption rate', tone: 'positive' },
      footnote: 'Yielding citizen vehicles logged in real time',
    },
  ],
  monthly: [
    {
      label: 'Ambulance Transit Delay',
      value: '-69.2%',
      trend: { value: '3,840 min', label: 'cumulative life-saving time', tone: 'positive' },
      footnote: 'Over 820 verified emergency missions',
    },
    {
      label: 'Sub-GHz RF Latency',
      value: '42.8 ms',
      trend: { value: '100%', label: '142-test adversarial suite', tone: 'positive' },
      footnote: 'Zero hardware faults, zero power-cycle drops',
    },
    {
      label: 'IRC:SP:12 Inter-Green Buffer',
      value: '5.5 s',
      trend: { value: 'Zero', label: 'accidents or conflicting feeds', tone: 'positive' },
      footnote: 'Statutory compliance across Raipur Commissionerate',
    },
    {
      label: 'Good Samaritan Waivers',
      value: '4,190 / 4,190',
      trend: { value: '₹41.9 Lakhs', label: 'citizen penalties waived', tone: 'positive' },
      footnote: 'Court-admissible SHA-256 tamper-evident trail',
    },
  ],
}

export type PreemptionStatus =
  | 'active'
  | 'clearance'
  | 'exempted'
  | 'normal'

export type PreemptionStreamRow = {
  id: string
  vehicle: string
  vehicleType: string
  plateNumber: string
  junction: string
  strobeFft: string
  confidence: string
  status: PreemptionStatus
  timestamp: string
  officer: string
}

export const preemptionStreamData: PreemptionStreamRow[] = [
  {
    id: 'PRE-2026-0847',
    vehicle: '108 Ambulance · Cardiac ICU',
    vehicleType: 'Medical ALS',
    plateNumber: 'CG-04-TR-4912',
    junction: 'Jaistambh Chowk (N)',
    strobeFft: '1.84 Hz (Optical Strobe)',
    confidence: '99.4%',
    status: 'active',
    timestamp: '10:14:22 IST',
    officer: 'Const. S. Verma (RF #12)',
  },
  {
    id: 'PRE-2026-0846',
    vehicle: 'Citizen WagonR (Yielding)',
    vehicleType: 'Good Samaritan',
    plateNumber: 'CG-04-MB-2219',
    junction: 'Jaistambh Chowk (N)',
    strobeFft: 'Preempted Stop-Line Pass',
    confidence: '98.9%',
    status: 'exempted',
    timestamp: '10:14:18 IST',
    officer: 'Automated ANPR AI',
  },
  {
    id: 'PRE-2026-0845',
    vehicle: 'Fire Tender 03 · Sector 2',
    vehicleType: 'Fire Engine',
    plateNumber: 'CG-04-FE-1002',
    junction: 'Ghadi Chowk (W)',
    strobeFft: '2.10 Hz (Emergency Strobe)',
    confidence: '99.1%',
    status: 'clearance',
    timestamp: '10:08:45 IST',
    officer: 'Officer R. Rathore (RF #04)',
  },
  {
    id: 'PRE-2026-0844',
    vehicle: 'Citizen Creta (Yielding)',
    vehicleType: 'Good Samaritan',
    plateNumber: 'CG-04-NL-8841',
    junction: 'Ghadi Chowk (W)',
    strobeFft: 'Left-Shoulder Waiver',
    confidence: '97.8%',
    status: 'exempted',
    timestamp: '10:08:39 IST',
    officer: 'Automated ANPR AI',
  },
  {
    id: 'PRE-2026-0843',
    vehicle: '108 Ambulance · Trauma Unit',
    vehicleType: 'Medical BLS',
    plateNumber: 'CG-04-TR-3105',
    junction: 'Telibandha Chowk',
    strobeFft: '1.82 Hz (Optical Strobe)',
    confidence: '98.7%',
    status: 'normal',
    timestamp: '09:52:10 IST',
    officer: 'Const. K. Dewangan (RF #09)',
  },
  {
    id: 'PRE-2026-0842',
    vehicle: 'Police PCR Van 08',
    vehicleType: 'Police Patrol',
    plateNumber: 'CG-04-PV-0008',
    junction: 'Fafadih Chowk',
    strobeFft: '1.95 Hz (Red-Blue Strobe)',
    confidence: '99.6%',
    status: 'normal',
    timestamp: '09:30:15 IST',
    officer: 'SI M. Tiwari (RF #01)',
  },
]
