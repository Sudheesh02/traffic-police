'use client'

import React, { useState } from 'react'
import {
  ChevronRight,
  ShieldCheck,
  Zap,
  Clock,
  ExternalLink,
  CheckCircle,
  AlertCircle,
  FileCheck,
} from 'lucide-react'
import {
  preemptionStreamData,
  type PreemptionStreamRow,
  type PreemptionStatus,
} from './data'
import { DashboardLink } from './navigation'

type StreamSectionProps = {
  customRows?: PreemptionStreamRow[]
}

export function StreamSection({ customRows }: StreamSectionProps) {
  const [selectedRow, setSelectedRow] = useState<PreemptionStreamRow | null>(null)
  const rows = customRows || preemptionStreamData

  return (
    <section className="flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-end justify-between gap-4">
        <div>
          <h2 className="text-base md:text-lg font-bold text-foreground tracking-tight">
            Live Preemption & Citizen Exemption Stream
          </h2>
          <p className="text-xs text-muted-foreground mt-0.5">
            Review and audit automated 868 MHz emergency overrides and statutory citizen e-challan exemptions
          </p>
        </div>

        <DashboardLink
          href="/whitelist"
          className="inline-flex items-center gap-1 text-xs font-semibold text-primary hover:underline"
        >
          <span>See all waivers</span>
          <ChevronRight className="size-4" />
        </DashboardLink>
      </div>

      {/* Astrix Data Table */}
      <div className="overflow-x-auto rounded-2xl border border-border bg-card/60">
        <table className="astrix-table min-w-[760px]">
          <thead>
            <tr>
              <th className="w-[30%]">Emergency / Incident</th>
              <th className="w-[20%]">Junction Node</th>
              <th className="w-[20%]">Strobe FFT / Sensor</th>
              <th className="w-[15%]">Status</th>
              <th className="w-[15%]">Logged At</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr
                key={row.id}
                onClick={() => setSelectedRow(row)}
                className="cursor-pointer"
              >
                <td>
                  <div className="space-y-0.5">
                    <p className="font-semibold text-xs text-foreground truncate">
                      {row.vehicle}
                    </p>
                    <div className="flex items-center gap-1.5 font-mono text-[11px] text-muted-foreground">
                      <span className="text-primary font-bold">{row.plateNumber}</span>
                      <span>·</span>
                      <span>{row.id}</span>
                    </div>
                  </div>
                </td>

                <td>
                  <span className="text-xs text-foreground font-medium">
                    {row.junction}
                  </span>
                </td>

                <td>
                  <div className="space-y-0.5">
                    <p className="text-xs font-mono text-cyan-400 font-medium">
                      {row.strobeFft}
                    </p>
                    <p className="text-[10px] text-muted-foreground">
                      Conf: {row.confidence}
                    </p>
                  </div>
                </td>

                <td>
                  <PreemptionStatusBadge status={row.status} />
                </td>

                <td>
                  <div className="space-y-0.5">
                    <span className="text-xs font-mono text-muted-foreground">
                      {row.timestamp}
                    </span>
                    <p className="text-[10px] text-muted-foreground/70 truncate">
                      {row.officer}
                    </p>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Row Details Modal / Audit Popup */}
      {selectedRow && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in">
          <div className="w-full max-w-md rounded-2xl border border-border bg-card p-5 shadow-2xl space-y-4">
            <div className="flex items-start justify-between border-b border-border pb-3">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground">
                  Audit Block #{selectedRow.id}
                </span>
                <h3 className="text-base font-bold text-foreground">
                  {selectedRow.vehicle}
                </h3>
              </div>
              <PreemptionStatusBadge status={selectedRow.status} />
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-border/60">
                <span className="text-muted-foreground">License Plate:</span>
                <span className="font-mono font-bold text-primary">{selectedRow.plateNumber}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-border/60">
                <span className="text-muted-foreground">Junction Location:</span>
                <span className="font-medium text-foreground">{selectedRow.junction}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-border/60">
                <span className="text-muted-foreground">Strobe FFT Verification:</span>
                <span className="font-mono text-cyan-400">{selectedRow.strobeFft}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-border/60">
                <span className="text-muted-foreground">Confidence Metric:</span>
                <span className="font-mono text-emerald-400">{selectedRow.confidence}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-border/60">
                <span className="text-muted-foreground">Statutory Exemption:</span>
                <span className="text-foreground">Sections 177 & 184 MVA 1988</span>
              </div>
              <div className="flex justify-between py-1 border-b border-border/60">
                <span className="text-muted-foreground">SHA-256 Proof:</span>
                <span className="font-mono text-[10px] text-muted-foreground truncate max-w-[200px]">
                  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
                </span>
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setSelectedRow(null)}
                className="px-4 py-2 rounded-xl bg-secondary text-xs font-semibold text-foreground hover:bg-secondary/80 transition-colors"
              >
                Close Audit View
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  )
}

function PreemptionStatusBadge({ status }: { status: PreemptionStatus }) {
  switch (status) {
    case 'active':
      return (
        <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-500/15 border border-emerald-500/30 px-2.5 py-1 text-xs font-semibold text-emerald-400">
          <span className="size-1.5 rounded-full bg-emerald-400 animate-pulse" />
          Priority Green
        </span>
      )
    case 'clearance':
      return (
        <span className="inline-flex items-center gap-1.5 rounded-full bg-amber-500/15 border border-amber-500/30 px-2.5 py-1 text-xs font-semibold text-amber-400">
          <span className="size-1.5 rounded-full bg-amber-400" />
          IRC Clearance
        </span>
      )
    case 'exempted':
      return (
        <span className="inline-flex items-center gap-1.5 rounded-full bg-cyan-500/15 border border-cyan-500/30 px-2.5 py-1 text-xs font-semibold text-cyan-400">
          <ShieldCheck className="size-3 text-cyan-400" />
          ₹0 Exempted
        </span>
      )
    case 'normal':
    default:
      return (
        <span className="inline-flex items-center gap-1 rounded-full bg-secondary border border-border px-2.5 py-1 text-xs font-medium text-muted-foreground">
          Fixed Cycle
        </span>
      )
  }
}
