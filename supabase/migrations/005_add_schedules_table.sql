-- supabase/migrations/005_add_schedules_table.sql
-- Table for recurring evaluation reminders

CREATE TABLE IF NOT EXISTS evaluation_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    frequency TEXT NOT NULL CHECK (frequency IN ('monthly', 'quarterly', 'biannual', 'annual')),
    next_due TIMESTAMPTZ NOT NULL,
    reminder_days_before INTEGER DEFAULT 7,
    active BOOLEAN DEFAULT true,
    created_by UUID REFERENCES profiles(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for checking due schedules
CREATE INDEX idx_evaluation_schedules_next_due ON evaluation_schedules(next_due) WHERE active = true;
CREATE INDEX idx_evaluation_schedules_created_by ON evaluation_schedules(created_by);

-- Enable RLS
ALTER TABLE evaluation_schedules ENABLE ROW LEVEL SECURITY;

-- RLS policies: users see only their own schedules
CREATE POLICY "Users can view own schedules" ON evaluation_schedules
    FOR SELECT USING (auth.uid() = created_by);

CREATE POLICY "Users can insert own schedules" ON evaluation_schedules
    FOR INSERT WITH CHECK (auth.uid() = created_by);

CREATE POLICY "Users can update own schedules" ON evaluation_schedules
    FOR UPDATE USING (auth.uid() = created_by);

CREATE POLICY "Users can delete own schedules" ON evaluation_schedules
    FOR DELETE USING (auth.uid() = created_by);

-- Updated at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_evaluation_schedules_updated_at
    BEFORE UPDATE ON evaluation_schedules
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();