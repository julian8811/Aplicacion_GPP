import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useQueryClient } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useActionPlans, useCreateActionPlan, useUpdateActionPlan, useDeleteActionPlan, useRecommendations } from '@/hooks/useApi'
import { Trash2, Plus, X, Check, ChevronDown, AlertCircle, Wand2 } from 'lucide-react'
import { toast } from '@/lib/toast'
import { cn } from '@/lib/utils'

type ActionPlan = {
  id: string
  evaluation_id: string
  element: string
  action: string
  responsible: string
  due_date: string | null
  status: 'pendiente' | 'en_progreso' | 'completada'
  priority?: string
}

type SortKey = 'status' | 'due_date'

// Status dropdown for inline editing
function StatusDropdown({ 
  currentStatus, 
  onSelect 
}: { 
  currentStatus: string
  onSelect: (status: string) => void
}) {
  const [open, setOpen] = useState(false)
  
  const statuses = [
    { value: 'pendiente', label: 'Pendiente', className: 'bg-red-100 text-red-800 border-red-200' },
    { value: 'en_progreso', label: 'En Progreso', className: 'bg-yellow-100 text-yellow-800 border-yellow-200' },
    { value: 'completada', label: 'Completada', className: 'bg-green-100 text-green-800 border-green-200' },
  ]
  
  const currentConfig = statuses.find(s => s.value === currentStatus) || statuses[0]
  
  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1 hover:opacity-80 transition-opacity"
      >
        <span className={cn(
          'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold uppercase tracking-wide border',
          currentConfig.className
        )}>
          {currentConfig.label}
        </span>
        <ChevronDown className="w-3 h-3 text-muted-foreground" />
      </button>
      {open && (
        <div className="absolute z-10 mt-1 w-40 bg-white border rounded-md shadow-lg">
          {statuses.map((status) => (
            <button
              key={status.value}
              onClick={() => {
                onSelect(status.value)
                setOpen(false)
              }}
              className={cn(
                'w-full text-left px-3 py-2 text-sm hover:bg-secondary transition-colors',
                status.value === currentStatus && 'bg-secondary'
              )}
            >
              <span className={cn(
                'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold uppercase tracking-wide border',
                status.className
              )}>
                {status.label}
              </span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

// Editable cell component
function EditableCell({ 
  value, 
  onSave,
  type = 'text',
  placeholder = ''
}: { 
  value: string
  onSave: (value: string) => void
  type?: 'text' | 'date'
  placeholder?: string
}) {
  const [editing, setEditing] = useState(false)
  const [tempValue, setTempValue] = useState(value)
  
  const handleSave = () => {
    onSave(tempValue)
    setEditing(false)
  }
  
  const handleCancel = () => {
    setTempValue(value)
    setEditing(false)
  }
  
  if (editing) {
    return (
      <div className="flex items-center gap-1">
        <input
          type={type}
          value={tempValue}
          onChange={(e) => setTempValue(e.target.value)}
          className="w-full px-2 py-1 text-sm border rounded focus:outline-none focus:ring-2 focus:ring-primary/50"
          placeholder={placeholder}
          autoFocus
          onKeyDown={(e) => {
            if (e.key === 'Enter') handleSave()
            if (e.key === 'Escape') handleCancel()
          }}
        />
        <button onClick={handleSave} className="p-1 text-green-600 hover:bg-green-50 rounded">
          <Check className="w-4 h-4" />
        </button>
        <button onClick={handleCancel} className="p-1 text-red-600 hover:bg-red-50 rounded">
          <X className="w-4 h-4" />
        </button>
      </div>
    )
  }
  
  return (
    <div 
      onClick={() => setEditing(true)}
      className="px-2 py-1 text-sm cursor-pointer hover:bg-secondary/50 rounded transition-colors min-h-[32px] flex items-center"
    >
      {value || <span className="text-muted-foreground italic">{placeholder}</span>}
    </div>
  )
}

// Auto-populate confirmation dialog
function AutoPopulateDialog({
  count,
  onConfirm,
  onCancel
}: {
  count: number
  onConfirm: () => void
  onCancel: () => void
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <Card className="w-full max-w-md mx-4">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Wand2 className="w-5 h-5" />
            Auto-popular Plan de Acción
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground mb-4">
            Se crearán <span className="font-bold text-foreground">{count}</span> planes de acción
            basados en las recomendaciones de prioridad ALTA. ¿Continuar?
          </p>
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={onCancel}>Cancelar</Button>
            <Button onClick={onConfirm}>Crear</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// Delete confirmation modal
function DeleteConfirmation({
  onConfirm,
  onCancel
}: {
  onConfirm: () => void
  onCancel: () => void
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <Card className="w-full max-w-md mx-4">
        <CardHeader>
          <CardTitle className="text-red-600">Confirmar eliminación</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground mb-4">
            ¿Estás seguro de que deseas eliminar esta acción? Esta acción no se puede deshacer.
          </p>
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={onCancel}>Cancelar</Button>
            <Button variant="destructive" onClick={onConfirm}>Eliminar</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// New action plan form
function NewActionPlanForm({ 
  evaluationId,
  onSuccess 
}: { 
  evaluationId: string
  onSuccess: () => void
}) {
  const [element, setElement] = useState('')
  const [action, setAction] = useState('')
  const [responsible, setResponsible] = useState('')
  const [dueDate, setDueDate] = useState('')
  const [showForm, setShowForm] = useState(false)
  
  const createActionPlan = useCreateActionPlan()
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!element.trim() || !action.trim()) {
      toast.error('Por favor completa los campos obligatorios')
      return
    }
    
    createActionPlan.mutate({
      evaluation_id: evaluationId,
      element: element.trim(),
      action: action.trim(),
      responsible: responsible.trim(),
      due_date: dueDate || null,
      status: 'pendiente',
    }, {
      onSuccess: () => {
        setElement('')
        setAction('')
        setResponsible('')
        setDueDate('')
        setShowForm(false)
        onSuccess()
      }
    })
  }
  
  if (!showForm) {
    return (
      <Button onClick={() => setShowForm(true)} className="w-full md:w-auto">
        <Plus className="w-4 h-4 mr-1" />
        Nueva Acción
      </Button>
    )
  }
  
  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle className="text-lg">Crear nueva acción</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Elemento *</label>
              <Input
                value={element}
                onChange={(e) => setElement(e.target.value)}
                placeholder="Ej: Análisis del contexto"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Responsable</label>
              <Input
                value={responsible}
                onChange={(e) => setResponsible(e.target.value)}
                placeholder="Nombre del responsable"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Acción *</label>
            <textarea
              value={action}
              onChange={(e) => setAction(e.target.value)}
              placeholder="Descripción de la acción a realizar..."
              className="w-full px-3 py-2 text-sm border rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 min-h-[80px] resize-y"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Fecha Límite</label>
            <Input
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
            />
          </div>
          <div className="flex justify-end gap-2">
            <Button 
              type="button" 
              variant="outline" 
              onClick={() => {
                setShowForm(false)
                setElement('')
                setAction('')
                setResponsible('')
                setDueDate('')
              }}
            >
              Cancelar
            </Button>
            <Button type="submit" disabled={createActionPlan.isPending}>
              {createActionPlan.isPending ? 'Creando...' : 'Crear Acción'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

export function ActionPlanPage() {
  const [searchParams] = useSearchParams()
  const evaluationId = searchParams.get('evaluation_id') || ''
  const queryClient = useQueryClient()
  
  const { data: actionPlans, isLoading } = useActionPlans(evaluationId || undefined)
  const { data: recommendations } = useRecommendations(evaluationId)
  const updateActionPlan = useUpdateActionPlan()
  const deleteActionPlan = useDeleteActionPlan()
  const createActionPlan = useCreateActionPlan()

  const [sortKey, setSortKey] = useState<SortKey>('status')
  const [sortAsc, setSortAsc] = useState(true)
  const [deleteId, setDeleteId] = useState<string | null>(null)
  const [autoPopulateCount, setAutoPopulateCount] = useState<number | null>(null)
  
  // Sort action plans
  const sortedPlans = [...(actionPlans || [])].sort((a, b) => {
    let comparison = 0
    
    if (sortKey === 'status') {
      const statusOrder = { pendiente: 0, en_progreso: 1, completada: 2 }
      comparison = statusOrder[a.status] - statusOrder[b.status]
    } else if (sortKey === 'due_date') {
      if (!a.due_date && !b.due_date) comparison = 0
      if (!a.due_date) comparison = 1
      if (!b.due_date) comparison = -1
      comparison = new Date(a.due_date!).getTime() - new Date(b.due_date!).getTime()
    }
    
    return sortAsc ? comparison : -comparison
  })
  
  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortAsc(!sortAsc)
    } else {
      setSortKey(key)
      setSortAsc(true)
    }
  }
  
  const handleUpdateField = (id: string, field: keyof ActionPlan, value: any) => {
    updateActionPlan.mutate({ id, [field]: value })
  }
  
  const handleDelete = (id: string) => {
    setDeleteId(id)
  }
  
  const confirmDelete = () => {
    if (deleteId) {
      deleteActionPlan.mutate(deleteId)
      setDeleteId(null)
    }
  }

  // Auto-populate from recommendations
  const altaRecommendations = recommendations?.filter(r => r.priority === 'ALTA') || []

  const handleAutoPopulate = () => {
    if (altaRecommendations.length === 0) {
      toast.error('No hay recomendaciones de prioridad ALTA')
      return
    }
    setAutoPopulateCount(altaRecommendations.length)
  }

  const confirmAutoPopulate = () => {
    if (!autoPopulateCount || !evaluationId) return

    altaRecommendations.forEach((rec) => {
      createActionPlan.mutate({
        evaluation_id: evaluationId,
        element: rec.element,
        action: rec.recommendation,
        responsible: '',
        due_date: null,
        status: 'pendiente',
      })
    })

    setAutoPopulateCount(null)
    toast.success(`${altaRecommendations.length} acciones creadas desde recomendaciones`)
    queryClient.invalidateQueries({ queryKey: ['action-plans'] })
  }
  
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-muted-foreground">Cargando planes de acción...</p>
      </div>
    )
  }
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Plan de Acción</h1>
          <p className="text-muted-foreground">
            Gestiona las acciones derivadas de tu evaluación
          </p>
        </div>
        {evaluationId && altaRecommendations.length > 0 && (
          <Button onClick={handleAutoPopulate} variant="outline">
            <Wand2 className="w-4 h-4 mr-2" />
            Auto-popular desde Recomendaciones ({altaRecommendations.length})
          </Button>
        )}
      </div>
      
      {/* New action form */}
      {evaluationId && <NewActionPlanForm evaluationId={evaluationId} onSuccess={() => {}} />}
      
      {/* Sort controls */}
      <div className="flex items-center gap-4">
        <span className="text-sm font-medium text-muted-foreground">Ordenar por:</span>
        <Button 
          size="sm" 
          variant={sortKey === 'status' ? 'default' : 'outline'}
          onClick={() => handleSort('status')}
        >
          Estado {sortKey === 'status' && (sortAsc ? '↑' : '↓')}
        </Button>
        <Button 
          size="sm" 
          variant={sortKey === 'due_date' ? 'default' : 'outline'}
          onClick={() => handleSort('due_date')}
        >
          Fecha Límite {sortKey === 'due_date' && (sortAsc ? '↑' : '↓')}
        </Button>
      </div>
      
      {/* Action plans table */}
      {sortedPlans.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <AlertCircle className="w-12 h-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">
              {evaluationId
                ? 'No hay acciones creadas para esta evaluación.'
                : 'No hay acciones creadas. Selecciona una evaluación para ver sus acciones o crear nuevas.'}
            </p>
            {evaluationId && (
              <p className="text-sm text-muted-foreground mt-2">
                Usa el formulario de arriba para crear tu primera acción.
              </p>
            )}
          </CardContent>
        </Card>
      ) : (
        <Card>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b bg-secondary/50">
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Elemento</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Acción</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Responsable</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Fecha Límite</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Estado</th>
                  <th className="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {sortedPlans.map((plan) => (
                  <tr key={plan.id} className="border-b hover:bg-secondary/30 transition-colors">
                    <td className="py-3 px-4">
                      <EditableCell
                        value={plan.element}
                        onSave={(value) => handleUpdateField(plan.id, 'element', value)}
                        placeholder="Elemento"
                      />
                    </td>
                    <td className="py-3 px-4 max-w-xs">
                      <EditableCell
                        value={plan.action}
                        onSave={(value) => handleUpdateField(plan.id, 'action', value)}
                        placeholder="Descripción de la acción"
                      />
                    </td>
                    <td className="py-3 px-4">
                      <EditableCell
                        value={plan.responsible}
                        onSave={(value) => handleUpdateField(plan.id, 'responsible', value)}
                        placeholder="Responsable"
                      />
                    </td>
                    <td className="py-3 px-4">
                      <EditableCell
                        value={plan.due_date || ''}
                        onSave={(value) => handleUpdateField(plan.id, 'due_date', value || null)}
                        type="date"
                        placeholder="Sin fecha"
                      />
                    </td>
                    <td className="py-3 px-4">
                      <StatusDropdown
                        currentStatus={plan.status}
                        onSelect={(status) => handleUpdateField(plan.id, 'status', status)}
                      />
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => handleDelete(plan.id)}
                        className="p-2 text-red-600 hover:bg-red-50 rounded transition-colors"
                        title="Eliminar"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
      
      {/* Summary */}
      {sortedPlans.length > 0 && (
        <Card>
          <CardContent className="py-4">
            <div className="flex gap-6 text-sm">
              <span className="text-muted-foreground">
                Total: <span className="font-medium text-foreground">{sortedPlans.length}</span> acciones
              </span>
              <span className="text-muted-foreground">
                Pendientes: <span className="font-medium text-red-600">
                  {sortedPlans.filter(p => p.status === 'pendiente').length}
                </span>
              </span>
              <span className="text-muted-foreground">
                En Progreso: <span className="font-medium text-yellow-600">
                  {sortedPlans.filter(p => p.status === 'en_progreso').length}
                </span>
              </span>
              <span className="text-muted-foreground">
                Completadas: <span className="font-medium text-green-600">
                  {sortedPlans.filter(p => p.status === 'completada').length}
                </span>
              </span>
            </div>
          </CardContent>
        </Card>
      )}
      
      {/* Delete confirmation modal */}
      {deleteId && (
        <DeleteConfirmation
          onConfirm={confirmDelete}
          onCancel={() => setDeleteId(null)}
        />
      )}

      {/* Auto-populate confirmation dialog */}
      {autoPopulateCount !== null && (
        <AutoPopulateDialog
          count={autoPopulateCount}
          onConfirm={confirmAutoPopulate}
          onCancel={() => setAutoPopulateCount(null)}
        />
      )}
    </div>
  )
}
