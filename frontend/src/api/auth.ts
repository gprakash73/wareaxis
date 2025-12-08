import apiClient from './client'
import type {
  LoginRequest,
  TokenResponse,
  User,
  TenantRegistration,
  RegistrationResponse,
} from '@/types'

export const authApi = {
  login: async (data: LoginRequest): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/auth/login', data)
    return response.data
  },

  register: async (data: TenantRegistration): Promise<RegistrationResponse> => {
    const response = await apiClient.post<RegistrationResponse>('/auth/register', data)
    return response.data
  },

  refreshToken: async (refreshToken: string): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/auth/refresh', {
      refresh_token: refreshToken,
    })
    return response.data
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me')
    return response.data
  },

  changePassword: async (currentPassword: string, newPassword: string): Promise<void> => {
    await apiClient.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    })
  },

  logout: async (): Promise<void> => {
    await apiClient.post('/auth/logout')
  },
}
