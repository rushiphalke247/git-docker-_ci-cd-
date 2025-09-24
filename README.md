#  CI/CD pipeline to build and deploy a web app.

This project is a simple Node.js web application containerized with Docker and deployed through a **Jenkins CI/CD pipeline**.  
The pipeline automatically builds and tests the application, creates a Docker image, and pushes it to **DockerHub**.

**Flowchart how the project Work**
 
Developer -> Push Code -> GitHub Repo
                            |
                            V
                     Jenkins CI/CD Pipeline
                            |
               -----------------------------
              |  Test Code  |  Build Image |
               -----------------------------
                            |
                      Push to DockerHub
                            |
                            V
                Deploy on Cloud (EC2/K8s/etc.)


 # Features
- Node.js + Express demo app
- Basic test script
- Dockerfile for containerization
- Jenkins pipeline for CI/CD
- Automatic DockerHub image push

## Project Structure

nodejs-demo-app/
├─ Jenkinsfile           # Jenkins pipeline configuration
├─ Dockerfile            # Container build instructions
├─ index.js              # Main app file
├─ package.json          # Node.js dependencies & scripts
├─ test.js               # Basic test
└─ README.md             # Project documentation

## ⚙️ Setup Instructions

### 1. Clone the repo
git clone https://github.com/rushiphalke247/nodejs-demo-app.git
cd nodejs-demo-app

### 2. Install dependencies
npm ci
### 3. Run locally
npm start

Visit [http://localhost:3000](http://localhost:3000) → you should see:
# Output
Hello from nodejs-demo-app!


## 🐳 Docker
# Check Docker Login
docker login

# Check docker image[locally]
docker images 

### Run container
docker run -p 3000:3000 <your-dockerhub-username>/nodejs-demo-app:local
 
# Generate Personal Access Token in Docker
  **Account Settings --> Personal Tokens --> Generate**
 
## 🔄 Jenkins CI/CD Pipeline

The pipeline (`Jenkinsfile`) runs on every push to the **main** branch:

1. **Checkout code**
2. **Install Node.js & dependencies**
3. **Run tests** (`npm test`)
4. **Build Docker image**
5. **Login to DockerHub** (using Jenkins credentials)
6. **Push Docker image** to DockerHub

## Jenkins Setup Requirements

### 1. Jenkins Plugins
Install the following plugins in Jenkins:
- Docker Pipeline
- NodeJS Plugin
- Pipeline Plugin
- Git Plugin

### 2. Global Tool Configuration
Configure in **Manage Jenkins → Global Tool Configuration**:
- **NodeJS**: Add Node.js 18 installation named `Node-18`
- **Docker**: Ensure Docker is available on Jenkins agents

### 3. Credentials Configuration
Go to **Manage Jenkins → Manage Credentials** and add:
- **dockerhub-credentials**: Username/password credential for DockerHub
  - Username: your DockerHub username
  - Password: your DockerHub access token (from DockerHub > Account Settings > Security > New Access Token)

### 4. Pipeline Job Setup
1. Create a new **Pipeline** job in Jenkins
2. Under **Pipeline → Definition**, select "Pipeline script from SCM"
3. Choose **Git** as SCM and enter your repository URL
4. Set **Branch Specifier** to `*/main`
5. **Script Path** should be `Jenkinsfile`


## ✅ Verifying the Pipeline

* Check **Jenkins dashboard** → your pipeline job should show successful builds
* Go to [DockerHub](https://hub.docker.com/) → your repo should contain `nodejs-demo-app`
* Pull and run the pushed image:

  docker pull <your-dockerhub-username>/nodejs-demo-app:latest
  docker run -p 3000:3000 <your-dockerhub-username>/nodejs-demo-app:latest

**CI/CD** → Automates building, testing, and deploying code.  
**Jenkins** → Open-source automation server for building CI/CD pipelines.  
**Docker** → Packages the app into a portable container image.  
**DockerHub** → Public/private registry to store and distribute Docker images.

