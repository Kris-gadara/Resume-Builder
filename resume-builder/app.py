import streamlit as st
import yaml
import os
import base64
from extract_skills import extract_skills_from_job
from generate_resume import generate_compact_resume
from docx_utils import update_resume_with_skills

# Set up page configurations
st.set_page_config(
    page_title="AI Resume Builder",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Design Aesthetics: Sleek, premium styling using custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.25rem !important;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #1E3A8A !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #3B82F6 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .card {
        background-color: #F3F4F6;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #E5E7EB;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "generated_docx" not in st.session_state:
    st.session_state.generated_docx = None
if "generated_pdf" not in st.session_state:
    st.session_state.generated_pdf = None

# Sidebar Navigation
st.sidebar.title("Navigation")
page_options = ["Home", "Resume Builder", "Generated Resume", "About"]
selected_page = st.sidebar.radio(
    "Go to",
    page_options,
    index=page_options.index(st.session_state.current_page)
)

st.sidebar.markdown("---")
st.sidebar.title("Configuration")
gemini_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password",
    value=os.getenv("GEMINI_API_KEY", ""),
    help="Enter your Gemini API key. If already set as an environment variable, it will be pre-filled."
)
if gemini_key:
    os.environ["GEMINI_API_KEY"] = gemini_key
    import google.generativeai as genai
    genai.configure(api_key=gemini_key)

# Update page state if changed via sidebar
if selected_page != st.session_state.current_page:
    st.session_state.current_page = selected_page
    st.rerun()

