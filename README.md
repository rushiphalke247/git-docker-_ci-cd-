#  CI/CD Pipeline to Build and Deploy a Web App

This project demonstrates a complete CI/CD pipeline using **Jenkins** and **Docker** to automatically build, test, and deploy a Python Flask web application.

**🎯 TASK 2 COMPLETED**: Simple Jenkins Pipeline for CI/CD with automated build, test, and deploy stages.

## 🏗️ Pipeline Architecture

```
Developer → Push Code → GitHub Repo
                           |
                           ▼
                    Jenkins CI/CD Pipeline
                           |
        ┌──────────────────────────────────────┐
        │  📋 Checkout → 🐍 Setup → 📦 Dependencies  │
        │  🔨 Build → 🧪 Test → 🐳 Docker Build     │
        │  📤 Push → 🚀 Deploy → ✅ Verify        │
        └──────────────────────────────────────┘
                           |
                    🌐 Live Application
                   (http://localhost:3001)
```

## ✨ Features

### Application Features
- **Python Flask** web application
- **RESTful API** with health endpoints
- **Comprehensive test suite** with multiple test cases
- **Docker containerization** for consistent deployments

### CI/CD Pipeline Features  
- **🔄 Automatic triggering** on code commits via webhooks
- **🔨 Build stage** with artifact generation and archiving
- **🧪 Comprehensive testing** with detailed reporting
- **🐳 Docker image** building and registry push
- **🚀 Automated deployment** with health verification
- **📊 Pipeline monitoring** with detailed logging
- **🧹 Automatic cleanup** and resource management

## 📁 Project Structure

```
python-demo-app/
├── Jenkinsfile              # 🔧 Jenkins pipeline configuration
├── Dockerfile               # 🐳 Container build instructions
├── app.py                   # 🐍 Main Flask application
├── requirements.txt         # 📦 Python dependencies
├── test.py                  # 🧪 Comprehensive test suite
├── README.md               # 📖 This documentation
├── JENKINS_SETUP.md        # 🛠️ Detailed setup guide
└── .gitignore              # 🚫 Git ignore rules
```

## 🚀 Quick Start

### Prerequisites
- **Jenkins** (local or cloud instance)
- **Docker** installed and running
- **Python 3.x** available
- **GitHub account** for repository hosting

### 1. Clone the Repository
```bash
git clone https://github.com/rushiphalke247/git-docker-_ci-cd-.git
cd git-docker-_ci-cd-
```

### 2. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit [http://localhost:3000](http://localhost:3000) → you should see:
```
Hello from python-demo-app!
```

### 3. Run Tests Locally
```bash
python test.py
```

## 🔧 Jenkins Pipeline Setup

### Quick Setup (5 minutes)
1. **Install Jenkins** with Docker Pipeline plugin
2. **Configure credentials** for DockerHub
3. **Create pipeline job** pointing to this repository
4. **Set up webhook** for automatic triggering
5. **Trigger first build** and monitor results

### Detailed Setup
📖 **See [JENKINS_SETUP.md](JENKINS_SETUP.md)** for comprehensive setup instructions including:
- Jenkins installation options (local, cloud, Docker)
- Required plugins and configurations
- Credential management
- Webhook setup
- Troubleshooting guide

## 🔄 Pipeline Stages

### 1. 📋 Checkout
```groovy
- Pulls latest code from repository
- Shows commit information  
- Sets up workspace
```

### 2. 🐍 Setup Environment
```groovy
- Verifies Python installation
- Checks pip availability
- Displays environment info
```

### 3. 📦 Install Dependencies
```groovy
- Installs requirements.txt packages
- Handles different pip command variations
- Confirms successful installation
```

### 4. 🔨 Build
```groovy
- Creates build artifacts
- Packages application files
- Archives build artifacts
```

### 5. 🧪 Test
```groovy
- Runs comprehensive test suite
- Generates test reports and logs
- Fails pipeline if tests fail
```

### 6. 🐳 Build Docker Image
```groovy
- Builds optimized Docker image
- Tags with latest and build number
- Prepares for registry push
```

### 7. 📤 Push to Registry
```groovy
- Pushes image to DockerHub
- Makes available for deployment
- Tags with multiple versions
```

### 8. 🚀 Deploy
```groovy
- Stops existing containers
- Runs new container with latest image
- Verifies deployment success
- Provides access URLs
```

## 🐳 Docker Usage

### Build and Run Locally
```bash
# Build image
docker build -t python-demo-app .

# Run container  
docker run -p 3000:3000 python-demo-app
```

