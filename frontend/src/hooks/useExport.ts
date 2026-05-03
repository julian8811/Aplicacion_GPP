import { useMutation } from '@tanstack/react-query'
import api from '@/lib/api'
import { toast } from '@/lib/toast'

export function useExport() {
  return useMutation({
    mutationFn: async () => {
      const response = await api.get('/export/backup', {
        responseType: 'blob',
      })
      return response.data as Blob
    },
    onSuccess: (data: Blob) => {
      // Create download link
      const url = window.URL.createObjectURL(data)
      const link = document.createElement('a')
      link.href = url
      
      // Set download filename
      const filename = `gpp_backup_${new Date().toISOString().slice(0, 10)}.zip`
      link.download = filename
      
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      toast.success('Backup descargado correctamente')
    },
    onError: () => {
      toast.error('Error al descargar el backup')
    },
  })
}