import { cn } from '@/lib/utils'

interface ResponsiveGridProps {
  children: React.ReactNode
  className?: string
}

export function ResponsiveGrid({ children, className }: ResponsiveGridProps) {
  return (
    <div className={cn('grid gap-4', 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3', className)}>
      {children}
    </div>
  )
}