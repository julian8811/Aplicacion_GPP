import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { ExportButton } from '@/components/admin/ExportButton'
import { AlertTriangle } from 'lucide-react'
import api from '@/lib/api'
import { ShieldAlert } from 'lucide-react'
import { Skeleton } from '@/components/shared/Skeleton'

export function ExportPage() {
  const { data: profile, isLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: async () => {
      const response = await api.get('/profiles/me')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-12 w-64" />
        <Skeleton className="h-48" />
      </div>
    )
  }

  if (profile?.role !== 'admin') {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-foreground">Exportar Datos</h1>
          <p className="text-muted-foreground">
            Descarga una copia completa de seguridad de todos tus datos
          </p>
        </div>
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <ShieldAlert className="w-12 h-12 text-error mb-4" />
            <p className="text-center text-foreground font-medium">
              Acceso denegado
            </p>
            <p className="text-center text-muted-foreground text-sm mt-2">
              Solo los administradores pueden realizar backups completos.
            </p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">Exportar Datos</h1>
        <p className="text-muted-foreground">
          Descarga una copia completa de seguridad de todos tus datos
        </p>
      </div>

      {/* Export Card */}
      <Card>
        <CardHeader>
          <CardTitle>Backup Completo</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">
            El backup incluirá:
          </p>
          <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1">
            <li>Todas las evaluaciones en formato JSON</li>
            <li>Todos los planes de acción en formato CSV</li>
            <li>Todas las recomendaciones en formato CSV</li>
            <li>Todas las plantillas en formato JSON</li>
            <li>Archivo metadata.json con información del export</li>
          </ul>
          
          <div className="flex items-start gap-3 p-4 bg-warning/10 rounded-lg border border-warning/20">
            <AlertTriangle className="w-5 h-5 text-warning flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-foreground">Nota sobre el tamaño</p>
              <p className="text-sm text-muted-foreground">
                Si tienes muchas evaluaciones, el archivo puede ser grande. 
                La descarga puede tardar unos minutos.
              </p>
            </div>
          </div>
          
          <ExportButton />
        </CardContent>
      </Card>
    </div>
  )
}