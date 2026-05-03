import { Card, CardContent } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { formatDate } from '@/lib/utils'
import { Template } from '@/hooks/useTemplates'
import { useNavigate } from 'react-router-dom'

interface TemplateCardProps {
  template: Template
  onUse?: (template: Template) => void
  onEdit?: (template: Template) => void
  onDelete?: (template: Template) => void
  showOwner?: boolean
}

export function TemplateCard({ template, onUse, onEdit, onDelete, showOwner = false }: TemplateCardProps) {
  const navigate = useNavigate()
  
  const handleUse = () => {
    if (onUse) {
      onUse(template)
    } else {
      navigate(`/evaluate/wizard?template_id=${template.id}`)
    }
  }

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex flex-col h-full">
          <div className="flex-1">
            <div className="flex items-start justify-between mb-2">
              <h3 className="font-semibold text-foreground">{template.name}</h3>
              {template.is_public && (
                <Badge variant="secondary">Público</Badge>
              )}
            </div>
            
            {template.description && (
              <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
                {template.description}
              </p>
            )}
            
            <div className="flex items-center gap-4 text-xs text-muted-foreground">
              <span>{formatDate(template.created_at)}</span>
              {showOwner && template.created_by && (
                <span>Creador: {template.created_by.slice(0, 8)}...</span>
              )}
            </div>
          </div>
          
          <div className="flex gap-2 mt-4 pt-3 border-t border-border">
            <Button size="sm" onClick={handleUse}>
              Usar
            </Button>
            {onEdit && (
              <Button size="sm" variant="outline" onClick={() => onEdit(template)}>
                Editar
              </Button>
            )}
            {onDelete && (
              <Button 
                size="sm" 
                variant="outline" 
                className="text-error hover:bg-error/10"
                onClick={() => onDelete(template)}
              >
                Eliminar
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}