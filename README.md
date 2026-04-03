# Student Feedback System with CI/CD Pipeline

This project is a complete beginner-friendly full-stack + DevOps example designed for pipeline-based delivery.

## Project Goal

Automate this flow:

Git -> Jenkins -> Docker -> Ansible -> Running App

## Project Structure

student-feedback-system/

- app/
  - app.py
  - database.py
  - requirements.txt
- templates/
  - index.html
  - feedback.html
- static/
  - style.css
- Dockerfile
- Jenkinsfile
- ansible/
  - inventory
  - deploy.yml

## App Features

- Student can submit:
  - Name
  - Feedback message
- Flask backend stores data in SQLite
- Feedback list is displayed on web pages

## Prerequisites

Install these tools:

- Git
- Python 3.11+
- Docker Desktop (or Docker Engine)
- Jenkins
- Ansible (can be from WSL/Linux)

## 1) Run App (Without Docker)

From project root:

```powershell
cd student-feedback-system
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
python app/app.py
```

Open: http://127.0.0.1:5000

## 2) Run App with Docker

From project root:

```powershell
docker build -t student-feedback-system:latest .
docker run -d --name student-feedback-container -p 5000:5000 student-feedback-system:latest
```

Open: http://127.0.0.1:5000

## 3) Deploy with Ansible

From project root:

```powershell
ansible-playbook -i ansible/inventory ansible/deploy.yml
```

This playbook:

- Checks Docker installation
- Builds latest image
- Stops old container
- Runs new container on port 5000

## 4) Jenkins Pipeline Setup

1. Start Jenkins.
2. Create a Pipeline job.
3. Connect your GitHub repository.
4. Set Script Path to Jenkinsfile.
5. Add GitHub webhook to trigger on push (or use Poll SCM).

### Pipeline Stages

- Clone Repo
- Build Docker Image
- Run Container
- Test Endpoint

## 5) Full CI/CD Workflow Explained

Comments in Jenkinsfile and ansible/deploy.yml explain each step clearly.

End-to-end flow:

1. You push code to GitHub.
2. GitHub webhook triggers Jenkins.
3. Jenkins checks out latest code and builds Docker image.
4. Jenkins runs deployment steps (directly or by calling Ansible).
5. Ansible rebuilds/redeploys the container.
6. Updated app is available at http://127.0.0.1:5000

## 6) Make It Ready to Push to GitHub

From project root:

```powershell
git init
git add .
git commit -m "Initial commit: Student Feedback System with CI/CD"
git branch -M main
git remote add origin https://github.com/<your-username>/student-feedback-system.git
git push -u origin main
```

## Optional: Jenkins Calls Ansible

If you want Jenkins to run Ansible as part of deploy, add this stage in Jenkinsfile:

```groovy
stage('Deploy with Ansible') {
    steps {
        sh 'ansible-playbook -i ansible/inventory ansible/deploy.yml'
    }
}
```

## Notes

- SQLite file is created automatically as feedback.db in project root.
- For Windows, running Ansible is easiest through WSL/Ubuntu.
- If port 5000 is busy, stop old container and retry.
