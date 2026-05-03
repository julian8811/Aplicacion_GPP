import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import api from '@/lib/api'
import { toast } from '@/lib/toast'
import { ClipboardList, FileText, CheckCircle2 } from 'lucide-react'

type EvaluationType = 'pa_only' | 'po_only' | 'both'

export function NewEvaluationPage() {
  const navigate = useNavigate()
  const [selectedType, setSelectedType] = useState<EvaluationType | null>(null)
  const [isCreating, setIsCreating] = useState(false)

  const handleCreate = async () => {
    if (!selectedType) {
      toast.error('Selecciona un tipo de evaluacion')
      return
    }

setIsCreating(true)
    try {
      const payload: Record<string, any> = {
        general_pct: 0,
        pa_pct: 0,
        po_pct: 0,
      }

      if (selectedType === 'pa_only') {
        payload.evaluaciones_pa = {}
      } else if (selectedType === 'po_only') {
        payload.evaluaciones_po = {}
      } else {
        payload.evaluaciones_pa = {}
        payload.evaluaciones_po = {}
      }

      const response = await api.post('/evaluations', payload)
      const evaluation = response.data

      toast.success('Evaluacion creada')
      // Navigate to wizard with evaluation ID and type
      navigate(`/evaluate/wizard?id=${evaluation.id}&type=${selectedType}`)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Error al crear evaluacion')
    } finally {
      setIsCreating(false)
    }
  }

  const options: { type: EvaluationType; title: string; description: string; badge: string }[] = [
    {
      type: 'pa_only',
      title: 'Autoevaluacion PA',
      description: 'Planeacion, Organizacion, Direccion y Control',
      badge: 'PA',
    },
    {
      type: 'po_only',
      title: 'Autoevaluacion PO',
      description: 'Logistica Compras, Produccion y Logistica Externa',
      badge: 'PO',
    },
    {
      type: 'both',
      title: 'Ambas (PA + PO)',
      description: 'Evaluacion completa del sistema de gestion',
      badge: 'PA + PO',
    },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Nueva Evaluacion</h1>
        <p className="text-muted-foreground">Selecciona el tipo de evaluacion que deseas realizar</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {options.map((option) => (
          <Card
            key={option.type}
            className={`cursor-pointer transition-all hover:border-primary ${
              selectedType === option.type ? 'border-primary ring-2 ring-primary/20' : ''
            }`}
            onClick={() => setSelectedType(option.type)}
          >
            <CardContent className="pt-6">
              <div className="flex items-start justify-between mb-4">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                  option.type === 'pa_only' ? 'bg-primary/10' :
                  option.type === 'po_only' ? 'bg-accent/10' :
                  'bg-success/10'
                }`}>
                  {option.type === 'pa_only' ? (
                    <ClipboardList className="w-6 h-6 text-primary" />
                  ) : option.type === 'po_only' ? (
                    <FileText className="w-6 h-6 text-accent" />
                  ) : (
                    <CheckCircle2 className="w-6 h-6 text-success" />
                  )}
                </div>
                <Badge variant={option.type === 'both' ? 'success' : 'default'}>
                  {option.badge}
                </Badge>
              </div>
              <h3 className="font-semibold mb-2">{option.title}</h3>
              <p className="text-sm text-muted-foreground">{option.description}</p>
              {selectedType === option.type && (
                <div className="mt-4 flex items-center gap-2 text-primary">
                  <CheckCircle2 className="w-4 h-4" />
                  <span className="text-sm font-medium">Seleccionado</span>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="flex justify-end gap-4">
        <Button variant="outline" onClick={() => navigate('/dashboard')}>
          Cancelar
        </Button>
        <Button onClick={handleCreate} disabled={!selectedType || isCreating}>
          {isCreating ? 'Creando...' : 'Comenzar Evaluacion'}
        </Button>
      </div>
    </div>
  )
}