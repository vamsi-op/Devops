// Jenkinsfile
// Local CI/CD pipeline:
// 1) Clone/checkout code from Git
// 2) Build Docker image
// 3) Replace running container with a new one
// 4) Optionally test endpoint

pipeline {
    agent any

    environment {
        IMAGE_NAME = 'student-feedback-system:latest'
        CONTAINER_NAME = 'student-feedback-container'
    }

    stages {
        stage('Clone Repo') {
            steps {
                // Jenkins checks out the branch connected to this job.
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }

        stage('Run Container') {
            steps {
                // Stop/remove old container if present, then run the new one.
                sh 'docker rm -f ${CONTAINER_NAME} || true'
                sh 'docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}'
            }
        }

        stage('Test Endpoint') {
            steps {
                // Basic health check for the home route.
                sh 'sleep 5'
                sh 'curl -f http://localhost:5000/'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished. App should be available at http://localhost:5000'
        }
    }
}
