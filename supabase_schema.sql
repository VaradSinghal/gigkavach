-- GigKavach Supabase Schema Setup
-- Run this in your Supabase SQL Editor

-- 1. Create Workers Table
CREATE TABLE IF NOT EXISTS workers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    worker_id TEXT UNIQUE NOT NULL,
    city TEXT NOT NULL,
    zone TEXT NOT NULL,
    primary_platform TEXT NOT NULL,
    secondary_platform TEXT,
    vehicle_type TEXT NOT NULL,
    avg_daily_hours NUMERIC,
    experience_weeks INTEGER,
    trust_score NUMERIC,
    avg_daily_income NUMERIC,
    avg_weekly_income NUMERIC,
    claim_count INTEGER DEFAULT 0,
    claim_rate NUMERIC DEFAULT 0.0,
    total_payout NUMERIC DEFAULT 0.0,
    is_flood_zone BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create Active Policies Table
CREATE TABLE IF NOT EXISTS policies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    policy_id TEXT UNIQUE NOT NULL,
    worker_id TEXT REFERENCES workers(worker_id) ON DELETE CASCADE,
    tier TEXT NOT NULL,
    weekly_premium NUMERIC NOT NULL,
    coverage_percentage NUMERIC NOT NULL,
    coverage_ceiling NUMERIC NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT NOT NULL,
    premium_breakdown JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create Claims Table
CREATE TABLE IF NOT EXISTS claims (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    claim_id TEXT UNIQUE NOT NULL,
    worker_id TEXT REFERENCES workers(worker_id) ON DELETE CASCADE,
    zone TEXT NOT NULL,
    city TEXT NOT NULL,
    trigger_type TEXT NOT NULL,
    trigger_label TEXT NOT NULL,
    trigger_data TEXT NOT NULL,
    status TEXT NOT NULL,
    action TEXT,
    confidence_score INTEGER,
    fraud_probability NUMERIC,
    validation_signals JSONB,
    inactive_hours NUMERIC,
    hourly_rate NUMERIC,
    coverage_pct NUMERIC,
    payout_amount NUMERIC,
    timeline JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Create Active Triggers Table (Live environmental alerts)
CREATE TABLE IF NOT EXISTS active_triggers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trigger_id TEXT NOT NULL,
    city TEXT NOT NULL,
    zone TEXT NOT NULL,
    label TEXT NOT NULL,
    threshold TEXT NOT NULL,
    current_value TEXT NOT NULL,
    risk_level NUMERIC NOT NULL,
    status TEXT NOT NULL,
    source TEXT NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(trigger_id, city, zone)
);

-- 5. Create Zone Risks Table (ML Clustering Output)
CREATE TABLE IF NOT EXISTS zone_risks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    city TEXT NOT NULL,
    zone TEXT NOT NULL,
    risk_score NUMERIC NOT NULL,
    risk_label TEXT NOT NULL,
    cluster_id INTEGER NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(city, zone)
);

-- Set Enable Realtime for Flutter and Admin App sync
ALTER PUBLICATION supabase_realtime ADD TABLE claims;
ALTER PUBLICATION supabase_realtime ADD TABLE active_triggers;
ALTER PUBLICATION supabase_realtime ADD TABLE policies;
ALTER PUBLICATION supabase_realtime ADD TABLE zone_risks;
