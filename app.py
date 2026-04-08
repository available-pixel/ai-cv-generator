# app.py
import streamlit as st
import base64
from modules.form import get_user_input
from modules.cv_generator import generate_cv_pdf
from modules.ats_score import calculate_ats_score

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI CV Generator",
    page_icon="📝",
    layout="wide"
)

# ================= PREMIUM CSS =================
st.markdown("""
<style>

/* Global */
.block-container {
    padding: 2rem 3rem;
    background-color: #F7F9FC;
}

/* Header */
.main-title {
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #4F46E5, #9333EA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    text-align: center;
    color: #6B7280;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    color: white;
}

/* Sidebar text fix */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Card style */
.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.06);
    margin-bottom: 20px;
    border: 1px solid #E5E7EB;
}

/* Hover effect (VERY premium feel) */
.card:hover {
    transform: translateY(-3px);
    transition: 0.2s ease;
}

/* ATS score big */
.score {
    font-size: 56px;
    font-weight: 800;
    text-align: center;
    color: #4F46E5;
}

/* Buttons (PRIMARY CTA) */
.stButton>button {
    border-radius: 10px;
    height: 48px;
    font-weight: 600;
    background: linear-gradient(90deg, #4F46E5, #9333EA);
    color: white;
    border: none;
}

/* Button hover */
.stButton>button:hover {
    opacity: 0.9;
}

/* Progress bar color */
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #4F46E5, #9333EA);
}

/* Divider */
hr {
    margin-top: 2rem;
    margin-bottom: 2rem;
}

/* PDF preview */
iframe {
    border-radius: 12px;
    border: 1px solid #E5E7EB;
}

/* Small feature cards */
.feature-card {
    text-align: center;
    padding: 20px;
}

/* Emoji size */
.feature-card h4 {
    font-size: 20px;
}

</style>
""", unsafe_allow_html=True)
# ================= HEADER =================
st.markdown("<div class='main-title'>📝 AI CV Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Create a professional, ATS-optimized CV in minutes</div>", unsafe_allow_html=True)

# ================= FUNCTIONS =================
def fill_demo_cv():
    """Fill Streamlit session state with a realistic demo CV."""
    # ---- BASIC INFO ----
    st.session_state.update({
        'name': "Jane Doe",
        'email': "jane.doe@example.com",
        'phone': "+1 555 123 4567",
        'location': "New York, USA",
        'linkedin': "https://linkedin.com/in/janedoe",
        'github': "https://github.com/janedoe",
        'website': "https://janedoe.dev",
        'profile': (
            "Results-driven software developer with 4+ years of experience building "
            "scalable full-stack web applications using Python, Django, and modern JS frameworks. "
            "Passionate about delivering high-performance solutions and exceptional user experiences."
        ),
        'skills': "Python, Django, Flask, JavaScript, React, SQL, Git, Docker, REST APIs, Machine Learning"
    })

    # ---- EDUCATION ----
    st.session_state['education_list'] = [
        {"degree": "B.Sc. Computer Science", "school": "University of Example", "year": "2023",
         "description": "Graduated with honors, focused on software development, algorithms, and database management."},
        {"degree": "M.Sc. Data Science", "school": "Example Tech University", "year": "2025",
         "description": "Specialized in machine learning, big data analytics, and AI applications in healthcare and finance."}
    ]
    for i, edu in enumerate(st.session_state['education_list']):
        st.session_state[f'degree_{i}'] = edu['degree']
        st.session_state[f'school_{i}'] = edu['school']
        st.session_state[f'year_{i}'] = edu['year']
        st.session_state[f'edu_desc_{i}'] = edu.get('description', '')

    # ---- EXPERIENCE ----
    st.session_state['experience_list'] = [
        {"job": "Software Engineer", "company": "TechCorp", "duration": "2023-2025",
         "description": "Developed full-stack web apps with Django and React, optimized backend performance, implemented automated testing, collaborated with cross-functional teams."},
        {"job": "Data Analyst", "company": "DataSolutions", "duration": "2022-2023",
         "description": "Analyzed complex datasets, built dashboards with Python and Tableau, improved data quality, and presented actionable insights to stakeholders."}
    ]
    for i, exp in enumerate(st.session_state['experience_list']):
        st.session_state[f'job_{i}'] = exp['job']
        st.session_state[f'company_{i}'] = exp['company']
        st.session_state[f'duration_{i}'] = exp['duration']
        st.session_state[f'desc_{i}'] = exp['description']

    # ---- PROJECTS ----
    st.session_state['project_list'] = [
        {"name": "Portfolio Website", "description": "Created personal portfolio website with React and responsive design, integrated contact forms and API backend.",
         "technologies": "React, JavaScript, CSS", "links": ["https://janedoe.dev", "", ""]},
        {"name": "ML Model Deployment", "description": "Built and deployed a machine learning model for customer churn prediction using Flask, Docker, and AWS.",
         "technologies": "Python, Flask, Docker, AWS", "links": ["https://ml.example.com", "", ""]}
    ]
    for i, proj in enumerate(st.session_state['project_list']):
        st.session_state[f'pname_{i}'] = proj['name']
        st.session_state[f'pdesc_{i}'] = proj['description']
        st.session_state[f'tech_{i}'] = proj['technologies']
        st.session_state[f'link1_{i}'] = proj['links'][0]
        st.session_state[f'link2_{i}'] = proj['links'][1]
        st.session_state[f'link3_{i}'] = proj['links'][2]

    # ---- LANGUAGES ----
    st.session_state['language_list'] = [
        {"language": "English", "level": "Native"},
        {"language": "French", "level": "Intermediate"},
        {"language": "Spanish", "level": "Beginner"}
    ]
    for i, lang in enumerate(st.session_state['language_list']):
        st.session_state[f'lang_{i}'] = lang['language']
        st.session_state[f'level_{i}'] = lang['level']

    # ---- RESEARCH ----
    st.session_state['research_list'] = [
        {"title": "AI Research Paper", "description": "Explored ML algorithms in healthcare to predict disease progression.", "authors": "Jane Doe", "publication": "Zenodo", "year": "2022", "link": "https://zenodo.org/record/123456"},
        {"title": "Data Science Trends", "description": "Analyzed emerging trends and tools in big data analytics.", "authors": "Jane Doe", "publication": "Zenodo", "year": "2023", "link": "https://zenodo.org/record/654321"}
    ]
    for i, res in enumerate(st.session_state['research_list']):
        st.session_state[f'r_title_{i}'] = res['title']
        st.session_state[f'r_desc_{i}'] = res['description']
        st.session_state[f'r_auth_{i}'] = res['authors']
        st.session_state[f'r_pub_{i}'] = res['publication']
        st.session_state[f'r_year_{i}'] = res['year']
        st.session_state[f'r_link_{i}'] = res['link']

    # ---- CERTIFICATIONS ----
    st.session_state['certificates_list'] = [
        {"name": "Machine Learning using Python", "link": "https://example.com/certificate/ml-python"},
        {"name": "Introduction to AI", "link": "https://example.com/certificate/ai-intro"},
        {"name": "Full-Stack Web Development", "link": "https://example.com/certificate/fullstack"},
        {"name": "Data Analysis with Python", "link": "https://example.com/certificate/data-python"}
    ]
    for i, cert in enumerate(st.session_state['certificates_list']):
        st.session_state[f'cert_name_{i}'] = cert['name']
        st.session_state[f'cert_link_{i}'] = cert['link']


