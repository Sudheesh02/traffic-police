import * as React from "react"
import { cn } from "@/lib/utils"

export const InputGroup = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => (
    <div
      ref={ref}
      data-slot="input-group"
      className={cn(
        "relative flex items-center rounded-xl border border-border/70 bg-secondary/70 transition-colors focus-within:border-primary/60 focus-within:ring-1 focus-within:ring-primary/40",
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
)
InputGroup.displayName = "InputGroup"

export const InputGroupAddon = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, children, ...props }, ref) => (
    <div
      ref={ref}
      data-slot="input-group-addon"
      className={cn("flex items-center px-2.5 text-muted-foreground", className)}
      {...props}
    >
      {children}
    </div>
  )
)
InputGroupAddon.displayName = "InputGroupAddon"

export const InputGroupInput = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      data-slot="input-group-input"
      className={cn(
        "h-full w-full bg-transparent text-sm text-foreground placeholder:text-muted-foreground focus:outline-none disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}
    />
  )
)
InputGroupInput.displayName = "InputGroupInput"
