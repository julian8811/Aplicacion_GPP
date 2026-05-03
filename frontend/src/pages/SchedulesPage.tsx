import { useState } from 'react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { Switch } from '@/components/ui/Switch'
import { useSchedules, useCreateSchedule, useUpdateSchedule, useDeleteSchedule, useTriggerSchedule, Schedule } from '@/hooks/useSchedules'
import { Skeleton } from '@/components/shared/Skeleton'
import { formatDate } from '@/lib/utils'
import { Plus, Calendar, Trash2, Play, Edit2 } from 'lucide-react'
import { toast } from '@/lib/toast'

const frequencyLabels: Record<Schedule['frequency'], string> = {
  monthly: 'Mensual',
  quarterly: 'Trimestral',
  biannual: 'Semestral',
  annual: 'Anual',
}

const frequencyOptions: { value: Schedule['frequency']; label: string }[] = [
  { value: 'monthly', label: 'Mensual' },
  { value: 'quarterly', label: 'Trimestral' },
  { value: 'biannual', label: 'Semestral' },
  { value: 'annual', label: 'Anual' },
]

function ScheduleForm({
  schedule,
  onSave,
  onCancel,
}: {
  schedule?: Schedule
  onSave: (data: { name: string; frequency: Schedule['frequency']; next_due: string; reminder_days_before: number }) => void
  onCancel: () => void
}) {
  const [name, setName] = useState(schedule?.name || '')
  const [frequency, setFrequency] = useState<Schedule['frequency']>(schedule?.frequency || 'quarterly')
  const [nextDue, setNextDue] = useState(
    schedule?.next_due ? new Date(schedule.next_due).toISOString().slice(0, 16) : ''
  )
  const [reminderDays, setReminderDays] = useState(schedule?.reminder_days_before || 7)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim() || !nextDue) {
      toast.error('Completa todos los campos')
      return
    }
    onSave({
      name,
      frequency,
      next_due: new Date(nextDue).toISOString(),
      reminder_days_before: reminderDays,
    })
  }

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle className="text-lg">{schedule ? 'Editar Programación' : 'Nueva Programación'}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              Nombre
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="ej. Evaluación trimestral"
              className="w-full px-3 py-2 border border-border rounded-lg bg-background text-foreground"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              Frecuencia
            </label>
            <select
              value={frequency}
              onChange={(e) => setFrequency(e.target.value as Schedule['frequency'])}
              className="w-full px-3 py-2 border border-border rounded-lg bg-background text-foreground"
            >
              {frequencyOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              Próxima fecha
            </label>
            <input
              type="datetime-local"
              value={nextDue}
              onChange={(e) => setNextDue(e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-lg bg-background text-foreground"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">
              Recordar antes (días)
            </label>
            <input
              type="number"
              value={reminderDays}
              onChange={(e) => setReminderDays(parseInt(e.target.value) || 7)}
              min={1}
              max={30}
              className="w-full px-3 py-2 border border-border rounded-lg bg-background text-foreground"
            />
          </div>

          <div className="flex gap-2 justify-end">
            <Button type="button" variant="outline" onClick={onCancel}>
              Cancelar
            </Button>
            <Button type="submit">
              {schedule ? 'Guardar' : 'Crear'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

function ScheduleCard({
  schedule,
  onEdit,
  onDelete,
  onTrigger,
  onToggleActive,
}: {
  schedule: Schedule
  onEdit: () => void
  onDelete: () => void
  onTrigger: () => void
  onToggleActive: (active: boolean) => void
}) {
  const isOverdue = new Date(schedule.next_due) < new Date()

  return (
    <Card className={!schedule.active ? 'opacity-60' : ''}>
      <CardContent className="pt-6">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="font-semibold text-foreground">{schedule.name}</h3>
              <Badge variant={schedule.active ? 'default' : 'secondary'}>
                {schedule.active ? 'Activo' : 'Inactivo'}
              </Badge>
              {isOverdue && schedule.active && (
                <Badge variant="error">Atrasado</Badge>
              )}
            </div>

            <div className="space-y-1 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                <span>
                  {frequencyLabels[schedule.frequency]} •{' '}
                  {formatDate(schedule.next_due)}
                </span>
              </div>
              <div>
                Recordatorio: {schedule.reminder_days_before} días antes
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Switch
              checked={schedule.active}
              onCheckedChange={onToggleActive}
            />
            <Button
              variant="ghost"
              size="sm"
              onClick={onTrigger}
              disabled={!schedule.active}
              title="Enviar recordatorio ahora"
            >
              <Play className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={onEdit}
              title="Editar"
            >
              <Edit2 className="w-4 h-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={onDelete}
              title="Eliminar"
              className="text-error hover:text-error"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export function SchedulesPage() {
  const { data: schedules, isLoading } = useSchedules()
  const createSchedule = useCreateSchedule()
  const updateSchedule = useUpdateSchedule()
  const deleteSchedule = useDeleteSchedule()
  const triggerSchedule = useTriggerSchedule()

  const [showForm, setShowForm] = useState(false)
  const [editingSchedule, setEditingSchedule] = useState<Schedule | null>(null)

  const handleCreate = (data: { name: string; frequency: Schedule['frequency']; next_due: string; reminder_days_before: number }) => {
    createSchedule.mutate(data, {
      onSuccess: () => {
        setShowForm(false)
      },
    })
  }

  const handleEdit = (data: { name: string; frequency: Schedule['frequency']; next_due: string; reminder_days_before: number }) => {
    if (!editingSchedule) return
    updateSchedule.mutate(
      { id: editingSchedule.id, ...data },
      {
        onSuccess: () => {
          setEditingSchedule(null)
        },
      }
    )
  }

  const handleDelete = (schedule: Schedule) => {
    if (confirm(`¿Eliminar "${schedule.name}"?`)) {
      deleteSchedule.mutate(schedule.id)
    }
  }

  const handleTrigger = (schedule: Schedule) => {
    triggerSchedule.mutate(schedule.id)
  }

  const handleToggleActive = (schedule: Schedule, active: boolean) => {
    updateSchedule.mutate({ id: schedule.id, active })
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-12 w-64" />
        <div className="grid gap-4">
          {[1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-32 w-full" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Programación de Evaluaciones</h1>
          <p className="text-muted-foreground">
            Configura recordatorios automáticos para tus evaluaciones periódicas
          </p>
        </div>
        {!showForm && !editingSchedule && (
          <Button onClick={() => setShowForm(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Nueva Programación
          </Button>
        )}
      </div>

      {(showForm || editingSchedule) && (
        <ScheduleForm
          schedule={editingSchedule || undefined}
          onSave={editingSchedule ? handleEdit : handleCreate}
          onCancel={() => {
            setShowForm(false)
            setEditingSchedule(null)
          }}
        />
      )}

      {!schedules || schedules.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Calendar className="w-12 h-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground text-center">
              No hay programaciones configuradas.
              <br />
              Crea una para recibir recordatorios automáticos.
            </p>
            {!showForm && (
              <Button className="mt-4" onClick={() => setShowForm(true)}>
                <Plus className="w-4 h-4 mr-2" />
                Crear Programación
              </Button>
            )}
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4">
          {schedules.map((schedule) => (
            <ScheduleCard
              key={schedule.id}
              schedule={schedule}
              onEdit={() => setEditingSchedule(schedule)}
              onDelete={() => handleDelete(schedule)}
              onTrigger={() => handleTrigger(schedule)}
              onToggleActive={(active) => handleToggleActive(schedule, active)}
            />
          ))}
        </div>
      )}
    </div>
  )
}