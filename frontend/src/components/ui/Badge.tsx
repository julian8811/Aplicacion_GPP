import * as React from "react"
import { cn } from "@/lib/utils"

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'secondary' | 'info'
}

const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    return (
      <span
        ref={ref}
        className={cn(
          "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold uppercase tracking-wide",
          {
            'default': 'bg-primary/10 text-primary border border-primary/20',
            'success': 'bg-green-100 text-green-800 border border-green-200',
            'warning': 'bg-yellow-100 text-yellow-800 border border-yellow-200',
            'error': 'bg-red-100 text-red-800 border border-red-200',
            'secondary': 'bg-slate-100 text-slate-800 border border-slate-200',
            'info': 'bg-blue-100 text-blue-800 border border-blue-200',
          }[variant],
          className
        )}
        {...props}
      />
    )
  }
)
Badge.displayName = "Badge"

export { Badge }