import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { toast } from '@/lib/toast'

export interface Schedule {
  id: string
  name: string
  frequency: 'monthly' | 'quarterly' | 'biannual' | 'annual'
  next_due: string
  reminder_days_before: number
  active: boolean
  created_by: string
  created_at: string
  updated_at: string
}

export function useSchedules() {
  return useQuery({
    queryKey: ['schedules'],
    queryFn: async () => {
      const response = await api.get('/schedules')
      return response.data as Schedule[]
    },
  })
}

export function useSchedule(id: string) {
  return useQuery({
    queryKey: ['schedules', id],
    queryFn: async () => {
      const response = await api.get(`/schedules/${id}`)
      return response.data as Schedule
    },
    enabled: !!id,
  })
}

export function useCreateSchedule() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (data: {
      name: string
      frequency: Schedule['frequency']
      next_due: string
      reminder_days_before?: number
      active?: boolean
    }) => {
      const response = await api.post('/schedules', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
      toast.success('Programación creada correctamente')
    },
    onError: () => {
      toast.error('Error al crear la programación')
    },
  })
}

export function useUpdateSchedule() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async ({ id, ...data }: { id: string } & Partial<Schedule>) => {
      const response = await api.put(`/schedules/${id}`, data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
      toast.success('Programación actualizada')
    },
    onError: () => {
      toast.error('Error al actualizar la programación')
    },
  })
}

export function useDeleteSchedule() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/schedules/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
      toast.success('Programación eliminada')
    },
    onError: () => {
      toast.error('Error al eliminar la programación')
    },
  })
}

export function useTriggerSchedule() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (id: string) => {
      const response = await api.post(`/schedules/${id}/trigger`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schedules'] })
      toast.success('Recordatorio enviado')
    },
    onError: () => {
      toast.error('Error al enviar el recordatorio')
    },
  })
}