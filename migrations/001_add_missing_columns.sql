-- Migration 001: Add missing columns from previous development sessions
-- Created: 2026-01-30
-- Purpose: Sync PostgreSQL schema with SQLAlchemy models

-- Add display_name to accounts table (custom account names)
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS display_name VARCHAR;

-- Add subscription-related columns to scheduled_payments table
ALTER TABLE scheduled_payments ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT TRUE;
ALTER TABLE scheduled_payments ADD COLUMN IF NOT EXISTS frequency VARCHAR DEFAULT 'monthly';
ALTER TABLE scheduled_payments ADD COLUMN IF NOT EXISTS email VARCHAR;

-- Verify changes
\echo 'Migration complete! Verify with:'
\echo '\d accounts'
\echo '\d scheduled_payments'
