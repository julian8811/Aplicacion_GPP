import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'

export interface Evaluation {
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

export interface ComparisonResult {
  evaluation_a: Evaluation
  evaluation_b: Evaluation
  pa_comparison: Array<{
    aspect: string
    eval_a_value: number
    eval_b_value: number
    delta: number
    delta_pct: number
  }>
  po_comparison: Array<{
    aspect: string
    eval_a_value: number
    eval_b_value: number
    delta: number
    delta_pct: number
  }>
  overall: {
    eval_a: {
      id: string
      fecha: string
      general_pct: number
      pa_pct: number
      po_pct: number
    }
    eval_b: {
      id: string
      fecha: string
      general_pct: number
      pa_pct: number
      po_pct: number
    }
    delta: {
      general_pct: number
      pa_pct: number
      po_pct: number
    }
  }
}

export function useComparison(evalAId: string, evalBId: string) {
  return useQuery({
    queryKey: ['comparison', evalAId, evalBId],
    queryFn: async () => {
      const response = await api.get(`/comparison/${evalAId}/${evalBId}`)
      return response.data as ComparisonResult
    },
    enabled: !!evalAId && !!evalBId,
  })
}