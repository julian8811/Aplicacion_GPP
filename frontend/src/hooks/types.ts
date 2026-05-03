export interface User {
  id: string
  email: string
  full_name?: string
  role: 'owner' | 'viewer'
  establishment_name?: string
}

export interface Evaluation {
  id: string
  user_id: string
  fecha: string
  general_pct: number
  pa_pct: number
  po_pct: number
  evaluaciones_pa: Record<string, Record<string, number>>
  evaluaciones_po: Record<string, Record<string, number>>
  action_plans?: ActionPlan[]
}

export interface ActionPlan {
  id: string
  evaluation_id: string
  element: string
  action: string
  responsible?: string
  due_date?: string
  status: 'pendiente' | 'en_progreso' | 'completada'
}