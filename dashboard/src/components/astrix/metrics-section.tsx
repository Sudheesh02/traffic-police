'use client'

import React, { useState } from 'react'
import {
  MetricCubeIcon,
  TrendingUpIcon,
  CalendarIcon,
  ChevronDownIcon,
  ExportIcon,
} from './icons'
import {
  dashboardMetricsByRange,
  dateRangeOptions,
  type DateRange,
  type MetricCard,
} from './data'

export function MetricsSection() {
  const [dateRange, setDateRange] = useState<DateRange>('today')
  const [isDropdownOpen, setIsDropdownOpen] = useState(false)

  const activeOption = dateRangeOptions.find((o) => o.value === dateRange) || dateRangeOptions[0]

  const handleExportTelemetry = () => {
    const dataStr =
      'data:text/json;charset=utf-8,' +
      encodeURIComponent(
        JSON.stringify(
          {
            corridor: 'Great Eastern Road (Jaistambh to Mekahara Hospital)',
            jurisdiction: 'Raipur Police Commissionerate',
            timestamp: new Date().toISOString(),
            metrics: dashboardMetricsByRange[dateRange],
          },
          null,
          2
        )
      )
    const downloadAnchor = document.createElement('a')
    downloadAnchor.setAttribute('href', dataStr)
    downloadAnchor.setAttribute('download', `raipur_itms_telemetry_${dateRange}.json`)
    document.body.appendChild(downloadAnchor)
    downloadAnchor.click()
    downloadAnchor.remove()
  }

  return (
    <section className="flex flex-col gap-4 md:gap-5">
      {/* Section Header */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-xl md:text-2xl font-bold tracking-tight text-foreground">
            Raipur ITMS Real-Time Telemetry
          </h1>
          <p className="text-xs md:text-sm text-muted-foreground mt-0.5">
            Great Eastern Road Corridor · Live Sub-GHz RF & Edge-AI Signal Automation
          </p>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          {/* Shift/Range Dropdown */}
          <div className="relative">
            <button
              type="button"
              onClick={() => setIsDropdownOpen((prev) => !prev)}
              className="flex items-center gap-2 h-10 px-3.5 rounded-xl border border-border bg-card hover:bg-secondary text-xs font-semibold text-foreground transition-all shadow-sm"
            >
              <CalendarIcon className="size-4 text-muted-foreground" />
              <span>{activeOption.label}</span>
              <ChevronDownIcon className="size-3.5 text-muted-foreground ml-1" />
            </button>

            {isDropdownOpen && (
              <div className="absolute right-0 mt-2 w-64 rounded-2xl border border-border bg-card p-1.5 shadow-2xl z-50 animate-in fade-in zoom-in-95">
                {dateRangeOptions.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => {
                      setDateRange(option.value)
                      setIsDropdownOpen(false)
                    }}
                    className={`flex items-center justify-between w-full px-3 py-2 rounded-xl text-xs transition-colors ${
                      dateRange === option.value
                        ? 'bg-primary/15 text-primary font-semibold'
                        : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                    }`}
                  >
                    <span>{option.label}</span>
                    {dateRange === option.value && <span className="size-1.5 rounded-full bg-primary" />}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Export Button */}
          <button
            type="button"
            onClick={handleExportTelemetry}
            className="flex items-center gap-2 h-10 px-3.5 rounded-xl border border-border bg-card hover:bg-secondary text-xs font-semibold text-foreground transition-all shadow-sm"
          >
            <ExportIcon className="size-4 text-muted-foreground" />
            <span className="hidden sm:inline">Export JSON</span>
          </button>
        </div>
      </div>

      {/* 4-Card Astrix Metric Grid */}
      <div className="grid gap-3.5 sm:grid-cols-2 xl:grid-cols-4">
        {dashboardMetricsByRange[dateRange].map((metric) => (
          <MetricCardItem key={metric.label} metric={metric} />
        ))}
      </div>
    </section>
  )
}

function MetricCardItem({ metric }: { metric: MetricCard }) {
  return (
    <article className="rounded-2xl border border-border bg-card p-4 md:p-5 hover:border-primary/50 transition-all shadow-sm hover:shadow-md flex flex-col justify-between">
      <div className="flex flex-col gap-3">
        <div className="flex items-center gap-3">
          <div className="flex size-9 items-center justify-center rounded-xl border border-primary/20 bg-primary/10 text-primary shrink-0">
            <MetricCubeIcon className="size-4" />
          </div>
          <p className="text-xs font-semibold text-muted-foreground leading-tight">
            {metric.label}
          </p>
        </div>

        <div>
          <p className="text-2xl md:text-3xl font-bold tracking-tight text-foreground font-mono tabular-nums">
            {metric.value}
          </p>
        </div>
      </div>

      <div className="flex flex-col gap-2 mt-3 pt-3 border-t border-border/50">
        {metric.trend && (
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="inline-flex items-center gap-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 text-xs font-semibold text-emerald-500">
              <TrendingUpIcon className="size-3" />
              {metric.trend.value}
            </span>
            <span className="text-[11px] text-muted-foreground font-medium">
              {metric.trend.label}
            </span>
          </div>
        )}

        {metric.footnote && (
          <p className="text-[11px] text-muted-foreground/80 leading-relaxed">
            {metric.footnote}
          </p>
        )}
      </div>
    </article>
  )
}
