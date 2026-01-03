from flask import Flask, request, render_template
import os

from resume_parser import extract_text
from text_preprocessing import clean_text
from analysis_engine import analyze_job_seeker
import uuid
import tempfile
from resume_validator import is_likely_resume



app = Flask(__name__)

# Config
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# JOB SEEKER PAGE
# -------------------------
@app.route("/job-seeker", methods=["GET", "POST"])
def job_seeker():
    if request.method == "POST":

        file = request.files.get("resume")
        jd_text = request.form.get("job_description", "").strip()

        if not file:
            return render_template(
                "job_seeker.html",
                error="Please upload a resume file."
            )

        if not jd_text:
            return render_template(
                "job_seeker.html",
                error="Please paste a job description."
            )

        temp_filename = f"{uuid.uuid4()}_{file.filename}"
        temp_path = os.path.join(app.config["UPLOAD_FOLDER"], temp_filename)

        file.save(temp_path)

        raw_text = extract_text(temp_path)
        cleaned_text = clean_text(raw_text)

        results = analyze_job_seeker(
            jd_text,
            raw_text,
            cleaned_text
        )

        os.remove(temp_path)


        return render_template(
            "job_seeker.html",
            results=results
        )

    return render_template("job_seeker.html")

# -------------------------
# RECRUITER PAGE
# -------------------------

@app.route("/recruiter", methods=["GET", "POST"])
def recruiter():
    if request.method == "POST":
        jd_text = request.form.get("job_description", "")
        files = request.files.getlist("resumes")

        results = []
        skipped_files = []

        for file in files:
            if not file.filename:
                continue

            # Create a unique temp file
            ext = os.path.splitext(file.filename)[1]
            temp_filename = f"{uuid.uuid4()}{ext}"
            temp_path = os.path.join(app.config["UPLOAD_FOLDER"], temp_filename)

            file.save(temp_path)

            # Extract RAW text
            raw_text = extract_text(temp_path)

            #  Resume validation MUST use raw text
            if not is_likely_resume(raw_text):
                skipped_files.append(file.filename)
                os.remove(temp_path)
                continue

            # Clean ONLY after validation
            cleaned_text = clean_text(raw_text)

            analysis = analyze_job_seeker(
                jd_text,
                raw_text,
                cleaned_text
            )
            analysis["name"] = file.filename
            results.append(analysis)



            # Delete temp file after processing
            os.remove(temp_path)


        # Sort by final match %
        results = sorted(
            results,
            key=lambda x: x["final_match_percent"],
            reverse=True
        )

        return render_template("recruiter.html", results=results,skipped_files=skipped_files)

    return render_template("recruiter.html")

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="127.0.0.1", port=5000, debug=True)
