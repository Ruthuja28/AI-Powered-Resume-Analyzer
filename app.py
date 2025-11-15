import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai
from pdf2image import convert_from_path
import pytesseract
import pdfplumber

# Load environment variables
load_dotenv()

# Configure Google Gemini AI
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    # Strip whitespace and remove quotes if present
    api_key = api_key.strip().strip('"').strip("'")
    
if not api_key:
    raise RuntimeError(
        "Environment variable GOOGLE_API_KEY not set.\n\n"
        "To fix this:\n"
        "1. Create a .env file in the project root directory\n"
        "2. Add the following line (without quotes):\n"
        "   GOOGLE_API_KEY=your_actual_api_key_here\n"
        "3. Make sure there are no spaces around the = sign\n"
        "4. Restart the application\n\n"
        "You can get your API key from: https://makersuite.google.com/app/apikey"
    )

try:
    genai.configure(api_key=api_key)
except Exception as e:
    raise RuntimeError(
        f"Failed to configure Google Generative AI: {str(e)}\n\n"
        "Please check:\n"
        "1. Your API key is correct and not expired\n"
        "2. The Generative Language API is enabled in Google Cloud Console\n"
        "3. Billing is enabled for your Google Cloud project"
    )

# Streamlit page config must be set before any other Streamlit commands
st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "AI Resume Analyzer - Powered by Google Gemini AI"}
)


# Validate API key format (after Streamlit is initialized)
if not api_key.startswith("AIza"):
    st.warning(
        "⚠️ Warning: Your API key doesn't appear to be in the correct format. "
        "Google API keys typically start with 'AIza'. Please verify your key is correct."
    )



# Preferred model names to try if listing models isn't available
PREFERRED_MODELS = [
    "gemini-2.5-pro",
    "gemini-pro",
    "gemini-2.5-flash",
    "gemini-1.5",
    "gemini-1.5-flash"
]


def select_supported_model(preferred_list=None):
    """Try to find a model that supports a generate method.
    1. Attempt `genai.list_models()` and pick the first model whose supported methods contain 'generate'.
    2. Otherwise fall back to the provided preferred list (or `PREFERRED_MODELS`).
    Returns a model name or None if nothing suitable found.
    """
    pref = preferred_list or PREFERRED_MODELS
    # Try listing models from the API (some SDK versions support this)
    try:
        models = genai.list_models()
        for m in models:
            if isinstance(m, dict):
                name = m.get("name")
                methods = m.get("supportedMethods") or m.get("methods") or []
            else:
                name = getattr(m, "name", None)
                methods = getattr(m, "supportedMethods", None) or getattr(m, "methods", None) or []
            if name and methods:
                if any("generate" in str(x).lower() for x in methods):
                    return name
    except Exception:
        # If listing models isn't available or fails, we'll fall back below
        pass

    # Fallback: use a preferred model name (user can change this list)
    for name in pref:
        try:
            # Return the name — constructing the object may still fail at call time,
            # but this provides an explicit fallback to try.
            return name
        except Exception:
            continue

    return None

