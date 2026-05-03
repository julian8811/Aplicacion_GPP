import * as React from "react"
import { cn } from "@/lib/utils"

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost' | 'destructive'
  size?: 'default' | 'sm' | 'lg' | 'icon'
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'default', ...props }, ref) => {
    return (
      <button
        className={cn(
          "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50",
          {
            'default': 'bg-primary text-white hover:bg-primary/90',
            'outline': 'border border-border bg-white hover:bg-secondary',
            'ghost': 'hover:bg-secondary',
            'destructive': 'bg-error text-white hover:bg-error/90',
          }[variant],
          {
            'default': 'h-10 px-4 py-2',
            'sm': 'h-8 px-3 text-sm',
            'lg': 'h-12 px-6',
            'icon': 'h-10 w-10',
          }[size],
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button }