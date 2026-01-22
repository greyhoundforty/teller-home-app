-- Teller Home App Database Initialization Script
-- This script creates the necessary tables for the application

-- Enable UUID extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Accounts table
CREATE TABLE IF NOT EXISTS accounts (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    display_name VARCHAR(255),
    type VARCHAR(50) NOT NULL,
    subtype VARCHAR(50),
    institution_name VARCHAR(255),
    currency VARCHAR(10) DEFAULT 'USD',
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_accounts_status ON accounts(status);
CREATE INDEX idx_accounts_type ON accounts(type);

-- Balances table
CREATE TABLE IF NOT EXISTS balances (
    id SERIAL PRIMARY KEY,
    account_id VARCHAR(255) NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    available DECIMAL(15, 2) NOT NULL,
    ledger DECIMAL(15, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_balances_account_id ON balances(account_id);
CREATE INDEX idx_balances_timestamp ON balances(timestamp DESC);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id VARCHAR(255) PRIMARY KEY,
    account_id VARCHAR(255) NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    amount DECIMAL(15, 2) NOT NULL,
    date TIMESTAMP NOT NULL,
    description VARCHAR(500) NOT NULL,
    category VARCHAR(100),
    type VARCHAR(50),
    status VARCHAR(50) DEFAULT 'posted',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transactions_account_id ON transactions(account_id);
CREATE INDEX idx_transactions_date ON transactions(date DESC);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_category ON transactions(category);

-- Scheduled Payments table
CREATE TABLE IF NOT EXISTS scheduled_payments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    account_id VARCHAR(255) REFERENCES accounts(id) ON DELETE SET NULL,
    day_of_month INTEGER NOT NULL CHECK (day_of_month BETWEEN 1 AND 31),
    is_active BOOLEAN DEFAULT TRUE,
    is_recurring BOOLEAN DEFAULT TRUE,
    category VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scheduled_payments_active ON scheduled_payments(is_active);
CREATE INDEX idx_scheduled_payments_day ON scheduled_payments(day_of_month);

-- User Enrollments table (for Teller Connect tokens)
CREATE TABLE IF NOT EXISTS user_enrollments (
    id SERIAL PRIMARY KEY,
    enrollment_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    access_token TEXT NOT NULL,  -- Should be encrypted in production
    institution_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_synced TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_enrollments_enrollment_id ON user_enrollments(enrollment_id);
CREATE INDEX idx_user_enrollments_user_id ON user_enrollments(user_id);
CREATE INDEX idx_user_enrollments_active ON user_enrollments(is_active);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to auto-update updated_at
CREATE TRIGGER update_accounts_updated_at BEFORE UPDATE ON accounts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_scheduled_payments_updated_at BEFORE UPDATE ON scheduled_payments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_enrollments_updated_at BEFORE UPDATE ON user_enrollments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create views for common queries
CREATE OR REPLACE VIEW account_summary AS
SELECT 
    a.id,
    a.name,
    a.type,
    a.subtype,
    a.institution_name,
    a.status,
    b.available,
    b.ledger,
    b.timestamp as balance_timestamp,
    (SELECT COUNT(*) FROM transactions WHERE account_id = a.id) as transaction_count
FROM accounts a
LEFT JOIN LATERAL (
    SELECT available, ledger, timestamp
    FROM balances
    WHERE account_id = a.id
    ORDER BY timestamp DESC
    LIMIT 1
) b ON true;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO teller;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO teller;

-- Insert some metadata
CREATE TABLE IF NOT EXISTS db_version (
    version VARCHAR(50) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT INTO db_version (version, description) VALUES 
    ('1.0.0', 'Initial schema with accounts, balances, transactions, and scheduled payments');

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Teller Home App database schema initialized successfully!';
END $$;
