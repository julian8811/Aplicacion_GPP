import { useMemo } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import { formatDate, getScoreColor, cn } from '@/lib/utils'
import { Skeleton } from '@/components/shared/Skeleton'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Legend,
} from 'recharts'
import { TrendingUp, TrendingDown, Minus, Target } from 'lucide-react'

// Types
interface Evaluation {
  id: string
  user_id: string
  fecha: string
  general_pct: number
  pa_pct: number
  po_pct: number
  establishment_name?: string
}

interface ActionPlan {
  id: string
  evaluation_id: string
  element: string
  action: string
  responsible: string
  due_date: string
  status: 'pendiente' | 'en_progreso' | 'completada'
}

interface Milestone {
  date: string
  label: string
  type: 'improvement' | 'plan_implemented'
  fromValue?: number
  toValue?: number
}

// Calculate if there was significant improvement between evaluations
function calculateMilestones(
  evaluations: Evaluation[],
  actionPlans: ActionPlan[]
): Milestone[] {
  if (!evaluations || evaluations.length < 2) return []

  const milestones: Milestone[] = []
  const completedPlans = actionPlans.filter(ap => ap.status === 'completada')

  // Sort evaluations by date
  const sortedEvals = [...evaluations].sort(
    (a, b) => new Date(a.fecha).getTime() - new Date(b.fecha).getTime()
  )

  // Find points where there was significant improvement (>15%) or plan was implemented
  for (let i = 1; i < sortedEvals.length; i++) {
    const prevEval = sortedEvals[i - 1]
    const currEval = sortedEvals[i]
    const improvement = currEval.general_pct - prevEval.general_pct

    // Check if there's a completed action plan around this time
    const relevantPlans = completedPlans.filter(plan => {
      const planDate = new Date(plan.due_date)
      const evalDate = new Date(currEval.fecha)
      // Plan was completed within 30 days before this evaluation
      return planDate <= evalDate && 
             planDate >= new Date(evalDate.getTime() - 30 * 24 * 60 * 60 * 1000)
    })

    if (relevantPlans.length > 0 && improvement > 10) {
      milestones.push({
        date: currEval.fecha,
        label: `Plan implementado (+${improvement.toFixed(0)}%)`,
        type: 'plan_implemented',
        fromValue: prevEval.general_pct,
        toValue: currEval.general_pct,
      })
    } else if (improvement > 15) {
      milestones.push({
        date: currEval.fecha,
        label: `Mejora +${improvement.toFixed(0)}%`,
        type: 'improvement',
        fromValue: prevEval.general_pct,
        toValue: currEval.general_pct,
      })
    }
  }

  return milestones
}

// Custom tooltip for chart
function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload || !payload.length) return null

  const data = payload[0].payload

  return (
    <div className="bg-background border border-border rounded-lg p-3 shadow-lg">
      <p className="font-semibold text-foreground mb-2">{formatDate(label)}</p>
      <div className="space-y-1">
        <p className="text-sm">
          <span className="text-muted-foreground">General:</span>{' '}
          <span className={getScoreColor(data.general_pct)}>{data.general_pct?.toFixed(1)}%</span>
        </p>
        <p className="text-sm">
          <span className="text-muted-foreground">PA:</span>{' '}
          <span className={getScoreColor(data.pa_pct)}>{data.pa_pct?.toFixed(1)}%</span>
        </p>
        <p className="text-sm">
          <span className="text-muted-foreground">PO:</span>{' '}
          <span className={getScoreColor(data.po_pct)}>{data.po_pct?.toFixed(1)}%</span>
        </p>
      </div>
      {data.milestone && (
        <p className="text-xs font-medium text-primary mt-2 pt-2 border-t">
          ★ {data.milestone}
        </p>
      )}
    </div>
  )
}

// Trend indicator component
function TrendIndicator({ from, to }: { from: number; to: number }) {
  const diff = to - from
  const Icon = diff > 0 ? TrendingUp : diff < 0 ? TrendingDown : Minus
  const colorClass = diff > 0 ? 'text-success' : diff < 0 ? 'text-error' : 'text-muted-foreground'

  return (
    <div className={`flex items-center gap-1 ${colorClass}`}>
      <Icon className="w-4 h-4" />
      <span className="text-sm font-medium">
        {diff > 0 ? '+' : ''}{diff.toFixed(1)}%
      </span>
    </div>
  )
}

