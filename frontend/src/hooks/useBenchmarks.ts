import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'

export interface Benchmark {
  id: string
  sector: string
  category: 'PA' | 'PO'
  aspect: string
  avg_score: number
  p25: number
  p75: number
  sample_size: number
  source: string
  created_at: string
}

export function useBenchmarks(sector?: string, category?: 'PA' | 'PO') {
  return useQuery({
    queryKey: ['benchmarks', sector, category],
    queryFn: async () => {
      const params = new URLSearchParams()
      if (sector) params.append('sector', sector)
      if (category) params.append('category', category)
      
      const response = await api.get(`/benchmarks?${params.toString()}`)
      return response.data as Benchmark[]
    },
  })
}

export function useBenchmarkSectors() {
  return useQuery({
    queryKey: ['benchmarks', 'sectors'],
    queryFn: async () => {
      const response = await api.get('/benchmarks/sectors/list')
      return response.data as { sector: string }[]
    },
  })
}