import { Button } from '@/components/ui/Button'
import { useExport } from '@/hooks/useExport'

interface ExportButtonProps {
  className?: string
}

export function ExportButton({ className }: ExportButtonProps) {
  const exportMutation = useExport()
  
  const handleExport = async () => {
    try {
      await exportMutation.mutateAsync()
    } catch (error) {
      // Error handling is done in the mutation
    }
  }

  return (
    <Button
      onClick={handleExport}
      disabled={exportMutation.isPending}
      className={className}
    >
      {exportMutation.isPending && (
        <div className="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2" />
      )}
      Descargar Backup
    </Button>
  )
}