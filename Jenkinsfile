pipeline {
    agent any

    environment {
        // Define Docker Hub credentials ID (should be configured in Jenkins)
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        // Define image name - update with your DockerHub username
        IMAGE_NAME = "${DOCKERHUB_CREDENTIALS_USR}/python-demo-app"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from repository
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                // Use Python tool configured in Jenkins
                script {
                    def pythonVersion = '3.11'
                    // Install Python if not available
                    if (isUnix()) {
                        sh 'python3 --version || echo "Python not found"'
                    } else {
                        bat 'python --version || echo "Python not found"'
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'pip install -r requirements.txt'
                    } else {
                        bat 'pip install -r requirements.txt'
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python test.py'
                    } else {
                        bat 'python test.py'
                    }
                }
            }
            post {
                always {
                    // Archive test results if available
                    script {
                        if (fileExists('test-results.xml')) {
                            junit 'test-results.xml'
                        }
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    def image = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                    
                    // Tag with build number as well
                    image.tag("${IMAGE_NAME}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Login and push to Docker Hub
                    docker.withRegistry('https://registry-1.docker.io/v2/', 'dockerhub-credentials') {
                        def image = docker.image("${IMAGE_NAME}:${IMAGE_TAG}")
                        image.push()
                        image.push("${BUILD_NUMBER}")
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up Docker images to save space
            script {
                if (isUnix()) {
                    sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true"
                    sh "docker rmi ${IMAGE_NAME}:${BUILD_NUMBER} || true"
                } else {
                    bat "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || exit 0"
                    bat "docker rmi ${IMAGE_NAME}:${BUILD_NUMBER} || exit 0"
                }
            }
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}