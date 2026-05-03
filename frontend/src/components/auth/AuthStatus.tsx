import { useAuth } from '@/hooks/useAuth'
import { LogOut, User } from 'lucide-react'

export function AuthStatus() {
  const { user, logout, isGuest } = useAuth()

  if (isGuest) {
    return (
      <div className="flex items-center gap-2 text-sm text-gray-500">
        <User className="h-4 w-4" />
        <span>Modo invitado</span>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="flex items-center gap-3">
      <div className="text-right">
        <p className="text-sm font-medium text-gray-900">{user.email}</p>
      </div>
      <button
        onClick={() => logout()}
        className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
        title="Cerrar sesión"
      >
        <LogOut className="h-5 w-5" />
      </button>
    </div>
  )
}