'use client'

import React, { type ReactNode } from 'react'
import { DashboardSidebar } from './sidebar'
import { DashboardTopbar } from './topbar'
import { useDashboardNavigation } from './navigation'

type DashboardLayoutProps = {
  children: ReactNode
  onOpenDispatch: () => void
  onPreemptToggle: () => void
  isPreempting: boolean
  audioEnabled: boolean
  onToggleAudio: () => void
}

export function AstrixDashboardLayout({
  children,
  onOpenDispatch,
  onPreemptToggle,
  isPreempting,
  audioEnabled,
  onToggleAudio,
}: DashboardLayoutProps) {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-background text-foreground font-sans">
      {/* Astrix Collapsible Sidebar */}
      <DashboardSidebar />

      {/* Main Content Area */}
      <div className="flex flex-1 flex-col overflow-hidden min-w-0">
        {/* Sticky Astrix Topbar */}
        <DashboardTopbar
          onOpenDispatch={onOpenDispatch}
          onPreemptToggle={onPreemptToggle}
          isPreempting={isPreempting}
          audioEnabled={audioEnabled}
          onToggleAudio={onToggleAudio}
        />

        {/* Scrollable Workspace Body */}
        <main className="flex-1 overflow-y-auto px-4 md:px-8 py-6 custom-scrollbar-x">
          <div className="max-w-7xl mx-auto">{children}</div>
        </main>
      </div>
    </div>
  )
}
