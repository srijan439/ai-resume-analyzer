# AI Resume Analyzer

A Streamlit-based resume intelligence dashboard that parses PDF and DOCX resumes, extracts skills and profile details, scores ATS readiness, detects career specialization, analyzes project strength, compares a resume against a target job description, and generates practical improvement suggestions.

The project is designed as a local-first AI/NLP application with optional DevOps assets for Docker, Jenkins, Kubernetes, Prometheus, and Terraform-based AWS deployment.

## Table of Contents

- [What This Project Does](#what-this-project-does)
- [Core Features](#core-features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Local Setup](#local-setup)
- [Run the Application](#run-the-application)
- [How to Use the Dashboard](#how-to-use-the-dashboard)
- [Docker Setup](#docker-setup)
- [Kubernetes Setup](#kubernetes-setup)
- [Terraform Setup](#terraform-setup)
- [Jenkins Pipeline](#jenkins-pipeline)
- [Prometheus Monitoring](#prometheus-monitoring)
- [Testing](#testing)
- [Configuration Notes](#configuration-notes)
- [Security Notes](#security-notes)
- [Cost Safety Notes](#cost-safety-notes)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

## What This Project Does

AI Resume Analyzer helps candidates and career mentors understand how well a resume communicates technical ability and role fit. The app accepts a resume file, extracts text, identifies skills, estimates ATS compatibility, detects the strongest specialization, evaluates project descriptions, and gives recommendations that can be used to improve the resume.

It is not a replacement for a human reviewer. Treat the output as a structured assistant for reviewing gaps, phrasing, role alignment, and technical representation.

## Core Features

- Resume upload through a Streamlit sidebar.
- PDF parsing with `pdfplumber`.
- DOCX parsing with `python-docx`.
- Resume text cleaning and section extraction.
- Contact/profile summary extraction for name, email, phone, education, experience, and skills.
- Skill extraction from a curated CSV database.
- Skill categorization by technical area.
- ATS score calculation with component-level feedback.
- Target specialization selection for roles such as AI/ML, Data Science, Cloud Engineering, DevOps, Backend Development, Frontend Development, and General Software.
- Role alignment scoring that combines specialization signals and job-description similarity.
- Project quality analysis with weak and strong signal detection.
- Dynamic project upgrade suggestions based on specialization and job description.
- Resume-to-job matching using TF-IDF and cosine similarity.
- Missing skill and keyword discovery from a target job description.
- Interactive charts using Plotly.
- Local rule-based resume chat for targeted improvement questions.
- Docker, Kubernetes, Jenkins, Terraform, and Prometheus files for deployment and DevOps learning.

## Technology Stack

| Area | Tools |
| --- | --- |
| App framework | Streamlit |
| Language | Python |
| NLP and text processing | spaCy, regex |
| Machine learning | scikit-learn TF-IDF and cosine similarity |
| Data handling | pandas, CSV |
| Resume parsing | pdfplumber, python-docx |
| Visualization | Plotly |
| Containerization | Docker |
| CI/CD | Jenkins |
| Orchestration | Kubernetes / Minikube |
| Monitoring config | Prometheus |
| Cloud infrastructure | Terraform, AWS EC2 |

## Architecture

```text
User
  |
  v
Streamlit UI (app.py)
  |
  +--> Upload and save resume temporarily in uploads/
  |
  +--> Parser layer
  |     +--> validate file type
  |     +--> extract PDF/DOCX text
  |     +--> clean text
  |     +--> extract profile fields and sections
  |
  +--> Analysis layer
  |     +--> skill extraction and categorization
  |     +--> ATS scoring
  |     +--> specialization detection
  |     +--> project quality analysis
  |     +--> job-description similarity
  |     +--> resume recommendations
  |
  +--> Presentation layer
        +--> metrics
        +--> Plotly charts
        +--> improvement tabs
        +--> resume chat
```

## Project Structure

```text
ai_resume_analyzer/
|-- app.py                         # Main Streamlit dashboard entry point
|-- README.md                      # Project documentation
|-- requirements.txt               # Python dependencies
|-- pyrightconfig.json             # Python type-checking config
|-- Dockerfile                     # Container build file
|-- Jenkinsfile                    # Jenkins CI/CD pipeline skeleton
|-- DEVOPS_SETUP_GUIDE.md          # Short DevOps checklist and required commands
|-- .dockerignore                  # Files excluded from Docker build context
|-- .gitignore                     # Local, generated, secret, and heavy files ignored by Git
|
|-- assets/
|   |-- .gitkeep                   # Placeholder for future images/icons/static files
|
|-- data/
|   |-- skills.csv                 # Skill database used by the analyzer
|
|-- k8s/
|   |-- deployment.yaml            # Kubernetes deployment for the Streamlit app
|   |-- service.yaml               # Kubernetes NodePort service
|
|-- monitoring/
|   |-- prometheus.yml             # Basic Prometheus scrape configuration
|
|-- terraform/
|   |-- main.tf                    # AWS EC2 infrastructure definition
|
|-- tests/
|   |-- test_logic.py              # Lightweight logic checks for specialization and project recommendations
|
|-- uploads/
|   |-- .gitkeep                   # Runtime upload folder placeholder; real resumes should not be committed
|
`-- utils/
    |-- __init__.py
    |-- ats.py                     # ATS scoring and role suggestions
    |-- parser.py                  # PDF/DOCX parsing and profile extraction
    |-- project_analyzer.py        # Project quality scoring and upgrade ideas
    |-- recommendations.py         # Resume improvement recommendations
    |-- resume_chat.py             # Rule-based resume Q&A helper
    |-- similarity.py              # Resume/job-description similarity and keyword gaps
    |-- skills.py                  # Skill database loading, extraction, and categorization
    |-- specialization.py          # Specialization detection and role alignment
    `-- visualization.py           # Plotly chart builders
```

## Local Setup

Run all commands from the project root:

```powershell
cd "C:\Users\SRIJAN MISHRA\OneDrive\Desktop\resume analyzer\ai_resume_analyzer"
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, allow the current session to run local scripts:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Install the spaCy English model:

```powershell
python -m spacy download en_core_web_sm
```

## Run the Application

Start Streamlit:

```powershell
streamlit run app.py
```

Open the local app:

```text
http://localhost:8501
```

If port `8501` is busy:

```powershell
streamlit run app.py --server.port 8502
```

## How to Use the Dashboard

1. Upload a PDF or DOCX resume from the sidebar.
2. Select a target specialization such as AI/ML, Data Science, Cloud Engineering, DevOps, Backend Development, or Frontend Development.
3. Optionally paste a target job description.
4. Review the dashboard tabs:
   - `Overview`: high-level quality, specialization, project, and alignment metrics.
   - `Specialization`: detected specialization and technical representation.
   - `Projects`: project quality score, weak signals, strong signals, and upgrade ideas.
   - `Improvements`: ATS component chart and detailed resume suggestions.
   - `Resume Chat`: local Q&A about resume quality, specialization, projects, and gaps.
   - `Profile`: extracted candidate fields, sections, and full resume text.
   - `Role Fit`: suitable roles and alignment context.

## Docker Setup

Build the Docker image:

```powershell
docker build -t ai-resume-analyzer .
```

Run the container:

```powershell
docker run -p 8501:8501 ai-resume-analyzer
```

Open:

```text
http://localhost:8501
```

Stop the container:

```powershell
docker ps
docker stop CONTAINER_ID
```

## Kubernetes Setup

The Kubernetes files are written for a local Minikube-style workflow where the Docker image is available inside the cluster.

Start Minikube:

```powershell
minikube start
```

Apply the Kubernetes manifests:

```powershell
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check resources:

```powershell
kubectl get pods
kubectl get services
```

Open the service:

```powershell
minikube service ai-resume-service
```

Delete the Kubernetes resources:

```powershell
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/service.yaml
```

Stop Minikube when you are done:

```powershell
minikube stop
```

## Terraform Setup

The Terraform configuration in `terraform/main.tf` creates an AWS EC2 instance in `ap-south-1`.

Before running Terraform:

- Install Terraform.
- Install and configure AWS CLI.
- Confirm your AWS account and region.
- Review the instance type and AMI in `terraform/main.tf`.
- Set a billing alert in AWS.

Run:

```powershell
cd terraform
terraform init
terraform plan
terraform apply
```

Destroy infrastructure when you are finished:

```powershell
terraform destroy
```

Do not leave cloud resources running after testing.

## Jenkins Pipeline

`Jenkinsfile` currently contains a simple pipeline with these stages:

- GitHub connection message.
- Build simulation message.
- Success message.

It is useful as a starting point, but it does not yet build, test, scan, or deploy the app. A production-ready pipeline should add dependency installation, tests, Docker build/push, image scanning, and deployment stages.

## Prometheus Monitoring

`monitoring/prometheus.yml` contains a basic Prometheus scrape config:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

This monitors Prometheus itself. The Streamlit app does not currently expose a Prometheus metrics endpoint, so application-level metrics would require additional instrumentation.

## Testing

Run the lightweight logic checks:

```powershell
python tests\test_logic.py
```

These checks cover:

- Target role reactivity in specialization detection.
- Dynamic project recommendations from job-description keywords.

For a more mature test suite, convert these script checks into `pytest` tests and add parser, ATS, similarity, and recommendations coverage.

## Configuration Notes

- `data/skills.csv` drives skill detection and categorization. Add new skills there when the analyzer misses common technologies.
- `uploads/` is for runtime files only. Keep `.gitkeep`, but do not commit real resumes.
- `assets/` is reserved for future static images, icons, or branding.
- The app runs locally and stores uploaded files inside the project `uploads/` folder.
- The Docker image installs dependencies and downloads a spaCy English model during build.
- `requirements.txt` is the source of truth for Python package installation.

## Security Notes

Never push these files or folders:

```text
.aws/
.env
terraform.tfstate
terraform.tfstate.backup
.terraform/
venv/
uploads/
*.pdf
*.docx
```

Security practices:

- Do not commit resumes, personal documents, API keys, AWS keys, SSH keys, or Terraform state.
- Keep `.env` files local.
- Rotate credentials immediately if they are accidentally committed.
- Use least-privilege IAM permissions for Terraform.
- Review `terraform plan` before applying infrastructure changes.
- Keep uploaded resumes temporary and delete them when they are no longer needed.

## Cost Safety Notes

Cloud and container tools can keep resources running in the background. For a learning or portfolio project, keep cost control boring and strict:

- Always stop Docker containers when not using them.
- Always stop Minikube after Kubernetes testing.
- Always destroy unused Terraform infrastructure.
- Avoid keeping EC2 instances running unnecessarily.
- Use AWS billing alerts before running `terraform apply`.
- Prefer short test runs over long-lived cloud deployments.
- Review AWS console after cleanup to confirm no EC2 instances, volumes, elastic IPs, or load balancers are still active.

Useful cleanup commands:

```powershell
docker ps
docker stop CONTAINER_ID

minikube stop

kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/service.yaml

cd terraform
terraform destroy
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'streamlit'`

Activate the virtual environment and install dependencies:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### spaCy model error

Install the English model:

```powershell
python -m spacy download en_core_web_sm
```

### `FileNotFoundError: data/skills.csv`

Run the app from the project root, not from another folder:

```powershell
cd "C:\Users\SRIJAN MISHRA\OneDrive\Desktop\resume analyzer\ai_resume_analyzer"
streamlit run app.py
```

### Port already in use

Use another Streamlit port:

```powershell
streamlit run app.py --server.port 8502
```

### Docker image cannot find local files

Build from the project root:

```powershell
docker build -t ai-resume-analyzer .
```

### Kubernetes image pull problem

`k8s/deployment.yaml` uses:

```yaml
imagePullPolicy: Never
```

That means Kubernetes expects the image to already exist inside the local cluster environment. Build the image in the Minikube Docker environment or push it to a registry and update the image name.

### Terraform credential error

Configure AWS credentials:

```powershell
aws configure
```

Then rerun:

```powershell
terraform plan
```

## Future Improvements

- Convert script-style tests to `pytest`.
- Add unit tests for parsing, ATS scoring, similarity, and recommendations.
- Add automatic cleanup for uploaded resumes.
- Add optional OCR support for scanned PDFs.
- Add a database for analysis history.
- Add authentication for multi-user deployments.
- Add a real metrics endpoint for Prometheus.
- Add GitHub Actions or a stronger Jenkins pipeline.
- Add Docker Compose for local app plus monitoring.
- Add Terraform variables instead of hard-coded AMI and instance values.
- Add CI checks for formatting, type checking, and dependency security.

