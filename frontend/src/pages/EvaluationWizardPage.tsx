import { useState, useEffect, useCallback } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useMatrices, useCalculateResults, useUpdateEvaluation } from '@/hooks/useApi'
import { useDraftStore } from '@/store/draftStore'
import { PAEvaluationPage } from './PAEvaluationPage'
import { POEvaluationPage } from './POEvaluationPage'
import { Button } from '@/components/ui/Button'
import { Card, CardContent } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { cn } from '@/lib/utils'
import { toast } from '@/lib/toast'

type Step = 'pa' | 'po' | 'review'

const STEPS: { id: Step; label: string; description: string }[] = [
  { id: 'pa', label: 'Proceso Administrativo', description: 'PA' },
  { id: 'po', label: 'Proceso Operativo', description: 'PO' },
  { id: 'review', label: 'Guardar Resultados', description: 'Revisar y enviar' },
]

const ASPECT_LABELS_PA: Record<string, string> = {
  'PLANEACIÓN': 'Planeación',
  'ORGANIZACIÓN': 'Organización',
  'DIRECCIÓN': 'Dirección',
  'CONTROL': 'Control',
}

const ASPECT_LABELS_PO: Record<string, string> = {
  'LOGÍSTICA DE COMPRAS': 'Logística de Compras',
  'GESTIÓN DE PRODUCCIÓN': 'Gestión de Producción',
  'LOGÍSTICA EXTERNA': 'Logística Externa',
}

interface MatrixData {
  PA: any
  PO: any
}

