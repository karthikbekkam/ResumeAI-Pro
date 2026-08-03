import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PDFReportGenerator:
    @staticmethod
    def generate_resume_report_pdf(resume, report_dict):
        """
        Generate a multi-page ReportLab PDF evaluation report for a given resume.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom Palette & Styles
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#4f46e5'),
            spaceAfter=6
        )

        subtitle_style = ParagraphStyle(
            'DocSubTitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=15
        )

        section_heading = ParagraphStyle(
            'SectionHead',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#0f172a'),
            spaceBefore=14,
            spaceAfter=8
        )

        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor('#334155')
        )

        bold_body = ParagraphStyle(
            'BoldBody',
            parent=body_style,
            fontName='Helvetica-Bold'
        )

        story = []

        # 1. Title Header
        story.append(Paragraph("ResumeAI Pro — Comprehensive Evaluation Report", title_style))
        upload_str = resume.upload_date.strftime('%B %d, %Y') if resume.upload_date else "N/A"
        story.append(Paragraph(f"<b>Candidate File:</b> {resume.original_filename} | <b>Date:</b> {upload_str} | <b>File Format:</b> {resume.file_type.upper()}", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e2e8f0'), spaceAfter=15))

        # 2. Executive Score Table
        overall_score = report_dict.get('overall_score', 0.0)
        skills_score = report_dict.get('skills_score', 0.0)
        exp_score = report_dict.get('experience_score', 0.0)
        fmt_score = report_dict.get('formatting_score', 0.0)
        edu_score = report_dict.get('education_score', 0.0)

        score_table_data = [
            [Paragraph("<b>Metric Category</b>", bold_body), Paragraph("<b>Sub-Score</b>", bold_body), Paragraph("<b>Status Assessment</b>", bold_body)],
            [Paragraph("Overall ATS Score", body_style), f"{overall_score}%", "High Compliance" if overall_score >= 75 else "Needs Optimization"],
            [Paragraph("Technical & Soft Skills", body_style), f"{skills_score}%", "Solid Keyword Coverage"],
            [Paragraph("Work Experience Metrics", body_style), f"{exp_score}%", "Measured Bullet Points"],
            [Paragraph("Layout & Formatting", body_style), f"{fmt_score}%", "Clean ATS Structure"],
            [Paragraph("Education & Certifications", body_style), f"{edu_score}%", "Verified Credentials"]
        ]

        t = Table(score_table_data, colWidths=[200, 100, 240])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 15))

        # 3. Gemini AI Review & Critique
        ai = report_dict.get('ai_suggestions', {})
        if ai and isinstance(ai, dict):
            story.append(Paragraph("Executive Review & AI Recommendations", section_heading))
            exec_summary = ai.get('executive_summary', 'Comprehensive candidate evaluation completed.')
            story.append(Paragraph(f"<b>Summary:</b> {exec_summary}", body_style))
            story.append(Spacer(1, 8))

            strengths = ai.get('strengths', [])
            if strengths:
                story.append(Paragraph("<b>Key Candidate Strengths:</b>", bold_body))
                for s in strengths:
                    story.append(Paragraph(f"• {s}", body_style))
                story.append(Spacer(1, 6))

            improvements = ai.get('improvement_areas', [])
            if improvements:
                story.append(Paragraph("<b>Recommended Action Items:</b>", bold_body))
                for imp in improvements:
                    story.append(Paragraph(f"• {imp}", body_style))
                story.append(Spacer(1, 12))

        # 4. Identified Skills & Missing Keywords
        story.append(Paragraph("Skill Taxonomy & Keyword Analysis", section_heading))
        extracted_skills = report_dict.get('extracted_skills', [])
        missing_kw = report_dict.get('missing_keywords', [])

        story.append(Paragraph(f"<b>Identified Skills:</b> {', '.join(extracted_skills) if extracted_skills else 'None recognized'}", body_style))
        story.append(Spacer(1, 4))
        story.append(Paragraph(f"<b>Recommended Keywords To Add:</b> {', '.join(missing_kw) if missing_kw else 'All core keywords present'}", body_style))
        story.append(Spacer(1, 15))

        # 5. Career Roadmap Summary
        story.append(Paragraph("Personalized 4-Step Career Roadmap", section_heading))
        roadmap_steps = [
            "Step 1: Incorporate missing high-frequency tech stack keywords into technical skills list.",
            "Step 2: Rewrite project bullet points using action verbs (e.g. 'Engineered', 'Architected').",
            "Step 3: Add quantifiable business metrics (e.g. 'Increased latency by 35% across 50k users').",
            "Step 4: Prepare tailored technical and behavioral STAR-method interview answers."
        ]
        for step in roadmap_steps:
            story.append(Paragraph(f"• {step}", body_style))

        doc.build(story)
        buffer.seek(0)
        return buffer