export function BenchmarkingPage() {
  // Fetch all evaluations
  const { data: evaluations, isLoading: evalsLoading } = useQuery({
    queryKey: ['evaluations'],
    queryFn: async () => {
      const response = await api.get('/evaluations')
      return (response.data as Evaluation[]) || []
    },
  })

  // Fetch all action plans
  const { data: actionPlans, isLoading: plansLoading } = useQuery({
    queryKey: ['action-plans'],
    queryFn: async () => {
      const response = await api.get('/action-plans')
      return (response.data as ActionPlan[]) || []
    },
  })

  const isLoading = evalsLoading || plansLoading

  // Prepare chart data
  const chartData = useMemo(() => {
    if (!evaluations) return []

    // Sort by date ascending for proper chart display
    const sorted = [...evaluations].sort(
      (a, b) => new Date(a.fecha).getTime() - new Date(b.fecha).getTime()
    )

    // Calculate milestones
    const milestones = calculateMilestones(sorted, actionPlans || [])

    // Build chart data with milestone annotations
    return sorted.map(eval_ => {
      const milestone = milestones.find(m => m.date === eval_.fecha)
      return {
        fecha: eval_.fecha,
        displayDate: formatDate(eval_.fecha),
        general_pct: eval_.general_pct,
        pa_pct: eval_.pa_pct,
        po_pct: eval_.po_pct,
        milestone: milestone?.label,
      }
    })
  }, [evaluations, actionPlans])

  // Calculate overall trend
  const overallTrend = useMemo(() => {
    if (!chartData || chartData.length < 2) return null
    
    const first = chartData[0].general_pct
    const last = chartData[chartData.length - 1].general_pct
    return { from: first, to: last }
  }, [chartData])

  // Get milestones for reference lines
  const milestones = useMemo(() => {
    if (!evaluations || !actionPlans) return []
    return calculateMilestones(evaluations, actionPlans)
  }, [evaluations, actionPlans])

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-12 w-64" />
        <Skeleton className="h-[400px] w-full" />
      </div>
    )
  }

  if (!evaluations || evaluations.length === 0) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-foreground">Análisis de Benchmarking</h1>
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Target className="w-12 h-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground text-center">
              No hay suficientes datos para mostrar el análisis de benchmarking.
              <br />
              Realiza al menos 2 evaluaciones para ver las tendencias.
            </p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Análisis de Benchmarking</h1>
          <p className="text-muted-foreground">
            Tendencia de tus evaluaciones a lo largo del tiempo
          </p>
        </div>
        {overallTrend && (
          <div className="flex items-center gap-4">
            <div className="text-sm text-muted-foreground">
              Evolución general:
            </div>
            <TrendIndicator from={overallTrend.from} to={overallTrend.to} />
          </div>
        )}
      </div>

      {/* Chart Card */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Evolución de Resultados</CardTitle>
            {milestones.length > 0 && (
              <Badge variant="success">
                {milestones.length} hito{milestones.length > 1 ? 's' : ''} marcado{milestones.length > 1 ? 's' : ''}
              </Badge>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {chartData.length >= 2 ? (
            <div className="h-[400px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={chartData}
                  margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis
                    dataKey="fecha"
                    tickFormatter={(value) => formatDate(value)}
                    tick={{ fontSize: 12 }}
                    angle={-45}
                    textAnchor="end"
                    interval="preserveStartEnd"
                  />
                  <YAxis
                    domain={[0, 100]}
                    tickFormatter={(value) => `${value}%`}
                    tick={{ fontSize: 12 }}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend
                    verticalAlign="top"
                    height={36}
                    formatter={(value) => {
                      const labels: Record<string, string> = {
                        general_pct: 'Cumplimiento General',
                        pa_pct: 'PA (Gestión)',
                        po_pct: 'PO (Operaciones)',
                      }
                      return labels[value] || value
                    }}
                  />
                  
                  {/* Milestone reference lines */}
                  {milestones.map((milestone, idx) => (
                    <ReferenceLine
                      key={`milestone-${idx}`}
                      x={milestone.date}
                      stroke="#3b82f6"
                      strokeDasharray="5 5"
                      label={{
                        value: milestone.label,
                        position: 'top',
                        fill: '#3b82f6',
                        fontSize: 10,
                      }}
                    />
                  ))}
                  
                  {/* Lines for each metric */}
                  <Line
                    type="monotone"
                    dataKey="general_pct"
                    stroke="#22c55e"
                    strokeWidth={3}
                    dot={{ r: 6, fill: '#22c55e' }}
                    activeDot={{ r: 8 }}
                    name="general_pct"
                  />
                  <Line
                    type="monotone"
                    dataKey="pa_pct"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    dot={{ r: 5, fill: '#3b82f6' }}
                    activeDot={{ r: 7 }}
                    name="pa_pct"
                  />
                  <Line
                    type="monotone"
                    dataKey="po_pct"
                    stroke="#f97316"
                    strokeWidth={2}
                    dot={{ r: 5, fill: '#f97316' }}
                    activeDot={{ r: 7 }}
                    name="po_pct"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-[300px]">
              <p className="text-muted-foreground">
                Se necesitan al menos 2 evaluaciones para mostrar el gráfico de tendencias.
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Milestones Legend */}
      {milestones.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Hitos Registrados</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {milestones.map((milestone, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-3 p-3 bg-secondary/50 rounded-lg"
                >
                  <div className="w-3 h-3 rounded-full bg-primary" />
                  <div className="flex-1">
                    <p className="font-medium text-foreground">{formatDate(milestone.date)}</p>
                    <p className="text-sm text-muted-foreground">{milestone.label}</p>
                  </div>
                  {milestone.fromValue !== undefined && milestone.toValue !== undefined && (
                    <TrendIndicator from={milestone.fromValue} to={milestone.toValue} />
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Summary Stats */}
      {chartData.length >= 2 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-sm font-medium text-muted-foreground mb-1">Primera Evaluación</p>
                <p className={cn('text-2xl font-bold', getScoreColor(chartData[0].general_pct))}>
                  {chartData[0].general_pct.toFixed(0)}%
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  {formatDate(chartData[0].fecha)}
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-sm font-medium text-muted-foreground mb-1">Última Evaluación</p>
                <p className={cn('text-2xl font-bold', getScoreColor(chartData[chartData.length - 1].general_pct))}>
                  {chartData[chartData.length - 1].general_pct.toFixed(0)}%
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  {formatDate(chartData[chartData.length - 1].fecha)}
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-sm font-medium text-muted-foreground mb-1">Mejor Resultado</p>
                <p className={cn('text-2xl font-bold', getScoreColor(chartData.length > 0 ? Math.max(...chartData.map(d => d.general_pct)) : 0))}>
                  {chartData.length > 0 ? Math.max(...chartData.map(d => d.general_pct)).toFixed(0) : 0}%
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  {chartData.length > 0 ? formatDate(chartData.find(d => d.general_pct === Math.max(...chartData.map(d => d.general_pct)))?.fecha || '') : ''}
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}