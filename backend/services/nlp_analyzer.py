import re
import math

class NLPAnalyzer:
    @staticmethod
    def segment_sections(text):
        """
        Segment raw resume text into distinct structured sections.
        """
        if not text:
            return {}

        sections = {
            "summary": "",
            "skills": "",
            "experience": "",
            "projects": "",
            "education": "",
            "certifications": "",
            "achievements": ""
        }

        # Normalize line breaks
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        current_section = "summary"
        section_lines = {key: [] for key in sections.keys()}

        header_patterns = {
            "skills": r"\b(skills|technical skills|core competencies)\b",
            "experience": r"\b(experience|work experience|employment|work history)\b",
            "projects": r"\b(projects|key projects|personal projects)\b",
            "education": r"\b(education|academic history|academic background)\b",
            "certifications": r"\b(certifications|certificates|licenses)\b",
            "achievements": r"\b(achievements|awards|honors)\b",
            "summary": r"\b(summary|profile|about me|objective)\b"
        }

        for line in lines:
            line_lower = line.lower()
            matched = False
            for sec_key, pat in header_patterns.items():
                if re.search(pat, line_lower) and len(line.split()) <= 4:
                    current_section = sec_key
                    matched = True
                    break
            if not matched:
                section_lines[current_section].append(line)

        for sec_key in sections:
            sections[sec_key] = "\n".join(section_lines[sec_key]).strip()

        return sections

    @staticmethod
    def categorize_skill_gaps(found_skills, missing_keywords):
        """
        Categorize missing keywords into Must Learn, Good to Learn, and Optional.
        """
        must_learn = []
        good_to_learn = []
        optional = []

        core_languages_db = {"Python", "Java", "SQL", "JavaScript", "TypeScript", "C++", "C#", "Go", "HTML", "CSS"}
        frameworks_db = {"Flask", "Django", "FastAPI", "React", "Next.Js", "Vue", "Node.Js", "Bootstrap", "Tailwind", "Spring Boot", "Docker", "Kubernetes", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Git", "Rest Api"}

        for kw in missing_keywords:
            kw_title = kw.title()
            if kw_title in core_languages_db:
                must_learn.append(kw_title)
            elif kw_title in frameworks_db:
                good_to_learn.append(kw_title)
            else:
                optional.append(kw_title)

        if not must_learn and missing_keywords:
            must_learn = [k.title() for k in missing_keywords[:2]]
            good_to_learn = [k.title() for k in missing_keywords[2:5]]
            optional = [k.title() for k in missing_keywords[5:]]

        return {
            "must_learn": must_learn,
            "good_to_learn": good_to_learn,
            "optional": optional
        }

    @staticmethod
    def calculate_readability_metrics(text):
        """
        Calculate word count, sentence count, average sentence length, and readability score.
        """
        words = re.findall(r"\b\w+\b", text)
        sentences = re.split(r"[.!?]+", text)
        sentences = [s for s in sentences if s.strip()]

        word_count = len(words)
        sentence_count = max(1, len(sentences))
        avg_words_per_sentence = round(word_count / sentence_count, 1)

        # Action verbs count
        action_verbs = {"engineered", "spearheaded", "architected", "optimized", "built", "developed", "designed", "implemented", "orchestrated", "automated", "created", "led", "managed", "improved"}
        found_action_verbs = [w.lower() for w in words if w.lower() in action_verbs]

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_words_per_sentence": avg_words_per_sentence,
            "action_verb_count": len(found_action_verbs),
            "readability_status": "Optimal" if 10 <= avg_words_per_sentence <= 22 else "Needs Tuning"
        }
