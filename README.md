#  CI/CD pipeline to build and deploy a web app.

This project is a simple Python web application containerized with Docker and deployed through a **Jenkins CI/CD pipeline**.  
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
- Python + Flask demo app
- Basic test script using unittest
- Dockerfile for containerization
- Jenkins pipeline for CI/CD
- Automatic DockerHub image push

## Project Structure

python-demo-app/
├─ Jenkinsfile           # Jenkins pipeline configuration
├─ Dockerfile            # Container build instructions
├─ app.py                # Main Flask app file
├─ requirements.txt      # Python dependencies
├─ test.py               # Basic test script
└─ README.md             # Project documentation

## ⚙️ Setup Instructions

### 1. Clone the repo
git clone https://github.com/rushiphalke247/python-demo-app.git
cd python-demo-app

### 2. Install dependencies
pip install -r requirements.txt
### 3. Run locally
python app.py

Visit [http://localhost:3000](http://localhost:3000) → you should see:
# Output
Hello from python-demo-app!


## 🐳 Docker
# Check Docker Login
docker login

# Check docker image[locally]
docker images 

### Run container
docker run -p 3000:3000 <your-dockerhub-username>/python-demo-app:latest
 
# Generate Personal Access Token in Docker
  **Account Settings --> Personal Tokens --> Generate**
 
## 🔄 Jenkins CI/CD Pipeline

The pipeline (`Jenkinsfile`) runs on every push to the **main** branch:

1. **Checkout code**
2. **Setup Python & install dependencies**
3. **Run tests** (`python test.py`)
4. **Build Docker image**
5. **Login to DockerHub** (using Jenkins credentials)
6. **Push Docker image** to DockerHub

## Jenkins Setup Requirements

### 1. Jenkins Plugins
Install the following plugins in Jenkins:
- Docker Pipeline
- Python Plugin
- Pipeline Plugin
- Git Plugin

### 2. Global Tool Configuration
Configure in **Manage Jenkins → Global Tool Configuration**:
- **Python**: Ensure Python 3.11+ is available on Jenkins agents
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
* Go to [DockerHub](https://hub.docker.com/) → your repo should contain `python-demo-app`
* Pull and run the pushed image:

  docker pull <your-dockerhub-username>/python-demo-app:latest
  docker run -p 3000:3000 <your-dockerhub-username>/python-demo-app:latest

**CI/CD** → Automates building, testing, and deploying code.  
**Jenkins** → Open-source automation server for building CI/CD pipelines.  
**Docker** → Packages the app into a portable container image.  
**DockerHub** → Public/private registry to store and distribute Docker images.

