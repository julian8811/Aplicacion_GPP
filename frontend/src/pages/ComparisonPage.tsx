import { useState, useMemo } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { ComparisonTable } from '@/components/comparison/ComparisonTable'
import { Skeleton } from '@/components/shared/Skeleton'
import { useEvaluations } from '@/hooks/useApi'
import { useComparison } from '@/hooks/useComparison'
import { formatDate, getScoreColor, cn } from '@/lib/utils'
import { ArrowLeftRight, TrendingUp, TrendingDown, Minus } from 'lucide-react'

export function ComparisonPage() {
  const { data: evaluations, isLoading: evalsLoading } = useEvaluations()
  
  const [evalAId, setEvalAId] = useState<string>('')
  const [evalBId, setEvalBId] = useState<string>('')
  
  const { data: comparison, isLoading: comparisonLoading } = useComparison(evalAId, evalBId)
  
  // Sort evaluations by date for better UX
  const sortedEvaluations = useMemo(() => {
    if (!evaluations) return []
    return [...evaluations].sort((a, b) => 
      new Date(b.fecha).getTime() - new Date(a.fecha).getTime()
    )
  }, [evaluations])
  
  const overall = comparison?.overall

  if (evalsLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-12 w-64" />
        <Skeleton className="h-48" />
        <Skeleton className="h-64" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Comparar Evaluaciones</h1>
          <p className="text-muted-foreground">
            Selecciona dos evaluaciones para comparar sus resultados
          </p>
        </div>
      </div>

      {/* Selection Card */}
      <Card>
        <CardContent className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium mb-2">Primera Evaluación (A)</label>
              <select
                className="w-full px-3 py-2 border border-border rounded-lg bg-background"
                value={evalAId}
                onChange={(e) => setEvalAId(e.target.value)}
              >
                <option value="">Seleccionar evaluación...</option>
                {sortedEvaluations.map(ev => (
                  <option key={ev.id} value={ev.id}>
                    {formatDate(ev.fecha)} - {ev.general_pct.toFixed(0)}%
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">Segunda Evaluación (B)</label>
              <select
                className="w-full px-3 py-2 border border-border rounded-lg bg-background"
                value={evalBId}
                onChange={(e) => setEvalBId(e.target.value)}
              >
                <option value="">Seleccionar evaluación...</option>
                {sortedEvaluations.map(ev => (
                  <option key={ev.id} value={ev.id}>
                    {formatDate(ev.fecha)} - {ev.general_pct.toFixed(0)}%
                  </option>
                ))}
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Comparison Results */}
      {comparisonLoading && (
        <div className="flex items-center justify-center py-12">
          <div className="h-8 w-8 border-4 border-primary border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {comparison && overall && (
        <>
          {/* Overall Summary */}
          <Card>
            <CardHeader>
              <CardTitle>Resumen de Comparación</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* General */}
                <div className="text-center p-4 bg-slate-50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-2">Cumplimiento General</p>
                  <div className="flex items-center justify-center gap-4">
                    <span className={cn("text-2xl font-bold", getScoreColor(overall.eval_a.general_pct))}>
                      {overall.eval_a.general_pct}%
                    </span>
                    <span className="text-muted-foreground">→</span>
                    <span className={cn("text-2xl font-bold", getScoreColor(overall.eval_b.general_pct))}>
                      {overall.eval_b.general_pct}%
                    </span>
                  </div>
                  <div className={cn(
                    "flex items-center justify-center gap-1 mt-2",
                    overall.delta.general_pct > 0 ? "text-success" : overall.delta.general_pct < 0 ? "text-error" : "text-muted-foreground"
                  )}>
                    {overall.delta.general_pct > 0 ? <TrendingUp className="w-4 h-4" /> : overall.delta.general_pct < 0 ? <TrendingDown className="w-4 h-4" /> : <Minus className="w-4 h-4" />}
                    <span className="font-medium">
                      {overall.delta.general_pct > 0 ? "+" : ""}{overall.delta.general_pct}%
                    </span>
                  </div>
                </div>

                {/* PA */}
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-2">PA (Gestión)</p>
                  <div className="flex items-center justify-center gap-4">
                    <span className={cn("text-2xl font-bold", getScoreColor(overall.eval_a.pa_pct))}>
                      {overall.eval_a.pa_pct}%
                    </span>
                    <span className="text-muted-foreground">→</span>
                    <span className={cn("text-2xl font-bold", getScoreColor(overall.eval_b.pa_pct))}>
                      {overall.eval_b.pa_pct}%
                    </span>
                  </div>
                  <div className={cn(
                    "flex items-center justify-center gap-1 mt-2",
                    overall.delta.pa_pct > 0 ? "text-success" : overall.delta.pa_pct < 0 ? "text-error" : "text-muted-foreground"
                  )}>
                    {overall.delta.pa_pct > 0 ? <TrendingUp className="w-4 h-4" /> : overall.delta.pa_pct < 0 ? <TrendingDown className="w-4 h-4" /> : <Minus className="w-4 h-4" />}
                    <span className="font-medium">
                      {overall.delta.pa_pct > 0 ? "+" : ""}{overall.delta.pa_pct}%
                    </span>
                  </div>
                </div>

                {/* PO */}
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-2">PO (Operaciones)</p>
                  <div className="flex items-center justify-center gap-4">
                    <span className={cn("text-2xl font-bold", getScoreColor(overall.eval_a.po_pct))}>
                      {overall.eval_a.po_pct}%
                    </span>
                    <span className="text-muted-foreground">→</span>
                    <span className={cn("text-2xl font-bold", getScoreColor(overall.eval_b.po_pct))}>
                      {overall.eval_b.po_pct}%
                    </span>
                  </div>
                  <div className={cn(
                    "flex items-center justify-center gap-1 mt-2",
                    overall.delta.po_pct > 0 ? "text-success" : overall.delta.po_pct < 0 ? "text-error" : "text-muted-foreground"
                  )}>
                    {overall.delta.po_pct > 0 ? <TrendingUp className="w-4 h-4" /> : overall.delta.po_pct < 0 ? <TrendingDown className="w-4 h-4" /> : <Minus className="w-4 h-4" />}
                    <span className="font-medium">
                      {overall.delta.po_pct > 0 ? "+" : ""}{overall.delta.po_pct}%
                    </span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* PA Comparison Table */}
          {comparison.pa_comparison && comparison.pa_comparison.length > 0 && (
            <ComparisonTable
              title="Proceso Administrativo (PA)"
              data={comparison.pa_comparison}
              evalALabel={`Eval A (${overall.eval_a.general_pct}%)`}
              evalBLabel={`Eval B (${overall.eval_b.general_pct}%)`}
            />
          )}

          {/* PO Comparison Table */}
          {comparison.po_comparison && comparison.po_comparison.length > 0 && (
            <ComparisonTable
              title="Proceso Operativo (PO)"
              data={comparison.po_comparison}
              evalALabel={`Eval A (${overall.eval_a.general_pct}%)`}
              evalBLabel={`Eval B (${overall.eval_b.general_pct}%)`}
            />
          )}
        </>
      )}

      {!evalAId || !evalBId && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <ArrowLeftRight className="w-12 h-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground text-center">
              Selecciona dos evaluaciones para ver la comparación
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}