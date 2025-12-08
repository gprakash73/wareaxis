import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import type { User } from '@/types'

interface AuthState {
  // State
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  tenantSlug: string | null
  isAuthenticated: boolean

  // Actions
  setUser: (user: User | null) => void
  setTokens: (accessToken: string, refreshToken: string) => void
  setTenantSlug: (slug: string) => void
  login: (user: User, accessToken: string, refreshToken: string, tenantSlug: string) => void
  logout: () => void
  hasRole: (role: string) => boolean
  hasPermission: (permission: string) => boolean
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      accessToken: null,
      refreshToken: null,
      tenantSlug: null,
      isAuthenticated: false,

      // Actions
      setUser: (user) => set({ user }),

      setTokens: (accessToken, refreshToken) =>
        set({ accessToken, refreshToken, isAuthenticated: !!accessToken }),

      setTenantSlug: (tenantSlug) => set({ tenantSlug }),

      login: (user, accessToken, refreshToken, tenantSlug) =>
        set({
          user,
          accessToken,
          refreshToken,
          tenantSlug,
          isAuthenticated: true,
        }),

      logout: () =>
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          tenantSlug: null,
          isAuthenticated: false,
        }),

      hasRole: (role) => {
        const { user } = get()
        if (!user) return false
        return user.roles.some((r) => r.code === role)
      },

      hasPermission: (permission) => {
        const { user } = get()
        if (!user) return false
        // Admin has all permissions
        if (user.roles.some((r) => r.code === 'admin')) return true
        // TODO: Check actual permissions from roles
        return false
      },
    }),
    {
      name: 'wms-auth',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        tenantSlug: state.tenantSlug,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
