// API Response Types

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface ApiError {
  detail: string
  errors?: Array<{
    loc: string[]
    msg: string
    type: string
  }>
}

// Auth Types

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface LoginRequest {
  username: string
  password: string
  tenant_slug: string
}

// User Types

export interface User {
  id: string
  email: string
  username: string
  first_name: string
  last_name: string
  full_name: string
  display_name?: string
  phone?: string
  avatar_url?: string
  is_active: boolean
  is_verified: boolean
  is_superuser: boolean
  last_login?: string
  default_warehouse_id?: string
  employee_id?: string
  department?: string
  job_title?: string
  roles: RoleBrief[]
  preferences: Record<string, unknown>
  created_at: string
  updated_at: string
}

export interface RoleBrief {
  id: string
  code: string
  name: string
}

export interface Role extends RoleBrief {
  description?: string
  is_system: boolean
  is_active: boolean
  permissions: Permission[]
  created_at: string
  updated_at: string
}

export interface Permission {
  id: string
  code: string
  name: string
  description?: string
  module: string
  is_active: boolean
}

// Tenant Types

export interface Tenant {
  id: string
  name: string
  slug: string
  description?: string
  is_active: boolean
  is_verified: boolean
  contact_email: string
  contact_phone?: string
  address_line1?: string
  address_line2?: string
  city?: string
  state?: string
  country?: string
  postal_code?: string
  timezone: string
  currency: string
  locale: string
  schema_name: string
  schema_created: boolean
  metadata: Record<string, unknown>
  created_at: string
  updated_at: string
}

export interface TenantSettings {
  id: string
  tenant_id: string
  features: Record<string, unknown>
  erp_type?: string
  erp_config: Record<string, unknown>
  allow_negative_stock: boolean
  default_stock_type: string
  ui_theme: string
  ui_config: Record<string, unknown>
  custom_fields: Record<string, unknown>
  created_at: string
  updated_at: string
}

// Form Types

export interface UserCreateForm {
  email: string
  username: string
  password: string
  first_name: string
  last_name: string
  display_name?: string
  phone?: string
  role_ids: string[]
  default_warehouse_id?: string
  employee_id?: string
  department?: string
  job_title?: string
}

export interface UserUpdateForm {
  email?: string
  first_name?: string
  last_name?: string
  display_name?: string
  phone?: string
  is_active?: boolean
  role_ids?: string[]
  default_warehouse_id?: string
  employee_id?: string
  department?: string
  job_title?: string
  preferences?: Record<string, unknown>
}

// Registration Types

export interface TenantRegistration {
  tenant_name: string
  tenant_slug: string
  contact_email: string
  admin_email: string
  admin_username: string
  admin_password: string
  admin_first_name: string
  admin_last_name: string
}

export interface RegistrationResponse {
  tenant: Tenant
  user: User
  tokens: TokenResponse
}
