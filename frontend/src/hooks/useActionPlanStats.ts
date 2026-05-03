import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'

interface ActionPlanStats {
  pending: number
  overdue: number
  due_this_week: number
}

export function useActionPlanStats() {
  return useQuery<ActionPlanStats>({
    queryKey: ['action-plan-stats'],
    queryFn: async () => {
      // Fetch pending count
      const pendingRes = await api.get('/action-plans', {
        params: { status: 'pendiente' }
      })

      // Fetch overdue count
      const overdueRes = await api.get('/action-plans', {
        params: { overdue: true }
      })

      // Fetch due this week count
      const dueThisWeekRes = await api.get('/action-plans', {
        params: { due_this_week: true }
      })

      return {
        pending: pendingRes.data?.length || 0,
        overdue: overdueRes.data?.length || 0,
        due_this_week: dueThisWeekRes.data?.length || 0,
      }
    },
    staleTime: 1000 * 60 * 2, // 2 minutes
    refetchInterval: 1000 * 60 * 5, // Refetch every 5 minutes
  })
}