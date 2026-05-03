import { useUIStore } from '@/stores/uiStore'
import { Sidebar } from './Sidebar'
import { BottomNav } from './BottomNav'
import { Outlet } from 'react-router-dom'
import { useMediaQuery } from '@/hooks/useMediaQuery'

export function AppShell() {
  const { sidebarCollapsed } = useUIStore()
  const isMobile = useMediaQuery('(max-width: 768px)')
  
  return (
    <div className="min-h-screen bg-background">
      {!isMobile && <Sidebar collapsed={sidebarCollapsed} />}
      <main 
        className={`transition-all duration-300 ${
          !isMobile ? (sidebarCollapsed ? 'ml-16' : 'ml-64') : 'pb-20'
        }`}
      >
        <div className="p-6">
          <Outlet />
        </div>
      </main>
      {isMobile && <BottomNav />}
    </div>
  )
}