-- supabase/migrations/006_seed_industry_benchmarks.sql
-- Industry benchmarking database for restaurant/food service sector

CREATE TABLE IF NOT EXISTS industry_benchmarks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sector TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('PA', 'PO')),
    aspect TEXT NOT NULL,
    avg_score FLOAT NOT NULL CHECK (avg_score >= 0 AND avg_score <= 100),
    p25 FLOAT NOT NULL CHECK (p25 >= 0 AND p25 <= 100),
    p75 FLOAT NOT NULL CHECK (p75 >= 0 AND p75 <= 100),
    sample_size INTEGER NOT NULL DEFAULT 0,
    source TEXT DEFAULT 'GPP Internal Research 2024',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(sector, category, aspect)
);

-- Enable RLS
ALTER TABLE industry_benchmarks ENABLE ROW LEVEL SECURITY;

-- RLS policy: public read for all authenticated users
CREATE POLICY "Anyone can view benchmarks" ON industry_benchmarks
    FOR SELECT USING (true);

-- Seed data for restaurant/food service sector
INSERT INTO industry_benchmarks (sector, category, aspect, avg_score, p25, p75, sample_size, source) VALUES
-- PA (Administración) aspects
('restaurant', 'PA', 'DIRECCIÓN', 65.0, 52.0, 78.0, 342, 'GPP Internal Research 2024'),
('restaurant', 'PA', 'PLANEACIÓN', 62.0, 48.0, 75.0, 342, 'GPP Internal Research 2024'),
('restaurant', 'PA', 'ORGANIZACIÓN', 60.0, 45.0, 74.0, 342, 'GPP Internal Research 2024'),
('restaurant', 'PA', 'INTEGRACIÓN', 58.0, 43.0, 72.0, 342, 'GPP Internal Research 2024'),
('restaurant', 'PA', 'DIRECCIÓN', 67.0, 54.0, 80.0, 298, 'GPP Internal Research 2024'),
('restaurant', 'PA', 'CONTROL', 60.0, 46.0, 73.0, 342, 'GPP Internal Research 2024'),

-- PO (Operaciones) aspects
('restaurant', 'PO', 'LOGÍSTICA', 68.0, 55.0, 81.0, 298, 'GPP Internal Research 2024'),
('restaurant', 'PO', 'PRODUCCIÓN', 63.0, 50.0, 76.0, 298, 'GPP Internal Research 2024'),
('restaurant', 'PO', 'EXTERNA', 58.0, 44.0, 72.0, 298, 'GPP Internal Research 2024'),
('restaurant', 'PO', 'CALIDAD', 65.0, 52.0, 78.0, 298, 'GPP Internal Research 2024'),
('restaurant', 'PO', 'SERVICIO', 70.0, 58.0, 82.0, 298, 'GPP Internal Research 2024'),
('restaurant', 'PO', 'COSTOS', 61.0, 47.0, 74.0, 298, 'GPP Internal Research 2024');