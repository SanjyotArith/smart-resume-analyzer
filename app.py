from flask import Flask, request, render_template
import os
from resume_parser import extract_text
from text_preprocessing import clean_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        raw_text = extract_text(file_path)
        cleaned_text = clean_text(raw_text)

        return f"""
        <h3>RAW TEXT</h3>
        <pre>{raw_text[:2000]}</pre>
        <h3>CLEANED TEXT</h3>
        <pre>{cleaned_text[:2000]}</pre>
        """

    return """
    <h2>Upload Resume</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="resume" required>
        <button type="submit">Upload</button>
    </form>
    """

if __name__ == "__main__":
    app.run(debug=True)
