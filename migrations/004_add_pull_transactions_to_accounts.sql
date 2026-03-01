-- Migration: Add pull_transactions flag to accounts table
-- When enabled, the previous 24h of transactions are pulled and shown on the dashboard
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS pull_transactions BOOLEAN DEFAULT FALSE;
