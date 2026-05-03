import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { useRecommendations, useCreateActionPlan, Recommendation } from '@/hooks/useApi'
import { Plus, AlertCircle } from 'lucide-react'
import { cn } from '@/lib/utils'

// Priority badge colors
function PriorityBadge({ priority }: { priority: string }) {
  const colors: Record<string, string> = {
    ALTA: 'bg-red-100 text-red-800 border-red-200',
    MEDIA: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    BAJA: 'bg-green-100 text-green-800 border-green-200',
  }
  
  return (
    <span className={cn(
      'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold uppercase tracking-wide border',
      colors[priority] || colors.BAJA
    )}>
      {priority}
    </span>
  )
}

// Single recommendation card
function RecommendationCard({ 
  recommendation, 
  onCreateAction 
}: { 
  recommendation: Recommendation
  onCreateAction: (rec: Recommendation) => void
}) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-base">{recommendation.element}</CardTitle>
          <PriorityBadge priority={recommendation.priority} />
        </div>
        <p className="text-sm text-muted-foreground font-medium">{recommendation.aspect}</p>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-foreground mb-4">{recommendation.recommendation}</p>
        <Button 
          size="sm" 
          onClick={() => onCreateAction(recommendation)}
          className="w-full"
        >
          <Plus className="w-4 h-4 mr-1" />
          Crear Acción
        </Button>
      </CardContent>
    </Card>
  )
}

// Group recommendations by aspect
function GroupedRecommendations({ 
  recommendations, 
  onCreateAction 
}: { 
  recommendations: Recommendation[]
  onCreateAction: (rec: Recommendation) => void
}) {
  // Group by aspect
  const grouped = recommendations.reduce(
    (acc, rec) => {
      if (!acc[rec.aspect]) acc[rec.aspect] = []
      acc[rec.aspect].push(rec)
      return acc
    },
    {} as Record<string, Recommendation[]>
  )
  
  const aspectOrder = [
    'PLANEACIÓN',
    'ORGANIZACIÓN', 
    'DIRECCIÓN',
    'CONTROL',
    'LOGÍSTICA DE COMPRAS',
    'GESTIÓN DE PRODUCCIÓN',
    'LOGÍSTICA EXTERNA',
  ]
  
  const sortedAspects = Object.keys(grouped).sort((a, b) => {
    const idxA = aspectOrder.indexOf(a)
    const idxB = aspectOrder.indexOf(b)
    if (idxA === -1 && idxB === -1) return a.localeCompare(b)
    if (idxA === -1) return 1
    if (idxB === -1) return -1
    return idxA - idxB
  })
  
  return (
    <div className="space-y-6">
      {sortedAspects.map((aspect) => (
        <div key={aspect} className="space-y-3">
          <h3 className="text-lg font-semibold text-foreground sticky top-0 bg-background py-2 border-b">
            {aspect}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {grouped[aspect].map((rec, idx) => (
              <RecommendationCard 
                key={`${rec.aspect}-${rec.element}-${idx}`}
                recommendation={rec}
                onCreateAction={onCreateAction}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

// Filter bar component
function FilterBar({ 
  priorityFilter, 
  onFilterChange 
}: { 
  priorityFilter: string
  onFilterChange: (filter: string) => void
}) {
  return (
    <div className="flex items-center gap-2 flex-wrap">
      <span className="text-sm font-medium text-muted-foreground">Filtrar por prioridad:</span>
      <Button 
        size="sm" 
        variant={priorityFilter === 'ALL' ? 'default' : 'outline'}
        onClick={() => onFilterChange('ALL')}
      >
        Todas
      </Button>
      <Button 
        size="sm" 
        variant={priorityFilter === 'ALTA' ? 'default' : 'outline'}
        onClick={() => onFilterChange('ALTA')}
        className={priorityFilter === 'ALTA' ? 'bg-red-600 hover:bg-red-700' : ''}
      >
        ALTA
      </Button>
      <Button 
        size="sm" 
        variant={priorityFilter === 'MEDIA' ? 'default' : 'outline'}
        onClick={() => onFilterChange('MEDIA')}
        className={priorityFilter === 'MEDIA' ? 'bg-yellow-600 hover:bg-yellow-700' : ''}
      >
        MEDIA
      </Button>
    </div>
  )
}

export function RecommendationsPage() {
  const [searchParams] = useSearchParams()
  const evaluationId = searchParams.get('evaluation_id') || ''

  const { data: recommendations, isLoading } = useRecommendations(evaluationId || '')
  const createActionPlan = useCreateActionPlan()

  const [priorityFilter, setPriorityFilter] = useState<string>('ALL')

  // Filter recommendations by priority
  const filteredRecommendations = recommendations?.filter(
    (rec) => priorityFilter === 'ALL' || rec.priority === priorityFilter
  ) || []

  // Handle creating action plan from recommendation
  const handleCreateAction = (rec: Recommendation) => {
    createActionPlan.mutate({
      evaluation_id: evaluationId,
      element: rec.element,
      action: rec.recommendation,
      responsible: '',
      due_date: null,
      status: 'pendiente',
    })
  }

  if (!evaluationId) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-foreground">Recomendaciones</h1>
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <AlertCircle className="w-12 h-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No se encontró el ID de la evaluación. Por favor, accedé desde la página de resultados.</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-muted-foreground">Cargando recomendaciones...</p>
      </div>
    )
  }
  
  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-foreground">Recomendaciones</h1>
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <AlertCircle className="w-12 h-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No hay recomendaciones disponibles para esta evaluación.</p>
          </CardContent>
        </Card>
      </div>
    )
  }
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Recomendaciones</h1>
          <p className="text-muted-foreground">
            Basadas en los resultados de tu evaluación
          </p>
        </div>
      </div>
      
      {/* Filter bar */}
      <Card>
        <CardContent className="py-4">
          <FilterBar priorityFilter={priorityFilter} onFilterChange={setPriorityFilter} />
        </CardContent>
      </Card>
      
      {/* Recommendations grouped by aspect */}
      <GroupedRecommendations 
        recommendations={filteredRecommendations}
        onCreateAction={handleCreateAction}
      />
      
      {/* Summary */}
      <Card>
        <CardContent className="py-4">
          <p className="text-sm text-muted-foreground">
            Mostrando {filteredRecommendations.length} de {recommendations.length} recomendaciones
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
