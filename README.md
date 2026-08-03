# ResumeAI Pro 🚀
> **AI-Powered Resume Analysis, ATS Optimization & Job Matching SaaS Platform**

ResumeAI Pro is a full-featured commercial SaaS web application built with Python Flask, Jinja2, Bootstrap 5, PostgreSQL, SQLAlchemy ORM, and Google Gemini AI. It empowers job seekers to analyze their resumes against Applicant Tracking Systems (ATS), match qualifications with job postings, and practice with AI-generated interview questions.

---

## 🌟 Key Features

### 1. 🔐 Security & Role-Based Authentication
- Secure registration and login using **Bcrypt** password hashing.
- Dual authentication system: **Flask Sessions** for Jinja2 views + **Flask JWT Extended** for REST APIs.
- Role-based authorization (`user` and `admin`) with custom `@login_required` and `@admin_required` decorators.
- Default Admin Account: `admin@resumeai.pro` / `Admin@123456`.

### 2. 📄 Resume Text Extraction & ATS Analyzer
- Multi-format text extraction via **PyMuPDF (`fitz`)** for PDFs and **`python-docx`** for DOC/DOCX.
- Hybrid rule-based parsing + NLP taxonomy database evaluating:
  - Technical & Soft Skills Coverage
  - Work Experience & Bullet Point Quality
  - Formatting & Structural Compliance (Length, Email/Phone regex, Bullet point detection)
  - Education & Certifications

### 3. 🤖 Google Gemini AI Integration
- Executive summary critique and bullet-point rewrites.
- High-impact action verb suggestions (e.g. *Spearheaded*, *Architected*, *Optimized*).
- Industry keyword recommendations.

### 4. 🎯 Job Description Matcher
- Paste text or upload job posting documents.
- Calculates exact match percentage score, matched skills badges, missing technical skills, and actionable recommendations.

### 5. 💬 AI Interview Question Generator
- Tailored Technical, HR, Behavioral (STAR method), and Project questions based on candidate credentials.
- Difficulty modes: `Easy`, `Medium`, `Hard`.

### 6. 📊 Interactive Analytics Dashboards
- **User Dashboard**: Metric counter cards, ATS progress line chart, Job fit score bar chart using **Chart.js**, recent activities.
- **Admin Panel**: User management (Search, Filter, Pagination, Delete user), Resume management, platform-wide ATS score distribution doughnut chart.

---

## 🏗️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | HTML5, CSS3 (Glassmorphism), Bootstrap 5, Vanilla JavaScript, Jinja2, Chart.js, Font Awesome |
| **Backend** | Python 3.10+, Flask, Blueprint Architecture, Flask-SQLAlchemy, Flask-Bcrypt, Flask-JWT-Extended |
| **Database** | PostgreSQL (PostgreSQL DDL schema included) / SQLite local fallback |
| **AI / NLP** | Google Gemini API (`google-genai`), PyMuPDF (`fitz`), `python-docx` |
| **Deployment** | Gunicorn, Render (`render.yaml`), Railway (`Procfile`) |

---

## 📂 Directory Structure

```
ResumeAI-Pro/
├── backend/
│   ├── app.py                     # Application factory & blueprint registration
│   ├── config.py                  # Environment & App configuration
│   ├── extensions.py              # Flask extensions (db, bcrypt, jwt, cors)
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Environment variables template
│   ├── models/                    # SQLAlchemy ORM Models
│   │   ├── user.py
│   │   ├── resume.py
│   │   ├── ats_report.py
│   │   ├── job_match.py
│   │   ├── interview.py
│   │   └── activity.py
│   ├── routes/                    # Blueprints
│   │   ├── auth_routes.py
│   │   ├── main_routes.py
│   │   ├── resume_routes.py
│   │   ├── job_routes.py
│   │   ├── interview_routes.py
│   │   ├── dashboard_routes.py
│   │   └── admin_routes.py
│   ├── services/                  # Business Logic
│   │   ├── file_parser.py         # PyMuPDF & python-docx parser
│   │   ├── ats_analyzer.py        # ATS Scoring engine & Skill taxonomy
│   │   ├── gemini_service.py      # Google Gemini AI Service
│   │   └── auth_service.py        # Authentication & Activity Logger
│   └── utils/                     # Helpers & Decorators
│       ├── helpers.py
│       └── decorators.py
├── frontend/
│   ├── templates/                 # Jinja2 HTML Templates
│   │   ├── layouts/               # Base layouts (base, navbar, footer)
│   │   ├── home/                  # Landing page
│   │   ├── auth/                  # Login, Register, Profile
│   │   ├── resume/                # Upload, Detail, History
│   │   ├── dashboard/             # User Dashboard
│   │   ├── admin/                 # Admin Panel & Tables
│   │   ├── job/                   # Job Matcher & Results
│   │   └── interview/             # Interview Generator & Q&A
│   └── static/
│       ├── css/                   # Glassmorphism & Custom CSS
│       └── js/                    # Chart.js & File Upload Handlers
├── database/
│   └── resumeai.sql               # PostgreSQL Schema & Seed script
├── Procfile                       # Gunicorn deployment config
├── render.yaml                    # Render Cloud deployment specification
├── README.md                      # Project documentation
├── .gitignore
└── LICENSE
```

