# ResumeAI Pro

<div align="center">

# 🚀 ResumeAI Pro
### AI-Powered Resume Analysis & Career Assistant

Analyze resumes, calculate ATS scores, receive AI-powered feedback, match resumes with job descriptions, and prepare for interviews—all in one application.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-orange)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

# 📖 Overview

ResumeAI Pro is a full-stack web application that helps job seekers improve their resumes using Artificial Intelligence.

The application accepts PDF and DOCX resumes, extracts important information, evaluates resume quality using ATS-style analysis, provides AI-powered suggestions through Google Gemini, compares resumes with job descriptions, and generates interview questions based on the uploaded resume.

The project is built with Flask and PostgreSQL using a modular architecture and is designed to demonstrate real-world software engineering practices.

---

# ✨ Key Features

## 👤 User Authentication

- User Registration
- Secure Login
- Password Encryption using Bcrypt
- JWT Authentication
- User Profile
- Role-Based Access

---

## 📄 Resume Management

- Upload PDF Resume
- Upload DOCX Resume
- Resume History
- Resume Storage
- Resume Parsing
- Delete Resume

---

## 📊 ATS Resume Analysis

- ATS Score (0–100)
- Resume Structure Analysis
- Keyword Analysis
- Skills Analysis
- Resume Formatting Check
- Readability Analysis
- Grammar Suggestions
- Missing Section Detection

---

## 🤖 AI Resume Review

Powered by Google Gemini AI

Generates:

- Professional Resume Review
- Resume Improvement Suggestions
- Better Professional Summary
- Improved Project Descriptions
- Career Recommendations
- Skill Recommendations

---

## 💼 Job Matching

Compare uploaded resume with a job description.

Provides:

- Match Percentage
- Matched Skills
- Missing Skills
- Missing Keywords
- Improvement Suggestions

---

## 🎯 Interview Preparation

Generate interview questions based on:

- Skills
- Projects
- Technologies
- Experience

Includes:

- Technical Questions
- HR Questions
- Behavioral Questions

---

## 📈 Dashboard

Displays:

- Resume History
- ATS Scores
- Job Matches
- AI Analysis History
- Charts & Analytics

---

## 👨‍💼 Admin Panel

- Dashboard
- User Management
- Resume Management
- Reports
- Analytics

---

# 🛠️ Tech Stack

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Jinja2 Templates
- Chart.js
- Font Awesome

---

## Backend

- Python
- Flask
- Flask Blueprints
- SQLAlchemy
- Flask JWT Extended
- Flask Bcrypt
- Flask CORS

---

## Database

- PostgreSQL

---

## Artificial Intelligence

- Google Gemini API

---

## Resume Parsing

- PyMuPDF
- python-docx

---

# 📂 Project Structure

```text
ResumeAI-Pro/

│── backend/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── uploads/
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── requirements.txt
│   └── .env.example

│── frontend/
│   ├── static/
│   └── templates/

│── database/
│   └── resumeai.sql

│── README.md
│── LICENSE
│── Procfile
│── render.yaml
│── .gitignore
```

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/karthikbekkam/ResumeAI-Pro.git
```

```bash
cd ResumeAI-Pro
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## 4. Configure Environment Variables

Rename

```
.env.example
```

to

```
.env
```

Update

- Database URL
- Secret Keys
- Gemini API Key

---

## 5. Create Database

Import

```
database/resumeai.sql
```

into PostgreSQL.

---

## 6. Run Application

```bash
cd backend
```

```bash
python app.py
```

Server

```
http://localhost:5000
```

---

# 📸 Screenshots

Add screenshots here after deployment.

```
docs/

home.png

login.png

dashboard.png

upload.png

analysis.png

job-match.png

admin-dashboard.png
```

---

# 🔒 Security Features

- Password Hashing
- JWT Authentication
- Input Validation
- Secure File Upload
- SQL Injection Protection
- Environment Variables

---

# 📌 Future Improvements

- Resume Version History
- Resume Templates
- AI Cover Letter Generator
- LinkedIn Profile Analyzer
- Resume PDF Export
- Multi-language Support
- Email Notifications
- Dark Mode

---

# 🌐 Deployment

The project is ready for deployment on:

- Render
- Railway

---

# 👨‍💻 Author

**Bekkam Karthik**

Computer Science & Engineering Student

GitHub

https://github.com/karthikbekkam

LinkedIn

(Add your LinkedIn URL)

---

# 📄 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork the repository

💡 Share your feedback

---

<div align="center">

Made with ❤️ using Flask, PostgreSQL, Bootstrap and Google Gemini AI

</div>