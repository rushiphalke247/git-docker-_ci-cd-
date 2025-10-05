pipeline {
    agent any

    environment {
        // Define Docker Hub credentials ID (should be configured in Jenkins)
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        // Define image name - update with your DockerHub username
        IMAGE_NAME = "${DOCKERHUB_CREDENTIALS_USR}/python-demo-app"
        IMAGE_TAG = "latest"
        // Define build artifacts
        ARTIFACT_NAME = "python-demo-app-${BUILD_NUMBER}.tar.gz"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Checking out source code...'
                // Checkout code from repository
                checkout scm
                
                // Display commit information
                script {
                    if (isUnix()) {
                        sh 'git log --oneline -1'
                    } else {
                        bat 'git log --oneline -1'
                    }
                }
            }
        }
    }
        stage('Setup Environment') {
            steps {
                echo '🐍 Setting up Python environment...'
                script {
                    if (isUnix()) {
                        sh '''
                            echo "Python version:"
                            python3 --version || echo "Python not found"
                            echo "Pip location:"
                            which pip3 || which pip || echo "pip not in PATH, will use python3 -m pip"
                            echo "Current working directory:"
                            pwd
                            echo "Directory contents:"
                            ls -la
                        '''
                    } else {
                        bat '''
                            echo "Python version:"
                            python --version || echo "Python not found"
                            echo "Pip location:"
                            where pip || echo "pip not found, will use python -m pip"
                            echo "Current working directory:"
                            cd
                            echo "Directory contents:"
                            dir
                        '''
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '📦 Installing project dependencies...'
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
                            echo "✅ Dependencies installed successfully"
                        '''
                    } else {
                        bat '''
                            where pip >nul 2>&1 && (
                                pip install -r requirements.txt
                            ) || (
                                python -m pip install -r requirements.txt
                            )
                            echo "✅ Dependencies installed successfully"
                        '''
                    }
                }
            }
        }

        stage('Build') {
            steps {
                echo '🔨 Building application...'
                script {
                    if (isUnix()) {
                        sh '''
                            echo "Creating build directory..."
                            mkdir -p build
                            
                            echo "Copying application files..."
                            cp app.py build/
                            cp requirements.txt build/
                            cp test.py build/
                            
                            echo "Creating build artifact..."
                            tar -czf ${ARTIFACT_NAME} build/
                            
                            echo "✅ Build completed successfully"
                            echo "📦 Artifact created: ${ARTIFACT_NAME}"
                        '''
                    } else {
                        bat '''
                            echo "Creating build directory..."
                            if not exist build mkdir build
                            
                            echo "Copying application files..."
                            copy app.py build\\
                            copy requirements.txt build\\
                            copy test.py build\\
                            
                            echo "✅ Build completed successfully"
                            echo "📦 Build files prepared in build directory"
                        '''
                    }
                }
            }
            post {
                success {
                    // Archive build artifacts
                    script {
                        if (isUnix()) {
                            archiveArtifacts artifacts: "${ARTIFACT_NAME}", fingerprint: true
                        } else {
                            archiveArtifacts artifacts: "build/**", fingerprint: true
                        }
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running tests...'
                script {
                    if (isUnix()) {
                        sh '''
                            echo "Starting test execution..."
                            python3 test.py 2>&1 | tee test-output.log
                            echo "✅ Tests completed"
                        '''
                    } else {
                        bat '''
                            echo "Starting test execution..."
                            python test.py > test-output.log 2>&1
                            type test-output.log
                            echo "✅ Tests completed"
                        '''
                    }
                }
            }
            post {
                always {
                    // Archive test results and logs
                    script {
                        if (fileExists('test-results.xml')) {
                            junit 'test-results.xml'
                        }
                        if (fileExists('test-output.log')) {
                            archiveArtifacts artifacts: 'test-output.log', fingerprint: true
                        }
                    }
                }
                failure {
                    echo '❌ Tests failed!'
                }
                success {
                    echo '✅ All tests passed!'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                script {
                    // Build Docker image
                    def image = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                    
                    // Tag with build number as well
                    image.tag("${IMAGE_NAME}:${BUILD_NUMBER}")
                    
                    echo "✅ Docker image built successfully"
                    echo "🏷️  Tagged as: ${IMAGE_NAME}:${IMAGE_TAG}"
                    echo "🏷️  Tagged as: ${IMAGE_NAME}:${BUILD_NUMBER}"
                }
            }
        }

        stage('Push to Registry') {
            steps {
                echo '🚀 Pushing Docker image to registry...'
                script {
                    // Login and push to Docker Hub
                    docker.withRegistry('https://registry-1.docker.io/v2/', 'dockerhub-credentials') {
                        def image = docker.image("${IMAGE_NAME}:${IMAGE_TAG}")
                        image.push()
                        image.push("${BUILD_NUMBER}")
                        
                        echo "✅ Docker image pushed successfully"
                        echo "📍 Available at: ${IMAGE_NAME}:${IMAGE_TAG}"
                        echo "📍 Available at: ${IMAGE_NAME}:${BUILD_NUMBER}"
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying application...'
                script {
                    if (isUnix()) {
                        sh '''
                            echo "Starting deployment process..."
                            
                            # Stop any existing container
                            docker stop python-demo-app || true
                            docker rm python-demo-app || true
                            
                            # Run the new container
                            docker run -d --name python-demo-app -p 3001:3000 ${IMAGE_NAME}:${BUILD_NUMBER}
                            
                            # Wait a moment for container to start
                            sleep 5
                            
                            # Check if container is running
                            if docker ps | grep python-demo-app; then
                                echo "✅ Application deployed successfully!"
                                echo "🌐 Application is running on port 3001"
                                echo "🔗 Access at: http://localhost:3001"
                            else
                                echo "❌ Deployment failed - container not running"
                                exit 1
                            fi
                        '''
                    } else {
                        bat '''
                            echo "Starting deployment process..."
                            
                            REM Stop any existing container
                            docker stop python-demo-app || exit 0
                            docker rm python-demo-app || exit 0
                            
                            REM Run the new container
                            docker run -d --name python-demo-app -p 3001:3000 %IMAGE_NAME%:%BUILD_NUMBER%
                            
                            REM Wait a moment for container to start
                            timeout /t 5
                            
                            REM Check if container is running
                            docker ps | findstr python-demo-app && (
                                echo "✅ Application deployed successfully!"
                                echo "🌐 Application is running on port 3001"
                                echo "🔗 Access at: http://localhost:3001"
                            ) || (
                                echo "❌ Deployment failed - container not running"
                                exit 1
                            )
                        '''
                    }
                }
            }
            post {
                success {
                    echo '🎉 Deployment completed successfully!'
                }
                failure {
                    echo '💥 Deployment failed!'
                }
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up...'
            // Clean up Docker images to save space
            script {
                if (isUnix()) {
                    sh """
                        docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true
                        # Keep the build-specific tag for deployment
                        echo "Keeping image: ${IMAGE_NAME}:${BUILD_NUMBER}"
                    """
                } else {
                    bat """
                        docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || exit 0
                        REM Keep the build-specific tag for deployment
                        echo "Keeping image: ${IMAGE_NAME}:${BUILD_NUMBER}"
                    """
                }
            }
        }
        success {
            echo '🎉 Pipeline completed successfully!'
            echo """
                📊 Build Summary:
                ├── Build Number: ${BUILD_NUMBER}
                ├── Docker Image: ${IMAGE_NAME}:${BUILD_NUMBER}
                ├── Deployment Port: 3001
                └── Status: SUCCESS ✅
            """
        }
        failure {
            echo '💥 Pipeline failed!'
            echo """
                📊 Build Summary:
                ├── Build Number: ${BUILD_NUMBER}
                ├── Status: FAILED ❌
                └── Check logs above for details
            """
        }
    }    
        cleanup {
            // Clean up workspace if needed
            cleanWs(cleanWhenFailure: false)
        }
