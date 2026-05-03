import { Routes, Route, Navigate } from 'react-router-dom'
import { AppShell } from '@/components/layout/AppShell'
import { DashboardPage } from '@/pages/DashboardPage'
import { EvaluationPage } from '@/pages/EvaluationPage'
import { EvaluationWizardPage } from '@/pages/EvaluationWizardPage'
import { PAEvaluationPage } from '@/pages/PAEvaluationPage'
import { POEvaluationPage } from '@/pages/POEvaluationPage'
import { ResultsPage } from '@/pages/ResultsPage'
import { ActionPlanPage } from '@/pages/ActionPlanPage'
import { RecommendationsPage } from '@/pages/RecommendationsPage'
import { HistoryPage } from '@/pages/HistoryPage'
import { BenchmarkingPage } from '@/pages/BenchmarkingPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { NewEvaluationPage } from '@/pages/NewEvaluationPage'
import { TemplatesPage } from '@/pages/TemplatesPage'
import { ComparisonPage } from '@/pages/ComparisonPage'
import { ExportPage } from '@/pages/admin/ExportPage'
import { LoginPage } from '@/pages/auth/LoginPage'
import { SignupPage } from '@/pages/auth/SignupPage'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import { Toaster } from 'sonner'
import { ErrorBoundary } from '@/components/shared/ErrorBoundary'

export default function App() {
  return (
    <>
      <Toaster position="top-right" richColors />
      <ErrorBoundary>
        <Routes>
          {/* Public auth routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />

          {/* Protected routes wrapped in AppShell */}
          <Route element={<ProtectedRoute><AppShell /></ProtectedRoute>}>
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="evaluate" element={<NewEvaluationPage />} />
            <Route path="evaluate/wizard" element={<EvaluationWizardPage />} />
            <Route path="evaluate/pa" element={<PAEvaluationPage />} />
            <Route path="evaluate/po" element={<POEvaluationPage />} />
            <Route path="evaluate/:id" element={<EvaluationPage />} />
            <Route path="results" element={<ResultsPage />} />
            <Route path="results/:id" element={<ResultsPage />} />
            <Route path="action-plans" element={<ActionPlanPage />} />
            <Route path="recommendations" element={<RecommendationsPage />} />
            <Route path="history" element={<HistoryPage />} />
            <Route path="benchmarking" element={<BenchmarkingPage />} />
            <Route path="templates" element={<TemplatesPage />} />
            <Route path="compare" element={<ComparisonPage />} />
            <Route path="settings" element={<SettingsPage />} />
            <Route path="admin/export" element={<ExportPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/dashboard" />} />
        </Routes>
      </ErrorBoundary>
    </>
  )
}