### Pull from DockerHub
```bash
# Pull latest image
docker pull rushiphalke2003/python-demo-app:latest

# Run from registry
docker run -p 3000:3000 rushiphalke2003/python-demo-app:latest
```

## 🧪 Testing

### Test Levels
- **Unit Tests**: Core application functionality
- **Integration Tests**: Route and endpoint testing  
- **Contract Tests**: API response validation
- **Health Tests**: Application availability checks

### Test Reports
- **Console Output**: Real-time test execution
- **JSON Reports**: Machine-readable test results
- **Archived Logs**: Historical test data
- **Coverage Metrics**: Code coverage analysis

### Run Test Suite
```bash
# Basic test run
python test.py

# Verbose test output
python -m unittest test.py -v

# Generate coverage report (if coverage installed)
coverage run test.py && coverage report
```

## 📊 Pipeline Monitoring

### Jenkins Dashboard Features
- **📈 Build History**: Track success/failure trends
- **⏱️ Stage Duration**: Identify bottlenecks  
- **📋 Console Logs**: Detailed execution information
- **🔔 Notifications**: Email/Slack alerts on failures
- **📊 Test Results**: Test execution summaries

### Application Monitoring
```bash
# Check deployment status
docker ps | grep python-demo-app

# View application logs
docker logs python-demo-app

# Monitor resource usage
docker stats python-demo-app

# Test application health
curl http://localhost:3001
```

## 🛠️ Configuration

### Environment Variables
- `PORT`: Application port (default: 3000)
- `IMAGE_NAME`: Docker image name
- `DOCKERHUB_CREDENTIALS`: Jenkins credential ID

### Pipeline Customization
Modify `Jenkinsfile` to customize:
- **Build stages**: Add/remove pipeline stages
- **Test configuration**: Change test commands
- **Deployment targets**: Modify deployment destinations
- **Notification settings**: Add Slack/email notifications

## 🔒 Security Best Practices

### Implemented Security Measures
- **🔐 Credential Management**: Secure storage of sensitive data
- **🛡️ Container Security**: Non-root user in containers
- **🔒 Network Security**: Minimal port exposure
- **📝 Audit Logging**: Complete pipeline audit trail

### Security Recommendations
- Regularly update base images
- Scan images for vulnerabilities
- Use specific version tags
- Implement proper access controls

## 🚨 Troubleshooting

### Common Issues
| Issue | Solution |
|-------|----------|
| **Pipeline fails at checkout** | Verify repository URL and credentials |
| **Docker permission denied** | Add jenkins user to docker group |
| **Port already in use** | Stop existing containers |
| **Tests failing** | Check application dependencies |
| **Push to registry fails** | Verify DockerHub credentials |

### Debug Commands
```bash
# Check Jenkins logs
tail -f /var/log/jenkins/jenkins.log

# Verify Docker connectivity
docker info

# Test Python environment  
python --version && pip --version

# Check application locally
python app.py &
curl http://localhost:3000
```

## 📚 Additional Resources

### Documentation
- **[Jenkins Setup Guide](JENKINS_SETUP.md)**: Comprehensive setup instructions
- **[Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)**: Official pipeline documentation
- **[Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)**: Container optimization guides

### Tools and Plugins
- **[Blue Ocean](https://www.jenkins.io/projects/blueocean/)**: Enhanced pipeline visualization
- **[Pipeline Stage View](https://plugins.jenkins.io/pipeline-stage-view/)**: Stage execution monitoring  
- **[Docker Pipeline](https://plugins.jenkins.io/docker-workflow/)**: Docker integration plugin

## 🎉 Success Metrics

A successful pipeline deployment includes:
- ✅ **All 8 stages completed** without errors
- ✅ **100% test pass rate** with comprehensive coverage
- ✅ **Docker image built and pushed** to registry
- ✅ **Application deployed and accessible** on port 3001
- ✅ **Health checks passing** post-deployment
- ✅ **Pipeline execution time** under 5 minutes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

The CI/CD pipeline will automatically test your changes!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

For issues and questions:
- **GitHub Issues**: [Create an issue](https://github.com/rushiphalke247/git-docker-_ci-cd-/issues)
- **Documentation**: Check [JENKINS_SETUP.md](JENKINS_SETUP.md)
- **Community**: Jenkins community forums

---

**🎯 TASK 2 STATUS: ✅ COMPLETED**
- ✅ Jenkins pipeline created with Jenkinsfile
- ✅ Build, test, and deploy stages implemented  
- ✅ Automatic triggering on commits configured
- ✅ Docker containerization integrated
- ✅ Comprehensive documentation provided

*Ready for production deployment! 🚀*


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

