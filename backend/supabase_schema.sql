-- ============================================================================
-- GPP (Gestión Por Procesos) - Schema completo para Supabase
-- ============================================================================

-- Crear tabla PROFILES (perfiles de usuarios)
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT,
    full_name TEXT,
    role TEXT DEFAULT 'owner',
    establishment_name TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Crear tabla EVALUATIONS (evaluaciones PA/PO)
CREATE TABLE IF NOT EXISTS evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fecha DATE DEFAULT CURRENT_DATE,
    general_pct FLOAT,
    pa_pct FLOAT,
    po_pct FLOAT,
    evaluaciones_pa JSONB DEFAULT '{}',
    evaluaciones_po JSONB DEFAULT '{}',
    pa_breakdown JSONB DEFAULT '{}',
    po_breakdown JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Crear tabla ACTION_PLANS (planes de acción)
CREATE TABLE IF NOT EXISTS action_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id UUID REFERENCES evaluations(id) ON DELETE CASCADE,
    element TEXT NOT NULL,
    action TEXT NOT NULL,
    responsible TEXT,
    due_date DATE,
    status TEXT DEFAULT 'pendiente' CHECK (status IN ('pendiente', 'en_progreso', 'completada')),
    priority TEXT DEFAULT 'media' CHECK (priority IN ('alta', 'media', 'baja')),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================================================
-- Deshabilitar RLS para acceso público (sin auth)
-- ============================================================================
ALTER TABLE profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE evaluations DISABLE ROW LEVEL SECURITY;
ALTER TABLE action_plans DISABLE ROW LEVEL SECURITY;

-- ============================================================================
-- Insertar datos de ejemplo (opcional - borrar si no querés)
-- ============================================================================

-- Insertar un profile por defecto para el guest user
INSERT INTO profiles (id, email, full_name, role, establishment_name)
VALUES ('00000000-0000-0000-0000-000000000000', 'guest@local', 'Guest User', 'owner', NULL)
ON CONFLICT (id) DO NOTHING;

-- ============================================================================
-- Verificación: listar tablas y sus RLS
-- ============================================================================
-- SELECT tablename, rowlevelsecurity FROM pg_tables WHERE schemaname = 'public';
-- SELECT table_name, row_security FROM information_schema.tables WHERE table_schema = 'public';