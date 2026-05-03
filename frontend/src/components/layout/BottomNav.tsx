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

interface BottomNavProps {
  overdueCount?: number
}

export function BottomNav({ overdueCount = 0 }: BottomNavProps) {
  const location = useLocation()
  
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-border safe-area-inset-bottom">
      <div className="flex items-center justify-around h-16">
        {navItems.map((item) => {
          const isActive = location.pathname === item.to
          const showBadge = item.to === '/action-plans' && overdueCount > 0
          
          return (
            <Link
              key={item.to}
              to={item.to}
              className={cn(
                "flex flex-col items-center justify-center gap-1 flex-1 h-full relative",
                isActive ? "text-primary" : "text-muted-foreground"
              )}
            >
              <item.icon size={20} />
              <span className="text-xs font-medium">{item.label}</span>
              {showBadge && (
                <span className="absolute top-1 right-1/2 translate-x-4 bg-error text-white text-xs font-bold rounded-full w-4 h-4 flex items-center justify-center">
                  {overdueCount > 9 ? '9+' : overdueCount}
                </span>
              )}
            </Link>
          )
        })}
      </div>
    </nav>
  )
}