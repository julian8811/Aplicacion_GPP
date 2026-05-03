import { Link, useLocation } from 'react-router-dom'
import { useUIStore } from '@/stores/uiStore'
import { cn } from '@/lib/utils'
import { 
  LayoutDashboard, 
  ClipboardList, 
  BarChart3, 
  CheckSquare, 
  History, 
  Settings,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/evaluate', icon: ClipboardList, label: 'Nueva Evaluacion' },
  { to: '/results', icon: BarChart3, label: 'Resultados' },
  { to: '/action-plans', icon: CheckSquare, label: 'Plan de Accion' },
  { to: '/history', icon: History, label: 'Historial' },
  { to: '/settings', icon: Settings, label: 'Configuracion' },
]

interface SidebarProps {
  collapsed: boolean
  overdueCount?: number
}

export function Sidebar({ collapsed, overdueCount = 0 }: SidebarProps) {
  const location = useLocation()
  const { toggleSidebar } = useUIStore()
  
  return (
    <aside className={cn(
      "fixed left-0 top-0 z-40 h-screen bg-slate-900 text-white transition-all duration-300",
      collapsed ? "w-16" : "w-64"
    )}>
      <div className="flex h-16 items-center justify-between px-4 border-b border-slate-800">
        {!collapsed && (
          <span className="text-lg font-bold tracking-tight">GPP</span>
        )}
        <button 
          onClick={toggleSidebar}
          className="p-1.5 rounded-md hover:bg-slate-800"
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>
      
      <nav className="p-2 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.to
          const showBadge = item.to === '/action-plans' && overdueCount > 0
          
          return (
            <Link
              key={item.to}
              to={item.to}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors relative",
                isActive 
                  ? "bg-primary text-white" 
                  : "text-slate-400 hover:bg-slate-800 hover:text-white"
              )}
            >
              <item.icon size={20} />
              {!collapsed && <span className="text-sm font-medium">{item.label}</span>}
              {showBadge && (
                <span className="absolute -top-1 -right-1 bg-error text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                  {overdueCount > 9 ? '9+' : overdueCount}
                </span>
              )}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}