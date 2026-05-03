import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { Input } from '@/components/ui/Input'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { formatDate, getScoreColor, cn } from '@/lib/utils'
import { Skeleton } from '@/components/shared/Skeleton'
import { 
  Search, 
  Download, 
  Eye, 
  Trash2, 
  ChevronLeft, 
  ChevronRight,
  Calendar,
  X,
  Filter
} from 'lucide-react'

// Types
interface Evaluation {
  id: string
  user_id: string
  fecha: string
  general_pct: number
  pa_pct: number
  po_pct: number
  establishment_name?: string
}

interface DeleteDialogProps {
  isOpen: boolean
  evaluation: Evaluation | null
  onConfirm: () => void
  onCancel: () => void
}

function DeleteConfirmationDialog({ isOpen, evaluation, onConfirm, onCancel }: DeleteDialogProps) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-background rounded-lg p-6 max-w-sm w-full mx-4 shadow-xl">
        <h3 className="text-lg font-semibold text-foreground mb-2">Confirmar eliminación</h3>
        <p className="text-muted-foreground mb-4">
          ¿Estás seguro de que deseas eliminar la evaluación del{' '}
          <span className="font-medium">{evaluation ? formatDate(evaluation.fecha) : ''}</span>?
          Esta acción no se puede deshacer.
        </p>
        <div className="flex gap-3 justify-end">
          <Button variant="outline" onClick={onCancel}>
            Cancelar
          </Button>
          <Button variant="destructive" onClick={onConfirm}>
            Eliminar
          </Button>
        </div>
      </div>
    </div>
  )
}

const ITEMS_PER_PAGE = 10

