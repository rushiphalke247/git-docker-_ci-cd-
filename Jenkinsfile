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
                    if (isUnix()) {
                        sh 'python3 --version || echo "Python not found"'
                        sh 'which pip3 || which pip || echo "pip not in PATH, will use python3 -m pip"'
                    } else {
                        bat 'python --version || echo "Python not found"'
                        bat 'where pip || echo "pip not found, will use python -m pip"'
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            if command -v pip3 >/dev/null 2>&1; then
                                pip3 install -r requirements.txt
                            elif command -v pip >/dev/null 2>&1; then
                                pip install -r requirements.txt
                            else
                                python3 -m pip install -r requirements.txt
                            fi
                        '''
                    } else {
                        bat '''
                            where pip >nul 2>&1 && (
                                pip install -r requirements.txt
                            ) || (
                                python -m pip install -r requirements.txt
                            )
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'python3 test.py'
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