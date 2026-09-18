'use client'

import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react'

export type DashboardRoutePath =
  | '/'
  | '/preemption'
  | '/corridor'
  | '/agents'
  | '/cctv'
  | '/whitelist'
  | '/reports'
  | '/settings'

type NavigationContextType = {
  pathname: DashboardRoutePath
  setPathname: (path: DashboardRoutePath) => void
  isSidebarCollapsed: boolean
  toggleSidebar: () => void
  theme: 'dark' | 'light'
  toggleTheme: () => void
}

const NavigationContext = createContext<NavigationContextType | undefined>(undefined)

export function DashboardNavigationProvider({ children }: { children: ReactNode }) {
  const [pathname, setPathname] = useState<DashboardRoutePath>('/')
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState<boolean>(false)
  const [theme, setTheme] = useState<'dark' | 'light'>('dark')

  useEffect(() => {
    const saved = (typeof window !== 'undefined' ? localStorage.getItem('astrix-theme') : null) as 'dark' | 'light' | null
    const initial = saved === 'light' ? 'light' : 'dark'
    setTheme(initial)
    if (typeof document !== 'undefined') {
      document.documentElement.classList.toggle('dark', initial === 'dark')
    }
  }, [])

  const toggleSidebar = () => setIsSidebarCollapsed((prev) => !prev)
  const toggleTheme = () => {
    setTheme((prev) => {
      const next = prev === 'dark' ? 'light' : 'dark'
      if (typeof window !== 'undefined') {
        localStorage.setItem('astrix-theme', next)
      }
      if (typeof document !== 'undefined') {
        document.documentElement.classList.toggle('dark', next === 'dark')
      }
      return next
    })
  }

  return (
    <NavigationContext.Provider
      value={{
        pathname,
        setPathname,
        isSidebarCollapsed,
        toggleSidebar,
        theme,
        toggleTheme,
      }}
    >
      <div className={`astrix-dashboard ${theme} min-h-screen bg-background text-foreground`}>{children}</div>
    </NavigationContext.Provider>
  )
}

export function useDashboardNavigation() {
  const context = useContext(NavigationContext)
  if (!context) {
    throw new Error('useDashboardNavigation must be used within DashboardNavigationProvider')
  }
  return context
}

type DashboardLinkProps = {
  href: DashboardRoutePath
  className?: string
  children: ReactNode
  onClick?: () => void
  'aria-current'?: 'page' | undefined
}

export function DashboardLink({
  href,
  className,
  children,
  onClick,
  'aria-current': ariaCurrent,
}: DashboardLinkProps) {
  const { setPathname } = useDashboardNavigation()

  return (
    <a
      href={`#${href}`}
      aria-current={ariaCurrent}
      className={className}
      onClick={(e) => {
        e.preventDefault()
        setPathname(href)
        if (onClick) onClick()
      }}
    >
      {children}
    </a>
  )
}
