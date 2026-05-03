-- Enable pg_cron extension
-- This requires Supabase Pro plan or pg_cron add-on

CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Schedule: Daily at 09:00 UTC check for due notifications
-- The check-due-notifications edge function handles the actual logic
--
-- Note: This uses pg_cron for scheduling. Alternative approaches:
-- 1. Supabase's built-in cron (if available in your plan)
-- 2. External scheduler (GitHub Actions, Railway scheduled deployments, etc.)
--
-- To schedule manually via SQL:
-- SELECT cron.schedule(
--   'check-due-notifications',
--   '0 9 * * *',  -- 9:00 AM UTC every day
--   $$
--   SELECT net.http_post(
--     url := 'YOUR_SUPABASE_URL/functions/v1/check-due-notifications',
--     headers := '{"Authorization": "Bearer YOUR_SERVICE_ROLE_KEY", "Content-Type": "application/json"}'
--   );
--   $$
-- );

-- View scheduled jobs
-- SELECT * FROM cron.job;

-- To unschedule:
-- SELECT cron.unschedule('check-due-notifications');