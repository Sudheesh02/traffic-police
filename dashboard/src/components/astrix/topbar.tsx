'use client'

import React, { useEffect, useRef, useState } from 'react'
import {
  Volume2,
  VolumeX,
  Radio,
  Zap,
  CheckCircle,
  AlertTriangle,
  Info,
  Clock,
  Send,
  Siren,
  Sun,
  Moon,
} from 'lucide-react'
import {
  BellIcon,
  CmdIcon,
  SearchIcon,
  SidebarToggleIcon,
} from './icons'
import { useDashboardNavigation } from './navigation'
import { notifications } from './data'

type TopbarProps = {
  onOpenDispatch: () => void
  onPreemptToggle: () => void
  isPreempting: boolean
  audioEnabled: boolean
  onToggleAudio: () => void
}

export function DashboardTopbar({
  onOpenDispatch,
  onPreemptToggle,
  isPreempting,
  audioEnabled,
  onToggleAudio,
}: TopbarProps) {
  const { toggleSidebar, theme, toggleTheme } = useDashboardNavigation()
  const [searchQuery, setSearchQuery] = useState('')
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false)
  const [currentTime, setCurrentTime] = useState('')
  const searchInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    const updateTime = () => {
      const now = new Date()
      setCurrentTime(
        now.toLocaleTimeString('en-IN', {
          timeZone: 'Asia/Kolkata',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: false,
        }) + ' IST'
      )
    }
    updateTime()
    const timer = setInterval(updateTime, 1000)
    return () => clearInterval(timer)
  }, [])

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault()
        searchInputRef.current?.focus()
      }
      if (event.key === 'Escape') {
        setIsNotificationsOpen(false)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return (
    <header className="flex h-16 items-center justify-between gap-3 md:gap-4 border-b border-border bg-card/80 backdrop-blur-md px-4 md:px-6 z-40 shrink-0">
      {/* Left: Mobile Sidebar Toggle + Search */}
      <div className="flex flex-1 items-center gap-2 md:gap-3 max-w-sm md:max-w-md">
        <button
          type="button"
          onClick={toggleSidebar}
          className="p-2 text-muted-foreground hover:text-foreground md:hidden rounded-lg hover:bg-secondary shrink-0"
          aria-label="Toggle Sidebar"
        >
          <SidebarToggleIcon className="size-5" />
        </button>

        <div className="relative flex-1 flex items-center min-w-0">
          <div className="absolute left-3 pointer-events-none text-muted-foreground">
            <SearchIcon className="size-4" />
          </div>
          <input
            ref={searchInputRef}
            type="text"
            placeholder="Search corridor, plates (CG 04)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full h-10 pl-9 pr-14 rounded-xl border border-border bg-secondary/70 text-xs md:text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary transition-all truncate"
          />
          <div className="absolute right-2.5 flex items-center gap-0.5 rounded-md bg-card border border-border px-1.5 py-0.5 text-[10px] font-mono text-muted-foreground pointer-events-none">
            <CmdIcon className="size-2.5" />
            <span>K</span>
          </div>
        </div>
      </div>

      {/* Middle: Live Raipur Telemetry Readout (visible on XL screens) */}
      <div className="hidden xl:flex items-center gap-3">
        <div className="flex items-center gap-2 rounded-xl bg-secondary/80 border border-border px-3 py-1.5 shadow-sm">
          <span className="relative flex size-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
            <span className="relative inline-flex rounded-full size-2 bg-emerald-500" />
          </span>
          <span className="text-xs font-semibold text-foreground">Raipur ITMS C2</span>
          <span className="text-xs text-muted-foreground">|</span>
          <span className="text-xs font-mono text-cyan-400 font-semibold">868.0 MHz (42ms)</span>
          <span className="text-xs text-muted-foreground">|</span>
          <span className="text-xs text-emerald-400 font-mono font-medium">IRC:SP:12 5.5s</span>
        </div>

        <div className="flex items-center gap-1.5 text-xs font-mono text-muted-foreground px-2">
          <Clock className="size-3.5 text-muted-foreground" />
          <span>{currentTime || '00:00:00 IST'}</span>
        </div>
      </div>

      {/* Right: Quick Actions & Notifications */}
      <div className="flex items-center gap-2">
        {/* Theme Toggle Button */}
        <button
          type="button"
          onClick={toggleTheme}
          title={theme === 'dark' ? 'Switch to Astrix Light Studio' : 'Switch to Tactical Slate Dark'}
          className="size-10 flex items-center justify-center rounded-xl border border-border bg-secondary/60 text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
        >
          {theme === 'dark' ? <Sun className="size-4 text-amber-400" /> : <Moon className="size-4 text-slate-600" />}
        </button>

        {/* Tactical Audio Toggle */}
        <button
          type="button"
          onClick={onToggleAudio}
          title={audioEnabled ? 'Audio Feedback Enabled (Click to Mute)' : 'Audio Muted'}
          className={`size-10 flex items-center justify-center rounded-xl border transition-colors ${
            audioEnabled
              ? 'border-primary/40 bg-primary/10 text-primary'
              : 'border-border bg-secondary/60 text-muted-foreground hover:text-foreground'
          }`}
        >
          {audioEnabled ? <Volume2 className="size-4" /> : <VolumeX className="size-4" />}
        </button>

        {/* Notifications Popover */}
        <div className="relative">
          <button
            type="button"
            onClick={() => setIsNotificationsOpen((prev) => !prev)}
            className="size-10 flex items-center justify-center rounded-xl border border-border bg-secondary/60 text-muted-foreground hover:text-foreground hover:bg-secondary relative transition-colors"
            aria-label="Notifications"
          >
            <BellIcon className="size-4" />
            <span className="absolute top-2 right-2 size-2 rounded-full bg-primary" />
          </button>

          {isNotificationsOpen && (
            <div className="absolute right-0 mt-2 w-80 md:w-96 rounded-2xl border border-border bg-card p-3 shadow-2xl z-50 animate-in fade-in zoom-in-95">
              <div className="flex items-center justify-between pb-2 border-b border-border">
                <span className="text-xs font-bold text-foreground">ITMS Preemption Alerts</span>
                <span className="text-[10px] text-muted-foreground">3 Unread Events</span>
              </div>
              <div className="divide-y divide-border/60 max-h-72 overflow-y-auto mt-2">
                {notifications.map((n) => (
                  <div key={n.id} className="py-2.5 px-2 hover:bg-secondary/50 rounded-xl transition-colors">
                    <div className="flex items-start gap-2.5">
                      <div className="mt-0.5">
                        {n.type === 'preemption' && <Radio className="size-4 text-primary" />}
                        {n.type === 'exemption' && <CheckCircle className="size-4 text-emerald-400" />}
                        {n.type === 'failover' && <AlertTriangle className="size-4 text-amber-400" />}
                        {n.type === 'audit' && <Info className="size-4 text-cyan-400" />}
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className="text-xs font-semibold text-foreground">
                          {n.title}
                        </p>
                        <p className="text-[11px] text-muted-foreground leading-relaxed mt-0.5">
                          {n.description}
                        </p>
                        <span className="text-[10px] text-muted-foreground/60 mt-1 block">
                          {n.time}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* CAD Emergency Dispatch Button */}
        <button
          type="button"
          onClick={onOpenDispatch}
          className="flex items-center gap-1.5 md:gap-2 h-10 px-3 md:px-3.5 rounded-xl bg-secondary hover:bg-secondary/80 border border-border text-xs font-semibold text-foreground transition-all shadow-sm"
        >
          <Siren className="size-4 text-amber-400 shrink-0" />
          <span className="hidden sm:inline">CAD Dispatch</span>
        </button>

        {/* Instant Preemption Override Trigger */}
        <button
          type="button"
          onClick={onPreemptToggle}
          className={`flex items-center gap-1.5 md:gap-2 h-10 px-3 md:px-4 rounded-xl font-bold text-xs transition-all shadow-md ${
            isPreempting
              ? 'bg-rose-600 text-white hover:bg-rose-700 animate-pulse'
              : 'bg-primary text-primary-foreground hover:opacity-90 glow-primary'
          }`}
        >
          <Zap className="size-4 shrink-0" />
          <span className="whitespace-nowrap">{isPreempting ? 'ABORT' : 'TRANSMIT OVERRIDE'}</span>
        </button>
      </div>
    </header>
  )
}
