import React from 'react'
import { Clock, CheckCircle, AlertTriangle, ShieldCheck } from 'lucide-react'

export type PreemptionStatus =
  | 'priority_green'
  | 'intergreen'
  | 'exempted'
  | 'normal'

const statusConfig: Record<
  string,
  {
    label: string
    className: string
    icon: React.ComponentType<{ className?: string }>
  }
> = {
  priority_green: {
    label: 'Priority Green (Active)',
    className: 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30',
    icon: CheckCircle,
  },
  intergreen: {
    label: 'IRC:SP:12 Clearance (5.5s)',
    className: 'bg-amber-500/15 text-amber-400 border border-amber-500/30',
    icon: AlertTriangle,
  },
  exempted: {
    label: 'Good Samaritan (₹0 Exemption)',
    className: 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30',
    icon: ShieldCheck,
  },
  normal: {
    label: 'Fixed Round-Robin Cycle',
    className: 'bg-muted text-muted-foreground border border-border',
    icon: Clock,
  },
}

export function PreemptionStatusBadge({ status }: { status: string }) {
  const normalized = status.toLowerCase().replace(/[\s-]/g, '_')
  const config =
    statusConfig[normalized] ||
    (status.includes('Green') || status.includes('PRIORITY')
      ? statusConfig.priority_green
      : status.includes('Clearance') || status.includes('Yellow')
      ? statusConfig.intergreen
      : status.includes('Exempt') || status.includes('Challan')
      ? statusConfig.exempted
      : statusConfig.normal)

  const Icon = config.icon

  return (
    <span
      className={`inline-flex h-7 items-center gap-1.5 rounded-xl px-3 text-xs font-semibold ${config.className}`}
    >
      <Icon className="size-3.5 shrink-0" />
      {config.label}
    </span>
  )
}
