import base64
import os

import streamlit as st

from extract_skills import extract_skills_from_job
from generate_resume import generate_compact_resume

st.set_page_config(page_title="AI Resume Builder", page_icon="📝", layout="wide")

if "generated_docx" not in st.session_state:
    st.session_state.generated_docx = None
if "generated_pdf" not in st.session_state:
    st.session_state.generated_pdf = None

st.title("📝 AI Resume Builder")
st.caption("Create a tailored resume directly from this Streamlit interface using Gemini AI.")

with st.sidebar:
    st.header("Configuration")
    gemini_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Enter your Gemini API key or set it as an environment variable.",
    )
    if gemini_key:
        os.environ["GEMINI_API_KEY"] = gemini_key
    st.info("The resume is generated entirely from this web form.")

with st.form("resume_form"):
    st.subheader("👤 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name *", placeholder="John Doe")
        email = st.text_input("Email *", placeholder="johndoe@example.com")
        phone = st.text_input("Phone *", placeholder="123-456-7890")
        address = st.text_input("Address", placeholder="City, Country")
    with col2:
        linkedin = st.text_input("LinkedIn Profile URL *", placeholder="https://linkedin.com/in/username")
        github = st.text_input("GitHub Profile URL", placeholder="https://github.com/username")
        portfolio = st.text_input("Portfolio Website URL", placeholder="https://myportfolio.com")

    st.markdown("---")
    st.subheader("📝 Professional Summary")
    summary = st.text_area(
        "Short professional summary *",
        placeholder="Passionate Software Engineer with 3+ years of experience building web applications...",
    )

    st.markdown("---")
    st.subheader("💡 Base Skills")
    skills_input = st.text_input(
        "Base skills (comma-separated) *",
        placeholder="Python, Flask, SQL, Git, Docker, Machine Learning",
    )

    st.markdown("---")
    st.subheader("🎯 Target Job Description")
    job_description = st.text_area(
        "Paste the job description *",
        placeholder="We are looking for a Software Engineer proficient in Python, FastAPI, and Docker...",
    )

    st.markdown("---")
    st.subheader("🎓 Education")
    num_edu = st.number_input("Number of education entries", min_value=1, max_value=5, value=1)
    education_list = []
    for i in range(num_edu):
        st.markdown(f"**Education #{i + 1}**")
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            degree = st.text_input(f"Degree/Title #{i + 1}", key=f"deg_{i}", placeholder="B.S. in Computer Science")
        with col_b:
            university = st.text_input(f"University/College #{i + 1}", key=f"univ_{i}", placeholder="State University")
        with col_c:
            gpa = st.text_input(f"CGPA/GPA #{i + 1}", key=f"gpa_{i}", placeholder="3.8/4.0")
        with col_d:
            graduation_date = st.text_input(f"Graduation Date #{i + 1}", key=f"year_{i}", placeholder="May 2024")
        education_list.append({
            "degree": degree,
            "university": university,
            "gpa": gpa,
            "graduation_date": graduation_date,
        })

    st.markdown("---")
    st.subheader("💼 Work Experience")
    num_exp = st.number_input("Number of experience entries", min_value=0, max_value=5, value=1)
    experience_list = []
    for i in range(num_exp):
        st.markdown(f"**Experience #{i + 1}**")
        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_a:
            role = st.text_input(f"Role/Title #{i + 1}", key=f"role_{i}", placeholder="Software Developer")
        with col_b:
            company = st.text_input(f"Company #{i + 1}", key=f"comp_{i}", placeholder="Tech Corp")
        with col_c:
            duration = st.text_input(f"Duration #{i + 1}", key=f"dur_{i}", placeholder="Jan 2022 - Present")
        responsibilities = st.text_area(
            f"Responsibilities #{i + 1} (one per line)",
            key=f"resp_{i}",
            placeholder="Developed API services\nOptimized database queries\nLed unit testing efforts",
        )
        experience_list.append({
            "title": role,
            "company": company,
            "duration": duration,
            "responsibilities": [entry.strip() for entry in responsibilities.split("\n") if entry.strip()],
        })

    st.markdown("---")
    st.subheader("🚀 Projects")
    num_proj = st.number_input("Number of project entries", min_value=0, max_value=5, value=1)
    project_list = []
    for i in range(num_proj):
        st.markdown(f"**Project #{i + 1}**")
        col_a, col_b = st.columns(2)
        with col_a:
            project_name = st.text_input(f"Project Name #{i + 1}", key=f"pname_{i}", placeholder="E-commerce App")
        with col_b:
            project_tech = st.text_input(f"Technologies Used #{i + 1}", key=f"ptech_{i}", placeholder="React, Node.js, MongoDB")
        project_desc = st.text_area(
            f"Project Description #{i + 1}",
            key=f"pdesc_{i}",
            placeholder="A fully functional e-commerce platform featuring secure payments and inventory management.",
        )
        project_link = st.text_input(f"Project Repository/Link #{i + 1}", key=f"pgit_{i}", placeholder="https://github.com/username/project")
        description_full = project_desc
        if project_tech:
            description_full += f" (Tech: {project_tech})"
        if project_link:
            description_full += f" [Link: {project_link}]"
        project_list.append({"name": project_name, "description": description_full})

    submitted = st.form_submit_button("Generate Resume ✨")

    if submitted:
        if not all([name, email, phone, linkedin, summary, skills_input, job_description]):
            st.error("Please fill in all required fields marked with *.")
        else:
            try:
                with st.spinner("Generating your resume with Gemini AI..."):
                    user_skills = {
                        "My Base Skills": [skill.strip() for skill in skills_input.split(",") if skill.strip()]
                    }
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
                                "address": address,
                            },
                        },
                        "summary": summary,
                        "education": [edu for edu in education_list if edu["university"]],
                        "experience": [exp for exp in experience_list if exp["company"]],
                        "projects": [proj for proj in project_list if proj["name"]],
                        "skills": enhanced_skills,
                    }

                    os.makedirs("output", exist_ok=True)
                    docx_path = "output/enhanced_resume.docx"
                    pdf_path = "output/enhanced_resume.pdf"
                    generate_compact_resume(resume_data, output_file=docx_path, generate_pdf=True)

                    st.session_state.generated_docx = docx_path
                    st.session_state.generated_pdf = pdf_path
                    st.success("Resume generated successfully.")
                    st.rerun()
            except Exception as exc:
                st.error(f"Failed to generate resume: {exc}")

if st.session_state.generated_docx and st.session_state.generated_pdf:
    st.markdown("---")
    st.subheader("📄 Generated Resume")
    st.success("Your resume is ready to download.")

    col1, col2 = st.columns(2)
    with col1:
        with open(st.session_state.generated_docx, "rb") as file:
            docx_data = file.read()
        st.download_button(
            "Download Word Document",
            data=docx_data,
            file_name="enhanced_resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with col2:
        with open(st.session_state.generated_pdf, "rb") as file:
            pdf_data = file.read()
        st.download_button(
            "Download PDF Document",
            data=pdf_data,
            file_name="enhanced_resume.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    try:
        with open(st.session_state.generated_pdf, "rb") as file:
            base64_pdf = base64.b64encode(file.read()).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as exc:
        st.error(f"Could not render PDF preview: {exc}")
else:
    st.info("Fill in the form and generate your resume from the web interface.")
