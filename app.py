import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
from PyPDF2 import PdfReader
import re

# --- 1. PRIVACY SHIELD LOGIC ---
def privacy_shield_with_report(text):
    report = {"Emails": 0, "Phones": 0, "Links": 0}
    
    # Scrub Emails
    emails = re.findall(r'\S+@\S+', text)
    report["Emails"] = len(emails)
    text = re.sub(r'\S+@\S+', '[EMAIL_HIDDEN]', text)
    
    # Scrub Phone Numbers
    phones = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4})', text)
    report["Phones"] = len(phones)
    text = re.sub(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4})', '[PHONE_HIDDEN]', text)
    
    # Scrub LinkedIn/Github
    links = re.findall(r'(linkedin\.com/in/|github\.com/)\S+', text)
    report["Links"] = len(links)
    text = re.sub(r'(linkedin\.com/in/|github\.com/)\S+', '[LINK_HIDDEN]', text)

    return text, report

def extract_pdf_text(upload_file):
    reader = PdfReader(upload_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # We use multi_cell to ensure text wraps correctly
    # 'encode' handles special characters that might crash a basic PDF generator
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    
    # Return the PDF as bytes
    return pdf.output()   

# --- 2. APP CONFIG & UI ---
st.set_page_config(page_title="SecureResume AI", page_icon="🛡️")

# API Setup (Using Secrets for Security)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key not found. Please add GEMINI_API_KEY to your Secrets.")

st.title("🚀 SecureResume AI")
st.markdown("Optimize your resume without leaking personal data.")

# Sidebar for instructions
with st.sidebar:
    st.header("How it works")
    st.write("1. Upload Resume")
    st.write("2. Privacy Shield scrubs PII")
    st.write("3. AI analyzes for ATS")

# Main Input
jd = st.text_area("Paste the Job Description (JD) here:", height=200)
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

if st.button("Analyze & Optimize"):
    if uploaded_file and jd:
        # Step 1: Extract and Scrub
        raw_text = extract_pdf_text(uploaded_file)
        safe_text, stats = privacy_shield_with_report(raw_text)
        
        # Step 2: Trust Dashboard
        with st.expander("🛡️ Privacy Shield Report", expanded=True):
            col1, col2, col3 = st.columns(3)
            col1.metric("Emails Hidden", stats["Emails"])
            col2.metric("Phones Hidden", stats["Phones"])
            col3.metric("Links Hidden", stats["Links"])
        
        # Step 3: AI Analysis
        with st.spinner("AI is analyzing your fit..."):
            prompt = f"""
            You are an expert Technical Recruiter. Analyze this resume against the JD.
            RESUME (Anonymized): {safe_text}
            JOB DESCRIPTION: {jd}
            
            Provide:
            1. ATS Score (0-100)
            2. Top 3 Missing Keywords
            3. 3 Bullet point improvements using the XYZ formula.
            """
            response = model.generate_content(prompt)
            st.markdown("### 🎯 Optimization Results")
            st.write(response.text)
            # --- NEW DOWNLOAD FEATURE ---
            result_text = response.text
            st.markdown("### 🎯 Optimization Results")
            st.write(result_text)

            # Generate the PDF file
            pdf_bytes = create_pdf(result_text)
            
            st.download_button(
                label="📥 Download Optimization Report as PDF",
                data=pdf_bytes,
                file_name="Resume_Optimization_Report.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Please upload a resume and paste a JD first.")