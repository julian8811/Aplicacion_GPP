-- Add branding fields to profiles table

-- logo_url already exists from 001_add_auth_fields.sql
-- primary_color already exists from 001_add_auth_fields.sql
-- Add footer_text if not exists
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS footer_text TEXT;