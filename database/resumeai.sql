-- ==========================================================
-- ResumeAI Pro Database Schema (PostgreSQL DDL)
-- ==========================================================

-- Drop tables if exists (Cascade)
DROP TABLE IF EXISTS activity_logs CASCADE;
DROP TABLE IF EXISTS interview_preps CASCADE;
DROP TABLE IF EXISTS job_matches CASCADE;
DROP TABLE IF EXISTS ats_reports CASCADE;
DROP TABLE IF EXISTS resumes CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    target_role VARCHAR(100),
    bio TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- 2. Resumes Table
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(20) NOT NULL,
    file_size INT NOT NULL,
    raw_text TEXT,
    ats_score FLOAT DEFAULT 0.0,
    upload_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_resumes_user_id ON resumes(user_id);

-- 3. ATS Reports Table
CREATE TABLE ats_reports (
    id SERIAL PRIMARY KEY,
    resume_id INT NOT NULL UNIQUE REFERENCES resumes(id) ON DELETE CASCADE,
    overall_score FLOAT NOT NULL DEFAULT 0.0,
    skills_score FLOAT DEFAULT 0.0,
    experience_score FLOAT DEFAULT 0.0,
    formatting_score FLOAT DEFAULT 0.0,
    education_score FLOAT DEFAULT 0.0,
    extracted_skills_json TEXT,
    missing_keywords_json TEXT,
    formatting_feedback_json TEXT,
    ai_suggestions_json TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ats_reports_resume_id ON ats_reports(resume_id);

-- 4. Job Matches Table
CREATE TABLE job_matches (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    resume_id INT NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    job_title VARCHAR(255) NOT NULL,
    job_description TEXT NOT NULL,
    match_percentage FLOAT NOT NULL DEFAULT 0.0,
    matched_skills_json TEXT,
    missing_skills_json TEXT,
    recommendations_json TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_job_matches_user_id ON job_matches(user_id);
CREATE INDEX idx_job_matches_resume_id ON job_matches(resume_id);

-- 5. Interview Preps Table
CREATE TABLE interview_preps (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    resume_id INT NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    target_role VARCHAR(150) NOT NULL,
    difficulty VARCHAR(20) NOT NULL DEFAULT 'Medium',
    questions_json TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_interview_preps_user_id ON interview_preps(user_id);
CREATE INDEX idx_interview_preps_resume_id ON interview_preps(resume_id);

-- 6. Activity Logs Table
CREATE TABLE activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,
    description TEXT,
    ip_address VARCHAR(50),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_activity_logs_user_id ON activity_logs(user_id);

-- Default Admin Seed (Password: Admin@123456 - Bcrypt hash)
INSERT INTO users (email, password_hash, full_name, role, target_role, bio) 
VALUES (
    'admin@resumeai.pro',
    '$2b$12$KIXp.jF7yR36dYpI3H4gDeu8mO8v7.K5.8c5n6.o4y6.q.Q.e.W.S', 
    'System Administrator',
    'admin',
    'Lead Platform Admin',
    'Default ResumeAI Pro Administrator account.'
);
