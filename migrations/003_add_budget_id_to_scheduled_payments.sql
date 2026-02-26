-- Migration: Add budget_id column to scheduled_payments table
-- Allows payments to be scoped to a budget persona (dad, mom, house)
-- NULL = visible on all budget calendars
ALTER TABLE scheduled_payments ADD COLUMN IF NOT EXISTS budget_id VARCHAR(20);
