import { useParams, Link, useSearchParams } from 'react-router-dom'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import {
  RadialBarChart,
  RadialBar,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Cell,
  Tooltip,
  LabelList,
} from 'recharts'
import { Download, Plus, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react'
import { useState } from 'react'
import { cn, getScoreColor } from '@/lib/utils'

// Types for ResultsPage
interface ResultsData {
  general_pct: number
  pa_pct: number
  po_pct: number
  priority: 'PA' | 'PO' | 'BALANCED'
  pa_breakdown: Record<string, number>
  po_breakdown: Record<string, number>
  questions: Array<{
    aspect: string
    question: string
    context: string
    rating: number
    percentage: number
  }>
}

// Helper to get gauge color based on percentage
function getGaugeColor(pct: number): string {
  if (pct >= 75) return '#22c55e' // green
  if (pct >= 60) return '#eab308' // yellow
  return '#ef4444' // red
}

// Gauge component using RadialBarChart
function HealthGauge({ percentage }: { percentage: number }) {
  const color = getGaugeColor(percentage)

  return (
    <div className="relative flex items-center justify-center">
      <ResponsiveContainer width={200} height={200}>
        <RadialBarChart
          cx="50%"
          cy="50%"
          innerRadius="60%"
          outerRadius="90%"
          barSize={20}
          data={[{ value: percentage, fill: color }]}
          startAngle={180}
          endAngle={0}
        >
          <RadialBar
            background={{ fill: '#e5e7eb' }}
            dataKey="value"
            cornerRadius={10}
          />
        </RadialBarChart>
      </ResponsiveContainer>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-4xl font-bold" style={{ color }}>
          {percentage.toFixed(0)}%
        </span>
        <span className="text-sm text-muted-foreground">Cumplimiento General</span>
      </div>
    </div>
  )
}

// Bar chart for PA or PO aspects
function AspectBarChart({
  data,
  title,
  colors,
}: {
  data: { aspect: string; percentage: number }[]
  title: string
  colors: string[]
}) {
  return (
    <div className="space-y-2">
      <h3 className="text-sm font-medium text-muted-foreground">{title}</h3>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
        >
          <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
          <YAxis type="category" dataKey="aspect" width={90} tick={{ fontSize: 12 }} />
          <Tooltip formatter={(value: number) => [`${value.toFixed(0)}%`, 'Porcentaje']} />
          <Bar dataKey="percentage" radius={[0, 4, 4, 0]}>
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
            ))}
            <LabelList
              dataKey="percentage"
              position="right"
              formatter={(v: number) => `${v.toFixed(0)}%`}
              style={{ fontSize: 12, fill: '#666' }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

// Collapsible detail table
function DetailTable({
  questions,
}: {
  questions: ResultsData['questions']
}) {
  const [expandedAspect, setExpandedAspect] = useState<string | null>(null)

  // Group questions by aspect
  const groupedQuestions = questions.reduce(
    (acc, q) => {
      if (!acc[q.aspect]) acc[q.aspect] = []
      acc[q.aspect].push(q)
      return acc
    },
    {} as Record<string, typeof questions>
  )

  const aspects = Object.keys(groupedQuestions).sort()

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-medium text-muted-foreground mb-3">
        Detalle de Preguntas
      </h3>
      {aspects.map((aspect) => (
        <div key={aspect} className="border rounded-lg overflow-hidden">
          <button
            onClick={() =>
              setExpandedAspect(expandedAspect === aspect ? null : aspect)
            }
            className="w-full flex items-center justify-between p-3 bg-secondary hover:bg-secondary/80 transition-colors"
          >
            <span className="font-medium">{aspect}</span>
            <div className="flex items-center gap-2">
              <Badge
                variant={
                  groupedQuestions[aspect][0].percentage >= 75
                    ? 'success'
                    : groupedQuestions[aspect][0].percentage >= 60
                    ? 'warning'
                    : 'error'
                }
              >
                {groupedQuestions[aspect].length} preguntas
              </Badge>
              {expandedAspect === aspect ? (
                <ChevronUp className="w-4 h-4" />
              ) : (
                <ChevronDown className="w-4 h-4" />
              )}
            </div>
          </button>
          {expandedAspect === aspect && (
            <div className="p-3">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2 text-muted-foreground">Pregunta</th>
                    <th className="text-center py-2 text-muted-foreground w-20">
                      Puntuacion
                    </th>
                    <th className="text-right py-2 text-muted-foreground w-20">
                      Porcentaje
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {groupedQuestions[aspect].map((q, idx) => (
                    <tr key={idx} className="border-b last:border-0">
                      <td className="py-2">
                        <p className="font-medium">{q.question}</p>
                        {q.context && (
                          <p className="text-xs text-muted-foreground mt-0.5">
                            {q.context}
                          </p>
                        )}
                      </td>
                      <td className="text-center py-2">
                        <Badge variant="default">{q.rating}/5</Badge>
                      </td>
                      <td className="text-right py-2">
                        <span className={cn('font-semibold', getScoreColor(q.percentage))}>
                          {q.percentage.toFixed(0)}%
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

// PDF download handler
async function handleDownloadPDF(id: string) {
  const response = await api.get(`/pdf/${id}`, { responseType: 'blob' })
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', `auditoria-${id}.pdf`)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

// Excel export handler
async function handleDownloadExcel(id: string) {
  const response = await api.get(`/export/excel/${id}`, { responseType: 'blob' })
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', `auditoria-${id}.xlsx`)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

export function ResultsPage() {
  const { id: idParam } = useParams<{ id: string }>()
  const [searchParams] = useSearchParams()
  const idFromQuery = searchParams.get('id')
  const id = idParam || idFromQuery

  const { data: evaluation, isLoading } = useQuery({
    queryKey: ['evaluation', id],
    queryFn: async () => {
      const response = await api.get(`/evaluations/${id}`)
      return response.data
    },
    enabled: !!id,
  })

  const { data: actionPlans } = useQuery({
    queryKey: ['action-plans', id],
    queryFn: async () => {
      const response = await api.get(`/action-plans?evaluation_id=${id}`)
      return response.data
    },
    enabled: !!id,
  })

  // Build results data from evaluation (API now provides enriched data)
  const resultsData: ResultsData | null = evaluation
    ? {
        general_pct: evaluation.general_pct,
        pa_pct: evaluation.pa_pct,
        po_pct: evaluation.po_pct,
        priority: evaluation.pa_pct < evaluation.po_pct - 5
          ? 'PA'
          : evaluation.po_pct < evaluation.pa_pct - 5
          ? 'PO'
          : 'BALANCED',
        pa_breakdown: evaluation.pa_breakdown,
        po_breakdown: evaluation.po_breakdown,
        questions: evaluation.questions,
      }
    : null

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-muted-foreground">Cargando resultados...</p>
      </div>
    )
  }

  if (!evaluation || !resultsData) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-foreground">Resultados</h1>
        <p className="text-muted-foreground">No se encontro la evaluacion.</p>
        <Link to="/dashboard">
          <Button variant="outline">Volver al Dashboard</Button>
        </Link>
      </div>
    )
  }

  // PA aspects data for bar chart
  const paAspects = [
    { aspect: 'PLANEACIÓN', percentage: resultsData.pa_breakdown['PLANEACIÓN'] || 0 },
    { aspect: 'ORGANIZACIÓN', percentage: resultsData.pa_breakdown['ORGANIZACIÓN'] || 0 },
    { aspect: 'DIRECCIÓN', percentage: resultsData.pa_breakdown['DIRECCIÓN'] || 0 },
    { aspect: 'CONTROL', percentage: resultsData.pa_breakdown['CONTROL'] || 0 },
  ]

  // PO aspects data for bar chart
  const poAspects = [
    { aspect: 'LOGÍSTICA DE COMPRAS', percentage: resultsData.po_breakdown['LOGÍSTICA DE COMPRAS'] || 0 },
    { aspect: 'GESTIÓN DE PRODUCCIÓN', percentage: resultsData.po_breakdown['GESTIÓN DE PRODUCCIÓN'] || 0 },
    { aspect: 'LOGÍSTICA EXTERNA', percentage: resultsData.po_breakdown['LOGÍSTICA EXTERNA'] || 0 },
  ]

  const existingActionPlan = actionPlans && actionPlans.length > 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Resultados</h1>
          <p className="text-muted-foreground">
            Evaluacion del {new Date(evaluation.fecha).toLocaleDateString('es-ES')}
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            onClick={() => handleDownloadPDF(evaluation.id)}
          >
            <Download className="w-4 h-4 mr-2" />
            Descargar PDF
          </Button>
          <Button
            variant="outline"
            onClick={() => handleDownloadExcel(evaluation.id)}
          >
            <Download className="w-4 h-4 mr-2" />
            Exportar Excel
          </Button>
          {existingActionPlan ? (
            <Link to={`/action-plans?evaluation_id=${evaluation.id}`}>
              <Button>
                <ExternalLink className="w-4 h-4 mr-2" />
                Ver Plan de Accion
              </Button>
            </Link>
          ) : (
            <Link to={`/action-plans?evaluation_id=${evaluation.id}`}>
              <Button>
                <Plus className="w-4 h-4 mr-2" />
                Crear Plan de Accion
              </Button>
            </Link>
          )}
        </div>
      </div>

      {/* Health Index Gauge */}
      <Card>
        <CardHeader>
          <CardTitle>Indice de Salud</CardTitle>
        </CardHeader>
        <CardContent className="flex justify-center py-8">
          <HealthGauge percentage={resultsData.general_pct} />
        </CardContent>
      </Card>

      {/* PA and PO percentages */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">PA (Gestion)</p>
                <p className={cn('text-3xl font-bold', getScoreColor(resultsData.pa_pct))}>
                  {resultsData.pa_pct.toFixed(0)}%
                </p>
              </div>
              <Badge
                variant={
                  resultsData.pa_pct >= 75 ? 'success' : resultsData.pa_pct >= 60 ? 'warning' : 'error'
                }
              >
                {resultsData.pa_pct >= 75 ? 'Bueno' : resultsData.pa_pct >= 60 ? 'Regular' : 'Necesita mejorar'}
              </Badge>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">PO (Operaciones)</p>
                <p className={cn('text-3xl font-bold', getScoreColor(resultsData.po_pct))}>
                  {resultsData.po_pct.toFixed(0)}%
                </p>
              </div>
              <Badge
                variant={
                  resultsData.po_pct >= 75 ? 'success' : resultsData.po_pct >= 60 ? 'warning' : 'error'
                }
              >
                {resultsData.po_pct >= 75 ? 'Bueno' : resultsData.po_pct >= 60 ? 'Regular' : 'Necesita mejorar'}
              </Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* PA Bar Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Desglose PA - Gestion</CardTitle>
        </CardHeader>
        <CardContent>
          <AspectBarChart
            data={paAspects}
            title="Porcentaje por aspecto"
            colors={['#3b82f6', '#6366f1', '#8b5cf6', '#a855f7']}
          />
        </CardContent>
      </Card>

      {/* PO Bar Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Desglose PO - Operaciones</CardTitle>
        </CardHeader>
        <CardContent>
          <AspectBarChart
            data={poAspects}
            title="Porcentaje por aspecto"
            colors={['#f97316', '#fb923c', '#fdba74']}
          />
        </CardContent>
      </Card>

      {/* Detail Table */}
      {resultsData.questions.length > 0 && (
        <Card>
          <CardContent className="pt-6">
            <DetailTable questions={resultsData.questions} />
          </CardContent>
        </Card>
      )}

      {/* Priority indicator */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center gap-3">
            <p className="text-sm font-medium text-muted-foreground">Prioridad:</p>
            <Badge
              variant={
                resultsData.priority === 'PA'
                  ? 'default'
                  : resultsData.priority === 'PO'
                  ? 'warning'
                  : 'success'
              }
            >
              {resultsData.priority === 'PA'
                ? 'Enfocarse en Gestion (PA)'
                : resultsData.priority === 'PO'
                ? 'Enfocarse en Operaciones (PO)'
                : 'Balanceado'}
            </Badge>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}