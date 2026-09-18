'use client'

import React, { useState } from 'react'
import {
  Moon,
  Sun,
  Shield,
  FileCheck,
  Radio,
  LogOut,
  ChevronUp,
} from 'lucide-react'
import { PoliceEmblemLogo, SidebarToggleIcon } from './icons'
import { DashboardLink, useDashboardNavigation } from './navigation'
import { currentUser, workspaceNavigation, type NavigationItem } from './data'

export function DashboardSidebar() {
  const { pathname, isSidebarCollapsed, toggleSidebar, theme, toggleTheme } = useDashboardNavigation()
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false)

  return (
    <aside
      className={`relative flex flex-col border-r border-border bg-sidebar transition-all duration-300 ease-in-out select-none ${
        isSidebarCollapsed ? 'w-20' : 'w-64'
      } shrink-0 h-screen overflow-hidden`}
    >
      {/* Brand Header */}
      <div className="flex h-16 items-center justify-between px-4 border-b border-border">
        {!isSidebarCollapsed && (
          <div className="flex items-center gap-3 overflow-hidden">
            <PoliceEmblemLogo className="size-8 shrink-0" />
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-sm tracking-wider text-foreground truncate">
                  SYNCHROCLEAR
                </span>
                <span className="rounded bg-primary/20 px-1 py-0.2 text-[10px] font-bold text-primary">
                  C2
                </span>
              </div>
              <p className="text-[11px] text-muted-foreground truncate font-medium">
                Raipur Traffic Police
              </p>
            </div>
          </div>
        )}

        {isSidebarCollapsed && (
          <div className="mx-auto">
            <PoliceEmblemLogo className="size-8" />
          </div>
        )}

        <button
          type="button"
          onClick={toggleSidebar}
          aria-label="Toggle Sidebar"
          className="p-1.5 text-muted-foreground hover:text-foreground hover:bg-secondary rounded-lg transition-colors ml-auto"
        >
          <SidebarToggleIcon className={`size-5 transition-transform duration-300 ${isSidebarCollapsed ? 'rotate-180' : ''}`} />
        </button>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1.5 no-scrollbar">
        {!isSidebarCollapsed && (
          <div className="px-3 pb-2 text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">
            Operational Modules
          </div>
        )}
        {workspaceNavigation.map((item: NavigationItem) => {
          const isActive = item.href === '/' ? pathname === '/' : pathname === item.href
          const Icon = item.icon

          return (
            <DashboardLink
              key={item.name}
              href={item.href}
              aria-current={isActive ? 'page' : undefined}
              className={`group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all ${
                isActive
                  ? 'bg-primary/15 text-primary shadow-sm font-semibold'
                  : 'text-muted-foreground hover:text-foreground hover:bg-secondary/60'
              } ${isSidebarCollapsed ? 'justify-center px-0' : ''}`}
            >
              <Icon className={`size-5 shrink-0 ${isActive ? 'text-primary' : 'text-muted-foreground group-hover:text-foreground'}`} />
              {!isSidebarCollapsed && (
                <>
                  <span className="truncate flex-1">{item.name}</span>
                  {item.badge && (
                    <span
                      className={`rounded-md px-1.5 py-0.5 text-xs font-semibold ${
                        isActive
                          ? 'bg-primary/20 text-primary'
                          : 'bg-secondary text-muted-foreground'
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </>
              )}
            </DashboardLink>
          )
        })}
      </nav>

      {/* Corridor Quick Health Indicator */}
      {!isSidebarCollapsed && (
        <div className="mx-3 my-2 p-3 rounded-xl bg-secondary/40 border border-border/80">
          <div className="flex items-center justify-between text-xs mb-1.5">
            <span className="text-muted-foreground font-medium">Corridor RF Link</span>
            <span className="text-emerald-400 font-mono font-bold">868.0 MHz</span>
          </div>
          <div className="w-full bg-secondary rounded-full h-1.5 overflow-hidden">
            <div className="bg-emerald-500 h-1.5 rounded-full w-[94%]" />
          </div>
          <p className="text-[10px] text-muted-foreground mt-1.5">
            42ms ping · -68 dBm (Great Eastern Rd)
          </p>
        </div>
      )}

      {/* Sidebar Footer User Profile */}
      <div className="p-3 border-t border-border relative">
        <button
          type="button"
          onClick={() => setIsUserMenuOpen((prev) => !prev)}
          className={`flex items-center gap-3 w-full p-2 rounded-xl text-left hover:bg-secondary/70 transition-colors ${
            isSidebarCollapsed ? 'justify-center' : ''
          }`}
        >
          <div className="relative flex size-9 shrink-0 items-center justify-center rounded-full bg-primary/15 border border-primary/30 text-primary font-bold text-xs tracking-wider shadow-sm">
            <span>{currentUser.initials}</span>
            <span className="absolute bottom-0 right-0 size-2.5 rounded-full bg-emerald-500 border-2 border-background" />
          </div>

          {!isSidebarCollapsed && (
            <div className="min-w-0 flex-1">
              <p className="text-sm font-semibold text-foreground truncate">
                {currentUser.name}
              </p>
              <p className="text-xs text-muted-foreground truncate">
                {currentUser.unit}
              </p>
            </div>
          )}

          {!isSidebarCollapsed && (
            <ChevronUp
              className={`size-4 text-muted-foreground transition-transform ${
                isUserMenuOpen ? 'rotate-180' : ''
              }`}
            />
          )}
        </button>

        {/* User Popup Dropdown */}
        {isUserMenuOpen && (
          <div
            className={`absolute bottom-16 ${
              isSidebarCollapsed ? 'left-20' : 'left-3 right-3'
            } w-60 rounded-xl border border-border bg-card p-2 shadow-2xl z-50 animate-in fade-in zoom-in-95`}
          >
            <div className="px-2 py-1.5 border-b border-border mb-1">
              <p className="text-xs font-semibold text-foreground">
                {currentUser.name}
              </p>
              <p className="text-[11px] text-muted-foreground truncate">
                {currentUser.email}
              </p>
            </div>

            <button
              type="button"
              onClick={toggleTheme}
              className="flex w-full items-center gap-2 px-2 py-1.5 text-xs text-muted-foreground hover:text-foreground hover:bg-secondary rounded-lg transition-colors"
            >
              {theme === 'dark' ? <Sun className="size-4" /> : <Moon className="size-4" />}
              {theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Tactical Dark'}
            </button>

            <div className="my-1 border-t border-border" />

            <div className="px-2 py-1 text-[10px] text-muted-foreground">
              Raipur Police Hackathon 2026
            </div>
          </div>
        )}
      </div>
    </aside>
  )
}
