import * as React from "react"
import { cn } from "@/lib/utils"

interface DropdownContextType {
  open: boolean
  setOpen: React.Dispatch<React.SetStateAction<boolean>>
}

const DropdownContext = React.createContext<DropdownContextType>({
  open: false,
  setOpen: () => {},
})

export function DropdownMenu({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = React.useState(false)
  const menuRef = React.useRef<HTMLDivElement>(null)

  React.useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    if (open) {
      document.addEventListener("mousedown", handleOutsideClick)
    }
    return () => document.removeEventListener("mousedown", handleOutsideClick)
  }, [open])

  return (
    <DropdownContext.Provider value={{ open, setOpen }}>
      <div ref={menuRef} className="relative inline-block text-left">
        {children}
      </div>
    </DropdownContext.Provider>
  )
}

export function DropdownMenuTrigger({
  children,
  asChild = false,
  className,
}: {
  children: React.ReactNode
  asChild?: boolean
  className?: string
}) {
  const { open, setOpen } = React.useContext(DropdownContext)

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation()
    setOpen((prev) => !prev)
  }

  if (asChild && React.isValidElement(children)) {
    return React.cloneElement(children as React.ReactElement<any>, {
      onClick: handleClick,
      "aria-expanded": open,
      className: cn(children.props.className, className),
    })
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      aria-expanded={open}
      className={cn("inline-flex items-center justify-center", className)}
    >
      {children}
    </button>
  )
}

export function DropdownMenuContent({
  children,
  align = "start",
  className,
}: {
  children: React.ReactNode
  align?: "start" | "end" | "center"
  className?: string
  collisionPadding?: number
}) {
  const { open } = React.useContext(DropdownContext)
  if (!open) return null

  const alignment =
    align === "end"
      ? "right-0"
      : align === "center"
      ? "left-1/2 -translate-x-1/2"
      : "left-0"

  return (
    <div
      data-slot="dropdown-menu-content"
      className={cn(
        "absolute z-50 mt-2 min-w-44 rounded-2xl border border-border/80 bg-card p-1.5 shadow-2xl backdrop-blur-xl animate-in fade-in-0 zoom-in-95",
        alignment,
        className
      )}
    >
      {children}
    </div>
  )
}

export function DropdownMenuItem({
  children,
  onClick,
  className,
}: {
  children: React.ReactNode
  onClick?: () => void
  className?: string
}) {
  const { setOpen } = React.useContext(DropdownContext)
  return (
    <div
      data-slot="dropdown-menu-item"
      onClick={() => {
        onClick?.()
        setOpen(false)
      }}
      className={cn(
        "relative flex cursor-pointer select-none items-center gap-2 rounded-xl px-3 py-2 text-sm text-foreground outline-none transition-colors hover:bg-secondary focus:bg-secondary",
        className
      )}
    >
      {children}
    </div>
  )
}

interface RadioGroupContextType {
  value: string
  onValueChange: (val: string) => void
}

const RadioGroupContext = React.createContext<RadioGroupContextType>({
  value: "",
  onValueChange: () => {},
})

export function DropdownMenuRadioGroup({
  value,
  onValueChange,
  children,
}: {
  value: string
  onValueChange: (val: string) => void
  children: React.ReactNode
}) {
  return (
    <RadioGroupContext.Provider value={{ value, onValueChange }}>
      <div className="space-y-0.5">{children}</div>
    </RadioGroupContext.Provider>
  )
}

export function DropdownMenuRadioItem({
  value,
  children,
  className,
}: {
  value: string
  children: React.ReactNode
  className?: string
}) {
  const { value: selectedVal, onValueChange } = React.useContext(RadioGroupContext)
  const { setOpen } = React.useContext(DropdownContext)
  const isChecked = selectedVal === value

  return (
    <div
      data-slot="dropdown-menu-radio-item"
      data-state={isChecked ? "checked" : "unchecked"}
      onClick={() => {
        onValueChange(value)
        setOpen(false)
      }}
      className={cn(
        "relative flex cursor-pointer select-none items-center rounded-xl px-3 py-2 text-sm text-muted-foreground outline-none transition-colors hover:bg-secondary hover:text-foreground data-[state=checked]:font-semibold data-[state=checked]:text-primary data-[state=checked]:bg-primary/10",
        className
      )}
    >
      <span className="flex-1">{children}</span>
      {isChecked && <span className="size-1.5 rounded-full bg-primary" />}
    </div>
  )
}

export function DropdownMenuGroup({ children }: { children: React.ReactNode }) {
  return <div className="space-y-0.5">{children}</div>
}

export function DropdownMenuLabel({
  children,
  className,
}: {
  children: React.ReactNode
  className?: string
}) {
  return (
    <div className={cn("px-3 py-1.5 text-xs font-bold uppercase tracking-wider text-muted-foreground", className)}>
      {children}
    </div>
  )
}

export function DropdownMenuSeparator({ className }: { className?: string }) {
  return <div className={cn("-mx-1.5 my-1.5 h-px bg-border/70", className)} />
}
