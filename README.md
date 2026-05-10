# AI Resume Intelligence & ATS Scoring System

A professional AI-powered resume analysis platform that provides comprehensive career intelligence, ATS scoring, and personalized improvement recommendations. Built for job seekers, career counselors, and HR professionals.

## 🚀 Project Overview

This application analyzes PDF and DOCX resumes using advanced NLP techniques to provide:

- **Resume Parsing**: Extracts text, skills, experience, and education from uploaded documents
- **Specialization Detection**: Identifies career tracks (AI/ML, Data Science, Cloud, DevOps, etc.)
- **ATS Scoring**: Evaluates resume compatibility with Applicant Tracking Systems
- **Project Quality Analysis**: Assesses project descriptions and technical depth
- **Career Alignment**: Matches resumes with job requirements using similarity algorithms
- **Intelligent Recommendations**: Provides mentor-style improvement suggestions

## ✨ Key Features

### Resume Intelligence
- Multi-format Support: PDF and DOCX resume parsing
- Text Extraction: Advanced OCR fallback for scanned documents
- Structured Parsing: Extracts contact info, education, experience sections

### Specialization Analysis
- Career Track Detection: AI/ML, Data Science, Cloud, DevOps, Backend, Frontend
- Skill Categorization: Technical vs. soft skills classification
- Project Evaluation: Quality assessment of portfolio projects

### ATS Optimization
- Compatibility Scoring: 0-100 ATS score with detailed breakdown
- Keyword Analysis: Industry-specific terminology detection
- Formatting Assessment: Resume structure and readability evaluation

### Career Intelligence
- Job Matching: TF-IDF similarity with job descriptions
- Gap Analysis: Identifies missing skills and experience
- Improvement Roadmap: Personalized career development suggestions

## 🛠️ Tech Stack

### Frontend
- Streamlit: Interactive web application framework
- Plotly: Data visualization and charts

### Backend
- Python 3.8+: Core programming language
- spaCy: Advanced NLP processing and entity recognition
- scikit-learn: Machine learning algorithms for similarity and clustering

### Data Processing
- pandas: Data manipulation and CSV handling
- pdfplumber: PDF text extraction
- python-docx: Microsoft Word document processing

## 📁 Project Structure

```
ai_resume_analyzer/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── pyrightconfig.json             # Python type checking config
├── assets/                         # Static assets (images, icons)
├── data/
│   └── skills.csv                  # Skills database
├── uploads/                        # Temporary resume storage (ignored)
└── utils/                          # Core analysis modules
    ├── __init__.py
    ├── parser.py                   # Resume text extraction
    ├── skills.py                   # Skill detection and categorization
    ├── ats.py                      # ATS scoring algorithm
    ├── similarity.py               # Job-resume matching
    ├── specialization.py           # Career track detection
    ├── project_analyzer.py         # Project quality assessment
    ├── recommendations.py          # Improvement suggestions
    ├── resume_chat.py              # Career Q&A system
    └── visualization.py            # Chart generation
```

## 🚀 Installation Guide

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/srijan439/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will open in your default web browser at `http://localhost:8501`.

## 📖 Usage Instructions

1. Launch the application using `streamlit run app.py`
2. Upload a resume in PDF or DOCX format using the file uploader
3. Wait for automatic analysis (typically 10-30 seconds)
4. Review the results: extracted content, skills analysis, ATS score, specialization, and recommendations

### Advanced Features
- Job Matching: Paste job descriptions for compatibility analysis
- Chat Interface: Ask career-related questions about your resume
- Visualization: Interactive charts showing skill distributions
- `utils/project_analyzer.py`
- `utils/recommendations.py`
- `utils/resume_chat.py`

This phase displays metrics, gauges, charts, tabs, expanders, project analysis, smart recommendations, and resume intelligence chat.

### Phase 5: Advanced NLP Improvements

Prepared for future work. The current project uses spaCy tokenization with a lightweight blank English pipeline. Later, you can add named entity recognition, better section parsing, and AI-generated resume feedback.

## Common Errors And Fixes

- `ModuleNotFoundError`: Activate the virtual environment and run `pip install -r requirements.txt`.
- No text extracted from PDF: Try a text-based PDF or DOCX. Scanned PDFs need OCR, which can be added later.
- Low skill count: Add more skills to `data/skills.csv` or make resume wording clearer.
- Low job match score: Paste a detailed job description and tailor resume keywords truthfully.
- Port already in use: Run `streamlit run app.py --server.port 8502`.

## Future Extensions

The structure is ready for later additions such as AI-generated resume suggestions, authentication, database integration, Docker, AWS, CI/CD, Kubernetes, and monitoring.
