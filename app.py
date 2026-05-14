import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.resume_parser import parse_resume
from utils.skill_extractor import extract_skills, get_missing_skills
from utils.scorer import calculate_score
from utils.recommender import recommend_jobs

st.set_page_config(
    page_title="ResumeAI - Smart Resume Screener",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f1a2e 100%); color: #e8e8f0; }
    section[data-testid="stSidebar"] { background: rgba(255,255,255,0.04); border-right: 1px solid rgba(255,255,255,0.08); }
    .metric-card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px; padding: 1.5rem; text-align: center; backdrop-filter: blur(10px); }
    .metric-card h1 { font-family: 'Space Grotesk', sans-serif; font-size: 2.8rem; font-weight: 600; margin: 0; }
    .metric-card p { color: rgba(255,255,255,0.55); font-size: 0.85rem; margin: 0.3rem 0 0; text-transform: uppercase; letter-spacing: 0.08em; }
    .score-excellent { color: #4ade80; }
    .score-good { color: #facc15; }
    .score-fair { color: #fb923c; }
    .score-poor { color: #f87171; }
    .job-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.10); border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 0.8rem; }
    .badge { display: inline-block; padding: 0.25rem 0.65rem; border-radius: 20px; font-size: 0.75rem; font-weight: 500; margin: 0.15rem; }
    .badge-green  { background: rgba(74,222,128,0.15);  color: #4ade80; border: 1px solid rgba(74,222,128,0.3); }
    .badge-red    { background: rgba(248,113,113,0.15); color: #f87171; border: 1px solid rgba(248,113,113,0.3); }
    .badge-purple { background: rgba(139,92,246,0.15);  color: #a78bfa; border: 1px solid rgba(139,92,246,0.3); }
    .badge-blue   { background: rgba(96,165,250,0.15);  color: #60a5fa; border: 1px solid rgba(96,165,250,0.3); }
    .section-title { font-family: 'Space Grotesk', sans-serif; font-size: 1.3rem; font-weight: 600; color: #e8e8f0; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid rgba(139,92,246,0.4); }
    .hero-title { font-family: 'Space Grotesk', sans-serif; font-size: 2.5rem; font-weight: 600; background: linear-gradient(135deg, #a78bfa, #60a5fa, #4ade80); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.3rem; }
    .stButton > button { background: linear-gradient(135deg, #7c3aed, #4f46e5); color: white; border: none; border-radius: 10px; font-weight: 500; padding: 0.6rem 1.5rem; }
    .stProgress > div > div > div { background: linear-gradient(90deg, #7c3aed, #4f46e5); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("""
        <div style='padding: 1rem 0; text-align:center;'>
            <div style='font-size:2.5rem;'>🎯</div>
            <div style='font-family:Space Grotesk; font-size:1.2rem; font-weight:600; color:#a78bfa;'>ResumeAI</div>
            <div style='font-size:0.75rem; color:rgba(255,255,255,0.45); margin-top:0.2rem;'>Smart Screening System</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigate", ["🏠 Home", "📄 Analyze Resume", "📊 Dashboard", "ℹ️ About"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""
        <div style='font-size:0.75rem; color:rgba(255,255,255,0.35); text-align:center;'>
            Built with Python · NLP · ML<br>
            <span style='color:#a78bfa;'>Krithika's Portfolio Project ✨</span>
        </div>
    """, unsafe_allow_html=True)

# ---------- HOME ----------
if page == "🏠 Home":
    st.markdown('<div class="hero-title">AI-Powered Resume Screener</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.55); font-size:1.05rem; margin-bottom:2rem;">Upload your resume · Get instant insights · Land your dream job</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("🧠", "NLP Parsing",   "Extracts skills & experience automatically"),
        ("📊", "Smart Scoring", "Ranks your resume from 0–100"),
        ("💼", "Job Match",     "Recommends best-fit roles for you"),
        ("📈", "Skill Gap",     "Tells you exactly what to learn next"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size:2rem; margin-bottom:0.5rem;">{icon}</div>
                    <div style="font-weight:600; font-size:0.95rem; color:#e8e8f0;">{title}</div>
                    <p>{desc}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 💼 Supported Job Roles")
    categories = {
        "📊 Data & AI":           ["Data Analyst", "Data Scientist", "ML Engineer", "AI/ML Intern", "Data Engineer", "BI Developer", "Business Analyst"],
        "💻 Software Dev":        ["Software Developer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Python Developer", "Java Developer", "JavaScript Developer"],
        "📱 Mobile & Web":        ["Mobile App Developer", "Web Developer", "UI/UX Designer"],
        "☁️ Cloud & DevOps":      ["Cloud Engineer", "DevOps Engineer", "Site Reliability Engineer"],
        "🔐 Cybersecurity":       ["Cybersecurity Analyst", "Ethical Hacker", "Security Engineer"],
        "🧪 Testing & QA":        ["QA Engineer", "Automation Test Engineer", "Manual Tester"],
        "🌐 Networking":          ["Network Engineer", "System Administrator", "IT Support Engineer"],
        "🗄️ Other IT":            ["Database Administrator", "ERP Consultant", "IT Project Manager", "Scrum Master", "Technical Writer", "Game Developer"],
    }
    for cat, roles in categories.items():
        with st.expander(cat):
            cols = st.columns(3)
            for i, role in enumerate(roles):
                with cols[i % 3]:
                    st.markdown(f"✅ {role}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Click **Analyze Resume** in the sidebar to get started!")

# ---------- ANALYZE RESUME ----------
elif page == "📄 Analyze Resume":
    st.markdown('<div class="section-title">📄 Resume Analysis</div>', unsafe_allow_html=True)

    job_role = st.selectbox("Target Job Role", [
        # Data & AI
        "Data Analyst", "Data Scientist", "ML Engineer", "AI/ML Intern",
        "Data Engineer", "BI Developer", "Business Analyst", "Research Analyst",
        # Software Development
        "Software Developer", "Frontend Developer", "Backend Developer",
        "Full Stack Developer", "Mobile App Developer", "Python Developer",
        "Java Developer", "JavaScript Developer",
        # Web & Design
        "Web Developer", "UI/UX Designer",
        # Cloud & DevOps
        "Cloud Engineer", "DevOps Engineer", "Site Reliability Engineer",
        # Cybersecurity
        "Cybersecurity Analyst", "Ethical Hacker", "Security Engineer",
        # Testing & QA
        "QA Engineer", "Automation Test Engineer", "Manual Tester",
        # Networking & Systems
        "Network Engineer", "System Administrator", "IT Support Engineer",
        # Other IT
        "Database Administrator", "ERP Consultant", "IT Project Manager",
        "Scrum Master", "Technical Writer", "Game Developer",
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload your Resume (PDF, DOCX or TXT)",
        type=["pdf", "docx", "txt"],
        help="Your file is processed locally and not stored"
    )

    if uploaded_file:
        with st.spinner("🔍 Parsing your resume with NLP..."):
            resume_text = parse_resume(uploaded_file)

        if resume_text:
            st.success(f"✅ Resume parsed successfully! ({len(resume_text.split())} words detected)")

            with st.spinner("🧠 Extracting skills and calculating score..."):
                extracted_skills = extract_skills(resume_text)
                score, breakdown   = calculate_score(resume_text, extracted_skills, job_role)
                jobs               = recommend_jobs(extracted_skills, job_role)
                missing            = get_missing_skills(extracted_skills, job_role)

            # ----- SCORE -----
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">🎯 Resume Score</div>', unsafe_allow_html=True)

            score_class = (
                "score-excellent" if score >= 75 else
                "score-good"      if score >= 55 else
                "score-fair"      if score >= 35 else
                "score-poor"
            )
            score_label = (
                "Excellent 🌟" if score >= 75 else
                "Good 👍"      if score >= 55 else
                "Fair 📈"      if score >= 35 else
                "Needs Work 📚"
            )

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="metric-card"><h1 class="{score_class}">{score}/100</h1><p>Overall Score</p></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-card"><h1 style="color:#60a5fa; font-size:1.8rem;">{score_label}</h1><p>Rating</p></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-card"><h1 style="color:#4ade80;">{len(extracted_skills)}</h1><p>Skills Found</p></div>', unsafe_allow_html=True)

            # ----- BREAKDOWN -----
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">📊 Score Breakdown</div>', unsafe_allow_html=True)
            for criterion, val in breakdown.items():
                st.markdown(f"**{criterion}** — {val}/100")
                st.progress(val / 100)

            # ----- EXTRACTED SKILLS -----
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">🛠️ Extracted Skills</div>', unsafe_allow_html=True)
            if extracted_skills:
                skill_html = " ".join(f'<span class="badge badge-green">{s}</span>' for s in extracted_skills)
                st.markdown(skill_html, unsafe_allow_html=True)
            else:
                st.warning("No recognizable technical skills found. Try adding more specific keywords to your resume.")

            # ----- MISSING SKILLS -----
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">🚀 Recommended Skills to Add</div>', unsafe_allow_html=True)
            st.caption(f"Skills that top **{job_role}** candidates have that you're missing:")
            if missing:
                miss_html = " ".join(f'<span class="badge badge-red">+ {s}</span>' for s in missing)
                st.markdown(miss_html, unsafe_allow_html=True)
            else:
                st.success("🎉 You have all key skills for this role!")

            # ----- JOB RECOMMENDATIONS -----
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">💼 Job Role Recommendations</div>', unsafe_allow_html=True)
            for job in jobs:
                match_color = (
                    "badge-green"  if job["match"] >= 75 else
                    "badge-blue"   if job["match"] >= 50 else
                    "badge-purple"
                )
                st.markdown(f"""
                    <div class="job-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <div style="font-weight:600; color:#e8e8f0;">{job['role']}</div>
                                <div style="font-size:0.8rem; color:rgba(255,255,255,0.45); margin-top:0.2rem;">{job['reason']}</div>
                            </div>
                            <span class="badge {match_color}">{job['match']}% Match</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # ----- RAW TEXT -----
            with st.expander("📝 View Extracted Resume Text"):
                st.text_area("Parsed Content", resume_text, height=250)

        else:
            st.error("❌ Could not read the resume. Please try a different file.")

# ---------- DASHBOARD ----------
elif page == "📊 Dashboard":
    st.markdown('<div class="section-title">📊 IT Skills Analytics Dashboard</div>', unsafe_allow_html=True)

    skills_data = {
        "Python": 95, "SQL": 90, "JavaScript": 88, "Java": 82,
        "React": 80, "Docker": 78, "AWS": 76, "Machine Learning": 74,
        "Git": 92, "Linux": 70, "TypeScript": 68, "Kubernetes": 65,
        "Power BI": 60, "Tableau": 58, "Cybersecurity": 55, "Node.js": 72
    }

    demand_data = pd.DataFrame({
        "Role":            ["Data Analyst", "Software Developer", "DevOps Engineer",
                            "ML Engineer", "Cybersecurity Analyst", "Full Stack Developer",
                            "Cloud Engineer", "QA Engineer"],
        "Openings":        [4200, 8500, 3200, 2900, 3800, 7200, 2800, 3100],
        "Avg Salary (LPA)":[ 8.5,  12.4,  14.8,  18.6,  13.2,  14.0,  16.4,  8.8]
    })

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top IT Skills in Market**")
        df_skills = pd.DataFrame(list(skills_data.items()), columns=["Skill", "Demand Score"])
        df_skills = df_skills.sort_values("Demand Score", ascending=True)
        fig = px.bar(
            df_skills, x="Demand Score", y="Skill", orientation="h",
            color="Demand Score",
            color_continuous_scale=["#4f46e5", "#7c3aed", "#4ade80"],
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False, margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Job Market Overview**")
        fig2 = px.scatter(
            demand_data, x="Openings", y="Avg Salary (LPA)",
            size="Openings", color="Role", text="Role",
            template="plotly_dark",
            color_discrete_sequence=["#a78bfa","#60a5fa","#4ade80","#fb923c","#f472b6","#facc15","#f87171","#34d399"]
        )
        fig2.update_traces(textposition="top center", textfont_size=9)
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False, margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Skill Demand by IT Role (Heatmap)**")
    heatmap_data = pd.DataFrame({
        "Python":     [95, 99, 70, 99, 40, 60, 80, 99, 50],
        "SQL":        [99, 60, 70, 85, 50, 65, 40, 85, 80],
        "JavaScript": [20, 99, 99, 20, 10, 30, 15, 20, 10],
        "Docker":     [30, 50, 99, 80, 40, 85, 99, 70, 30],
        "Security":   [20, 20, 50, 20, 99, 30, 60, 20, 30],
        "ML/AI":      [40, 20, 10, 99, 20, 20, 30, 99, 10],
        "Cloud":      [40, 60, 70, 75, 70, 99, 90, 75, 40],
        "Testing":    [30, 60, 60, 40, 40, 30, 30, 30, 99],
    }, index=["Data Analyst", "Frontend Dev", "Full Stack Dev", "Data Scientist",
              "Cyber Analyst", "DevOps Eng", "Cloud Eng", "ML Engineer", "QA Engineer"])

    fig3 = px.imshow(
        heatmap_data, text_auto=True, aspect="auto",
        color_continuous_scale=["#1a1a3e", "#4f46e5", "#4ade80"],
        template="plotly_dark"
    )
    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig3, use_container_width=True)

# ---------- ABOUT ----------
elif page == "ℹ️ About":
    st.markdown('<div class="section-title">ℹ️ About This Project</div>', unsafe_allow_html=True)
    st.markdown("""
    ### 🎯 AI-Powered Resume Screening & Job Recommendation System
    **Built by:** Krithika
    **Stack:** Python · NLP · Machine Learning · Streamlit · Plotly

    ---

    #### 🔧 How It Works
    1. **Resume Parsing** — Extracts text from PDF, DOCX & TXT files
    2. **Skill Extraction** — NLP keyword matching across 250+ IT skills
    3. **Scoring Engine** — Multi-criteria weighted algorithm (Skills 40% + Experience 25% + Education 15% + Quality 20%)
    4. **Job Recommendation** — TF-IDF + Cosine Similarity across 35+ IT roles
    5. **Skill Gap Analysis** — Role-specific missing skill detection
    6. **Dashboard** — Real-time IT market analytics with Plotly

    ---

    #### 📚 Technologies Used

    | Category       | Tools                                      |
    |----------------|--------------------------------------------|
    | Language       | Python 3.10+                               |
    | NLP            | Regex, Keyword Matching, TF-IDF            |
    | ML             | Scikit-learn, Cosine Similarity            |
    | Frontend       | Streamlit                                  |
    | Visualization  | Plotly                                     |
    | File Parsing   | PyPDF2, python-docx                        |
    | Data           | Pandas, NumPy                              |

    ---

    #### 💡 Resume Line for Your Portfolio
    > *Built NLP pipeline extracting 250+ IT skills from PDF/DOCX resumes; implemented TF-IDF cosine similarity for job recommendation across 35+ roles; multi-criteria scoring algorithm — Python · Scikit-learn · Streamlit · Plotly*
    """)