export function HistoryPage() {
  const queryClient = useQueryClient()

  // Fetch all evaluations
  const { data: evaluations, isLoading } = useQuery({
    queryKey: ['evaluations'],
    queryFn: async () => {
      const response = await api.get('/evaluations')
      return (response.data as Evaluation[]) || []
    },
  })

  // Filter state
  const [searchQuery, setSearchQuery] = useState('')
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')
  const [sortOrder, setSortOrder] = useState<'desc' | 'asc'>('desc')
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1)

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: async (evaluationId: string) => {
      await api.delete(`/evaluations/${evaluationId}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['evaluations'] })
    },
  })

  // Delete dialog state
  const [deleteDialog, setDeleteDialog] = useState<{
    isOpen: boolean
    evaluation: Evaluation | null
  }>({
    isOpen: false,
    evaluation: null,
  })

  // Calculate active filters count
  const activeFiltersCount = useMemo(() => {
    let count = 0
    if (searchQuery.trim()) count++
    if (dateFrom) count++
    if (dateTo) count++
    return count
  }, [searchQuery, dateFrom, dateTo])

  // Clear all filters
  const clearFilters = () => {
    setSearchQuery('')
    setDateFrom('')
    setDateTo('')
    setCurrentPage(1)
  }

  // Toggle sort order
  const toggleSort = () => {
    setSortOrder(prev => prev === 'desc' ? 'asc' : 'desc')
  }

  // Filter and sort evaluations
  const filteredEvaluations = useMemo(() => {
    if (!evaluations) return []

    let filtered = [...evaluations]

    // Search filter (establishment name or date)
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(evaluation => {
        const establishmentMatch = evaluation.establishment_name?.toLowerCase().includes(query)
        const dateMatch = formatDate(evaluation.fecha).toLowerCase().includes(query)
        return establishmentMatch || dateMatch
      })
    }

    // Date range filter
    if (dateFrom) {
      const fromDate = new Date(dateFrom)
      filtered = filtered.filter(evaluation => new Date(evaluation.fecha) >= fromDate)
    }

    if (dateTo) {
      const toDate = new Date(dateTo)
      toDate.setHours(23, 59, 59, 999) // End of day
      filtered = filtered.filter(evaluation => new Date(evaluation.fecha) <= toDate)
    }

    // Sort by date
    filtered.sort((a, b) => {
      const dateA = new Date(a.fecha).getTime()
      const dateB = new Date(b.fecha).getTime()
      return sortOrder === 'desc' ? dateB - dateA : dateA - dateB
    })

    return filtered
  }, [evaluations, searchQuery, dateFrom, dateTo, sortOrder])

  // Pagination
  const totalPages = Math.ceil((filteredEvaluations?.length || 0) / ITEMS_PER_PAGE)
  const paginatedEvaluations = filteredEvaluations?.slice(
    (currentPage - 1) * ITEMS_PER_PAGE,
    currentPage * ITEMS_PER_PAGE
  )

  // Handle page change
  const goToPage = (page: number) => {
    setCurrentPage(Math.max(1, Math.min(page, totalPages)))
  }

  // Handle delete
  const handleDelete = (evaluation: Evaluation) => {
    setDeleteDialog({ isOpen: true, evaluation })
  }

  const confirmDelete = () => {
    if (deleteDialog.evaluation) {
      deleteMutation.mutate(deleteDialog.evaluation.id)
      setDeleteDialog({ isOpen: false, evaluation: null })
    }
  }

  const cancelDelete = () => {
    setDeleteDialog({ isOpen: false, evaluation: null })
  }

  // Handle CSV export
  const handleExportCSV = () => {
    const csvRows = [
      ['Fecha', 'Establecimiento', 'Cumplimiento General %', 'PA %', 'PO %'],
      ...filteredEvaluations.map(e => [
        formatDate(e.fecha),
        e.establishment_name || '',
        e.general_pct?.toFixed(1) || '0',
        e.pa_pct?.toFixed(1) || '0',
        e.po_pct?.toFixed(1) || '0',
      ])
    ].map(row => row.join(',')).join('\n')

    const blob = new Blob([csvRows], { type: 'text/csv;charset=utf-8;' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `GPP_History_${new Date().toISOString().split('T')[0]}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  }

  // Get score badge variant
  const getBadgeVariant = (pct: number): 'success' | 'warning' | 'error' => {
    if (pct >= 75) return 'success'
    if (pct >= 60) return 'warning'
    return 'error'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Historial de Evaluaciones</h1>
          <p className="text-muted-foreground">
            {isLoading ? 'Cargando...' : `${filteredEvaluations?.length || 0} evaluaciones`}
          </p>
        </div>
        <Button
          variant="outline"
          onClick={handleExportCSV}
          disabled={!evaluations || evaluations.length === 0}
        >
          <Download className="w-4 h-4 mr-2" />
          Exportar CSV
        </Button>
      </div>

      {/* Filters Card */}
      <Card>
        <CardContent className="pt-6">
          <div className="space-y-4">
            {/* Search Row */}
            <div className="flex items-center gap-4 flex-wrap">
              <div className="relative flex-1 min-w-[200px]">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="Buscar por establecimiento o fecha..."
                  value={searchQuery}
                  onChange={(e) => {
                    setSearchQuery(e.target.value)
                    setCurrentPage(1)
                  }}
                  className="pl-10"
                />
              </div>
              
              {/* Sort Toggle */}
              <Button variant="outline" onClick={toggleSort}>
                <Calendar className="w-4 h-4 mr-2" />
                {sortOrder === 'desc' ? 'Más reciente' : 'Más antigua'}
              </Button>

              {/* Clear Filters */}
              {activeFiltersCount > 0 && (
                <Button variant="ghost" onClick={clearFilters}>
                  <X className="w-4 h-4 mr-2" />
                  Limpiar ({activeFiltersCount})
                </Button>
              )}
            </div>

            {/* Date Range Row */}
            <div className="flex items-center gap-4 flex-wrap">
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">Desde:</span>
                <Input
                  type="date"
                  value={dateFrom}
                  onChange={(e) => {
                    setDateFrom(e.target.value)
                    setCurrentPage(1)
                  }}
                  className="w-auto"
                />
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">Hasta:</span>
                <Input
                  type="date"
                  value={dateTo}
                  onChange={(e) => {
                    setDateTo(e.target.value)
                    setCurrentPage(1)
                  }}
                  className="w-auto"
                />
              </div>

              {/* Active filters indicator */}
              {activeFiltersCount > 0 && (
                <Badge variant="default" className="flex items-center gap-1">
                  <Filter className="w-3 h-3" />
                  {activeFiltersCount} filtro{activeFiltersCount > 1 ? 's' : ''} activo{activeFiltersCount > 1 ? 's' : ''}
                </Badge>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Evaluations Table */}
      <Card>
        <CardContent className="p-0">
          {isLoading ? (
            <div className="p-6 space-y-4">
              <Skeleton className="h-12 w-full" />
              <Skeleton className="h-12 w-full" />
              <Skeleton className="h-12 w-full" />
            </div>
          ) : paginatedEvaluations && paginatedEvaluations.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b bg-secondary/50">
                    <th className="text-left p-4 font-semibold text-foreground">Fecha</th>
                    <th className="text-left p-4 font-semibold text-foreground">Establecimiento</th>
                    <th className="text-center p-4 font-semibold text-foreground">Cumplimiento General</th>
                    <th className="text-center p-4 font-semibold text-foreground">PA %</th>
                    <th className="text-center p-4 font-semibold text-foreground">PO %</th>
                    <th className="text-right p-4 font-semibold text-foreground">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {paginatedEvaluations.map((evaluation) => (
                    <tr key={evaluation.id} className="border-b hover:bg-secondary/30 transition-colors">
                      <td className="p-4">
                        <span className="font-medium">{formatDate(evaluation.fecha)}</span>
                      </td>
                      <td className="p-4 text-muted-foreground">
                        {evaluation.establishment_name || '-'}
                      </td>
                      <td className="p-4 text-center">
                        <Badge variant={getBadgeVariant(evaluation.general_pct)}>
                          {evaluation.general_pct?.toFixed(0) || 0}%
                        </Badge>
                      </td>
                      <td className="p-4 text-center">
                        <span className={cn('font-semibold', getScoreColor(evaluation.pa_pct))}>
                          {evaluation.pa_pct?.toFixed(0) || 0}%
                        </span>
                      </td>
                      <td className="p-4 text-center">
                        <span className={cn('font-semibold', getScoreColor(evaluation.po_pct))}>
                          {evaluation.po_pct?.toFixed(0) || 0}%
                        </span>
                      </td>
                      <td className="p-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <Link to={`/results?id=${evaluation.id}`}>
                            <Button variant="ghost" size="icon" title="Ver detalles">
                              <Eye className="w-4 h-4" />
                            </Button>
                          </Link>
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleDelete(evaluation)}
                            title="Eliminar"
                            className="text-error hover:text-error"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-12">
              <Calendar className="w-12 h-12 text-muted-foreground mb-4" />
              <p className="text-muted-foreground mb-2">
                {activeFiltersCount > 0
                  ? 'No se encontraron evaluaciones con los filtros aplicados'
                  : 'No hay evaluaciones registradas'}
              </p>
              {activeFiltersCount > 0 && (
                <Button variant="outline" onClick={clearFilters}>
                  Limpiar filtros
                </Button>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Pagination */}
      {totalPages > 1 && (
        <Card>
          <CardContent className="py-4">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <p className="text-sm text-muted-foreground">
                Mostrando {((currentPage - 1) * ITEMS_PER_PAGE) + 1} - {Math.min(currentPage * ITEMS_PER_PAGE, filteredEvaluations?.length || 0)} de {filteredEvaluations?.length || 0}
              </p>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => goToPage(currentPage - 1)}
                  disabled={currentPage === 1}
                >
                  <ChevronLeft className="w-4 h-4" />
                </Button>
                <span className="text-sm font-medium">
                  Página {currentPage} de {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => goToPage(currentPage + 1)}
                  disabled={currentPage === totalPages}
                >
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Delete Confirmation Dialog */}
      <DeleteConfirmationDialog
        isOpen={deleteDialog.isOpen}
        evaluation={deleteDialog.evaluation}
        onConfirm={confirmDelete}
        onCancel={cancelDelete}
      />
    </div>
  )
}