# 🚀 SecureResume AI: Privacy-First Resume Optimizer

**SecureResume AI** is a Full-Stack AI Wrapper designed to help job seekers optimize their resumes for ATS (Applicant Tracking Systems) without sacrificing personal data privacy. 

Built with a **Security-First** mindset, this tool uses a custom middleware layer to sanitize PII (Personally Identifiable Information) before it ever reaches the LLM.

## 🛡️ Key Features
- **Privacy Shield Middleware:** Automatically detects and redacts emails, phone numbers, and physical addresses using Regex-based sanitization.
- **ATS Logic Engine:** Analyzes resumes against specific Job Descriptions using the **Google XYZ Formula** (Action + Metric + Result).
- **Trust Dashboard:** Real-time visual feedback showing exactly what data was hidden from the AI.
- **Gemini 1.5 Flash Integration:** High-speed, high-context analysis for complex technical resumes.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Frontend/UI:** Streamlit
- **AI Engine:** Google Gemini 1.5 Flash (via Generative AI API)
- **Security:** Custom Python Middleware (RegEx)
- **Parsing:** PyPDF2

## 🏗️ Architecture
1. **User Input:** User uploads a PDF and a Job Description.
2. **Data Sanitization:** Local Python script scans for PII and replaces it with placeholders (e.g., `[EMAIL_HIDDEN]`).
3. **Prompt Orchestration:** The sanitized text is wrapped in a specialized Recruiter-Persona prompt.
4. **AI Inference:** Gemini processes the request and returns optimization suggestions.
5. **Output:** User receives a Match Score, Missing Keywords, and Bullet Point improvements.

## 🚀 How to Run Locally
1. Clone the repo:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/secure-resume-ai.git](https://github.com/YOUR_USERNAME/secure-resume-ai.git)# secure-resume-ai
