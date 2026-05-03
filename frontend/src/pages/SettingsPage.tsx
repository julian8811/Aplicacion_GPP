import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { api } from '@/lib/api'
import { useAuthStore } from '@/stores/authStore'
import { Bell, Shield, Palette, Save, Check, Upload, Image as ImageIcon } from 'lucide-react'
import { BrandingPreview } from '@/components/settings/BrandingPreview'

interface NotificationPreferences {
  action_plan_reminders: boolean
  weekly_summary: boolean
  marketing: boolean
}

interface BrandingSettings {
  logo_url: string | null
  primary_color: string
  footer_text: string
}

export function SettingsPage() {
  const { user } = useAuthStore()
  const [preferences, setPreferences] = useState<NotificationPreferences>({
    action_plan_reminders: true,
    weekly_summary: true,
    marketing: false,
  })
  const [isLoading, setIsLoading] = useState(false)
  const [saved, setSaved] = useState(false)
  const [establishmentName, setEstablishmentName] = useState('')

  // Branding state
  const [branding, setBranding] = useState<BrandingSettings>({
    logo_url: null,
    primary_color: '#2563eb',
    footer_text: '',
  })
  const [brandingSaved, setBrandingSaved] = useState(false)
  const [isUploadingLogo, setIsUploadingLogo] = useState(false)

  // Fetch profile data on mount
  useEffect(() => {
    async function fetchProfile() {
      try {
        const response = await api.get('/profiles/me')
        if (response.data) {
          setEstablishmentName(response.data.establishment_name || '')
          setBranding(prev => ({
            ...prev,
            logo_url: response.data.logo_url || null,
            primary_color: response.data.primary_color || '#2563eb',
            footer_text: response.data.footer_text || '',
          }))
        }
      } catch (error) {
        console.error('Failed to fetch profile:', error)
      }
    }
    fetchProfile()
  }, [])

  const handleGoogleConnect = () => {
    // Placeholder for future OAuth integration
  }

  const handleToggle = (key: keyof NotificationPreferences) => {
    setPreferences(prev => ({ ...prev, [key]: !prev[key] }))
    setSaved(false)
  }

  const handleSavePreferences = async () => {
    if (!user) return

    setIsLoading(true)
    setSaved(false)

    try {
      await api.put('/notifications/preferences', preferences)
      setSaved(true)
      setTimeout(() => setSaved(false), 3000)
    } catch (error) {
      console.error('Failed to save preferences:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogoUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Por favor selecciona un archivo de imagen')
      return
    }

    // Validate file size (max 2MB)
    if (file.size > 2 * 1024 * 1024) {
      alert('El archivo debe ser menor a 2MB')
      return
    }

    setIsUploadingLogo(true)

    try {
      // Convert to base64 for simplicity (alternatively use Supabase Storage)
      const reader = new FileReader()
      reader.onload = async (e) => {
        const base64 = e.target?.result as string
        setBranding(prev => ({ ...prev, logo_url: base64 }))
        setIsUploadingLogo(false)
      }
      reader.onerror = () => {
        alert('Error al leer el archivo')
        setIsUploadingLogo(false)
      }
      reader.readAsDataURL(file)
    } catch (error) {
      console.error('Logo upload error:', error)
      setIsUploadingLogo(false)
    }
  }

  const handleSaveBranding = async () => {
    if (!user) return

    setIsLoading(true)
    setBrandingSaved(false)

    try {
      await api.patch('/profiles/me', {
        establishment_name: establishmentName,
        logo_url: branding.logo_url,
        primary_color: branding.primary_color,
        footer_text: branding.footer_text,
      })
      setBrandingSaved(true)
      setTimeout(() => setBrandingSaved(false), 3000)
    } catch (error) {
      console.error('Failed to save branding:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6 max-w-3xl">
      <h1 className="text-2xl font-bold text-foreground">Configuración</h1>

      {/* Section: Email Notifications */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Bell className="h-5 w-5" />
            Notificaciones por Email
          </CardTitle>
          <CardDescription>
            Configura qué emails quieres recibir
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Action plan reminders */}
          <div className="flex items-center justify-between py-3 border-b">
            <div className="space-y-0.5">
              <div className="font-medium">Recordatorios de planes de acción</div>
              <div className="text-sm text-muted-foreground">
                7 días antes, el día del vencimiento, y cuando están vencidos
              </div>
            </div>
            <ToggleSwitch
              checked={preferences.action_plan_reminders}
              onChange={() => handleToggle('action_plan_reminders')}
            />
          </div>

          {/* Weekly summary */}
          <div className="flex items-center justify-between py-3 border-b">
            <div className="space-y-0.5">
              <div className="font-medium">Resumen semanal</div>
              <div className="text-sm text-muted-foreground">
                Un email cada semana con tu actividad y estadísticas
              </div>
            </div>
            <ToggleSwitch
              checked={preferences.weekly_summary}
              onChange={() => handleToggle('weekly_summary')}
            />
          </div>

          {/* Marketing emails */}
          <div className="flex items-center justify-between py-3">
            <div className="space-y-0.5">
              <div className="font-medium">Emails de marketing</div>
              <div className="text-sm text-muted-foreground">
                Novedades, tips y contenido promocional
              </div>
            </div>
            <ToggleSwitch
              checked={preferences.marketing}
              onChange={() => handleToggle('marketing')}
            />
          </div>

          <div className="pt-4 flex items-center gap-3">
            <Button onClick={handleSavePreferences} disabled={isLoading} size="sm">
              {isLoading ? (
                'Guardando...'
              ) : saved ? (
                <>
                  <Check className="h-4 w-4 mr-1" />
                  Guardado
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-1" />
                  Guardar preferencias
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Section: Connected Accounts */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            Cuentas Conectadas
          </CardTitle>
          <CardDescription>Gestiona tus cuentas vinculadas</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center border">
                <svg className="w-6 h-6" viewBox="0 0 24 24">
                  <path
                    fill="#4285F4"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="#34A853"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  />
                  <path
                    fill="#EA4335"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  />
                </svg>
              </div>
              <div>
                <p className="font-medium">Google</p>
                <p className="text-sm text-muted-foreground">Conectar</p>
              </div>
            </div>
            <button
              onClick={handleGoogleConnect}
              className="px-4 py-2 text-sm font-medium rounded-lg border hover:bg-secondary transition-colors"
            >
              Conectar
            </button>
          </div>
          <p className="text-sm text-muted-foreground">
            Conecta tu cuenta de Google para una experiencia personalizada
          </p>
        </CardContent>
      </Card>

      {/* Section: Branding */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Palette className="h-5 w-5" />
            Personalización de Marca
          </CardTitle>
          <CardDescription>
            Configura el aspecto de tus PDFs generados
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Branding Settings Form */}
            <div className="space-y-4">
              {/* Logo Upload */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Logo</label>
                <div className="flex items-center gap-4">
                  <div className="w-20 h-20 border rounded-lg flex items-center justify-center bg-secondary overflow-hidden">
                    {branding.logo_url ? (
                      <img
                        src={branding.logo_url}
                        alt="Logo"
                        className="w-full h-full object-contain"
                      />
                    ) : (
                      <ImageIcon className="w-8 h-8 text-muted-foreground" />
                    )}
                  </div>
                  <div>
                    <label
                      htmlFor="logo-upload"
                      className="inline-flex items-center gap-1 px-3 py-2 text-sm font-medium rounded-md border hover:bg-secondary transition-colors cursor-pointer"
                    >
                      <Upload className="h-4 w-4 mr-1" />
                      {isUploadingLogo ? 'Subiendo...' : 'Subir Logo'}
                    </label>
                    <input
                      id="logo-upload"
                      type="file"
                      accept="image/*"
                      onChange={handleLogoUpload}
                      className="hidden"
                      disabled={isUploadingLogo}
                    />
                    <p className="text-xs text-muted-foreground mt-1">Max 2MB, JPG o PNG</p>
                  </div>
                </div>
              </div>

              {/* Primary Color */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Color Principal</label>
                <div className="flex items-center gap-3">
                  <input
                    type="color"
                    value={branding.primary_color}
                    onChange={(e) => setBranding(prev => ({ ...prev, primary_color: e.target.value }))}
                    className="w-12 h-10 rounded border cursor-pointer"
                  />
                  <input
                    type="text"
                    value={branding.primary_color}
                    onChange={(e) => setBranding(prev => ({ ...prev, primary_color: e.target.value }))}
                    className="flex-1 px-3 py-2 border rounded-md text-sm"
                    placeholder="#2563eb"
                  />
                </div>
              </div>

              {/* Footer Text */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Texto de Pie de Página</label>
                <input
                  type="text"
                  value={branding.footer_text}
                  onChange={(e) => setBranding(prev => ({ ...prev, footer_text: e.target.value }))}
                  className="w-full px-3 py-2 border rounded-md text-sm"
                  placeholder="Texto personalizado para el pie del PDF"
                  maxLength={100}
                />
                <p className="text-xs text-muted-foreground">
                  Máx. 100 caracteres
                </p>
              </div>

              {/* Save Button */}
              <Button onClick={handleSaveBranding} disabled={isLoading}>
                {isLoading ? (
                  'Guardando...'
                ) : brandingSaved ? (
                  <>
                    <Check className="h-4 w-4 mr-1" />
                    Guardado
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4 mr-1" />
                    Guardar Marca
                  </>
                )}
              </Button>
            </div>

            {/* Live Preview */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Vista Previa</label>
              <BrandingPreview
                logoUrl={branding.logo_url}
                primaryColor={branding.primary_color}
                footerText={branding.footer_text}
                establishmentName={establishmentName}
              />
              <p className="text-xs text-muted-foreground">
                Así se verá tu PDF con la configuración actual
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

// Toggle Switch component
interface ToggleSwitchProps {
  checked: boolean
  onChange: () => void
}

function ToggleSwitch({ checked, onChange }: ToggleSwitchProps) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      onClick={onChange}
      className={`
        relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent 
        transition-colors duration-200 ease-in-out focus-visible:outline-none focus-visible:ring-2 
        focus-visible:ring-primary focus-visible:ring-offset-2
        ${checked ? 'bg-primary' : 'bg-muted'}
      `}
    >
      <span
        className={`
          pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 
          transition duration-200 ease-in-out
          ${checked ? 'translate-x-5' : 'translate-x-0'}
        `}
      />
    </button>
  )
}