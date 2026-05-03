import { Card, CardContent } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { cn } from '@/lib/utils'

interface ComparisonTableProps {
  title: string
  data: Array<{
    aspect: string
    eval_a_value: number
    eval_b_value: number
    delta: number
    delta_pct: number
  }>
  evalALabel?: string
  evalBLabel?: string
}

export function ComparisonTable({ title, data, evalALabel = "Eval A", evalBLabel = "Eval B" }: ComparisonTableProps) {
  return (
    <Card>
      <CardContent className="p-4">
        <h3 className="font-semibold text-foreground mb-4">{title}</h3>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-2 px-2 text-sm font-medium text-muted-foreground">Aspecto</th>
                <th className="text-center py-2 px-2 text-sm font-medium text-muted-foreground">{evalALabel}</th>
                <th className="text-center py-2 px-2 text-sm font-medium text-muted-foreground">{evalBLabel}</th>
                <th className="text-center py-2 px-2 text-sm font-medium text-muted-foreground">Diferencia</th>
                <th className="text-center py-2 px-2 text-sm font-medium text-muted-foreground">%</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, idx) => (
                <tr key={idx} className="border-b border-border/50">
                  <td className="py-2 px-2 text-sm">{row.aspect}</td>
                  <td className="py-2 px-2 text-center text-sm font-medium">{row.eval_a_value}%</td>
                  <td className="py-2 px-2 text-center text-sm font-medium">{row.eval_b_value}%</td>
                  <td className={cn(
                    "py-2 px-2 text-center text-sm font-medium",
                    row.delta > 0 ? "text-success" : row.delta < 0 ? "text-error" : "text-muted-foreground"
                  )}>
                    {row.delta > 0 ? "+" : ""}{row.delta}%
                  </td>
                  <td className={cn(
                    "py-2 px-2 text-center text-sm",
                    row.delta > 0 ? "text-success" : row.delta < 0 ? "text-error" : "text-muted-foreground"
                  )}>
                    <Badge 
                      variant={row.delta > 0 ? "success" : row.delta < 0 ? "error" : "secondary"}
                      className="text-xs"
                    >
                      {row.delta_pct > 0 ? "+" : ""}{row.delta_pct}%
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  )
}