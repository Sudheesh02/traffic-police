import type { SVGProps } from 'react'

export type IconProps = SVGProps<SVGSVGElement>

export function MetricCubeIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 14 14"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M6.66667 0C6.34901 0 6.03528 0.0701311 5.74786 0.205387L1.53121 2.18969C0.596563 2.62953 0 3.56958 0 4.60254V9.33333C0 9.99851 0.384153 10.6038 0.986014 10.8871L5.74786 13.1279C6.03528 13.2632 6.34901 13.3333 6.66667 13.3333C6.98432 13.3333 7.29805 13.2632 7.58547 13.1279L12.3473 10.8871C12.9492 10.6038 13.3333 9.99851 13.3333 9.33333V4.60254C13.3333 3.56958 12.7368 2.62953 11.8021 2.18969L7.58547 0.205387C7.29805 0.0701314 6.98432 0 6.66667 0ZM12 8.25464L7.33333 5.92131V1.56033L11.2344 3.39612C11.7017 3.61604 12 4.08606 12 4.60254V8.25464ZM6.66667 7.07869L11.8229 9.65678C11.8091 9.66559 11.7946 9.67357 11.7796 9.68065L7.01774 11.9215C6.90792 11.9732 6.78804 12 6.66667 12C6.54529 12 6.42541 11.9732 6.31559 11.9215L1.55374 9.68065C1.53869 9.67357 1.52425 9.66559 1.51047 9.65678L6.66667 7.07869ZM6 5.92131L1.33333 8.25464V4.60254C1.33333 4.08606 1.63161 3.61604 2.09894 3.39612L6 1.56033V5.92131Z"
        fill="currentColor"
      />
    </svg>
  )
}

export function TrendingUpIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 12 12"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        d="M8.5 3C8.37 3 8.24 3.05 8.15 3.15C8.05 3.24 8 3.37 8 3.5C8 3.63 8.05 3.76 8.15 3.85C8.24 3.95 8.37 4 8.5 4H9.29L7 6.29L5.1 4.4C5.01 4.3 4.88 4.25 4.75 4.25C4.62 4.25 4.49 4.3 4.4 4.4L1.15 7.65C1.05 7.74 1 7.87 1 8C1 8.13 1.05 8.26 1.15 8.35C1.24 8.45 1.37 8.5 1.5 8.5C1.63 8.5 1.76 8.45 1.85 8.35L4.75 5.46L6.65 7.35C6.74 7.45 6.87 7.5 7 7.5C7.13 7.5 7.26 7.45 7.35 7.35L10 4.71V5.5C10 5.63 10.05 5.76 10.15 5.85C10.24 5.95 10.37 6 10.5 6C10.63 6 10.76 5.95 10.85 5.85C10.95 5.76 11 5.63 11 5.5V3.5C11 3.37 10.95 3.24 10.85 3.15C10.76 3.05 10.63 3 10.5 3H8.5Z"
        fill="currentColor"
      />
    </svg>
  )
}

export function CheckCircleIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        d="M8 1.5C4.41 1.5 1.5 4.41 1.5 8C1.5 11.59 4.41 14.5 8 14.5C11.59 14.5 14.5 11.59 14.5 8C14.5 4.41 11.59 1.5 8 1.5ZM10.85 6.85L7.35 10.35C7.16 10.55 6.84 10.55 6.65 10.35L5.15 8.85C4.95 8.66 4.95 8.34 5.15 8.15C5.34 7.95 5.66 7.95 5.85 8.15L7 9.29L10.15 6.15C10.34 5.95 10.66 5.95 10.85 6.15C11.05 6.34 11.05 6.66 10.85 6.85Z"
        fill="currentColor"
      />
    </svg>
  )
}

export function WarningCircleIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        d="M8 1.33C4.32 1.33 1.33 4.32 1.33 8C1.33 11.68 4.32 14.67 8 14.67C11.68 14.67 14.67 11.68 14.67 8C14.67 4.32 11.68 1.33 8 1.33ZM8 10C7.45 10 7 9.55 7 9C7 8.45 7.45 8 8 8C8.55 8 9 8.45 9 9C9 9.55 8.55 10 8 10ZM8.67 6.67H7.33V4H8.67V6.67Z"
        fill="currentColor"
      />
    </svg>
  )
}

export function CalendarIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        d="M6 2v2H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-2V2h-2v2H8V2H6zm10 6H4V6h12v2zm0 2v6H4v-6h12z"
        fill="currentColor"
      />
    </svg>
  )
}

export function ExportIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        d="M10 2L5 7h3v6h4V7h3l-5-5zm-7 14v2h14v-2H3z"
        fill="currentColor"
      />
    </svg>
  )
}

export function ChevronDownIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        d="M5.5 7.5L10 12l4.5-4.5"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function ChevronRightIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        d="M7.5 4.5L13 10l-5.5 5.5"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function CmdIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 12 12"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        d="M3 2a2 2 0 0 0-2 2v0a2 2 0 0 0 2 2h1V4a2 2 0 0 0-1-1.73V2zm0 8a2 2 0 0 1-2-2v0a2 2 0 0 1 2-2h1v2a2 2 0 0 1-1 2zm6-8a2 2 0 0 1 2 2v0a2 2 0 0 1-2 2H8V4a2 2 0 0 1 1-1.73V2zm0 8a2 2 0 0 0 2-2v0a2 2 0 0 0-2-2H8v2a2 2 0 0 0 1 2zM5 4h2v4H5V4z"
        stroke="currentColor"
        strokeWidth="1.2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function SearchIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        d="M9 3.5a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11zM1 9a8 8 0 1 1 14.32 4.906l3.387 3.387a1 1 0 0 1-1.414 1.414l-3.387-3.387A8 8 0 0 1 1 9z"
        fill="currentColor"
      />
    </svg>
  )
}

export function BellIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        d="M10 2a6 6 0 0 0-6 6v3.586l-.707.707A1 1 0 0 0 4 14h12a1 1 0 0 0 .707-1.707L16 11.586V8a6 6 0 0 0-6-6zm-2 13a2 2 0 1 0 4 0H8z"
        fill="currentColor"
      />
    </svg>
  )
}

export function SidebarToggleIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <rect x="3" y="4" width="18" height="16" rx="3" stroke="currentColor" strokeWidth="2" />
      <path d="M9 4v16" stroke="currentColor" strokeWidth="2" />
      <path d="M14 10l-2 2 2 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

export function FullscreenIcon({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 20 20"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        d="M3 7V4a1 1 0 0 1 1-1h3M17 7V4a1 1 0 0 0-1-1h-3M3 13v3a1 1 0 0 0 1 1h3M17 13v3a1 1 0 0 1-1 1h-3"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function PoliceEmblemLogo({ className, ...props }: IconProps) {
  return (
    <svg
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <rect width="32" height="32" rx="8" fill="#0F2B5C" />
      <path
        d="M16 6L7 10v6c0 6.5 3.8 12.3 9 14 5.2-1.7 9-7.5 9-14v-6L16 6z"
        fill="#2563EB"
        fillOpacity="0.3"
        stroke="#E5A93C"
        strokeWidth="1.5"
      />
      <path d="M16 11v10M11 16h10" stroke="#E5A93C" strokeWidth="2" strokeLinecap="round" />
      <circle cx="16" cy="16" r="2.5" fill="#06B6D4" />
    </svg>
  )
}
