-- Initialize PostgreSQL database for WMS Pro

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create public schema tables for tenant management

-- Tenants table
CREATE TABLE IF NOT EXISTS public.tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    contact_phone VARCHAR(50),
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    timezone VARCHAR(50) DEFAULT 'UTC' NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD' NOT NULL,
    locale VARCHAR(10) DEFAULT 'en-US' NOT NULL,
    schema_name VARCHAR(100) UNIQUE NOT NULL,
    schema_created BOOLEAN DEFAULT FALSE NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Tenant settings table
CREATE TABLE IF NOT EXISTS public.tenant_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID UNIQUE NOT NULL REFERENCES public.tenants(id) ON DELETE CASCADE,
    features JSONB DEFAULT '{}'::jsonb NOT NULL,
    erp_type VARCHAR(50),
    erp_config JSONB DEFAULT '{}'::jsonb NOT NULL,
    allow_negative_stock BOOLEAN DEFAULT FALSE NOT NULL,
    default_stock_type VARCHAR(20) DEFAULT 'unrestricted' NOT NULL,
    ui_theme VARCHAR(20) DEFAULT 'light' NOT NULL,
    ui_config JSONB DEFAULT '{}'::jsonb NOT NULL,
    custom_fields JSONB DEFAULT '{}'::jsonb NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_tenants_slug ON public.tenants(slug);
CREATE INDEX IF NOT EXISTS idx_tenants_is_active ON public.tenants(is_active);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tenants table
DROP TRIGGER IF EXISTS update_tenants_updated_at ON public.tenants;
CREATE TRIGGER update_tenants_updated_at
    BEFORE UPDATE ON public.tenants
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Apply trigger to tenant_settings table
DROP TRIGGER IF EXISTS update_tenant_settings_updated_at ON public.tenant_settings;
CREATE TRIGGER update_tenant_settings_updated_at
    BEFORE UPDATE ON public.tenant_settings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO wms;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO wms;
