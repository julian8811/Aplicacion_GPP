import { useNavigate } from 'react-router-dom'

export function EvaluationPage() {
  const navigate = useNavigate()

  // Redirect to NewEvaluationPage for creating new evaluations
  const handleNewEvaluation = () => {
    navigate('/evaluations/new')
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-foreground">Nueva Evaluación</h1>
      <p className="text-muted-foreground">Evaluation wizard coming soon...</p>
      <button
        onClick={handleNewEvaluation}
        className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
      >
        Crear Nueva Evaluación
      </button>
    </div>
  )
}

export function EvaluationDetailPage({ id }: { id: string }) {
  const navigate = useNavigate()

  const handleViewResults = () => {
    navigate(`/results/${id}`)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-foreground">Detalle de Evaluación</h1>
      <p className="text-muted-foreground">ID: {id}</p>
      <button
        onClick={handleViewResults}
        className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
      >
        Ver Resultados
      </button>
    </div>
  )
}