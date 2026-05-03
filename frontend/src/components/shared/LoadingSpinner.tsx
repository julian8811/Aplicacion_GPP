import { cn } from '@/lib/utils'

export function LoadingSpinner({ className }: { className?: string }) {
  return (
    <div className={cn("animate-spin w-6 h-6 border-2 border-primary border-t-transparent rounded-full", className)} />
  )
}