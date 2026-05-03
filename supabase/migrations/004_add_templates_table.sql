-- Create evaluation_templates table for storing reusable evaluation configurations

CREATE TABLE IF NOT EXISTS evaluation_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    pa_config JSONB DEFAULT '{"selected_aspects": [], "questions": []}'::jsonb,
    po_config JSONB DEFAULT '{"selected_aspects": [], "questions": []}'::jsonb,
    is_public BOOLEAN DEFAULT false,
    created_by UUID REFERENCES profiles(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_templates_created_by ON evaluation_templates(created_by);
CREATE INDEX IF NOT EXISTS idx_templates_is_public ON evaluation_templates(is_public);

-- Enable RLS
ALTER TABLE evaluation_templates ENABLE ROW LEVEL SECURITY;

-- RLS policies: users can see their own templates + public templates
CREATE POLICY "Users can view own templates" ON evaluation_templates
    FOR SELECT USING (created_by = auth.uid() OR is_public = true);

CREATE POLICY "Users can insert own templates" ON evaluation_templates
    FOR INSERT WITH CHECK (created_by = auth.uid());

CREATE POLICY "Users can update own templates" ON evaluation_templates
    FOR UPDATE USING (created_by = auth.uid());

CREATE POLICY "Users can delete own templates" ON evaluation_templates
    FOR DELETE USING (created_by = auth.uid());

-- Add updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_evaluation_templates_updated_at
    BEFORE UPDATE ON evaluation_templates
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();