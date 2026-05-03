import { Link } from 'react-router-dom'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { useAuth } from '@/hooks/useAuth'
import api from '@/lib/api'
import { useQuery } from '@tanstack/react-query'
import { BarChart3, ClipboardList, TrendingUp, Calendar, Activity, PlusCircle, Eye, BarChart2 } from 'lucide-react'
import { formatDate, getScoreColor } from '@/lib/utils'
import { Skeleton } from '@/components/shared/Skeleton'
import { ActionPlanSummaryWidget } from '@/components/dashboard/ActionPlanSummaryWidget'

export function DashboardPage() {
  const { user, isGuest } = useAuth()

  const { data: evaluations, isLoading } = useQuery({
    queryKey: ['evaluations'],
    queryFn: async () => {
      const response = await api.get('/evaluations')
      return response.data
    },
  })

  const latestEval = evaluations?.[0]

  // Health index gauge color
  const getGaugeColor = (pct: number) => {
    if (pct >= 75) return '#059669' // green
    if (pct >= 60) return '#d97706' // yellow
    return '#be123c' // red
  }

  const displayName = isGuest
    ? 'Invitado'
    : user?.email?.split('@')[0] || 'Usuario'

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">
            Hola, {displayName}
          </h1>
          {isGuest && (
            <p className="text-muted-foreground text-sm">
              Modo invitado - los cambios no se guardaran
            </p>
          )}
        </div>
        <div className="flex gap-2 items-center">
          {evaluations && evaluations.length >= 2 && (
            <Link to="/benchmarking">
              <Badge variant="success" className="flex items-center gap-1 px-3 py-1.5">
                <BarChart2 className="w-3.5 h-3.5" />
                Benchmarking disponible
              </Badge>
            </Link>
          )}
          <Link to="/evaluate">
            <Button>
              <PlusCircle className="w-4 h-4 mr-2" />
              Nueva Evaluacion
            </Button>
          </Link>
        </div>
      </div>

      {/* Health Index Gauge + KPIs */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Health Index Gauge */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5" />
              Indice de Salud
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex justify-center py-8">
                <Skeleton className="w-40 h-40 rounded-full" />
              </div>
            ) : latestEval ? (
              <div className="flex flex-col items-center">
                {/* Radial Gauge Visualization */}
                <div className="relative w-40 h-40">
                  <svg viewBox="0 0 100 100" className="w-full h-full">
                    {/* Background arc */}
                    <path
                      d="M 15 80 A 35 35 0 1 1 85 80"
                      fill="none"
                      stroke="#e2e8f0"
                      strokeWidth="10"
                      strokeLinecap="round"
                    />
                    {/* Progress arc */}
                    <path
                      d="M 15 80 A 35 35 0 1 1 85 80"
                      fill="none"
                      stroke={getGaugeColor(latestEval.general_pct)}
                      strokeWidth="10"
                      strokeLinecap="round"
                      strokeDasharray={`${(latestEval.general_pct / 100) * 175} 175`}
                      className="transition-all duration-500"
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className={`text-3xl font-bold ${getScoreColor(latestEval.general_pct)}`}>
                      {latestEval.general_pct.toFixed(0)}%
                    </span>
                    <span className="text-xs text-muted-foreground">general</span>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground mt-4">
                  Ultima evaluacion: {formatDate(latestEval.fecha)}
                </p>
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="w-40 h-40 mx-auto rounded-full bg-secondary flex items-center justify-center">
                  <Activity className="w-12 h-12 text-muted-foreground" />
                </div>
                <p className="text-muted-foreground mt-4">Sin datos</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* KPI Cards */}
        <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Evaluaciones Totales
                  </p>
                  <Skeleton isLoading={isLoading} className="h-8 w-16 mt-1">
                    <p className="text-3xl font-bold">{evaluations?.length || 0}</p>
                  </Skeleton>
                </div>
                <div className="w-12 h-12 rounded-full bg-success/10 flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-success" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    PA Promedio
                  </p>
                  <Skeleton isLoading={isLoading} className="h-8 w-16 mt-1">
                    <p className="text-3xl font-bold">
                      {latestEval ? latestEval.pa_pct?.toFixed(0) || '--' : '--'}%
                    </p>
                  </Skeleton>
                </div>
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <BarChart3 className="w-6 h-6 text-primary" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    PO Promedio
                  </p>
                  <Skeleton isLoading={isLoading} className="h-8 w-16 mt-1">
                    <p className="text-3xl font-bold">
                      {latestEval ? latestEval.po_pct?.toFixed(0) || '--' : '--'}%
                    </p>
                  </Skeleton>
                </div>
                <div className="w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center">
                  <ClipboardList className="w-6 h-6 text-accent" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Proxima Evaluacion
                  </p>
                  <Skeleton isLoading={isLoading} className="h-8 w-24 mt-1">
                    <p className="text-lg font-semibold">
                      {latestEval ? formatDate(latestEval.fecha) : 'Ninguna'}
                    </p>
                  </Skeleton>
                </div>
                <div className="w-12 h-12 rounded-full bg-warning/10 flex items-center justify-center">
                  <Calendar className="w-6 h-6 text-warning" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Action Plan Summary Widget - only show if logged in (not guest) */}
      {!isGuest && <ActionPlanSummaryWidget />}

      {/* Quick Actions */}
      <div className="flex gap-4 flex-wrap">
        <Link to="/evaluate">
          <Button size="lg">
            <PlusCircle className="w-5 h-5 mr-2" />
            Nueva Evaluacion
          </Button>
        </Link>
        {latestEval && (
          <Link to={`/results?id=${latestEval.id}`}>
            <Button variant="outline" size="lg">
              <Eye className="w-5 h-5 mr-2" />
              Ver Resultados
            </Button>
          </Link>
        )}
      </div>

      {/* Recent evaluations */}
      <Card>
        <CardHeader>
          <CardTitle>Evaluaciones Recientes</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-4">
              <Skeleton className="h-20 w-full" />
              <Skeleton className="h-20 w-full" />
              <Skeleton className="h-20 w-full" />
            </div>
          ) : evaluations?.length > 0 ? (
            <div className="space-y-4">
              {evaluations.slice(0, 5).map((eval_: any) => (
                <div
                  key={eval_.id}
                  className="flex items-center justify-between p-4 bg-secondary rounded-lg hover:bg-secondary/80 transition-colors"
                >
                  <div className="flex-1">
                    <p className="font-medium">{formatDate(eval_.fecha)}</p>
                    <div className="flex gap-4 mt-1 text-sm text-muted-foreground">
                      <span>PA: <span className={getScoreColor(eval_.pa_pct)}>{eval_.pa_pct?.toFixed(0)}%</span></span>
                      <span>PO: <span className={getScoreColor(eval_.po_pct)}>{eval_.po_pct?.toFixed(0)}%</span></span>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <Badge variant={
                      eval_.general_pct >= 75 ? 'success' :
                      eval_.general_pct >= 60 ? 'warning' : 'error'
                    }>
                      {eval_.general_pct.toFixed(0)}%
                    </Badge>
                    <Link to={`/results?id=${eval_.id}`}>
                      <Button variant="ghost" size="icon">
                        <Eye className="w-4 h-4" />
                      </Button>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="w-16 h-16 mx-auto rounded-full bg-secondary flex items-center justify-center mb-4">
                <ClipboardList className="w-8 h-8 text-muted-foreground" />
              </div>
              <p className="text-muted-foreground mb-4">
                No tienes evaluaciones aun
              </p>
              <Link to="/evaluate">
                <Button>Crear tu primera evaluacion</Button>
              </Link>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}