# ================= SIDEBAR =================
st.sidebar.title("🚀 Navigation")

menu = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📋 Build CV", "📊 ATS Score", "📄 Preview & Download"]
)

# ================= HOME =================
if menu == "🏠 Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("## Welcome 👋")
    st.write("This AI CV Generator helps you create a professional resume optimized for Applicant Tracking Systems (ATS).")

    st.markdown("### How it works:")
    st.markdown("""
    1. 📋 Fill your information  
    2. 📊 Check your ATS score  
    3. 📄 Download your CV  
    """)

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='card feature-card'><h4>⚡ Fast</h4><p>Generate CV in seconds</p></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card feature-card'><h4>🎯 ATS Optimized</h4><p>Improve job success rate</p></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='card feature-card'><h4>📄 Professional</h4><p>Clean modern design</p></div>", unsafe_allow_html=True)

# ================= BUILD CV =================
elif menu == "📋 Build CV":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    # HEADER + BUTTON ROW
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("📋 Fill Your Information")

    with col2:
        if st.button("🎯 Load Demo CV"):
            fill_demo_cv()
            st.success("Demo CV loaded!")

    st.markdown("<hr>", unsafe_allow_html=True)

    # FORM
    user_data = get_user_input()
    st.session_state['user_data'] = user_data

    st.markdown("</div>", unsafe_allow_html=True)

# ================= ATS SCORE =================
elif menu == "📊 ATS Score":
    user_data = st.session_state.get('user_data', None)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 ATS Score")

    if not user_data:
        st.warning("Fill the CV first")
    else:
        score = calculate_ats_score(user_data)

        # BIG SCORE
        st.markdown(f"<div class='score'>{score}/100</div>", unsafe_allow_html=True)

        st.progress(score)

        if score < 50:
            st.error("Weak CV - Add more content")
        elif score < 75:
            st.info("Good CV - Improve details")
        else:
            st.success("Excellent CV 🚀")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= PREVIEW =================
elif menu == "📄 Preview & Download":
    user_data = st.session_state.get('user_data', None)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📄 CV Preview")

    if not user_data:
        st.warning("Fill the CV first")
    else:
        import tempfile

        with st.spinner("Generating CV..."):
            pdf_bytes = generate_cv_pdf(user_data, return_bytes=True)

        # ✅ Download
        st.download_button(
            "⬇️ Download CV",
            pdf_bytes,
            f"{user_data.get('name','My_CV')}.pdf",
            "application/pdf"
        )

        # ✅ Save + Preview
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name

        st.write("### 📄 Preview")
        st.pdf(tmp_path)

    st.markdown("</div>", unsafe_allow_html=True)