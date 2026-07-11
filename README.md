# AI Resume Builder

A Streamlit-based resume generator that helps you create a polished, tailored resume from a web form. The app uses the Google Gemini API to improve and reorganize your skills based on a target job description, then generates both a Word document and a PDF.

## What this project does

- 🧠 Enhances your skills for a specific job description using Gemini AI.
- 📝 Collects your profile, experience, education, projects, and summary from a simple form.
- 📄 Generates a DOCX resume and a PDF version for download.
- 🌐 Runs entirely through the Streamlit frontend.

## Project structure

```plaintext
Resume-Builder/
├── README.md
└── resume-builder/
    ├── app.py                     # Main Streamlit web app
    ├── extract_skills.py          # Gemini-based skill enhancement
    ├── docx_utils.py              # Word document helpers
    ├── generate_resume.py         # Resume DOCX generation
    ├── generate_pdfs.py           # PDF generation
    ├── resume_skeleton.yaml       # Example resume structure
    └── requirements.txt           # Python dependencies
```

## Getting started

### 1. Set your Gemini API key

Use either of these options:

- Windows PowerShell:
  ```powershell
  $env:GEMINI_API_KEY="your-gemini-api-key"
  ```
- Linux/macOS:
  ```bash
  export GEMINI_API_KEY="your-gemini-api-key"
  ```

You can also enter the key directly in the Streamlit sidebar when the app starts.

### 2. Install dependencies

```bash
cd resume-builder
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Notes

- This project is intentionally web-only. There is no terminal-based resume generation flow anymore.
- The generated files are saved in the output folder inside the project.

## License

MIT
