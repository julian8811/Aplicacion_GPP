interface BrandingPreviewProps {
  logoUrl?: string | null
  primaryColor?: string | null
  footerText?: string | null
  establishmentName?: string
}

export function BrandingPreview({
  logoUrl,
  primaryColor = "#2563eb",
  footerText,
  establishmentName = "Mi Establecimiento"
}: BrandingPreviewProps) {
  // Ensure we have valid values
  const safePrimaryColor = primaryColor || "#2563eb"
  const safeLogoUrl = logoUrl || undefined

  return (
    <div className="border rounded-lg overflow-hidden bg-white">
      {/* Preview Header */}
      <div
        className="px-4 py-3 flex items-center justify-between"
        style={{ backgroundColor: safePrimaryColor }}
      >
        <div className="flex items-center gap-3">
          {safeLogoUrl ? (
            <img
              src={safeLogoUrl}
              alt="Logo"
              className="h-8 w-auto object-contain"
            />
          ) : (
            <span className="text-white font-bold text-lg">AUDITORIA GPP</span>
          )}
        </div>
        <span className="text-white/80 text-sm">
          {establishmentName}
        </span>
      </div>

      {/* Preview Content - Simplified PDF look */}
      <div className="p-4 space-y-3">
        <div className="text-sm space-y-1">
          <div className="font-semibold text-foreground">Resumen de Resultados</div>
          <div className="flex gap-4 text-xs text-muted-foreground">
            <span>PA: <span className="font-medium">85%</span></span>
            <span>PO: <span className="font-medium">72%</span></span>
            <span>General: <span className="font-medium">78%</span></span>
          </div>
        </div>

        {/* Mini bar chart preview */}
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-xs">
            <span className="w-8">PA</span>
            <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
              <div
                className="h-full rounded-full"
                style={{
                  width: '85%',
                  backgroundColor: safePrimaryColor
                }}
              />
            </div>
            <span className="w-8">85%</span>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <span className="w-8">PO</span>
            <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
              <div
                className="h-full rounded-full"
                style={{
                  width: '72%',
                  backgroundColor: safePrimaryColor,
                  opacity: 0.7
                }}
              />
            </div>
            <span className="w-8">72%</span>
          </div>
        </div>
      </div>

      {/* Preview Footer */}
      <div
        className="px-4 py-2 border-t text-xs text-center text-muted-foreground"
        style={{ borderColor: safePrimaryColor + '30' }}
      >
        {footerText || 'GPP Auditoria'}
      </div>
    </div>
  )
}