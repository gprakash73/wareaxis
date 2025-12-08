import apiClient from './client'
import type {
  Tenant,
  TenantSettings,
  PaginatedResponse,
} from '@/types'

export interface ListTenantsParams {
  page?: number
  page_size?: number
  is_active?: boolean
}

export interface TenantUpdateForm {
  name?: string
  description?: string
  contact_email?: string
  contact_phone?: string
  address_line1?: string
  address_line2?: string
  city?: string
  state?: string
  country?: string
  postal_code?: string
  timezone?: string
  currency?: string
  locale?: string
  is_active?: boolean
}

export interface TenantSettingsUpdateForm {
  features?: Record<string, unknown>
  erp_type?: string
  erp_config?: Record<string, unknown>
  allow_negative_stock?: boolean
  default_stock_type?: string
  ui_theme?: string
  ui_config?: Record<string, unknown>
  custom_fields?: Record<string, unknown>
}

export const tenantsApi = {
  list: async (params: ListTenantsParams = {}): Promise<PaginatedResponse<Tenant>> => {
    const response = await apiClient.get<PaginatedResponse<Tenant>>('/tenants', { params })
    return response.data
  },

  get: async (tenantId: string): Promise<Tenant> => {
    const response = await apiClient.get<Tenant>(`/tenants/${tenantId}`)
    return response.data
  },

  getCurrent: async (): Promise<Tenant> => {
    const response = await apiClient.get<Tenant>('/tenants/current')
    return response.data
  },

  update: async (tenantId: string, data: TenantUpdateForm): Promise<Tenant> => {
    const response = await apiClient.patch<Tenant>(`/tenants/${tenantId}`, data)
    return response.data
  },

  updateCurrentSettings: async (data: TenantSettingsUpdateForm): Promise<TenantSettings> => {
    const response = await apiClient.patch<TenantSettings>('/tenants/current/settings', data)
    return response.data
  },

  delete: async (tenantId: string): Promise<void> => {
    await apiClient.delete(`/tenants/${tenantId}`)
  },
}
