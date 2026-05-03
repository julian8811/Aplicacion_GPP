import { Line } from 'recharts'
import { Benchmark } from '@/hooks/useBenchmarks'

interface IndustryBenchmarkLineProps {
  benchmarks: Benchmark[]
  dataKey: 'general_pct' | 'pa_pct' | 'po_pct'
  category?: 'PA' | 'PO'
}

export function IndustryBenchmarkLine({ benchmarks, dataKey, category }: IndustryBenchmarkLineProps) {
  // Filter benchmarks by category if specified
  const filteredBenchmarks = category
    ? benchmarks.filter((b) => b.category === category)
    : benchmarks

  if (!filteredBenchmarks.length) return null

  // Calculate average across all benchmarks (for general_pct)
  const avgScore =
    dataKey === 'general_pct'
      ? filteredBenchmarks.reduce((sum, b) => sum + b.avg_score, 0) / filteredBenchmarks.length
      : filteredBenchmarks.find((b) => {
          // Map dataKey to aspect - this is simplified
          if (dataKey === 'pa_pct' && b.category === 'PA') return true
          if (dataKey === 'po_pct' && b.category === 'PO') return true
          return false
        })?.avg_score || 0

  if (!avgScore) return null

  return (
    <>
      {/* Render reference lines for each benchmark aspect */}
      {filteredBenchmarks.map((benchmark) => (
        <Line
          key={benchmark.id}
          type="monotone"
          dataKey={() => benchmark.avg_score}
          stroke="#9ca3af"
          strokeWidth={2}
          strokeDasharray="5 5"
          dot={false}
          name={`Industria ${benchmark.category} ${benchmark.aspect}`}
        />
      ))}
    </>
  )
}

// Legend content for industry benchmarks
export function IndustryBenchmarkLegend({ benchmarks }: { benchmarks: Benchmark[] }) {
  if (!benchmarks.length) return null

  const totalSample = benchmarks.reduce((sum, b) => sum + b.sample_size, 0)
  const source = benchmarks[0]?.source || 'GPP Research'

  return (
    <div className="flex items-center gap-4 text-sm text-muted-foreground">
      <div className="flex items-center gap-2">
        <div className="w-4 h-0.5 bg-muted-foreground border-dashed border-t-2" />
        <span>Promedio industria ({totalSample} empresas)</span>
      </div>
      <span className="text-xs">Fuente: {source}</span>
    </div>
  )
}