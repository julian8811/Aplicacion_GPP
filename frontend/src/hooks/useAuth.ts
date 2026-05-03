import { useEffect, useCallback } from 'react'
import { supabase } from '@/lib/supabase'
import { useAuthStore } from '@/stores/authStore'

export function useAuth() {
  const {
    user,
    session,
    isLoading,
    isGuest,
    setSession,
    setGuestMode,
    reset
  } = useAuthStore()

  // Check for guest mode from URL
  const checkGuestMode = useCallback(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search)
      const guestMode = params.get('mode') === 'guest'
      setGuestMode(guestMode)
      return guestMode
    }
    return false
  }, [setGuestMode])

  // Login with email/password
  const login = useCallback(async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    })

    if (error) {
      return { error }
    }

    setSession(data.session)
    setGuestMode(false)
    return { error: null }
  }, [setSession, setGuestMode])

  // Signup with email/password
  const signup = useCallback(async (
    email: string,
    password: string,
    establishmentName: string
  ) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          establishment_name: establishmentName
        }
      }
    })

    if (error) {
      return { error }
    }

    // If sign up successful but email confirmation needed, session is null
    if (data.session) {
      setSession(data.session)
      setGuestMode(false)
    }

    return { error: null }
  }, [setSession, setGuestMode])

  // Logout
  const logout = useCallback(async () => {
    await supabase.auth.signOut()
    reset()
  }, [reset])

  // Listen for auth state changes
  useEffect(() => {
    checkGuestMode()

    const {
      data: { subscription }
    } = supabase.auth.onAuthStateChange((event, session) => {
      if (event === 'SIGNED_IN' && session) {
        setSession(session)
      } else if (event === 'SIGNED_OUT') {
        reset()
      }
    })

    // Initial session check
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session) {
        setSession(session)
      } else {
        setSession(null)
        checkGuestMode()
      }
    })

    return () => {
      subscription.unsubscribe()
    }
  }, [setSession, reset, checkGuestMode])

  return {
    user,
    session,
    isLoading,
    isGuest,
    login,
    signup,
    logout,
    checkGuestMode
  }
}