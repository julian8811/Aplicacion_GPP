import { cn } from '@/lib/utils'

interface SliderQuestionProps {
  id: string
  question: string
  context?: string
  value: number
  onChange: (value: number) => void
  disabled?: boolean
}

export function SliderQuestion({ id, question, context, value, onChange, disabled }: SliderQuestionProps) {
  return (
    <div className="bg-white p-4 rounded-lg border border-border mb-4">
      <div className="mb-3">
        <label htmlFor={id} className="text-sm font-medium text-foreground">
          {question}
        </label>
        {context && (
          <p className="text-xs text-muted-foreground mt-1">{context}</p>
        )}
      </div>
      <div className="flex items-center gap-4">
        <input
          type="range"
          id={id}
          min="0"
          max="5"
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          disabled={disabled}
          className="flex-1 h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary"
        />
        <div className={cn(
          "w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm",
          value === 0 && "bg-slate-100 text-slate-500",
          value === 1 && "bg-red-100 text-red-700",
          value === 2 && "bg-orange-100 text-orange-700",
          value === 3 && "bg-yellow-100 text-yellow-700",
          value === 4 && "bg-lime-100 text-lime-700",
          value === 5 && "bg-green-100 text-green-700"
        )}>
          {value}
        </div>
      </div>
      <div className="flex justify-between mt-2 text-xs text-muted-foreground">
        <span>0 - No cumple</span>
        <span>3 - Cumple parcialmente</span>
        <span>5 - Cumple totalmente</span>
      </div>
    </div>
  )
}