import { createContext, useContext } from 'react'

export type User = {
  id: string
  email: string
  role: 'owner' | 'viewer'
  full_name?: string
  establishment_name?: string
}

const guestUser: User = {
  id: "00000000-0000-0000-0000-000000000000",
  email: "guest@local",
  role: "owner",
  full_name: "Guest User",
  establishment_name: undefined
}

const GuestUserContext = createContext(guestUser)

export function GuestUserProvider({ children }: { children: React.ReactNode }) {
  return (
    <GuestUserContext.Provider value={guestUser}>
      {children}
    </GuestUserContext.Provider>
  )
}

export function useGuestUser() {
  return useContext(GuestUserContext)
}