pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo "Building the application..."
                sh 'docker build -t myapp:latest .'
            }
        }

        stage('Test') {
            steps {
                echo "Running tests..."
                // placeholder, replace with real tests
                sh 'echo "All tests passed!"'
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying the application..."
                // Run the container (example)
                sh 'docker run -d -p 3000:3000 myapp:latest'
            }
        }
    }
}

