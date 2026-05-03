import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User, Session } from '@supabase/supabase-js'

interface AuthState {
  user: User | null
  session: Session | null
  isLoading: boolean
  isGuest: boolean

  // Actions
  setSession: (session: Session | null) => void
  setGuestMode: (isGuest: boolean) => void
  reset: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      session: null,
      isLoading: true,
      isGuest: false,

      setSession: (session) => {
        set({
          session,
          user: session?.user ?? null,
          isLoading: false
        })
      },

      setGuestMode: (isGuest) => set({ isGuest }),

      reset: () => set({
        user: null,
        session: null,
        isLoading: false,
        isGuest: false
      })
    }),
    {
      name: 'gpp-auth',
      partialize: (state) => ({
        session: state.session,
        user: state.user,
        isGuest: state.isGuest
      })
    }
  )
)