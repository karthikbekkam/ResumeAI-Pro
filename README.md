# 🚀 ResumeAI Pro

<div align="center">

# AI-Powered Resume Analysis & Career Assistant

Analyze resumes, calculate ATS scores, receive AI-powered feedback, match resumes with job descriptions, and prepare for interviews—all in one platform.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-black)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-orange)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

# 📖 Project Overview

ResumeAI Pro is a full-stack web application that helps students and job seekers analyze and improve their resumes using Artificial Intelligence.

Users can upload their resumes, receive ATS-style analysis, AI-generated feedback, compare resumes with job descriptions, generate interview questions, and track their resume improvement history.

The application is built using Flask with a modular architecture and follows real-world software engineering practices.

---

# ✨ Features

## 🔐 Authentication

- User Registration
- Secure Login
- JWT Authentication
- Password Hashing (Bcrypt)
- User Profile
- Role-Based Access

---

## 📄 Resume Management

- Upload PDF Resume
- Upload DOCX Resume
- Resume History
- Resume Parsing
- Delete Resume
- Resume Storage

---

## 📊 ATS Resume Analysis

The system evaluates:

- Resume Structure
- Contact Information
- Professional Summary
- Technical Skills
- Projects
- Work Experience
- Education
- Certifications
- Resume Formatting
- ATS Keywords
- Readability

Provides:

- ATS Score
- Strengths
- Weaknesses
- Missing Skills
- Improvement Suggestions

---

## 🤖 AI Resume Review

Powered by Google Gemini AI.

Generates:

- Professional Resume Feedback
- Resume Improvement Suggestions
- Better Professional Summary
- Improved Project Descriptions
- Career Recommendations
- Skill Recommendations

---

## 💼 Job Matching

Compare an uploaded resume with a job description.

Provides:

- Job Match Percentage
- Matched Skills
- Missing Skills
- Missing Keywords
- Improvement Suggestions

---

## 🎯 Interview Preparation

Generate interview questions based on:

- Resume Skills
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
- ATS Reports
- Job Match Reports
- AI Analysis History
- Charts & Analytics

---

## 👨‍💼 Admin Panel

- Dashboard
- User Management
- Resume Management
- Analytics
- Reports

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

- SQL Database
- SQLAlchemy ORM

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

backend/
│
├── models/
├── routes/
├── services/
├── utils/
├── uploads/
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
└── .env.example

frontend/
│
├── static/
└── templates/

database/
│
└── resumeai.sql

README.md
LICENSE
Procfile
render.yaml
.gitignore
```

---

# 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/karthikbekkam/ResumeAI-Pro.git
```

```bash
cd ResumeAI-Pro
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

### Configure Environment Variables

Rename

```
backend/.env.example
```

to

```
backend/.env
```

Update:

- Secret Key
- JWT Secret
- Database Connection
- Gemini API Key

---

### Create Database

Import:

```
database/resumeai.sql
```

Update the database configuration in:

```
backend/config.py
```

---

### Run the Application

```bash
cd backend
```

```bash
python app.py
```

Open:

```
http://localhost:5000
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

# 📸 Screenshots

Add screenshots after deployment.

Example:

- Home Page
- Login
- Dashboard
- Resume Upload
- ATS Analysis
- AI Review
- Job Matching
- Interview Questions
- Admin Dashboard

---

# 🌐 Deployment

This project is ready for deployment on platforms such as:

- Render
- Railway

---

# 🚀 Future Improvements

- Resume Version History
- AI Cover Letter Generator
- Resume Templates
- LinkedIn Profile Analysis
- Email Notifications
- Multi-language Support
- Dark Mode

---

# 👨‍💻 Author

**Bekkam Karthik**

Computer Science & Engineering Student

**GitHub:**  
https://github.com/karthikbekkam

**LinkedIn:**  
(Add your LinkedIn profile URL)

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

Made with ❤️ using Flask, SQLAlchemy, Bootstrap, and Google Gemini AI.

</div>