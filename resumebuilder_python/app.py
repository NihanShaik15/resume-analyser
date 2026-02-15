import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
import pdf2image
import io
import base64

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="ATS Resume Matcher")
st.title("📄 ATS Resume Matcher")

job_description = st.text_area("Paste Job Description")
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Convert PDF to image
def pdf_to_image(uploaded_file):
    images = pdf2image.convert_from_bytes(uploaded_file.read())
    img = images[0]
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return {
        "mime_type": "image/jpeg",
        "data": base64.b64encode(buffer.getvalue()).decode()
    }

# Gemini response
def ats_response(jd, resume_img):
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    prompt = """
    You are an advanced ATS (Applicant Tracking System).

    Analyze the resume against the job description and give output in this format:

    1. Percentage Match (numeric %)
    2. Missing Keywords (comma separated)
    3. How can the candidate improve their skills (bullet points)
    4. Final ATS Decision (Short conclusion)

    Be clear, professional, and ATS-friendly.
    """

    response = model.generate_content([prompt, jd, resume_img])
    return response.text

# Button
if st.button("Check ATS Match"):
    if resume_file and job_description:
        resume_image = pdf_to_image(resume_file)
        result = ats_response(job_description, resume_image)

        st.subheader("📊 ATS Analysis Result")
        st.write(result)
    else:
        st.warning("Please upload resume and enter job description")
