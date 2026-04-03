// Jenkinsfile
// CI/CD pipeline:
// 1) Clone/checkout code from Git
// 2) Build Docker image
// 3) Deploy via Ansible playbook (default)
// 4) Or run container directly with Docker
// 5) Optionally test endpoint

pipeline {
    agent any

    parameters {
        // Use Ansible deployment by default to match full Git -> Jenkins -> Docker -> Ansible flow.
        booleanParam(name: 'USE_ANSIBLE_DEPLOY', defaultValue: true, description: 'Deploy with ansible-playbook instead of direct docker run')
    }

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
                script {
                    if (isUnix()) {
                        sh 'docker build -t ${IMAGE_NAME} .'
                    } else {
                        bat 'docker build -t %IMAGE_NAME% .'
                    }
                }
            }
        }

        stage('Run Container') {
            when {
                expression { return !params.USE_ANSIBLE_DEPLOY }
            }
            steps {
                // Stop/remove old container if present, then run the new one.
                script {
                    if (isUnix()) {
                        sh 'docker rm -f ${CONTAINER_NAME} || true'
                        sh 'docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}'
                    } else {
                        bat 'docker rm -f %CONTAINER_NAME% || exit /b 0'
                        bat 'docker run -d --name %CONTAINER_NAME% -p 5000:5000 %IMAGE_NAME%'
                    }
                }
            }
        }

        stage('Deploy via Playbook') {
            when {
                expression { return params.USE_ANSIBLE_DEPLOY }
            }
            steps {
                // Ansible handles container replacement using ansible/deploy.yml.
                script {
                    if (isUnix()) {
                        sh 'ansible-playbook -i ansible/inventory ansible/deploy.yml'
                    } else {
                        bat 'ansible-playbook -i ansible/inventory ansible/deploy.yml'
                    }
                }
            }
        }

        stage('Test Endpoint') {
            steps {
                // Basic health check for the home route.
                script {
                    if (isUnix()) {
                        sh 'sleep 5'
                        sh 'curl -f http://127.0.0.1:5000/'
                    } else {
                        bat 'timeout /t 5 /nobreak > NUL'
                        bat 'curl -f http://127.0.0.1:5000/'
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished. App should be available at http://127.0.0.1:5000'
        }
    }
}
