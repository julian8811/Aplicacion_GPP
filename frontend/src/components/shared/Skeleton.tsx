interface SkeletonProps {
  isLoading?: boolean
  className?: string
  children?: React.ReactNode
}

export function Skeleton({ isLoading, className = '', children }: SkeletonProps) {
  if (!isLoading) {
    return <>{children}</>
  }

  return (
    <div className={`animate-pulse bg-secondary rounded ${className}`}>
      <div className="invisible">{children}</div>
    </div>
  )
}