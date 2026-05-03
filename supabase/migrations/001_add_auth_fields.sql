-- Add auth-related fields to profiles table

ALTER TABLE profiles ADD COLUMN IF NOT EXISTS role TEXT DEFAULT 'editor';
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS email TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS last_login TIMESTAMPTZ;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS logo_url TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS primary_color TEXT;