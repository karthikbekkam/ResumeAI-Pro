import os
import re
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def sanitize_file_name(filename):
    clean_name = secure_filename(filename)
    if not clean_name:
        clean_name = "resume_upload"
    return clean_name

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def format_file_size(size_in_bytes):
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 * 1024:
        return f"{round(size_in_bytes / 1024, 1)} KB"
    else:
        return f"{round(size_in_bytes / (1024 * 1024), 2)} MB"
