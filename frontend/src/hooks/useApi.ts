import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { toast } from '@/lib/toast'

interface Evaluation {
  id: string
  fecha: string
  general_pct: number
  pa_pct: number
  po_pct: number
  evaluaciones_pa?: any
  evaluaciones_po?: any
  pa_breakdown?: Record<string, number>
  po_breakdown?: Record<string, number>
}

interface ActionPlan {
  id: string
  evaluation_id: string
  element: string
  action: string
  responsible: string
  due_date: string | null
  status: 'pendiente' | 'en_progreso' | 'completada'
}

export function useMatrices() {
  return useQuery({
    queryKey: ['matrices'],
    queryFn: async () => {
      const response = await api.get('/matrices')
      return response.data
    },
  })
}

export function useCalculateResults() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (data: { evals_pa: any, evals_po: any }) => {
      const response = await api.post('/results/calculate', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['evaluations'] })
    },
  })
}

export function useEvaluations() {
  return useQuery({
    queryKey: ['evaluations'],
    queryFn: async () => {
      const response = await api.get('/evaluations')
      return response.data as Evaluation[]
    },
  })
}

export function useEvaluation(id: string) {
  return useQuery({
    queryKey: ['evaluations', id],
    queryFn: async () => {
      const response = await api.get(`/evaluations/${id}`)
      return response.data as Evaluation
    },
    enabled: !!id,
  })
}

export function useCreateEvaluation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (data: Partial<Evaluation>) => {
      const response = await api.post('/evaluations', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['evaluations'] })
    },
  })
}

export function useUpdateEvaluation() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async ({ id, ...data }: { id: string } & Partial<Evaluation>) => {
      const response = await api.put(`/evaluations/${id}`, data)
      return response.data
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['evaluations'] })
      queryClient.invalidateQueries({ queryKey: ['evaluation', variables.id] })
    },
  })
}

export function useActionPlans(evaluationId?: string) {
  return useQuery({
    queryKey: ['action-plans', evaluationId],
    queryFn: async () => {
      const params = evaluationId ? { evaluation_id: evaluationId } : {}
      const response = await api.get('/action-plans', { params })
      return response.data as ActionPlan[]
    },
  })
}

export interface Recommendation {
  aspect: string
  element: string
  recommendation: string
  priority: 'ALTA' | 'MEDIA' | 'BAJA'
  current_score?: number
}

export function useRecommendations(evaluationId: string) {
  return useQuery({
    queryKey: ['recommendations', evaluationId],
    queryFn: async () => {
      const response = await api.get(`/recommendations?evaluation_id=${evaluationId}`)
      return response.data as Recommendation[]
    },
    enabled: !!evaluationId,
  })
}

export function useCreateActionPlan() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (data: Partial<ActionPlan>) => {
      const response = await api.post('/action-plans', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['action-plans'] })
      toast.success('Acción creada correctamente')
    },
  })
}

export function useUpdateActionPlan() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async ({ id, ...data }: { id: string } & Partial<ActionPlan>) => {
      const response = await api.put(`/action-plans/${id}`, data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['action-plans'] })
    },
  })
}

export function useDeleteActionPlan() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/action-plans/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['action-plans'] })
      toast.success('Acción eliminada')
    },
  })
}

// Profile hooks
export function useUpdateProfile() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: async (data: { full_name: string; establishment_name: string }) => {
      const response = await api.patch('/profiles/me', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profiles'] })
      toast.success('Perfil actualizado')
    },
  })
}