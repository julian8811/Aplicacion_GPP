import { useEffect, useState, useCallback } from 'react'
import { useMatrices } from '@/hooks/useApi'
import { SliderQuestion } from '@/components/shared/SliderQuestion'
import { useDraftStore } from '@/store/draftStore'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'

interface POQuestion {
  id: string
  pregunta: string
  contexto?: string
}

interface POAspect {
  [key: string]: POQuestion[]
}

interface POMatrix {
  [aspect: string]: POAspect
}

const ASPECT_LABELS: Record<string, string> = {
  'LOGÍSTICA DE COMPRAS': 'Logística de Compras',
  'GESTIÓN DE PRODUCCIÓN': 'Gestión de Producción',
  'LOGÍSTICA EXTERNA': 'Logística Externa',
}

export function POEvaluationPage() {
  const { data: matrices, isLoading, error } = useMatrices()
  const [values, setValues] = useState<Record<string, Record<string, number>>>({})
  const [lastSaved, setLastSaved] = useState<Date | null>(null)
  const { poDraft, setPODraft } = useDraftStore()

  // Load draft on mount
  useEffect(() => {
    if (Object.keys(poDraft).length > 0) {
      setValues(poDraft)
    }
  }, [poDraft])

  // Initialize empty values when matrices load
  useEffect(() => {
    if (matrices?.PO) {
      const po = matrices.PO as POMatrix
      const initialValues: Record<string, Record<string, number>> = {}
      
      Object.keys(po).forEach(aspect => {
        initialValues[aspect] = {}
        Object.keys(po[aspect]).forEach(category => {
          po[aspect][category]?.forEach((q: POQuestion) => {
            initialValues[aspect][q.id] = poDraft[aspect]?.[q.id] || 0
          })
        })
      })
      
      if (Object.keys(poDraft).length === 0) {
        setValues(initialValues)
      }
    }
  }, [matrices, poDraft])

  // Auto-save every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      if (Object.keys(values).length > 0) {
        setPODraft(values)
        setLastSaved(new Date())
      }
    }, 30000)

    return () => clearInterval(interval)
  }, [values, setPODraft])

  const handleValueChange = useCallback((aspect: string, questionId: string, value: number) => {
    setValues(prev => ({
      ...prev,
      [aspect]: {
        ...prev[aspect],
        [questionId]: value
      }
    }))
  }, [])

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
  }

  if (isLoading) {
    return (
      <div className="space-y-4">
        <div className="h-8 w-48 bg-muted animate-pulse rounded" />
        <div className="h-4 w-32 bg-muted animate-pulse rounded" />
        {[1, 2, 3].map(i => (
          <div key={i} className="h-32 bg-muted animate-pulse rounded-lg" />
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <Card className="border-error">
        <CardContent className="p-4">
          <p className="text-error">Error al cargar las preguntas. Por favor intenta de nuevo.</p>
        </CardContent>
      </Card>
    )
  }

  if (!matrices?.PO) {
    return (
      <Card className="border-error">
        <CardContent className="p-4">
          <p className="text-error">No se encontraron las preguntas del proceso operativo.</p>
        </CardContent>
      </Card>
    )
  }

  const po = matrices.PO as POMatrix

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Proceso Operativo (PO)</h1>
          <p className="text-muted-foreground mt-1">Evalúa cada aspecto del proceso operativo</p>
        </div>
        {lastSaved && (
          <Badge variant="success">
            Guardado: {formatTime(lastSaved)}
          </Badge>
        )}
      </div>

      {Object.entries(po).map(([aspect, categories]) => {
        const aspectLabel = ASPECT_LABELS[aspect] || aspect
        
        return (
          <Card key={aspect}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                {aspectLabel}
                <Badge variant="default">{Object.keys(categories).length} categorías</Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {Object.entries(categories).map(([category, questions]) => (
                <div key={category}>
                  <h3 className="text-sm font-semibold text-muted-foreground mb-3 uppercase tracking-wide">
                    {category}
                  </h3>
                  <div className="space-y-2">
                    {questions.map((q: POQuestion) => (
                      <SliderQuestion
                        key={q.id}
                        id={q.id}
                        question={q.pregunta}
                        context={q.contexto}
                        value={values[aspect]?.[q.id] || 0}
                        onChange={(val) => handleValueChange(aspect, q.id, val)}
                      />
                    ))}
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}