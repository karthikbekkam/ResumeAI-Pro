import re
from services.nlp_analyzer import NLPAnalyzer

# Extensive Skill Taxonomy Database
SKILL_TAXONOMY = {
    "Programming Languages": ["python", "javascript", "typescript", "java", "c++", "c#", "php", "ruby", "go", "golang", "rust", "swift", "kotlin", "sql", "r", "html", "css", "bash"],
    "Frameworks & Libraries": ["flask", "django", "fastapi", "react", "next.js", "vue", "angular", "express", "node.js", "bootstrap", "tailwind", "jquery", "spring", "spring boot", "laravel", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch"],
    "Cloud & DevOps": ["aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "terraform", "ci/cd", "jenkins", "github actions", "linux", "nginx", "gunicorn"],
    "Databases & Tools": ["postgresql", "postgres", "mysql", "sqlite", "mongodb", "redis", "elasticsearch", "git", "github", "jira", "postman", "rest api", "graphql"],
    "Soft Skills & Management": ["leadership", "communication", "problem solving", "teamwork", "agile", "scrum", "project management", "time management", "critical thinking", "collaboration"]
}

SECTION_PATTERNS = {
    "education": [r"\beducation\b", r"\bacademic\b", r"\bqualifications\b"],
    "experience": [r"\bexperience\b", r"\bemployment\b", r"\bwork history\b", r"\bprofessional experience\b"],
    "projects": [r"\bprojects\b", r"\bkey projects\b", r"\bpersonal projects\b"],
    "skills": [r"\bskills\b", r"\btechnical skills\b", r"\bcompetencies\b"],
    "certifications": [r"\bcertifications\b", r"\bcertificates\b", r"\blicenses\b"],
    "achievements": [r"\bachievements\b", r"\bhonors\b", r"\bawards\b"]
}

class ATSAnalyzer:
    @staticmethod
    def analyze_resume(resume_text):
        if not resume_text or len(resume_text.strip()) == 0:
            return {
                "overall_score": 0.0,
                "skills_score": 0.0,
                "experience_score": 0.0,
                "formatting_score": 0.0,
                "education_score": 0.0,
                "extracted_skills": [],
                "missing_keywords": ["Python", "SQL", "Git", "Project Management"],
                "skill_gaps": {"must_learn": ["Python", "SQL"], "good_to_learn": ["Git"], "optional": ["Jira"]},
                "formatting_feedback": ["Resume text is empty or unreadable."],
                "readability": {"word_count": 0, "readability_status": "Empty"},
                "section_analysis": {}
            }

        text_lower = resume_text.lower()

        # 1. Extract Skills & NLP Categorized Skill Gaps
        found_skills, missing_skills = ATSAnalyzer._extract_skills(text_lower)
        categorized_gaps = NLPAnalyzer.categorize_skill_gaps(found_skills, missing_skills)

        # 2. NLP Section Segmentation
        section_status = ATSAnalyzer._analyze_sections(text_lower)
        readability = NLPAnalyzer.calculate_readability_metrics(resume_text)

        # 3. Formatting & Contact Check
        formatting_issues, formatting_score = ATSAnalyzer._assess_formatting(resume_text, text_lower)

        # 4. Sub-scores Calculation
        skills_score = min(100.0, max(20.0, (len(found_skills) / 12.0) * 100.0))
        
        experience_score = 40.0
        if section_status.get("experience"):
            experience_score += 40.0
        if section_status.get("projects") or section_status.get("achievements"):
            experience_score += 20.0

        education_score = 50.0
        if section_status.get("education"):
            education_score += 40.0
        if section_status.get("certifications"):
            education_score += 10.0

        overall_score = round(
            (skills_score * 0.35) +
            (experience_score * 0.30) +
            (formatting_score * 0.20) +
            (education_score * 0.15),
            1
        )

        return {
            "overall_score": overall_score,
            "skills_score": round(skills_score, 1),
            "experience_score": round(experience_score, 1),
            "formatting_score": round(formatting_score, 1),
            "education_score": round(education_score, 1),
            "extracted_skills": found_skills,
            "missing_keywords": missing_skills[:8],
            "skill_gaps": categorized_gaps,
            "formatting_feedback": formatting_issues,
            "readability": readability,
            "section_analysis": section_status
        }

    @staticmethod
    def _extract_skills(text_lower):
        found_skills = []
        missing_skills = []

        for category, skills_list in SKILL_TAXONOMY.items():
            for skill in skills_list:
                pattern = r"\b" + re.escape(skill) + r"\b"
                if re.search(pattern, text_lower):
                    found_skills.append(skill.title())
                else:
                    missing_skills.append(skill.title())

        found_skills = list(dict.fromkeys(found_skills))
        missing_skills = list(dict.fromkeys(missing_skills))
        return found_skills, missing_skills

    @staticmethod
    def _analyze_sections(text_lower):
        section_status = {}
        for section, patterns in SECTION_PATTERNS.items():
            found = any(re.search(pat, text_lower) for pat in patterns)
            section_status[section] = found
        return section_status

    @staticmethod
    def _assess_formatting(raw_text, text_lower):
        issues = []
        score = 100.0

        words = raw_text.split()
        word_count = len(words)

        if word_count < 150:
            issues.append("Resume length is under 150 words. Add more details under work experience and projects.")
            score -= 25.0
        elif word_count > 1200:
            issues.append("Resume exceeds 1,200 words. Aim for a concise 1-2 page layout for ATS efficiency.")
            score -= 15.0

        if not re.search(r"[\w\.-]+@[\w\.-]+\.\w+", raw_text):
            issues.append("No valid email address format detected in contact section.")
            score -= 20.0

        if not re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", raw_text):
            issues.append("No phone number format recognized.")
            score -= 10.0

        if not (re.search(r"•|-|\*", raw_text) or "achievement" in text_lower):
            issues.append("Use bullet points for project accomplishments to improve recruiter readability.")
            score -= 10.0

        if not issues:
            issues.append("Formatting is excellent! Contact information and bullet points detected cleanly.")

        return issues, max(20.0, score)