---

## ⚡ Quick Start & Installation

### 1. Prerequisites
- Python 3.10 or higher
- PostgreSQL (or SQLite for quick local test)

### 2. Clone & Setup Environment
```bash
git clone https://github.com/your-username/ResumeAI-Pro.git
cd ResumeAI-Pro/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables Setup
Copy `.env.example` to `.env` inside `backend/` and update your settings:
```bash
cp .env.example .env
```
Set your Google Gemini API Key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/resumeai_db
```

### 4. Run Development Server
```bash
python app.py
```
Open your browser at `http://127.0.0.1:5000`.

---

## 🛢️ Database Schema (PostgreSQL)

The relational database comprises 6 interconnected tables:
1. `users`: Stores credentials, hashed passwords, roles (`user`/`admin`), and target roles.
2. `resumes`: Tracks uploaded files, raw parsed text, file sizes, and ATS overall scores.
3. `ats_reports`: Stores category sub-scores (Skills, Experience, Formatting, Education) and JSON payloads for extracted skills and AI critique.
4. `job_matches`: Stores job description text, match percentages, matched/missing skills.
5. `interview_preps`: Stores categorized technical, HR, behavioral, and project interview Q&As.
6. `activity_logs`: Audit trail logging user logins, profile updates, and file uploads.

---

## 📡 REST API Documentation

### Auth & User Endpoints
- `POST /auth/register` - Register new user account.
- `POST /auth/login` - Authenticate user & return JWT token.
- `GET /auth/api/me` - Get current authenticated user profile.

### Resume & ATS Endpoints
- `POST /resume/upload` - Upload PDF/DOCX file and execute ATS analysis.
- `GET /resume/history` - List user uploaded resumes (JSON / HTML).
- `GET /resume/<id>` - Fetch specific resume detail & ATS breakdown report.
- `DELETE /resume/delete/<id>` - Delete resume file and database record.

### Job Matcher & Interview Endpoints
- `POST /job/match` - Run AI job comparison between resume and job description.
- `POST /interview/generator` - Generate interview questions based on resume credentials.

### Admin Endpoints
- `GET /admin/users` - Paginated user accounts list with search filter.
- `GET /admin/resumes` - Paginated resume list across all users.
- `GET /admin/api/analytics` - System ATS distribution and platform statistics.

---

## 🚀 Deployment Guide

### Deploying to Render
1. Push your repository to GitHub.
2. Connect repository to **Render**.
3. Render automatically detects `render.yaml`.
4. Set environment variable `GEMINI_API_KEY` in Render dashboard.

### Deploying to Railway
1. Create new project on **Railway**.
2. Deploy from GitHub Repo.
3. Railway automatically detects `Procfile` (`gunicorn --chdir backend app:app`).
4. Add PostgreSQL database plugin in Railway.

---

## 💡 Technical Interview Talking Points

- **Why Flask Blueprint Architecture?** Ensures clean separation of concerns, scalability, and easy modular testing.
- **Dual Session & JWT Strategy**: Combines server-side session management for traditional Jinja rendering with stateless JWT bearer tokens for asynchronous REST API clients.
- **Resilient Fallback Design**: If the Gemini API hits rate limits or missing credentials, the system gracefully falls back to rule-based NLP extraction without throwing 500 runtime errors.
- **Security Best Practices**: Bcrypt password hashing, parameter binding in SQLAlchemy to prevent SQL Injection, safe filename sanitization, and strict extension & size checks.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
