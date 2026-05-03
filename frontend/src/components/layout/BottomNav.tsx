import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import { 
  LayoutDashboard, 
  ClipboardList, 
  BarChart3, 
  CheckSquare,
  Settings
} from 'lucide-react'

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Home' },
  { to: '/evaluate', icon: ClipboardList, label: 'Evaluar' },
  { to: '/results', icon: BarChart3, label: 'Resultados' },
  { to: '/action-plans', icon: CheckSquare, label: 'Acciones' },
  { to: '/settings', icon: Settings, label: 'Ajustes' },
]

export function BottomNav() {
  const location = useLocation()
  
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-border safe-area-inset-bottom">
      <div className="flex items-center justify-around h-16">
        {navItems.map((item) => {
          const isActive = location.pathname === item.to
          return (
            <Link
              key={item.to}
              to={item.to}
              className={cn(
                "flex flex-col items-center justify-center gap-1 flex-1 h-full",
                isActive ? "text-primary" : "text-muted-foreground"
              )}
            >
              <item.icon size={20} />
              <span className="text-xs font-medium">{item.label}</span>
            </Link>
          )
        })}
      </div>
    </nav>
  )
}