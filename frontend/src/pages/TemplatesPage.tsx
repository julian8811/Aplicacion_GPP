import { useState, useMemo } from 'react'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { TemplateCard } from '@/components/templates/TemplateCard'
import { Skeleton } from '@/components/shared/Skeleton'
import { useTemplates, useDeleteTemplate, useCreateTemplateFromEvaluation } from '@/hooks/useTemplates'
import { Plus, Download, Filter } from 'lucide-react'
import { toast } from '@/lib/toast'
import { useNavigate, useSearchParams } from 'react-router-dom'

type FilterType = 'all' | 'mine' | 'public'

export function TemplatesPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [filter, setFilter] = useState<FilterType>('all')
  
  const { data: templates, isLoading } = useTemplates()
  const deleteTemplate = useDeleteTemplate()
  const createFromEvaluation = useCreateTemplateFromEvaluation()
  
  const selectedEvaluationId = searchParams.get('from_evaluation')
  
  const filteredTemplates = useMemo(() => {
    if (!templates) return []
    
    switch (filter) {
      case 'mine':
        return templates.filter(t => !t.is_public)
      case 'public':
        return templates.filter(t => t.is_public)
      default:
        return templates
    }
  }, [templates, filter])
  
  const handleDelete = async (template: any) => {
    if (confirm(`¿Eliminar la plantilla "${template.name}"?`)) {
      try {
        await deleteTemplate.mutateAsync(template.id)
      } catch (error) {
        toast.error('Error al eliminar la plantilla')
      }
    }
  }
  
  const handleCreateFromEvaluation = async () => {
    if (!selectedEvaluationId) {
      toast.error('Selecciona una evaluación primero')
      return
    }
    
    const name = prompt('Nombre de la plantilla:')
    if (!name) return
    
    try {
      await createFromEvaluation.mutateAsync({
        evaluation_id: selectedEvaluationId,
        name,
        description: `Plantilla creada desde evaluación`
      })
      toast.success('Plantilla creada exitosamente')
      navigate(`/templates`)
    } catch {
      toast.error('Error al crear la plantilla')
    }
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-12 w-64" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3].map(i => (
            <Skeleton key={i} className="h-40" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Plantillas de Evaluación</h1>
          <p className="text-muted-foreground">
            Crea y gestiona plantillas para iniciar evaluaciones rápidamente
          </p>
        </div>
        
        <div className="flex gap-2">
          {selectedEvaluationId && (
            <Button onClick={handleCreateFromEvaluation}>
              <Download className="w-4 h-4 mr-2" />
              Crear desde Evaluación
            </Button>
          )}
          <Button onClick={() => navigate('/evaluate/wizard?action=blank')}>
            <Plus className="w-4 h-4 mr-2" />
            Nueva Plantilla en Blanco
          </Button>
        </div>
      </div>

      {/* Filter */}
      <Card>
        <CardContent className="p-4">
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground mr-2">Filtrar:</span>
            <Button 
              size="sm" 
              variant={filter === 'all' ? 'default' : 'outline'}
              onClick={() => setFilter('all')}
            >
              Todas
            </Button>
            <Button 
              size="sm" 
              variant={filter === 'mine' ? 'default' : 'outline'}
              onClick={() => setFilter('mine')}
            >
              Mis Plantillas
            </Button>
            <Button 
              size="sm" 
              variant={filter === 'public' ? 'default' : 'outline'}
              onClick={() => setFilter('public')}
            >
              Públicas
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Templates Grid */}
      {filteredTemplates.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <p className="text-muted-foreground text-center">
              {filter === 'public' 
                ? "No hay plantillas públicas disponibles."
                : "No has creado ninguna plantilla todavía."}
              <br />
              Crea una desde una evaluación existente o comienza de cero.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredTemplates.map(template => (
            <TemplateCard
              key={template.id}
              template={template}
              onDelete={handleDelete}
              showOwner={filter === 'all'}
            />
          ))}
        </div>
      )}
    </div>
  )
}