# Custom CSS for Dark Mode Theme
def load_custom_css():
    st.markdown("""
    <style>
 /* White Title */
    .main-title {
       text-align: center;
       font-size: 3rem;
       font-weight: 900;
       margin-top: 0.5rem;
       margin-bottom: 1.5rem;
       color: white !important;   /* PURE WHITE TEXT */
   }


    /* Main background and text */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #ec4899;
        --accent-color: #14b8a6;
        --dark-bg: #0f172a;
        --card-bg: #1e293b;
        --border-color: #334155;
    }
    body, .stApp, [data-testid="stAppViewContainer"] {
    [data-testid="stMarkdownContainer"] * {
    color: #ffffff !important;
    }

    
    /* Overall theme */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f35 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f35 100%) !important;
        border-right: 2px solid #334155 !important;
    }
    
    [data-testid="stSidebar"] > div {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f35 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6 {
        color: #f1f5f9 !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] li {
        color: #cbd5e1 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #cbd5e1 !important;
    }
    
    [data-testid="stSidebar"] code {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border: 1px solid #334155 !important;
    }
    
    [data-testid="stSidebar"] button {
        background-color: rgba(99, 102, 241, 0.2) !important;
        color: #f1f5f9 !important;
        border: 1px solid #6366f1 !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background-color: rgba(99, 102, 241, 0.4) !important;
    }
    
    [data-testid="stSidebar"] .stExpander {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid #334155 !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: #334155 !important;
    }
    
    /* Header styling */
    [data-testid="stHeader"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-bottom: 2px solid #6366f1;
    }
    
    /* Title styling */
    h1 {
        color: #f1f5f9;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #ec4899);
        -webkit-background-clip: text;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #f1f5f9;
    }
    
    /* Text styling */
    p, span, label {
        color: #cbd5e1;
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        border: 2px dashed #6366f1;
        border-radius: 10px;
        padding: 20px;
        background-color: rgba(99, 102, 241, 0.05);
    }
    
    /* File uploader text - make it white (drag and drop area) */
    [data-testid="stFileUploader"] > div:first-child p,
    [data-testid="stFileUploader"] > div:first-child span,
    [data-testid="stFileUploader"] > div:first-child label,
    [data-testid="stFileUploader"] > div:first-child div,
    [data-testid="stFileUploader"] > div:first-child .stMarkdown,
    [data-testid="stFileUploader"] > div > div:first-child p,
    [data-testid="stFileUploader"] > div > div:first-child span,
    [data-testid="stFileUploader"] > div > div:first-child label,
    [data-testid="stFileUploader"] > div > div:first-child div {
        color: #ffffff !important;
    }
    
    /* Uploaded file name text - make it white */
    [data-testid="stFileUploader"] .uploadedFile,
    [data-testid="stFileUploader"] .uploadedFileData,
    [data-testid="stFileUploader"] .uploadedFileName,
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"],
    [data-testid="stFileUploader"] .stFileUploaderFileName,
    [data-testid="stFileUploader"] .uploadedFileData > span,
    [data-testid="stFileUploader"] .uploadedFileData > div,
    [data-testid="stFileUploader"] .uploadedFileData > p {
        color: #ffffff !important;
    }
    
    /* Target uploaded file container specifically - file name stays white */
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) {
        color: #ffffff !important;
    }
    
    /* File icon - make it white */
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) > div:first-child svg,
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) svg:first-child,
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) svg,
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) > div svg,
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) > div:first-of-type svg {
        filter: brightness(0) invert(1) !important;
    }
    
    /* SVG paths within the uploaded file icon - make white */
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) svg path,
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) > div svg path {
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }
    
    /* File size text - make it white for better visibility */
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) > div:last-child,
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) span:last-child,
    [data-testid="stFileUploader"] .uploadedFileSize,
    [data-testid="stFileUploader"] [class*="size"],
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) > div:nth-child(2),
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) > div:nth-child(3),
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) > div:nth-child(4),
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) p,
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) span,
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) div {
        color: #ffffff !important;
    }
    
    /* Target all text elements in uploaded file container except the first child (icon) */
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) > *:not(:first-child),
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) > *:not(:first-child) * {
        color: #ffffff !important;
    }
    
    /* Make uploaded file section more visible with lighter background */
    [data-testid="stFileUploader"] > div > div > div:not(:first-child) {
        background-color: rgba(255, 255, 255, 0.1) !important;
        padding: 8px 12px !important;
        border-radius: 6px !important;
    }
    
    /* Text area styling */
    textarea {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 2px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    /* Textarea placeholder text */
    textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Target job description textarea specifically */
    [data-testid="stTextArea"] textarea {
        color: #ffffff !important;
    }
    
    [data-testid="stTextArea"] textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
  /* Force darker button for ALL st.button elements */
    div.stButton > button, 
    .stButton > button, 
     button[kind="secondary"], 
     button[kind="primary"] {
        background: linear-gradient(135deg, #2b2e99, #8b1552) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 22px !important;
        font-weight: 650 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 12px rgba(43, 46, 153, 0.35) !important;
        transition: 0.2s ease-in-out !important;
    }

/* Hover */
    div.stButton > button:hover,
    .stButton > button:hover,
    button[kind="secondary"]:hover,
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #3a3ec0, #a31a63) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(43, 46, 153, 0.45) !important;
   }

    /* Success/Error/Warning messages */
    .stSuccess {
        background-color: rgba(20, 184, 166, 0.1) !important;
        border: 1px solid #14b8a6 !important;
        border-radius: 8px;
        color: #5eead4 !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid #ef4444 !important;
        border-radius: 8px;
        color: #fca5a5 !important;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid #f59e0b !important;
        border-radius: 8px;
        color: #fcd34d !important;
    }
    
    /* Spinner text */
    .stSpinner {
        color: #6366f1;
    }
    
    /* Divider */
    hr {
        border-color: #334155;
        margin: 2rem 0;
    }
    
    /* Column containers */
    [data-testid="column"] {
        gap: 1.5rem;
    }
    
    /* Cards/Containers */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column"] {
        background-color: rgba(30, 41, 59, 0.5);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    /* Footer text links */
    a {
        color: #6366f1;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    a:hover {
        color: #ec4899;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

# Load custom CSS (after page config)
load_custom_css()

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        # Try direct text extraction
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        if text.strip():
            return text.strip()
    except Exception as e:
        print(f"Direct text extraction failed: {e}")

    # Fallback to OCR for image-based PDFs
    print("Falling back to OCR for image-based PDF.")
    try:
        images = convert_from_path(pdf_path)
        for image in images:
            page_text = pytesseract.image_to_string(image)
            text += page_text + "\n"
    except Exception as e:
        print(f"OCR failed: {e}")

    return text.strip()

# Function to get response from Gemini AI
def analyze_resume(resume_text, job_description=None):
    if not resume_text:
        return {"error": "Resume text is required for analysis."}
    
    # Use the dynamic model selection function
    selected_model_name = select_supported_model()
    if not selected_model_name:
        raise RuntimeError(
            "No suitable model found. Please check your API key and ensure you have access to Gemini models. "
            "Available models can be listed at https://ai.google.dev/models"
        )
    
    try:
        model = genai.GenerativeModel(selected_model_name)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize model '{selected_model_name}': {str(e)}")
    
    base_prompt = f"""
    You are an experienced HR with Technical Experience in the field of any one job role from Data Science, Data Analyst, DevOPS, Machine Learning Engineer, Prompt Engineer, AI Engineer, Full Stack Web Development, Big Data Engineering, Marketing Analyst, Human Resource Manager, Software Developer your task is to review the provided resume.
    Please share your professional evaluation on whether the candidate's profile aligns with the role.ALso mention Skills he already have and siggest some skills to imorve his resume , alos suggest some course he might take to improve the skills.Highlight the strengths and weaknesses.

    Resume:
    {resume_text}
    """

    if job_description:
        base_prompt += f"""
        Additionally, compare this resume to the following job description:
        
        Job Description:
        {job_description}
        
        Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        """

    try:
        response = model.generate_content(base_prompt)
    except Exception as e:
        # Provide a helpful, actionable error for common auth problems
        msg = str(e).lower()
        error_details = []
        
        if "api key not valid" in msg or "api_key_invalid" in msg or "invalid api key" in msg:
            error_details.append("❌ API key is invalid or incorrect")
            error_details.append("   → Check that your .env file contains: GOOGLE_API_KEY=your_key (no quotes)")
            error_details.append("   → Verify the key is correct at: https://makersuite.google.com/app/apikey")
        elif "permission denied" in msg or "403" in msg:
            error_details.append("❌ Permission denied - API key may be restricted")
            error_details.append("   → Remove API key restrictions temporarily (APIs & Services -> Credentials)")
            error_details.append("   → Or add 'Generative Language API' to allowed APIs for this key")
        elif "quota" in msg or "429" in msg or "rate limit" in msg or "resource exhausted" in msg:
            error_details.append("❌ Quota Exceeded - API Usage Limit Reached")
            error_details.append("")
            error_details.append("📊 **What this means:**")
            error_details.append("   You've reached your API usage limit for Google Generative AI.")
            error_details.append("")
            error_details.append("🔧 **How to fix:**")
            error_details.append("")
            error_details.append("   **Option 1: Wait and Retry (Free Tier)**")
            error_details.append("   → Free tier has daily/minute limits that reset over time")
            error_details.append("   → Wait a few minutes or hours and try again")
            error_details.append("   → Check quota limits: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas")
            error_details.append("")
            error_details.append("   **Option 2: Enable Billing (Recommended)**")
            error_details.append("   → Go to: https://console.cloud.google.com/billing")
            error_details.append("   → Link a billing account to your project")
            error_details.append("   → This increases your quota limits significantly")
            error_details.append("")
            error_details.append("   **Option 3: Request Quota Increase**")
            error_details.append("   → Go to: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas")
            error_details.append("   → Select your project and request a quota increase")
            error_details.append("   → This may require billing to be enabled")
            error_details.append("")
            error_details.append("   **Option 4: Use a Different API Key**")
            error_details.append("   → Create a new project with a new API key")
            error_details.append("   → Get new key: https://makersuite.google.com/app/apikey")
            error_details.append("")
            error_details.append("💡 **Tip:** Check your current usage at:")
            error_details.append("   https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/metrics")
        elif "billing" in msg:
            error_details.append("❌ Billing not enabled")
            error_details.append("   → Enable billing in Google Cloud Console for your project")
        else:
            error_details.append(f"❌ Error: {str(e)}")
        
        # Add quick fix checklist for non-quota errors
        if not error_details or ("api key" in error_details[0].lower() and "quota" not in error_details[0].lower()):
            error_details.append("")
            error_details.append("📋 Quick Fix Checklist:")
            error_details.append("   1. Verify .env file exists in project root")
            error_details.append("   2. Check .env contains: GOOGLE_API_KEY=your_key (no quotes, no spaces)")
            error_details.append("   3. Enable 'Generative Language API' in Google Cloud Console")
            error_details.append("   4. Ensure billing is enabled for your Google Cloud project")
            error_details.append("   5. Remove API key restrictions temporarily while testing")
            error_details.append("   6. Restart the application after making changes")
        
        raise RuntimeError("\n".join(error_details))

    analysis = getattr(response, "text", str(response)).strip()
    return analysis


# Sidebar information
with st.sidebar:
    st.markdown("### 📌 About")
    st.markdown("""
    **AI Resume Analyzer** leverages cutting-edge AI to evaluate your resume and match it with job descriptions.
    
    #### Features:
    - 📄 Resume Analysis
    - 💼 Job Matching
    - 🎯 Skill Gap Analysis
    - 📚 Course Recommendations
    """)
    st.markdown("---")
    st.markdown("""
    ### 🚀 How to Use:
    1. Upload your resume (PDF)
    2. (Optional) Paste a job description
    3. Click "Analyze Resume"
    4. Get AI-powered insights
    """)
    st.markdown("---")
    with st.expander("ℹ️ About API Quotas", expanded=False):
        st.info("""
        **Free Tier Limits:**
        - Google Generative AI has rate limits
        - Limits reset automatically over time
        
        **If you hit quota limits:**
        - ⏰ Wait a few minutes/hours and retry
        - 💳 Enable billing for higher limits
        - 📊 [Check your usage](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas)
        
        [Learn more about pricing](https://ai.google.dev/pricing)
        """)

# Diagnostics in sidebar
with st.sidebar.expander("🔧 API Diagnostics", expanded=False):
    # Get fresh API key for diagnostics
    diag_api_key = os.getenv("GOOGLE_API_KEY")
    if diag_api_key:
        diag_api_key = diag_api_key.strip().strip('"').strip("'")
    
    st.write("**API Key Status:**", "✅ Present" if diag_api_key else "❌ Not Found")
    
    if diag_api_key:
        masked_key = (diag_api_key[:4] + "..." + diag_api_key[-4:]) if len(diag_api_key) > 8 else "***"
        st.write("**Key Preview:**", masked_key)
        
        # Check key format
        if not diag_api_key.startswith("AIza"):
            st.warning("⚠️ Key format may be incorrect (should start with 'AIza')")
        else:
            st.success("✅ Key format looks correct")
    else:
        st.error("**No API key found!**")
        st.markdown("""
        **To fix:**
        1. Create a `.env` file in the project root
        2. Add: `GOOGLE_API_KEY=your_key_here`
        3. Restart the app
        """)

    st.markdown("---")
    
    if st.button("🧪 Test API Connection", use_container_width=True):
        if not diag_api_key:
            st.error("❌ No API key to test. Please add GOOGLE_API_KEY to your .env file.")
        else:
            with st.spinner("Testing API key..."):
                try:
                    # Reconfigure with the diagnostic key
                    genai.configure(api_key=diag_api_key)
                    
                    # Try to list models
                    try:
                        models = genai.list_models()
                        count = len(models) if models is not None else 0
                        
                        if count > 0:
                            st.success(f"✅ **Authentication Successful!**")
                            st.success(f"Found {count} available model(s)")
                            
                            # Show first few models
                            names = []
                            for m in (models or [])[:10]:
                                if isinstance(m, dict):
                                    name = m.get("name", "Unknown")
                                else:
                                    name = getattr(m, "name", str(m))
                                if name:
                                    names.append(name.replace("models/", ""))
                            
                            if names:
                                st.write("**Available models:**")
                                for name in names:
                                    st.code(name, language=None)
                        else:
                            st.warning("⚠️ Authentication successful but no models found")
                            
                    except Exception as e:
                        error_msg = str(e).lower()
                        if "permission" in error_msg or "403" in error_msg:
                            st.error("❌ **Permission Denied**")
                            st.info("""
                            **Possible causes:**
                            - API key restrictions are blocking access
                            - Generative Language API not enabled
                            - Billing not enabled for the project
                            
                            **Fix:** Go to Google Cloud Console → APIs & Services → Enable 'Generative Language API'
                            """)
                        elif "quota" in error_msg or "429" in error_msg or "rate limit" in error_msg:
                            st.error("❌ **Quota Exceeded**")
                            st.markdown("""
                            **Your API quota has been exceeded.**
                            
                            **Quick fixes:**
                            - ⏰ **Wait**: Free tier limits reset over time (try again in a few minutes/hours)
                            - 💳 **Enable Billing**: Increases quota limits significantly
                            - 📊 **Check Usage**: [View your quota usage](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas)
                            - 🔑 **New Key**: Create a new project with a fresh API key
                            
                            **Learn more:** [Google AI Studio Quota Info](https://ai.google.dev/pricing)
                            """)
                        else:
                            st.warning(f"⚠️ Model listing failed: {str(e)}")
                            st.info("This might be normal. Try using the app - it may still work with fallback models.")
                            
                except Exception as e:
                    error_msg = str(e).lower()
                    if "api key" in error_msg or "invalid" in error_msg:
                        st.error("❌ **Authentication Failed**")
                        st.error("Your API key is invalid or incorrect.")
                        st.markdown("""
                        **Check:**
                        1. Key is correct in `.env` file (no quotes, no spaces)
                        2. Key hasn't been revoked or regenerated
                        3. Get a new key: https://makersuite.google.com/app/apikey
                        """)
                    else:
                        st.error(f"❌ **Error:** {str(e)}")

# Main title with icon
st.markdown("""
    <style>
        h1.custom-title {
            color: white !important;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        p.custom-sub {
            color: white !important;
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
    </style>

    <h1 class="custom-title">🤖 AI Resume Analyzer</h1>
    <p class="custom-sub">Intelligent Resume Evaluation & Job Matching Powered by Google Gemini AI</p>
    """, unsafe_allow_html=True)



# Two-column layout for upload and job description
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(236, 72, 153, 0.1)); 
                border: 2px solid #6366f1; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;'>
    <h3 style='color: #6366f1; margin-top: 0;'>📄 Upload Resume</h3>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(20, 184, 166, 0.1), rgba(59, 130, 246, 0.1)); 
                border: 2px solid #14b8a6; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;'>
    <h3 style='color: #14b8a6; margin-top: 0;'>💼 Job Description</h3>
    </div>
    """, unsafe_allow_html=True)
    job_description = st.text_area(
        "Paste job description here",
        placeholder="Enter the job description for matching analysis...",
        height=200,
        label_visibility="collapsed"
    )

# Status indicators
if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully!", icon="✅")
else:
    st.info("ℹ️ Please upload a resume in PDF format to get started.", icon="ℹ️")



# Analysis section
st.markdown("---")

if uploaded_file:
    # Save uploaded file locally for processing
    with open("uploaded_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    # Extract text from PDF
    resume_text = extract_text_from_pdf("uploaded_resume.pdf")

    # Analysis button with enhanced styling
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        analyze_button = st.button(
            "🔍 Analyze Resume",
            use_container_width=True,
            
        )

    if analyze_button:
        with st.spinner("🤖 AI is analyzing your resume... This may take a moment..."):
            try:
                # Analyze resume
                analysis = analyze_resume(resume_text, job_description)
                
                # Success message
                st.success("✨ Analysis complete!", icon="✨")
                
                # Display analysis in a nice container
                st.markdown("""
                <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(20, 184, 166, 0.1)); 
                            border: 2px solid #334155; border-radius: 12px; padding: 2rem; margin-top: 1.5rem;'>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📊 Analysis Results")
                st.markdown(analysis)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Download button for results
                results_text = f"Resume Analysis Results\n{'='*50}\n\n{analysis}"
                st.download_button(
                    label="📥 Download Results as Text",
                    data=results_text,
                    file_name="resume_analysis.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}", icon="❌")
else:
    st.info("👆 Upload a resume and optionally provide a job description to get started!", icon="👆")


# Footer
st.markdown("""
<style>
footer {
    position: relative;
    bottom: 0;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: #94a3b8;'>
    <p style='margin: 0.5rem 0;'>
        <strong>Powered by</strong> 
        <span style='color: #6366f1;'><b>Streamlit</b></span> 
        and 
        <span style='color: #ec4899;'><b>Google Gemini AI</b></span>
    </p>
    <p style='margin: 0.5rem 0; font-size: 0.9rem;'>
        Developed by 
        <a href="https://www.linkedin.com/in/ruthuja-r-chavan-73bba6365 " target="_blank" style='color: #6366f1; font-weight: bold; text-decoration: none;'>    
        </a>
    </p>
        <p style='margin-top: 1rem; font-size: 0.8rem; color: #64748b;'></p>
        <p style='color: white;'>©AI Resume Analyzer | Built with ❤️ for Career Growth</p>
    
</div>
""", unsafe_allow_html=True)