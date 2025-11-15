# AI-Powered Resume Analyzer  

**AI-Powered Resume Analyzer**, a cutting-edge application designed to mimic the expertise of an HR professional! This tool leverages the power of **Google Generative AI** to analyze resumes, evaluate job compatibility, and offer actionable insights for career enhancement.  

---

## 📋 **Project Overview**  

The **AI-Powered Resume Analyzer** serves as a virtual HR assistant, providing:  
- Detailed resume evaluation, including strengths and weaknesses.  
- Suggestions for skill improvement and recommended courses.  
- Job-specific resume analysis to measure compatibility and alignment with job descriptions.  

Whether you’re a job seeker or a recruiter, this tool simplifies resume assessment and improvement.  

---

## 🔑 **Features**  

### 1️⃣ **General Resume Analysis**  
- Summarizes the resume in one line.  
- Highlights existing skill sets.  
- Identifies skill gaps and suggests improvements.  
- Recommends popular courses to enhance the resume.  
- Provides a thorough evaluation of strengths and weaknesses.  

### 2️⃣ **Resume Matching with Job Description**  
- Analyzes resume compatibility with a specific job description.  
- Provides a match score in percentage.  
- Highlights missing skills and areas needing improvement.  
- Suggests whether the resume is ready for the job or requires further enhancements.  

---

## 🛠️ **Tech Stack**  

| **Component**       | **Technology**                  |  
|----------------------|----------------------------------|  
| **Frontend**         | [Streamlit](https://streamlit.io/) |  
| **Backend**          | Python                          |  
| **AI Model**         | [Google Generative AI (Gemini)](https://developers.generativeai.google/) |  
| **PDF Parsing**      | `pdfplumber`                    |  
| **OCR Fallback**     | `pytesseract`                   |  
| **Environment Config** | `.env` for API key security    |  

---

## 🚀 **Setup & Installation**

### Prerequisites
- Python 3.7 or higher
- Google API Key for Generative AI (Gemini)

### Step 1: Install Dependencies
```bash
pip install -r requirement.txt
```

### Step 2: Get Your Google API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key" or use an existing key
4. Copy your API key

### Step 3: Configure Environment Variables
1. Create a `.env` file in the project root directory
2. Add your API key to the file:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
   **Important:**
   - Do NOT use quotes around the API key
   - Do NOT add spaces around the `=` sign
   - Replace `your_actual_api_key_here` with your actual key

### Step 4: Enable Required APIs
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create a new one)
3. Navigate to **APIs & Services** → **Library**
4. Search for "Generative Language API"
5. Click **Enable**
6. Ensure **billing is enabled** for your project

### Step 5: Run the Application
```bash
streamlit run app.py
```

### Troubleshooting

#### API Key Issues
If you encounter authentication errors:
- ✅ Verify `.env` file exists in the project root
- ✅ Check the key has no quotes or spaces: `GOOGLE_API_KEY=AIza...`
- ✅ Ensure "Generative Language API" is enabled in Google Cloud Console
- ✅ Verify billing is enabled for your Google Cloud project
- ✅ Remove API key restrictions temporarily while testing
- ✅ Restart the application after making changes
- ✅ Use the "🧪 Test API Connection" button in the sidebar diagnostics

#### Quota Exceeded Errors
If you see "Quota exceeded" or "429" errors:

**Free Tier Limits:**
- Google Generative AI has rate limits on the free tier
- Limits reset over time (usually hourly/daily)
- Check your quota usage: [Google Cloud Console Quotas](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas)

**Solutions:**
1. **Wait and Retry** - Free tier limits reset automatically
2. **Enable Billing** - Significantly increases quota limits (see [Pricing](https://ai.google.dev/pricing))
3. **Request Quota Increase** - Available in Google Cloud Console
4. **Use a New API Key** - Create a new project with fresh limits

**Check Current Usage:**
- [View Quota Metrics](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/metrics)
- [Manage Quotas](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas)

---

## 📊 **How It Works**

1. **Resume Parsing**  
   - Extracts text from PDF files using `pdfplumber` or OCR as a fallback.

2. **AI Analysis**  
   - Utilizes Google Generative AI to summarize and analyze resume content.  
   - Matches skills with job descriptions for compatibility scoring.

3. **Insightful Feedback**  
   - Provides actionable suggestions for skill enhancement, including course recommendations.  
   - Highlights strengths and weaknesses to refine resumes for better opportunities.

---

![image](https://github.com/user-attachments/assets/418e54ef-82d0-474b-a6bc-9a30d72f27f5)

## 🙌 **Contributing**

Welcome contributions to make this tool better!

1. **Fork** the repository.  
2. **Create a new branch** for your feature or bug fix.  
3. **Submit a pull request** with detailed information about your changes.
