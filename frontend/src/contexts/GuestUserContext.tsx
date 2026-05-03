import { createContext, useContext, ReactNode } from 'react'

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

interface GuestUserContextType {
  user: User
  isGuest: boolean
}

const GuestUserContext = createContext<GuestUserContextType>({
  user: guestUser,
  isGuest: true
})

export function GuestUserProvider({
  children,
  isGuestMode = false
}: {
  children: ReactNode
  isGuestMode?: boolean
}) {
  return (
    <GuestUserContext.Provider
      value={{
        user: isGuestMode ? guestUser : { ...guestUser, id: '' },
        isGuest: isGuestMode
      }}
    >
      {children}
    </GuestUserContext.Provider>
  )
}

export function useGuestUser() {
  return useContext(GuestUserContext)
}