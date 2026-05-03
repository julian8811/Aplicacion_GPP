import { ReactNode } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'

interface ProtectedRouteProps {
  children: ReactNode
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { user, isLoading, isGuest } = useAuth()
  const location = useLocation()

  // Check for guest mode from URL
  const urlParams = new URLSearchParams(location.search)
  const isGuestMode = urlParams.get('mode') === 'guest'

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900" />
      </div>
    )
  }

  // Allow guest mode bypass
  if (isGuestMode || isGuest) {
    return <>{children}</>
  }

  // Require authentication
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  return <>{children}</>
}