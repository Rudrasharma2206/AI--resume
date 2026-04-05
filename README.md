# 📋 ResumeCheck AI

An AI-powered resume analyzer built with **Streamlit** and **Mistral AI**. Upload your resume as a PDF, select your target job role, and get instant structured feedback.

---

## 🚀 Features

- 📄 **PDF Resume Parsing** — Extracts text from uploaded PDF resumes
- 🎯 **Role-Specific Analysis** — Tailored feedback based on your target job role
- 📊 **Resume Score** — Get a score out of 100 with a status indicator
- 💡 **Structured Feedback** — Organized into tabs: Strengths, Missing Skills, Experience, Projects, What to Fix, and Final Verdict
- ⬇️ **Downloadable Report** — Save the full analysis as a `.txt` file
- 🔌 **No SDK dependency** — Calls Mistral API directly via `requests`

---

## 📸 Screenshots

### Home Screen
![Home Screen](screenshots/home.png)

### Resume Analysis Result
![Analysis Result](screenshots/result.png)

### Score & Tabs
![Score Tabs](screenshots/tabs.png)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web UI |
| Mistral AI | LLM for resume analysis |
| pdfplumber | PDF text extraction |
| requests | Direct API calls |
| python-dotenv | Environment variable management |

---

## 📦 Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/AI-resume.git
cd AI-resume
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install streamlit pdfplumber requests python-dotenv
```

---

## 🔑 Setup API Key

Create a `.env` file in the project root:

```
MISTRAL_API_KEY=your_mistral_api_key_here
```

Get your free API key at → [https://console.mistral.ai](https://console.mistral.ai)

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
AI-resume/
├── app.py              # Main Streamlit application
├── .env                # API key (do NOT commit this)
├── .gitignore          # Should include .env
├── README.md           # This file
└── screenshots/        # Screenshots for README
    ├── home.png
    ├── result.png
    └── tabs.png
```

---

## 🎯 Supported Job Roles

- Machine Learning Engineer
- Data Scientist
- Data Analyst
- Software Engineer (Backend / Frontend)
- Full Stack Developer
- DevOps / Cloud Engineer
- AI / ML Research Intern
- Python Developer
- Business Analyst

---

## ⚠️ Notes

- Only **text-based PDFs** are supported. Scanned/image PDFs will not work.
- Make sure your `.env` file is listed in `.gitignore` before pushing to GitHub.

---

## 🙌 Credits

Built with ❤️ using [Streamlit](https://streamlit.io) and [Mistral AI](https://mistral.ai)
