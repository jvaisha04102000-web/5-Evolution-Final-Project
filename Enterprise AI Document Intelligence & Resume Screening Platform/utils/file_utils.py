import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file, upload_folder):
    """
    Saves uploaded file securely
    """
    if not file:
        raise ValueError("No file provided")

    if not allowed_file(file.filename):
        raise ValueError("Invalid file type")

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    return file_path