import { useUIStore } from '@/stores/uiStore'
import { Sidebar } from './Sidebar'
import { BottomNav } from './BottomNav'
import { Outlet } from 'react-router-dom'
import { useMediaQuery } from '@/hooks/useMediaQuery'
import { AuthStatus } from '@/components/auth/AuthStatus'
import { useAuth } from '@/hooks/useAuth'
import { useActionPlanStats } from '@/hooks/useActionPlanStats'
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'

interface SidebarAdminLink {
  to: string
  icon: any
  label: string
}

export function AppShell() {
  const { sidebarCollapsed } = useUIStore()
  const isMobile = useMediaQuery('(max-width: 768px)')
  const { isGuest, user } = useAuth()
  const { data: stats } = useActionPlanStats()

  const overdueCount = stats?.overdue || 0

  // Fetch user profile to check admin role
  const { data: profile } = useQuery({
    queryKey: ['profile'],
    queryFn: async () => {
      const response = await api.get('/profiles/me')
      return response.data
    },
    enabled: !isGuest && !!user,
  })

  const isAdmin = profile?.role === 'admin'
  
  const adminLinks: SidebarAdminLink[] = [
    { to: '/admin/export', label: 'Exportar', icon: 'FileDown' },
  ]

  return (
    <div className="min-h-screen bg-background">
      {/* Header with auth status - only show on mobile or when not using sidebar */}
      <header className="fixed top-0 left-0 right-0 h-16 bg-white border-b flex items-center justify-between px-4 z-40">
        <div className="flex items-center gap-4">
          <h1 className="text-lg font-bold text-gray-900">GPP</h1>
          {isGuest && (
            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
              Modo invitado
            </span>
          )}
        </div>
        <AuthStatus />
      </header>

      {!isMobile && <Sidebar collapsed={sidebarCollapsed} overdueCount={overdueCount} adminLinks={isAdmin ? adminLinks : []} />}
      <main
        className={`transition-all duration-300 ${
          !isMobile ? (sidebarCollapsed ? 'ml-16' : 'ml-64') : 'ml-0 mt-16 pb-20'
        }`}
      >
        <div className="p-6">
          <Outlet />
        </div>
      </main>
      {isMobile && <BottomNav overdueCount={overdueCount} />}
    </div>
  )
}