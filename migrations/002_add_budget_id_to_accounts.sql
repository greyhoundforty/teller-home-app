-- Migration: Add budget_id column to accounts table
-- Valid values: 'dad', 'mom', 'house', NULL (unassigned)
ALTER TABLE accounts ADD COLUMN IF NOT EXISTS budget_id VARCHAR(20);