# ----------------- HOME PAGE -----------------
if st.session_state.current_page == "Home":
    st.markdown("<h1 class='main-title'>📝 AI Resume Builder</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Tailor your resume to any job description using advanced Gemini AI</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Features
        - 🧠 **AI-Powered Skill Enhancement**: Automatically aligns your skills to match the target job description.
        - 📄 **Export formats**: Generates both polished Word (`.docx`) and print-ready PDF files.
        - 🛠️ **Customizable Form**: Replace raw YAML editing with a simple, dynamic web form.
        - ⚡ **Instant Downloads**: Generate and preview your documents in real-time.
        """)
        
        st.write("")
        if st.button("Build Resume 🚀", key="build_resume_home"):
            st.session_state.current_page = "Resume Builder"
            st.rerun()
            
    with col2:
        st.info("💡 **Pro-Tip:** Make sure to have your Gemini API Key set in your environment variables (`GEMINI_API_KEY`) to leverage AI-powered resume enhancement!")

# ----------------- RESUME BUILDER PAGE -----------------
elif st.session_state.current_page == "Resume Builder":
    st.markdown("<h1 class='main-title'>🛠️ Resume Builder</h1>", unsafe_allow_html=True)
    st.write("Fill in your details below to generate your customized resume.")

    with st.form("resume_form"):
        # 1. Personal Information
        st.subheader("👤 Personal Information")
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email *", placeholder="johndoe@example.com")
            phone = st.text_input("Phone *", placeholder="123-456-7890")
            address = st.text_input("Address", placeholder="City, Country")
        with c2:
            linkedin = st.text_input("LinkedIn Profile URL *", placeholder="https://linkedin.com/in/username")
            github = st.text_input("GitHub Profile URL", placeholder="https://github.com/username")
            portfolio = st.text_input("Portfolio Website URL", placeholder="https://myportfolio.com")

        st.markdown("---")

        # 2. Professional Summary
        st.subheader("📝 Professional Summary")
        summary = st.text_area(
            "Write a short, engaging professional summary *",
            placeholder="Passionate Software Engineer with 3+ years of experience building web applications..."
        )

        st.markdown("---")

        # 3. Skills
        st.subheader("💡 Base Skills")
        skills_input = st.text_input(
            "Enter your base skills (comma-separated) *",
            placeholder="Python, Flask, SQL, Git, Docker, Machine Learning"
        )

        st.markdown("---")

        # 4. Job Description
        st.subheader("🎯 Target Job Description")
        job_description = st.text_area(
            "Paste the target job description here *",
            placeholder="We are looking for a Software Engineer proficient in Python, FastAPI, and Docker..."
        )

        st.markdown("---")

        # Dynamic fields (Education, Experience, Projects) will be handled outside/inside form
        # Note: Since Streamlit form state resets easily, we capture inputs inside the form.
        # Streamlit doesn't natively support dynamic number of inputs easily inside a standard form.
        # We can ask the user how many items they want to add first using a slider/number input.
        st.subheader("🎓 Education")
        num_edu = st.number_input("Number of Education entries", min_value=1, max_value=5, value=1)
        education_list = []
        for i in range(num_edu):
            st.markdown(f"**Education #{i+1}**")
            ec1, ec2, ec3, ec4 = st.columns(4)
            with ec1:
                deg = st.text_input(f"Degree/Title #{i+1}", key=f"deg_{i}", placeholder="B.S. in Computer Science")
            with ec2:
                univ = st.text_input(f"University/College #{i+1}", key=f"univ_{i}", placeholder="State University")
            with ec3:
                gpa = st.text_input(f"CGPA/GPA #{i+1}", key=f"gpa_{i}", placeholder="3.8/4.0")
            with ec4:
                year = st.text_input(f"Graduation Date #{i+1}", key=f"year_{i}", placeholder="May 2024")
            education_list.append({"degree": deg, "university": univ, "gpa": gpa, "graduation_date": year})

        st.markdown("---")

        st.subheader("💼 Work Experience")
        num_exp = st.number_input("Number of Experience entries", min_value=0, max_value=5, value=1)
        experience_list = []
        for i in range(num_exp):
            st.markdown(f"**Experience #{i+1}**")
            ex1, ex2, ex3 = st.columns([1, 1, 1])
            with ex1:
                role = st.text_input(f"Role/Title #{i+1}", key=f"role_{i}", placeholder="Software Developer")
            with ex2:
                comp = st.text_input(f"Company #{i+1}", key=f"comp_{i}", placeholder="Tech Corp")
            with ex3:
                dur = st.text_input(f"Duration #{i+1}", key=f"dur_{i}", placeholder="Jan 2022 - Present")
            
            resp = st.text_area(
                f"Responsibilities #{i+1} (one per line)",
                key=f"resp_{i}",
                placeholder="Developed API services\nOptimized database queries\nLed unit testing efforts"
            )
            experience_list.append({
                "title": role,
                "company": comp,
                "duration": dur,
                "responsibilities": [r.strip() for r in resp.split("\n") if r.strip()]
            })

        st.markdown("---")

        st.subheader("🚀 Projects")
        num_proj = st.number_input("Number of Project entries", min_value=0, max_value=5, value=1)
        project_list = []
        for i in range(num_proj):
            st.markdown(f"**Project #{i+1}**")
            pr1, pr2 = st.columns(2)
            with pr1:
                p_name = st.text_input(f"Project Name #{i+1}", key=f"pname_{i}", placeholder="E-commerce App")
            with pr2:
                p_tech = st.text_input(f"Technologies Used #{i+1}", key=f"ptech_{i}", placeholder="React, Node.js, MongoDB")
            
            p_desc = st.text_area(
                f"Project Description #{i+1}",
                key=f"pdesc_{i}",
                placeholder="A fully functional e-commerce platform featuring secure payments and inventory management."
            )
            p_git = st.text_input(f"Project Repository/Link #{i+1}", key=f"pgit_{i}", placeholder="https://github.com/username/project")
            
            # Format description to match backend structure
            description_full = p_desc
            if p_tech:
                description_full += f" (Tech: {p_tech})"
            if p_git:
                description_full += f" [Link: {p_git}]"

            project_list.append({
                "name": p_name,
                "description": description_full
            })

        # Submit button inside form
        submitted = st.form_submit_button("Generate Resume ✨")

        if submitted:
            # Simple UI validation
            if not name or not email or not phone or not linkedin or not summary or not skills_input or not job_description:
                st.error("🚨 Please fill in all required fields marked with *")
            else:
                try:
                    with st.spinner("Processing... Restructuring skills using Gemini AI 🤖"):
                        # Format the input data to match what the backend expects
                        user_skills = {
                            "My Base Skills": [s.strip() for s in skills_input.split(",") if s.strip()]
                        }

                        # Call the existing AI skill extraction
                        enhanced_skills = extract_skills_from_job(job_description, user_skills)
                        
                        resume_data = {
                            "header": {
                                "name": name,
                                "contact": {
                                    "phone": phone,
                                    "email": email,
                                    "linkedin": linkedin,
                                    "github": github,
                                    "portfolio": portfolio,
                                    "address": address
                                }
                            },
                            "summary": summary,
                            "education": [edu for edu in education_list if edu["university"]],
                            "experience": [exp for exp in experience_list if exp["company"]],
                            "projects": [proj for proj in project_list if proj["name"]],
                            "skills": enhanced_skills
                        }

                        # Save output directory
                        os.makedirs("output", exist_ok=True)
                        docx_path = "output/enhanced_resume.docx"
                        pdf_path = "output/enhanced_resume.pdf"

                        # Generate outputs using existing business logic
                        generate_compact_resume(resume_data, output_file=docx_path, generate_pdf=True)

                        # Update session state with output paths
                        st.session_state.generated_docx = docx_path
                        st.session_state.generated_pdf = pdf_path
                        st.session_state.current_page = "Generated Resume"
                        
                        st.success("🎉 Resume generated successfully!")
                        st.rerun()

                except Exception as e:
                    st.error(f"❌ Failed to generate resume: {str(e)}")

# ----------------- GENERATED RESUME PAGE -----------------
elif st.session_state.current_page == "Generated Resume":
    st.markdown("<h1 class='main-title'>🎓 Generated Resume</h1>", unsafe_allow_html=True)

    docx_path = st.session_state.generated_docx
    pdf_path = st.session_state.generated_pdf

    if not docx_path or not pdf_path or not os.path.exists(docx_path) or not os.path.exists(pdf_path):
        st.warning("⚠️ No resume found. Please go to the Resume Builder page to build one.")
        if st.button("Go to Builder 🛠️"):
            st.session_state.current_page = "Resume Builder"
            st.rerun()
    else:
        st.success("🎉 Your resume is ready for download!")

        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            with open(docx_path, "rb") as f:
                docx_data = f.read()
            st.download_button(
                label="📥 Download Word Document (DOCX)",
                data=docx_data,
                file_name="enhanced_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        with col2:
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            st.download_button(
                label="📥 Download PDF Document",
                data=pdf_data,
                file_name="enhanced_resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # PDF Preview rendering
        st.markdown("### 📄 PDF Preview")
        try:
            with open(pdf_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not render PDF preview: {str(e)}")

# ----------------- ABOUT PAGE -----------------
elif st.session_state.current_page == "About":
    st.markdown("<h1 class='main-title'>ℹ️ About</h1>", unsafe_allow_html=True)

    st.markdown("""
    ### Project Overview
    The **AI Resume Builder** is an intelligent, automated assistant designed to tailor and generate premium resumes for specific job descriptions. 
    It bridges the gap between generic resumes and target requirements by leveraging advanced Gemini AI Models.

    ### Technologies Used
    - **Streamlit**: Web frontend layer.
    - **Google Gemini API**: Skill enhancement and reorganization engine.
    - **python-docx**: Compiling and formatting the Microsoft Word document.
    - **ReportLab**: Synthesizing the high-quality PDF.
    - **PyYAML**: Data parsing.

    ### Workflow Architecture
    """)

    st.markdown("""
    ```mermaid
    graph TD
        A[User Inputs Data in Web UI] --> B[Form Data Configured to Dict]
        B --> C[Gemini AI analyzes Job Description]
        C --> D[Enhanced Skills Structured]
        D --> E[python-docx creates .docx File]
        E --> F[ReportLab compiles PDF File]
        F --> G[Download buttons & PDF preview rendered]
    ```
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Author
    Developed during the summer internship project for Semester 6.
    """)
