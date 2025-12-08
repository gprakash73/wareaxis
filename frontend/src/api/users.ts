import apiClient from './client'
import type {
  User,
  Role,
  Permission,
  PaginatedResponse,
  UserCreateForm,
  UserUpdateForm,
} from '@/types'

export interface ListUsersParams {
  page?: number
  page_size?: number
  is_active?: boolean
  role?: string
}

export const usersApi = {
  list: async (params: ListUsersParams = {}): Promise<PaginatedResponse<User>> => {
    const response = await apiClient.get<PaginatedResponse<User>>('/users', { params })
    return response.data
  },

  get: async (userId: string): Promise<User> => {
    const response = await apiClient.get<User>(`/users/${userId}`)
    return response.data
  },

  create: async (data: UserCreateForm): Promise<User> => {
    const response = await apiClient.post<User>('/users', data)
    return response.data
  },

  update: async (userId: string, data: UserUpdateForm): Promise<User> => {
    const response = await apiClient.patch<User>(`/users/${userId}`, data)
    return response.data
  },

  delete: async (userId: string): Promise<void> => {
    await apiClient.delete(`/users/${userId}`)
  },

  activate: async (userId: string): Promise<void> => {
    await apiClient.post(`/users/${userId}/activate`)
  },

  deactivate: async (userId: string): Promise<void> => {
    await apiClient.post(`/users/${userId}/deactivate`)
  },

  resetPassword: async (userId: string, newPassword: string): Promise<void> => {
    await apiClient.post(`/users/${userId}/reset-password`, null, {
      params: { new_password: newPassword },
    })
  },

  listRoles: async (): Promise<Role[]> => {
    const response = await apiClient.get<Role[]>('/users/roles')
    return response.data
  },

  listPermissions: async (): Promise<Permission[]> => {
    const response = await apiClient.get<Permission[]>('/users/permissions')
    return response.data
  },
}
