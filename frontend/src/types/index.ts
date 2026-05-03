/**
 * Centralized shared TypeScript types for GPP frontend.
 * All shared types should be imported from this file.
 */

// User types
export interface User {
  id: string
  email: string
  full_name?: string
  role: Role
  establishment_name?: string
}

export type Role = 'owner' | 'admin' | 'editor' | 'viewer'

// Evaluation types
export interface Evaluation {
  id: string
  user_id: string
  fecha: string
  general_pct: number
  pa_pct: number
  po_pct: number
  evaluaciones_pa: Record<string, Record<string, number>>
  evaluaciones_po: Record<string, Record<string, number>>
  owner_id?: string
  establishment_name?: string
  action_plans?: ActionPlan[]
}

// Action Plan types
export interface ActionPlan {
  id: string
  evaluation_id: string
  element: string
  action: string
  responsible?: string
  due_date?: string
  status: ActionPlanStatus
  reminder_sent?: boolean
  owner_id?: string
  created_at?: string
  updated_at?: string
}

export type ActionPlanStatus = 'pendiente' | 'en_progreso' | 'completada'

// Template types
export interface Template {
  id: string
  name: string
  description?: string
  pa_config: TemplateConfig
  po_config: TemplateConfig
  is_public: boolean
  created_by: string
  created_at: string
  updated_at: string
}

export interface TemplateConfig {
  selected_aspects: string[]
  questions: Record<string, Record<string, number>>
}

// Benchmark types
export interface Benchmark {
  id: string
  sector: string
  category: 'PA' | 'PO'
  aspect: string
  avg_score: number
  sample_size: number
  source: string
}

// Schedule types
export interface EvaluationSchedule {
  id: string
  name: string
  frequency: 'monthly' | 'quarterly' | 'biannual' | 'annual'
  next_due: string
  reminder_days_before: number
  active: boolean
  created_by: string
  created_at: string
}

// Notification types
export interface NotificationPreferences {
  action_plan_reminders: boolean
  weekly_summary: boolean
  marketing: boolean
}

// Branding types
export interface BrandingSettings {
  logo_url: string | null
  primary_color: string
  footer_text?: string
}

// Auth types
export interface AuthSession {
  access_token: string
  refresh_token: string
  user: User
}

// API Response types
export interface ApiError {
  error: string
  message: string
  status_code?: number
}