import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { toast } from '@/lib/toast'

export interface Template {
  id: string
  name: string
  description?: string
  pa_config: {
    selected_aspects: string[]
    questions: Record<string, Record<string, number>>
  }
  po_config: {
    selected_aspects: string[]
    questions: Record<string, Record<string, number>>
  }
  is_public: boolean
  created_by: string
  created_at: string
  updated_at: string
}

export function useTemplates() {
  return useQuery({
    queryKey: ['templates'],
    queryFn: async () => {
      const response = await api.get('/templates')
      return response.data as Template[]
    },
  })
}

export function useTemplate(id: string) {
  return useQuery({
    queryKey: ['templates', id],
    queryFn: async () => {
      const response = await api.get(`/templates/${id}`)
      return response.data as Template
    },
    enabled: !!id,
  })
}

export function useCreateTemplate() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (data: {
      name: string
      description?: string
      pa_config?: Template['pa_config']
      po_config?: Template['po_config']
      is_public?: boolean
    }) => {
      const response = await api.post('/templates', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['templates'] })
      toast.success('Plantilla creada correctamente')
    },
  })
}

export function useUpdateTemplate() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async ({ id, ...data }: { id: string } & Partial<Template>) => {
      const response = await api.put(`/templates/${id}`, data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['templates'] })
      toast.success('Plantilla actualizada')
    },
  })
}

export function useDeleteTemplate() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/templates/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['templates'] })
      toast.success('Plantilla eliminada')
    },
  })
}

export function useCreateTemplateFromEvaluation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (data: {
      evaluation_id: string
      name: string
      description?: string
    }) => {
      const response = await api.post(`/templates/from-evaluation/${data.evaluation_id}`, {
        name: data.name,
        description: data.description || '',
      })
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['templates'] })
      toast.success('Plantilla creada desde evaluación')
    },
  })
}