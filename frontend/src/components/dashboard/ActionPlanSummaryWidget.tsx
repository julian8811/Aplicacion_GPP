import { Link } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { useActionPlanStats } from '@/hooks/useActionPlanStats'
import { Skeleton } from '@/components/shared/Skeleton'
import { AlertCircle, Clock, CheckSquare } from 'lucide-react'

export function ActionPlanSummaryWidget() {
  const { data: stats, isLoading } = useActionPlanStats()

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CheckSquare className="w-5 h-5" />
            Planes de Accion
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4">
            <Skeleton className="h-20" />
            <Skeleton className="h-20" />
            <Skeleton className="h-20" />
          </div>
        </CardContent>
      </Card>
    )
  }

  const { pending = 0, overdue = 0, due_this_week = 0 } = stats || {}

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <CheckSquare className="w-5 h-5" />
          Planes de Accion
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-3 gap-4">
          {/* Overdue - Red */}
          <Link to="/action-plans?filter=overdue">
            <div className="flex flex-col items-center p-4 rounded-lg bg-error/10 hover:bg-error/20 transition-colors cursor-pointer">
              <AlertCircle className="w-6 h-6 text-error mb-2" />
              <span className="text-2xl font-bold text-error">{overdue}</span>
              <span className="text-xs text-muted-foreground mt-1">Vencidos</span>
            </div>
          </Link>

          {/* Due this week - Yellow */}
          <Link to="/action-plans?filter=due_this_week">
            <div className="flex flex-col items-center p-4 rounded-lg bg-warning/10 hover:bg-warning/20 transition-colors cursor-pointer">
              <Clock className="w-6 h-6 text-warning mb-2" />
              <span className="text-2xl font-bold text-warning">{due_this_week}</span>
              <span className="text-xs text-muted-foreground mt-1">Esta semana</span>
            </div>
          </Link>

          {/* Pending - Default */}
          <Link to="/action-plans?filter=pendiente">
            <div className="flex flex-col items-center p-4 rounded-lg bg-secondary hover:bg-secondary/80 transition-colors cursor-pointer">
              <CheckSquare className="w-6 h-6 text-muted-foreground mb-2" />
              <span className="text-2xl font-bold">{pending}</span>
              <span className="text-xs text-muted-foreground mt-1">Pendientes</span>
            </div>
          </Link>
        </div>
      </CardContent>
    </Card>
  )
}