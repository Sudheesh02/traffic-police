import * as React from "react"
import { cn } from "@/lib/utils"

type SidebarContextProps = {
  open: boolean
  setOpen: (open: boolean) => void
  openMobile: boolean
  setOpenMobile: (open: boolean) => void
  isMobile: boolean
  toggleSidebar: () => void
}

const SidebarContext = React.createContext<SidebarContextProps | null>(null)

export function useSidebar() {
  const context = React.useContext(SidebarContext)
  if (!context) {
    throw new Error("useSidebar must be used within a SidebarProvider.")
  }
  return context
}

export function SidebarProvider({
  defaultOpen = true,
  className,
  style,
  children,
}: {
  defaultOpen?: boolean
  className?: string
  style?: React.CSSProperties
  children: React.ReactNode
}) {
  const [open, setOpen] = React.useState(defaultOpen)
  const [openMobile, setOpenMobile] = React.useState(false)
  const [isMobile, setIsMobile] = React.useState(false)

  React.useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 1024)
    }
    checkMobile()
    window.addEventListener("resize", checkMobile)
    return () => window.removeEventListener("resize", checkMobile)
  }, [])

  const toggleSidebar = React.useCallback(() => {
    if (isMobile) {
      setOpenMobile((prev) => !prev)
    } else {
      setOpen((prev) => !prev)
    }
  }, [isMobile])

  return (
    <SidebarContext.Provider
      value={{
        open,
        setOpen,
        openMobile,
        setOpenMobile,
        isMobile,
        toggleSidebar,
      }}
    >
      <div
        className={cn("flex min-h-screen w-full bg-background text-foreground", className)}
        style={style}
      >
        {children}
      </div>
    </SidebarContext.Provider>
  )
}

export function Sidebar({
  collapsible = "icon",
  className,
  children,
}: {
  collapsible?: "offcanvas" | "icon" | "none"
  className?: string
  children: React.ReactNode
}) {
  const { open, openMobile, setOpenMobile, isMobile } = useSidebar()

  if (isMobile) {
    if (!openMobile) return null
    return (
      <div className="fixed inset-0 z-50 flex">
        <div
          className="fixed inset-0 bg-background/80 backdrop-blur-sm transition-opacity"
          onClick={() => setOpenMobile(false)}
        />
        <aside
          data-slot="sidebar"
          data-mobile="true"
          className={cn(
            "relative flex h-full w-72 flex-col border-r border-border bg-sidebar p-4 shadow-2xl z-10",
            className
          )}
        >
          {children}
        </aside>
      </div>
    )
  }

  return (
    <aside
      data-slot="sidebar"
      data-collapsible={collapsible}
      data-state={open ? "expanded" : "collapsed"}
      className={cn(
        "group sticky top-0 flex h-screen flex-col border-r border-border bg-sidebar transition-[width] duration-200 ease-linear",
        open ? "w-64" : "w-18",
        className
      )}
    >
      {children}
    </aside>
  )
}

export function SidebarHeader({ className, children }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      data-slot="sidebar-header"
      className={cn("flex h-16 items-center px-4 border-b border-border/50", className)}
    >
      {children}
    </div>
  )
}

export function SidebarContent({ className, children }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      data-slot="sidebar-content"
      className={cn("flex-1 overflow-y-auto overflow-x-hidden p-3 space-y-1 no-scrollbar", className)}
    >
      {children}
    </div>
  )
}

export function SidebarFooter({ className, children }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      data-slot="sidebar-footer"
      className={cn("p-3 border-t border-border/50", className)}
    >
      {children}
    </div>
  )
}

export function SidebarMenu({ className, children }: React.HTMLAttributes<HTMLUListElement>) {
  return <ul data-slot="sidebar-menu" className={cn("space-y-1", className)}>{children}</ul>
}

export function SidebarMenuItem({ className, children }: React.HTMLAttributes<HTMLLIElement>) {
  return <li data-slot="sidebar-menu-item" className={cn("list-none", className)}>{children}</li>
}

export function SidebarMenuButton({
  asChild = false,
  isActive = false,
  tooltip,
  className,
  children,
  ...props
}: {
  asChild?: boolean
  isActive?: boolean
  tooltip?: string
  className?: string
  children: React.ReactNode
} & React.ButtonHTMLAttributes<HTMLButtonElement>) {
  const { open } = useSidebar()
  if (asChild && React.isValidElement(children)) {
    return React.cloneElement(children as React.ReactElement<any>, {
      "aria-current": isActive ? "page" : undefined,
      title: !open ? tooltip : undefined,
      className: cn(children.props.className, className),
    })
  }

  return (
    <button
      type="button"
      title={!open ? tooltip : undefined}
      aria-current={isActive ? "page" : undefined}
      className={cn(
        "flex w-full items-center gap-2.5 rounded-xl px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-sidebar-accent hover:text-foreground",
        isActive && "bg-sidebar-accent text-primary font-semibold",
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}

export function SidebarTrigger({ className, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  const { toggleSidebar } = useSidebar()
  return (
    <button
      type="button"
      onClick={toggleSidebar}
      className={cn(
        "inline-flex size-9 items-center justify-center rounded-lg border border-border text-muted-foreground hover:bg-secondary hover:text-foreground",
        className
      )}
      aria-label="Toggle Sidebar"
      {...props}
    >
      <svg className="size-4.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect width="18" height="18" x="3" y="3" rx="2" />
        <path d="M9 3v18" />
      </svg>
    </button>
  )
}
