-- ESG Data Tracker - Database Tables
-- Run this in your Supabase SQL Editor

-- Companies table
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    industry VARCHAR(100),
    market_cap BIGINT,
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ESG Scores table
CREATE TABLE IF NOT EXISTS esg_scores (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    environmental_score FLOAT,
    social_score FLOAT,
    governance_score FLOAT,
    overall_score FLOAT,
    data_source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- News table
CREATE TABLE IF NOT EXISTS news (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT,
    url TEXT,
    sentiment_score FLOAT,
    source VARCHAR(100),
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Metrics table
CREATE TABLE IF NOT EXISTS metrics (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    value FLOAT,
    data_source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_companies_ticker ON companies(ticker);
CREATE INDEX IF NOT EXISTS idx_esg_scores_company_id ON esg_scores(company_id);
CREATE INDEX IF NOT EXISTS idx_esg_scores_created_at ON esg_scores(created_at);
CREATE INDEX IF NOT EXISTS idx_news_company_id ON news(company_id);
CREATE INDEX IF NOT EXISTS idx_news_created_at ON news(created_at);
CREATE INDEX IF NOT EXISTS idx_metrics_company_id ON metrics(company_id);

-- Enable Row Level Security (RLS)
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE esg_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE news ENABLE ROW LEVEL SECURITY;
ALTER TABLE metrics ENABLE ROW LEVEL SECURITY;

-- Create policies to allow public read access
CREATE POLICY "Allow public read access on companies" ON companies FOR SELECT USING (true);
CREATE POLICY "Allow public read access on esg_scores" ON esg_scores FOR SELECT USING (true);
CREATE POLICY "Allow public read access on news" ON news FOR SELECT USING (true);
CREATE POLICY "Allow public read access on metrics" ON metrics FOR SELECT USING (true);

-- Allow public insert for data collection
CREATE POLICY "Allow public insert on companies" ON companies FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public insert on esg_scores" ON esg_scores FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public insert on news" ON news FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public insert on metrics" ON metrics FOR INSERT WITH CHECK (true);

-- Create a function to update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for companies table
CREATE TRIGGER update_companies_updated_at 
    BEFORE UPDATE ON companies 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO companies (ticker, name, sector, industry, market_cap, country) VALUES
('AAPL', 'Apple Inc.', 'Technology', 'Consumer Electronics', 3200000000000, 'USA'),
('MSFT', 'Microsoft Corporation', 'Technology', 'Software', 3100000000000, 'USA'),
('GOOGL', 'Alphabet Inc.', 'Technology', 'Internet Services', 2000000000000, 'USA'),
('TSLA', 'Tesla, Inc.', 'Consumer Discretionary', 'Electric Vehicles', 900000000000, 'USA'),
('NVDA', 'NVIDIA Corporation', 'Technology', 'Semiconductors', 1500000000000, 'USA')
ON CONFLICT (ticker) DO NOTHING;

-- Insert sample ESG scores
INSERT INTO esg_scores (company_id, environmental_score, social_score, governance_score, overall_score, data_source)
SELECT 
    c.id,
    CASE c.ticker
        WHEN 'AAPL' THEN 75.5
        WHEN 'MSFT' THEN 85.2
        WHEN 'GOOGL' THEN 81.0
        WHEN 'TSLA' THEN 92.0
        WHEN 'NVDA' THEN 73.2
    END,
    CASE c.ticker
        WHEN 'AAPL' THEN 82.3
        WHEN 'MSFT' THEN 88.1
        WHEN 'GOOGL' THEN 84.5
        WHEN 'TSLA' THEN 88.5
        WHEN 'NVDA' THEN 79.1
    END,
    CASE c.ticker
        WHEN 'AAPL' THEN 77.8
        WHEN 'MSFT' THEN 85.0
        WHEN 'GOOGL' THEN 80.2
        WHEN 'TSLA' THEN 93.1
        WHEN 'NVDA' THEN 76.5
    END,
    CASE c.ticker
        WHEN 'AAPL' THEN 78.5
        WHEN 'MSFT' THEN 86.1
        WHEN 'GOOGL' THEN 81.9
        WHEN 'TSLA' THEN 91.2
        WHEN 'NVDA' THEN 76.3
    END,
    'Sample Data'
FROM companies c;

-- Insert sample news
INSERT INTO news (company_id, title, content, url, sentiment_score, source, published_at)
SELECT 
    c.id,
    CASE c.ticker
        WHEN 'AAPL' THEN 'Apple Announces New Sustainability Initiative'
        WHEN 'TSLA' THEN 'Tesla Leads in Electric Vehicle ESG Performance'
        WHEN 'MSFT' THEN 'Microsoft Achieves Carbon Negative Goal'
    END,
    CASE c.ticker
        WHEN 'AAPL' THEN 'Apple Inc. today announced ambitious new environmental goals for carbon neutrality by 2030...'
        WHEN 'TSLA' THEN 'Tesla continues to set standards in environmental sustainability with their electric vehicle leadership...'
        WHEN 'MSFT' THEN 'Microsoft has successfully achieved its carbon negative goals ahead of schedule...'
    END,
    'https://example.com/' || LOWER(c.ticker) || '-sustainability',
    CASE c.ticker
        WHEN 'AAPL' THEN 0.85
        WHEN 'TSLA' THEN 0.92
        WHEN 'MSFT' THEN 0.88
    END,
    CASE c.ticker
        WHEN 'AAPL' THEN 'Reuters'
        WHEN 'TSLA' THEN 'Bloomberg'
        WHEN 'MSFT' THEN 'TechCrunch'
    END,
    CURRENT_TIMESTAMP - INTERVAL '1 day'
FROM companies c
WHERE c.ticker IN ('AAPL', 'TSLA', 'MSFT');

-- Verify the setup
SELECT 'Companies created:' as status, COUNT(*) as count FROM companies
UNION ALL
SELECT 'ESG scores created:', COUNT(*) FROM esg_scores
UNION ALL
SELECT 'News articles created:', COUNT(*) FROM news; 