# 🚀 Jenkins CI/CD Pipeline Setup Guide

## Task 2: Simple Jenkins Pipeline for CI/CD

This guide provides complete instructions for setting up a Jenkins CI/CD pipeline that automatically builds, tests, and deploys a Python Flask application.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Jenkins Installation](#jenkins-installation)
- [Pipeline Configuration](#pipeline-configuration)
- [Pipeline Stages](#pipeline-stages)
- [Webhook Setup](#webhook-setup)
- [Testing the Pipeline](#testing-the-pipeline)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### Required Tools
- **Java 11 or higher** (for Jenkins)
- **Docker** (for containerization)
- **Git** (for version control)
- **Python 3.x** (for the application)
- **GitHub/GitLab account** (for repository hosting)

### Required Credentials
- **DockerHub account** for container registry
- **GitHub/GitLab access token** for webhooks

## 🏗️ Jenkins Installation

### Option 1: Local Jenkins Installation

#### Windows Installation
```bash
# Download and install Jenkins from official website
# https://www.jenkins.io/download/

# Or use Chocolatey
choco install jenkins

# Start Jenkins service
net start jenkins
```

#### Linux Installation
```bash
# Ubuntu/Debian
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### Option 2: Docker Jenkins Installation
```bash
# Run Jenkins in Docker
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

### Option 3: Cloud Jenkins (Recommended for Testing)
- **AWS**: Use AWS EC2 with Jenkins AMI
- **Google Cloud**: Use Google Cloud Compute Engine
- **Azure**: Use Azure Virtual Machines

## ⚙️ Pipeline Configuration

### 1. Initial Jenkins Setup
1. Open Jenkins at `http://localhost:8080`
2. Get initial admin password:
   ```bash
   # Linux
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   
   # Windows
   type "C:\Program Files\Jenkins\secrets\initialAdminPassword"
   
   # Docker
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Install suggested plugins
4. Create admin user

### 2. Required Jenkins Plugins
Install these plugins via **Manage Jenkins → Manage Plugins**:
- **Pipeline Plugin** (usually pre-installed)
- **Docker Pipeline Plugin**
- **Git Plugin** (usually pre-installed)
- **GitHub Integration Plugin**

### 3. Configure Global Tools
Go to **Manage Jenkins → Global Tool Configuration**:

#### Python Configuration
- Add Python installation or ensure Python is in PATH
- Configure pip if needed

#### Docker Configuration
- Ensure Docker is available on Jenkins agent
- Test with: `docker --version`

### 4. Set Up Credentials
Go to **Manage Jenkins → Manage Credentials → Global**:

#### DockerHub Credentials
- **Kind**: Username with password
- **ID**: `dockerhub-credentials`
- **Username**: Your DockerHub username
- **Password**: Your DockerHub password/token
- **Description**: DockerHub Registry Credentials

#### GitHub Credentials (for webhooks)
- **Kind**: Secret text
- **Secret**: Your GitHub personal access token
- **ID**: `github-webhook-token`
- **Description**: GitHub Webhook Token

## 🔄 Pipeline Stages

Our Jenkins pipeline includes the following stages:

### 1. **Checkout** 
- Pulls latest code from repository
- Shows commit information
- Sets up workspace

### 2. **Setup Environment** 
- Verifies Python installation
- Checks pip availability
- Lists workspace contents

### 3. **Install Dependencies** 
- Installs Python packages from requirements.txt
- Handles different pip command variations
- Confirms successful installation

### 4. **Build** 
- Creates build directory
- Copies application files
- Creates build artifacts
- Archives artifacts for later use

### 5. **Test** 
- Runs comprehensive test suite
- Generates test reports
- Archives test logs
- Fails pipeline if tests fail

### 6. **Build Docker Image**
- Creates Docker image from Dockerfile
- Tags image with latest and build number
- Optimizes image layers

### 7. **Push to Registry** 
- Pushes Docker image to DockerHub
- Makes image available for deployment
- Tags with multiple versions

### 8. **Deploy** 
- Stops existing application container
- Runs new container with updated image
- Verifies deployment success
- Provides access URLs

##  Webhook Setup

### Automatic Pipeline Triggering

#### 1. Create Jenkins Pipeline Job
1. Go to **Jenkins Dashboard → New Item**
2. Choose **Pipeline** project
3. Name it `python-demo-app-pipeline`

#### 2. Configure Pipeline
In the pipeline configuration:
- **Build Triggers**: Check "GitHub hook trigger for GITScm polling"
- **Pipeline Definition**: Choose "Pipeline script from SCM"
- **SCM**: Git
- **Repository URL**: `https://github.com/yourusername/git-docker-_ci-cd-.git`
- **Branch**: `*/main`
- **Script Path**: `Jenkinsfile`

#### 3. GitHub Webhook Setup
1. Go to your GitHub repository
2. Navigate to **Settings → Webhooks**
3. Click **Add webhook**
4. Configure:
   - **Payload URL**: `http://your-jenkins-url:8080/github-webhook/`
   - **Content type**: `application/json`
   - **Events**: Choose "Just the push event"
   - **Active**:  Checked

#### 4. Test Webhook
- Make a code change and push to repository
- Jenkins should automatically trigger the pipeline

## Testing the Pipeline

### 1. Manual Pipeline Trigger
- Go to your pipeline project
- Click **Build Now**
- Monitor the build in real-time

### 2. Automatic Trigger Test
```bash
# Make a simple change
echo "# Updated on $(date)" >> README.md

# Commit and push
git add README.md
git commit -m "Test pipeline trigger"
git push origin main
```

### 3. Verify Pipeline Stages
Check that all stages execute successfully:
- Checkout
-  Setup Environment  
-  Install Dependencies
-  Build
-  Test
-  Build Docker Image
-  Push to Registry
-  Deploy

### 4. Verify Deployment
After successful deployment:
```bash
# Check running containers
docker ps | grep python-demo-app

# Test the application
curl http://localhost:3001
# Should return: "Hello from python-demo-app!"
```

##  Monitoring and Logs

### Pipeline Monitoring
- **Blue Ocean UI**: Better visualization of pipeline stages
- **Console Output**: Detailed logs for each stage
- **Build History**: Track pipeline success/failure over time

### Application Monitoring
```bash
# Check container logs
docker logs python-demo-app

# Monitor container stats
docker stats python-demo-app

# Check application health
curl http://localhost:3001
```

##  Troubleshooting

### Common Issues and Solutions

#### 1. Pipeline Fails at Checkout
```
Error: Could not authenticate with repository
```
**Solution**: Check repository URL and credentials

#### 2. Python/Pip Not Found
```
Error: python3: command not found
```
**Solutions**: 
- Install Python on Jenkins agent
- Add Python to PATH
- Use Docker agent with Python pre-installed

#### 3. Docker Permission Issues
```
Error: permission denied while trying to connect to Docker daemon
```
**Solutions**:
```bash
# Add jenkins user to docker group (Linux)
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins

# Fix Docker socket permissions
sudo chmod 666 /var/run/docker.sock
```

#### 4. Port Already in Use
```
Error: Port 3001 is already allocated
```
**Solution**:
```bash
# Kill existing container
docker stop python-demo-app
docker rm python-demo-app
```

#### 5. DockerHub Push Fails
```
Error: denied: requested access to the resource is denied
```
**Solutions**:
- Verify DockerHub credentials in Jenkins
- Check image name format: `username/repository:tag`
- Ensure DockerHub repository exists

### Debug Commands
```bash
# Check Jenkins logs
tail -f /var/log/jenkins/jenkins.log

# Check Docker daemon
systemctl status docker

# Verify network connectivity
ping registry-1.docker.io

# Test Python environment
python3 --version
pip3 --version
```

##  Pipeline Success Metrics

A successful pipeline run should show:
-  All stages completed successfully
-  Tests passing with 100% success rate
-  Docker image built and pushed
-  Application deployed and accessible
-  No errors in console output

##  Conclusion

You now have a complete CI/CD pipeline that:
1. **Automatically triggers** on code commits
2. **Builds** the application with proper artifacts
3. **Tests** the application thoroughly
4. **Deploys** the application in a containerized environment
5. **Monitors** the deployment status
