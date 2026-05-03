import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { toast } from 'sonner'

export function SignupPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [establishmentName, setEstablishmentName] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)
  const { signup } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    const { error } = await signup(email, password, establishmentName)

    if (error) {
      toast.error(error.message || 'Error al registrar')
      setIsLoading(false)
      return
    }

    // Check if email confirmation is required
    toast.success('Revisa tu correo para confirmar tu cuenta')
    setIsSuccess(true)
    setIsLoading(false)

    // If no email confirmation needed, redirect to login
    setTimeout(() => {
      navigate('/login')
    }, 2000)
  }

  if (isSuccess) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
        <div className="max-w-md w-full text-center">
          <div className="mb-4">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
              <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
          <h2 className="text-2xl font-bold text-gray-900">¡Registro exitoso!</h2>
          <p className="mt-2 text-gray-600">
            Te hemos enviado un correo de confirmación. Revisa tu bandeja de entrada y confirma tu cuenta para continuar.
          </p>
          <p className="mt-4 text-sm text-gray-500">
            Redirigiendo a login...
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h1 className="text-3xl font-bold text-center text-gray-900">
            GPP
          </h1>
          <h2 className="mt-6 text-center text-2xl font-semibold text-gray-900">
            Crear Cuenta
          </h2>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="establishmentName" className="block text-sm font-medium text-gray-700">
                Nombre del establecimiento
              </label>
              <Input
                id="establishmentName"
                type="text"
                value={establishmentName}
                onChange={(e) => setEstablishmentName(e.target.value)}
                placeholder="Mi Restaurante"
                required
                className="mt-1"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Correo electrónico
              </label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="tu@email.com"
                required
                className="mt-1"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Contraseña
              </label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                minLength={6}
                className="mt-1"
              />
              <p className="mt-1 text-xs text-gray-500">
                Mínimo 6 caracteres
              </p>
            </div>
          </div>

          <Button
            type="submit"
            className="w-full"
            disabled={isLoading}
          >
            {isLoading ? 'Creando cuenta...' : 'Crear Cuenta'}
          </Button>
        </form>

        <p className="text-center text-sm text-gray-500">
          ¿Ya tienes cuenta?{' '}
          <Link to="/login" className="text-blue-600 hover:text-blue-700 font-medium">
            Inicia sesión
          </Link>
        </p>
      </div>
    </div>
  )
}