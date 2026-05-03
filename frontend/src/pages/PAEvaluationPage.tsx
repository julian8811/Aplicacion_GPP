import { useEffect, useState, useCallback } from 'react'
import { useMatrices } from '@/hooks/useApi'
import { SliderQuestion } from '@/components/shared/SliderQuestion'
import { useDraftStore } from '@/store/draftStore'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'

interface PAQuestion {
  id: string
  pregunta: string
  contexto?: string
}

interface PAAspect {
  [key: string]: PAQuestion[]
}

interface PAMatrix {
  [aspect: string]: PAAspect
}

const ASPECT_LABELS: Record<string, string> = {
  'PLANEACIÓN': 'Planeación',
  'ORGANIZACIÓN': 'Organización',
  'DIRECCIÓN': 'Dirección',
  'CONTROL': 'Control',
}

export function PAEvaluationPage() {
  const { data: matrices, isLoading, error } = useMatrices()
  const [values, setValues] = useState<Record<string, Record<string, number>>>({})
  const [lastSaved, setLastSaved] = useState<Date | null>(null)
  const { paDraft, setPADraft } = useDraftStore()

  // Load draft on mount
  useEffect(() => {
    if (Object.keys(paDraft).length > 0) {
      setValues(paDraft)
    }
  }, [paDraft])

  // Initialize empty values when matrices load
  useEffect(() => {
    if (matrices?.PA) {
      const pa = matrices.PA as PAMatrix
      const initialValues: Record<string, Record<string, number>> = {}
      
      Object.keys(pa).forEach(aspect => {
        initialValues[aspect] = {}
        Object.keys(pa[aspect]).forEach(category => {
          pa[aspect][category]?.forEach((q: PAQuestion) => {
            initialValues[aspect][q.id] = paDraft[aspect]?.[q.id] || 0
          })
        })
      })
      
      if (Object.keys(paDraft).length === 0) {
        setValues(initialValues)
      }
    }
  }, [matrices, paDraft])

  // Auto-save every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      if (Object.keys(values).length > 0) {
        setPADraft(values)
        setLastSaved(new Date())
      }
    }, 30000)

    return () => clearInterval(interval)
  }, [values, setPADraft])

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

  if (!matrices?.PA) {
    return (
      <Card className="border-error">
        <CardContent className="p-4">
          <p className="text-error">No se encontraron las preguntas del proceso administrativo.</p>
        </CardContent>
      </Card>
    )
  }

  const pa = matrices.PA as PAMatrix

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Proceso Administrativo (PA)</h1>
          <p className="text-muted-foreground mt-1">Evalúa cada aspecto del proceso administrativo</p>
        </div>
        {lastSaved && (
          <Badge variant="success">
            Guardado: {formatTime(lastSaved)}
          </Badge>
        )}
      </div>

      {Object.entries(pa).map(([aspect, categories]) => {
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
                    {questions.map((q: PAQuestion) => (
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