-- Migration: Add display_name column to accounts table
-- Run this with: mise run postgres-shell
-- Then paste this command at the psql prompt

ALTER TABLE accounts ADD COLUMN IF NOT EXISTS display_name VARCHAR;

-- Verify the column was added
\d accounts
