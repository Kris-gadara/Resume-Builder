# AI Resume Builder

An intelligent, web-based Resume Builder that uses the Google Gemini API to dynamically customize and enhance your resume's technical skills based on any target job description. The application generates both polished Word (`.docx`) and high-quality PDF files.

## Features

- 🧠 **AI-Powered Skill Reorganization**: Automatically aligns your skills to match the target job description using the Gemini API.
- 🎨 **Beautiful UI**: Simple, modern web interface built with Streamlit.
- 📝 **Compact Word Document Generation**: Programmatically outputs a well-formatted `.docx` file using `python-docx`.
- 📄 **Print-Ready PDF Compilation**: Converts and structures the resume into a print-ready PDF using `ReportLab`.
- 📥 **Real-time Previews and Downloads**: View your PDF inline in the browser and download the generated files instantly.

---

## Project Structure

```plaintext
Resume-Builder/
├── .gitignore
├── README.md
└── resume-builder/
    ├── app.py                     # Streamlit web interface entrypoint
    ├── main.py                     # CLI entrypoint for the application
    ├── extract_skills.py           # Logic for extracting/enhancing skills using Gemini API
    ├── docx_utils.py               # Formatting helpers for Word documents
    ├── generate_resume.py          # Logic for building the DOCX resume
    ├── generate_pdfs.py            # PDF generation logic using ReportLab
    ├── resume_skeleton_example.yaml # Example structure for resume data
    └── requirements.txt            # Python dependencies
```

---

## Getting Started

### **1. Set up Environment Variables**
Ensure you have your Gemini API Key. You can set it in your environment:
- **Windows (PowerShell)**:
  ```powershell
  $env:GEMINI_API_KEY="your-gemini-api-key"
  ```
- **Linux/macOS**:
  ```bash
  export GEMINI_API_KEY="your-gemini-api-key"
  ```

### **2. Install Dependencies**
Navigate to the `resume-builder` folder and install dependencies:
```bash
cd resume-builder
pip install -r requirements.txt
```

### **3. Run the Web Application**
Start the Streamlit server:
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

---

## Contributing
Feel free to fork this repository, open issues, and submit pull requests!

## License
Licensed under the MIT License.