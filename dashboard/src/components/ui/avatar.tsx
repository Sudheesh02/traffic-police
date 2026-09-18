import * as React from "react"
import { cn } from "@/lib/utils"

export function Avatar({ className, children, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      data-slot="avatar"
      className={cn("relative flex size-9 shrink-0 overflow-hidden rounded-full border border-border/80 bg-secondary", className)}
      {...props}
    >
      {children}
    </div>
  )
}

export function AvatarImage({ src, alt = "", className, ...props }: React.ImgHTMLAttributes<HTMLImageElement>) {
  const [error, setError] = React.useState(false)
  if (error || !src) return null
  return (
    <img
      src={src}
      alt={alt}
      onError={() => setError(true)}
      className={cn("aspect-square size-full object-cover", className)}
      {...props}
    />
  )
}

export function AvatarFallback({ children, className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("flex size-full items-center justify-center rounded-full bg-secondary text-xs font-semibold text-foreground", className)}
      {...props}
    >
      {children}
    </div>
  )
}