export function EvaluationWizardPage() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const evaluationId = searchParams.get('id') || ''
  const { data: matrices, isLoading } = useMatrices()
  const calculateResults = useCalculateResults()
  const updateEvaluation = useUpdateEvaluation()
  const { paDraft, poDraft, setPADraft, setPODraft, clearDrafts } = useDraftStore()
  
  const [currentStep, setCurrentStep] = useState<Step>('pa')
  const [paValues, setPaValues] = useState<Record<string, Record<string, number>>>({})
  const [poValues, setPoValues] = useState<Record<string, Record<string, number>>>({})
  const [lastSaved, setLastSaved] = useState<Date | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Initialize from draft store
  useEffect(() => {
    if (Object.keys(paDraft).length > 0) {
      setPaValues(paDraft)
    }
    if (Object.keys(poDraft).length > 0) {
      setPoValues(poDraft)
    }
  }, [paDraft, poDraft])

  // Initialize empty values when matrices load
  useEffect(() => {
    if (matrices) {
      const matrixData = matrices as MatrixData
      
      if (matrixData.PA && Object.keys(paDraft).length === 0) {
        const initialPA: Record<string, Record<string, number>> = {}
        Object.keys(matrixData.PA).forEach(aspect => {
          initialPA[aspect] = {}
          Object.keys(matrixData.PA[aspect]).forEach(category => {
            matrixData.PA[aspect][category]?.forEach((q: any) => {
              initialPA[aspect][q.id] = 0
            })
          })
        })
        setPaValues(initialPA)
      }
      
      if (matrixData.PO && Object.keys(poDraft).length === 0) {
        const initialPO: Record<string, Record<string, number>> = {}
        Object.keys(matrixData.PO).forEach(aspect => {
          initialPO[aspect] = {}
          Object.keys(matrixData.PO[aspect]).forEach(category => {
            matrixData.PO[aspect][category]?.forEach((q: any) => {
              initialPO[aspect][q.id] = 0
            })
          })
        })
        setPoValues(initialPO)
      }
    }
  }, [matrices, paDraft, poDraft])

  // Auto-save every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      if (currentStep === 'pa' && Object.keys(paValues).length > 0) {
        setPADraft(paValues)
        setLastSaved(new Date())
      } else if (currentStep === 'po' && Object.keys(poValues).length > 0) {
        setPODraft(poValues)
        setLastSaved(new Date())
      }
    }, 30000)

    return () => clearInterval(interval)
  }, [currentStep, paValues, poValues, setPADraft, setPODraft])

  const currentStepIndex = STEPS.findIndex(s => s.id === currentStep)

  const handleNext = useCallback(() => {
    // Save current step data
    if (currentStep === 'pa') {
      setPADraft(paValues)
    } else if (currentStep === 'po') {
      setPODraft(poValues)
    }
    
    const nextIndex = currentStepIndex + 1
    if (nextIndex < STEPS.length) {
      setCurrentStep(STEPS[nextIndex].id)
    }
  }, [currentStep, currentStepIndex, paValues, poValues, setPADraft, setPODraft])

  const handleBack = useCallback(() => {
    const prevIndex = currentStepIndex - 1
    if (prevIndex >= 0) {
      setCurrentStep(STEPS[prevIndex].id)
    }
  }, [currentStepIndex])

  const handleSubmit = async () => {
    if (!evaluationId) {
      toast.error('No se encontró el ID de la evaluación')
      return
    }
    
    setIsSubmitting(true)
    try {
      // Calculate results
      const results = await calculateResults.mutateAsync({
        evals_pa: paValues,
        evals_po: poValues,
      })
      
      // Save results to evaluation
      await updateEvaluation.mutateAsync({
        id: evaluationId,
        general_pct: results.general_pct,
        pa_pct: results.pa_pct,
        po_pct: results.po_pct,
        evaluaciones_pa: paValues,
        evaluaciones_po: poValues,
      })
      
      // Clear drafts after successful submit
      clearDrafts()
      
      // Navigate to results with evaluation ID
      navigate(`/results/${evaluationId}`)
    } catch (error) {
      console.error('Error saving results:', error)
      toast.error('Error al guardar los resultados')
      setIsSubmitting(false)
    }
  }

  // Save draft to file using browser File API
  const handleSaveDraft = useCallback(() => {
    const draftData = {
      paValues,
      poValues,
      fecha: new Date().toISOString(),
    }
    
    const blob = new Blob([JSON.stringify(draftData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `gpp_draft_${new Date().toISOString().slice(0, 10)}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    
    setLastSaved(new Date())
  }, [paValues, poValues])

  // Load draft from file using browser File API
  const handleLoadDraft = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return
    
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const content = e.target?.result as string
        const draftData = JSON.parse(content)
        
        if (draftData.paValues) {
          setPaValues(draftData.paValues)
          setPADraft(draftData.paValues)
        }
        if (draftData.poValues) {
          setPoValues(draftData.poValues)
          setPODraft(draftData.poValues)
        }
        
        setLastSaved(new Date())
      } catch (error) {
        console.error('Error loading draft:', error)
        alert('Error al cargar el borrador. Archivo inválido.')
      }
    }
    reader.readAsText(file)
    
    // Reset input so same file can be loaded again
    event.target.value = ''
  }, [setPADraft, setPODraft])

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
  }

  const getStepStatus = (index: number) => {
    if (index < currentStepIndex) return 'completed'
    if (index === currentStepIndex) return 'current'
    return 'pending'
  }

  const countQuestionsAnswered = (values: Record<string, Record<string, number>>) => {
    let answered = 0
    let total = 0
    Object.values(values).forEach(aspect => {
      Object.values(aspect).forEach(val => {
        if (val > 0) answered++
        total++
      })
    })
    return { answered, total }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="h-8 w-8 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Cargando...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Progress Indicator */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Progreso de Evaluación</h2>
            {lastSaved && (
              <Badge variant="success">
                Último guardado: {formatTime(lastSaved)}
              </Badge>
            )}
          </div>
          
          <div className="flex items-center justify-between">
            {STEPS.map((step, index) => {
              const status = getStepStatus(index)
              return (
                <div key={step.id} className="flex items-center">
                  <div className="flex flex-col items-center">
                    <div
                      className={cn(
                        "w-10 h-10 rounded-full flex items-center justify-center font-semibold text-sm transition-all",
                        status === 'completed' && "bg-green-500 text-white",
                        status === 'current' && "bg-primary text-white",
                        status === 'pending' && "bg-slate-200 text-slate-500"
                      )}
                    >
                      {status === 'completed' ? (
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      ) : (
                        index + 1
                      )}
                    </div>
                    <span className={cn(
                      "text-xs mt-2 font-medium",
                      status === 'current' ? "text-foreground" : "text-muted-foreground"
                    )}>
                      {step.label}
                    </span>
                  </div>
                  {index < STEPS.length - 1 && (
                    <div className={cn(
                      "w-20 h-1 mx-2 rounded",
                      status === 'completed' ? "bg-green-500" : "bg-slate-200"
                    )} />
                  )}
                </div>
              )
            })}
          </div>

          {/* Question count for current step */}
          <div className="mt-4 pt-4 border-t border-border">
            {currentStep === 'pa' && (() => {
              const { answered, total } = countQuestionsAnswered(paValues)
              return (
                <p className="text-sm text-muted-foreground">
                  Preguntas respondidas: <span className="font-medium text-foreground">{answered}</span> de {total}
                </p>
              )
            })()}
            {currentStep === 'po' && (() => {
              const { answered, total } = countQuestionsAnswered(poValues)
              return (
                <p className="text-sm text-muted-foreground">
                  Preguntas respondidas: <span className="font-medium text-foreground">{answered}</span> de {total}
                </p>
              )
            })()}
            {currentStep === 'review' && (
              <p className="text-sm text-muted-foreground">
                Revisa tus respuestas antes de guardar los resultados.
              </p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Step Content */}
      <div className="min-h-[500px]">
        {currentStep === 'pa' && (
          <PAEvaluationPage />
        )}
        {currentStep === 'po' && (
          <POEvaluationPage />
        )}
        {currentStep === 'review' && (
          <ReviewStep
            paValues={paValues}
            poValues={poValues}
            onSaveDraft={handleSaveDraft}
            onLoadDraft={handleLoadDraft}
          />
        )}
      </div>

      {/* Navigation Buttons */}
      <div className="flex justify-between pt-4 border-t border-border">
        <Button
          variant="outline"
          onClick={handleBack}
          disabled={currentStepIndex === 0}
        >
          ← Anterior
        </Button>
        
        {currentStep === 'review' ? (
          <Button
            variant="default"
            className="bg-primary text-primary-foreground hover:bg-primary/90"
            onClick={handleSubmit}
            disabled={isSubmitting}
          >
            {isSubmitting && (
              <div className="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2" />
            )}
            {isSubmitting ? 'Guardando...' : 'Guardar y Ver Resultados'}
          </Button>
        ) : (
          <Button onClick={handleNext}>
            Siguiente →
          </Button>
        )}
      </div>
    </div>
  )
}

// Review Step Component
interface ReviewStepProps {
  paValues: Record<string, Record<string, number>>
  poValues: Record<string, Record<string, number>>
  onSaveDraft?: () => void
  onLoadDraft?: (event: React.ChangeEvent<HTMLInputElement>) => void
}

function ReviewStep({ paValues, poValues, onSaveDraft, onLoadDraft }: ReviewStepProps) {
  const paAspects = Object.keys(paValues)
  const poAspects = Object.keys(poValues)

  const calculateAspectAverage = (values: Record<string, Record<string, number>>, aspect: string) => {
    const aspectValues = Object.values(values[aspect] || {})
    if (aspectValues.length === 0) return 0
    const sum = aspectValues.reduce((a, b) => a + b, 0)
    return Math.round((sum / aspectValues.length) * 20) // Convert 0-5 to 0-100
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardContent className="p-6">
          <h2 className="text-xl font-bold mb-4">Resumen de Evaluación</h2>
          <p className="text-muted-foreground mb-6">
            Revisa el resumen de tus respuestas antes de guardar los resultados.
          </p>

          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <span className="w-8 h-8 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center text-sm font-bold">PA</span>
                Proceso Administrativo
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {paAspects.map(aspect => {
                  const avg = calculateAspectAverage(paValues, aspect)
                  const label = ASPECT_LABELS_PA[aspect] || aspect
                  return (
                    <div key={aspect} className="bg-slate-50 p-4 rounded-lg text-center">
                      <p className="text-sm text-muted-foreground mb-1">{label}</p>
                      <p className="text-2xl font-bold text-foreground">{avg}%</p>
                    </div>
                  )
                })}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                <span className="w-8 h-8 bg-green-100 text-green-700 rounded-full flex items-center justify-center text-sm font-bold">PO</span>
                Proceso Operativo
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {poAspects.map(aspect => {
                  const avg = calculateAspectAverage(poValues, aspect)
                  const label = ASPECT_LABELS_PO[aspect] || aspect
                  return (
                    <div key={aspect} className="bg-slate-50 p-4 rounded-lg text-center">
                      <p className="text-sm text-muted-foreground mb-1">{label}</p>
                      <p className="text-2xl font-bold text-foreground">{avg}%</p>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Draft Actions */}
            <div className="flex gap-4 pt-4 border-t border-border">
              <Button
                variant="outline"
                onClick={onSaveDraft}
                disabled={Object.keys(paValues).length === 0 && Object.keys(poValues).length === 0}
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                </svg>
                Guardar Borrador
              </Button>

              <Button
                variant="outline"
                onClick={() => document.getElementById('load-draft-input')?.click()}
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                Cargar Borrador
              </Button>
              <input
                id="load-draft-input"
                type="file"
                accept="application/json,.json"
                onChange={onLoadDraft}
                className="hidden"
              />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}