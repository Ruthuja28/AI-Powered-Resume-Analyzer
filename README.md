#**🚀 AI-Powered Resume Analyzer** 

The AI-Powered Resume Analyzer is an advanced application designed to replicate the expertise of an HR professional. Leveraging Google Generative AI (Gemini), this tool evaluates resumes, assesses job compatibility, and provides actionable recommendations to enhance career prospects. 


##**📝 Project Overview** 

This tool acts as a virtual HR assistant, enabling: 
✅ Comprehensive Resume Evaluation – Highlight strengths and weaknesses. 
🎯 Skill Enhancement Suggestions – Recommend courses for improvement. 
📊 Job-Specific Analysis – Measure alignment with particular job descriptions. 
Whether you are a job seeker or a recruiter, it simplifies resume assessment and optimizes professional profiles. 

##**✨ Key Features**

**1️⃣ General Resume Analysis** 
🧾 Generates a one-line summary of the resume. 
💡 Highlights existing skills. 
⚠️ Identifies skill gaps and suggests improvements. 
📖 Recommends popular courses for skill enhancement. 
💪 Evaluates overall strengths and weaknesses. 

**2️⃣ Resume Matching with Job Descriptions**
🔍 Compares resume against a specific job description. 
📊 Provides a match score (%). 
⚡ Highlights missing skills and areas requiring improvement. 
✅ Suggests if the resume is ready for the role or needs refinement. 

 

##**🛠️ Technology Stack** 
| Component          | Technology                       |
|------------------- |----------------------------------|
| 🖥️ Frontend       | Streamlit                        |
| ⚙️ Backend        | Python                           |
| 🤖 AI Model       | Google Generative AI (Gemini)    |
| 📄 PDF Parsing    | pdfplumber                       |
| 🖼️ OCR Fallback   | pytesseract                      |
| 🔐 Environment    | .env for API key security        |


##**⚡ Setup & Installation** 

**Prerequisites** 
Python 3.7 or higher 
Google API Key for Generative AI (Gemini) 

**Steps** 
Install Dependencies 
pip install -r requirements.txt 
 
**Obtain Google API Key**
Visit Google AI Studio 
Sign in and create a new API key or use an existing one 
Copy the key 

**Configure Environment Variables** 
Create a .env file in the project root 
Add your API key: 
GOOGLE_API_KEY=your_actual_api_key_here 
 
**Enable Required APIs** 
Google Cloud Console → APIs & Services → Library 
Search and enable Generative Language API 
Ensure billing is enabled 
Run the Application 
streamlit run app.py 
 
##**🛠 Troubleshooting** 

**🔑 API Key Issues** 
Ensure .env exists in the project root 
No quotes or spaces in the key 
Verify Generative Language API is enabled 
Confirm billing is active 
Temporarily remove API restrictions 
Restart the app 
Test API connection using the sidebar button 

**⏳ Quota Exceeded / Rate Limit Errors** 
Google Generative AI free tier has rate limits 
Options: Wait for reset, enable billing, request quota increase, or use a new API key 

 

##**⚙️ How It Works**

**1️⃣ Resume Parsing** 
Extracts text from PDF using pdfplumber 
Falls back to OCR if needed 

**2️⃣ AI Analysis**
Uses Google Generative AI to summarize and evaluate the resume 
Matches skills with job descriptions for compatibility scoring 

**3️⃣ Insightful Feedback** 
Suggests skill improvements and course recommendations 
Highlights strengths and weaknesses for better career opportunities 

#**🤝 Contributing** 
We welcome contributions! 
Fork the repository 
Create a new branch for your feature or bug fix 
Submit a pull request with details of your changes 


<img width="1913" height="895" alt="Screenshot 2025-11-16 041308" src="https://github.com/user-attachments/assets/033650c7-8900-4033-8837-ab9fca36f889" />




 
