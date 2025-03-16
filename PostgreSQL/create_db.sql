CREATE DATABASE postgres;
CREATE USER postgres WITH PASSWORD password;
GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;

\c user_analytics

CREATE SCHEMA IF NOT EXISTS STG;
CREATE SCHEMA IF NOT EXISTS DM;
SET search_path TO STG;
ALTER DEFAULT PRIVILEGES IN SCHEMA STG GRANT ALL PRIVILEGES ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA DM GRANT ALL PRIVILEGES ON TABLES TO postgres;

-- Таблица для хранения сессий пользователей
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id VARCHAR(20) NOT NULL PRIMARY KEY,
    user_id VARCHAR(20) NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    pages_visited TEXT[],
    device VARCHAR(50),
    actions TEXT[]
);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_device ON user_sessions(device);

-- Таблица для истории изменения цен товаров
CREATE TABLE IF NOT EXISTS product_price_history (
    product_id VARCHAR(20) NOT NULL PRIMARY KEY,
    price_changes TEXT[],
    current_price DECIMAL(10,2),
    currency VARCHAR(3)
);

-- Таблица для логов событий
CREATE TABLE IF NOT EXISTS event_logs (
    event_id VARCHAR(20) NOT NULL PRIMARY KEY,
    timestamp TIMESTAMP,
    event_type VARCHAR(50),
    details TEXT
);

CREATE INDEX idx_event_logs_event_type ON event_logs(event_type);

-- Таблица для обращений в поддержку
CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id VARCHAR(20) NOT NULL PRIMARY KEY,
    user_id VARCHAR(20) NOT NULL,
    status VARCHAR(50),
    issue_type VARCHAR(50),
    messages TEXT[],
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE INDEX idx_support_tickets_status ON support_tickets(status);

-- Таблица для рекомендаций пользователям
CREATE TABLE IF NOT EXISTS user_recommendations (
    user_id VARCHAR(20) NOT NULL,
    recommended_products TEXT[],
    last_updated TIMESTAMP
);

-- Таблица для очереди модерации отзывов
CREATE TABLE IF NOT EXISTS moderation_queue (
    review_id VARCHAR(20) NOT NULL PRIMARY KEY,
    user_id VARCHAR(20) NOT NULL,
    product_id VARCHAR,
    review_text TEXT,
    rating INTEGER,
    moderation_status VARCHAR(20),
    flags TEXT[],
    submitted_at TIMESTAMP
);

-- Таблица для хранения поисковых запросов
CREATE TABLE IF NOT EXISTS search_queries (
    query_id VARCHAR(20) NOT NULL PRIMARY KEY,
    user_id VARCHAR(20) NOT NULL,
    query_text TEXT,
    timestamp TIMESTAMP,
    filters TEXT[],
    results_count INTEGER
);

CREATE INDEX idx_search_queries_user_id ON search_queries(user_id);
