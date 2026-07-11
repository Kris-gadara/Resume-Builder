# Resume Builder

This project is now a Streamlit-only resume generator. You fill in your information in the web UI, provide a job description, and the app generates a tailored resume as a Word document and PDF.

## Features

- **AI-based skill enhancement** using the Gemini API.
- **Web-first resume creation** through a simple Streamlit interface.
- **DOCX and PDF export** for download.
- **No terminal-based generation flow** remains in the project.

## Project structure

```plaintext
resume-builder/
├── app.py                     # Main Streamlit web app
├── extract_skills.py          # Gemini-based skill enhancement
├── docx_utils.py              # Word document helpers
├── generate_resume.py         # Resume DOCX generation
├── generate_pdfs.py           # PDF generation
├── requirements.txt           # Python dependencies
└── README.md                  # Project instructions
```

## Installation

```bash
cd resume-builder
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Notes

- Set your Gemini API key in the environment or in the Streamlit sidebar before generating a resume.
- Generated files are saved in the output folder inside the project.

## License

MIT
