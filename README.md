markdown# Automated CI/CD Pipeline for Containerized Node.js Application

This repository contains a fully automated, production-ready CI/CD pipeline built for a containerized Node.js application. The pipeline automates the lifecycle from source code management to containerized deployment and infrastructure monitoring.

---

## 🏗️ Architecture Overview

Use code with caution.Developer ──> [Git Push] ──> GitHub ──> [Webhook/Poll] ──> Jenkins Server│┌─────────────────────── [Vision-Action Loop] ─────────────┘▼[1. Checkout] ──> [2. Multi-stage Build] ──> [3. Test Execution]│┌────────────────────────────────────────────────┘▼[4. Push to Docker Hub] ──> [5. Blue/Green Zero-Downtime Deploy]│┌────────────────────────────────────────────────┘▼[6. Infrastructure Monitoring] <── Prometheus + Grafana
### Production Isolation Strategy (Design Note)
To maintain a cost-effective setup for this evaluation, all components (Jenkins, Application, Prometheus, and Grafana) run on a single **AWS EC2 (t3.medium)** instance. 

To eliminate resource and networking conflicts in this single-node topology:
* **Network Isolation:** Ports are explicitly mapped (`3000` for the application, `8080` for Jenkins, `9090` for Prometheus, and `4000` for Grafana) to prevent internal binding overlapping.
* **Deployment Stability:** The deployment phase uses a **zero-downtime rollover script** (detailed below) ensuring the production application is never knocked offline by a failing build stage.

---

## 🛠️ Tech Stack & Tools

* **Source Control:** GitHub
* **CI/CD Automation:** Jenkins (Declarative Pipeline)
* **Containerization:** Docker (Multi-stage builds)
* **Cloud Infrastructure:** AWS EC2 (Ubuntu 22.04 LTS)
* **Monitoring & Observability:** Prometheus & Grafana

---

## 🚀 Step-by-Step Implementation Guide

### Step 1: Clone and Local Verification
To run and verify the environment configuration locally before automated deployment:
```bash
# Clone the repository
git clone https://github.com<your-username>/devops-cicd-assignment.git
cd devops-cicd-assignment

# Build the production multi-stage image
docker build -t sample-app:latest .

# Run container locally
docker run -d -p 3000:3000 --name local-test sample-app:latest

# Verify endpoint availability
curl http://localhost:3000/health
```

### Step 2: Infrastructure & Host Provisioning
The EC2 server requires dependencies to execute the Jenkins lifecycle securely. Use the following baseline to provision the instance:
```bash
sudo apt update && sudo apt upgrade -y

# Docker Engine Installation
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://docker.com | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=\((dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://docker.com\)(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update && sudo apt install docker-ce -y

# Jenkins System & Core Installation (Java 17 runtime dependency)
sudo apt install fontconfig openjdk-17-jre -y
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://jenkins.io
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://jenkins.io binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update && sudo apt install jenkins -y

# Security Matrix and Permissions Alignment
sudo usermod -aG docker jenkins
sudo usermod -aG docker ubuntu
sudo systemctl restart jenkins
sudo systemctl restart docker
```

### Step 3: CI/CD Pipeline Automation
The core automation is handled natively by the `Jenkinsfile` using a declarative syntax model. 

#### Pipeline Stages Detailed:
1. **Checkout:** Pulls the targeted git state directly onto the workspace directory.
2. **Build:** Compiles the localized `Dockerfile` into an absolute image tagged with the unique `${BUILD_NUMBER}` metric.
3. **Test:** Spins up an isolated ephemeral container instance to execute unit tests (`npm test`).
4. **Push Image:** Securely injects credentials into the docker engine socket, authenticates against Docker Hub registries, and ships images tagged as `latest` and `${BUILD_NUMBER}`.
5. **Zero-Downtime Deploy:** Instead of blindly terminating the old workspace application, the pipeline executes a safe sequence:
   * Spins up the incoming image version under a temporary tracking identifier (`app-candidate`).
   * Tests the new container's operational health status via curling `/health`.
   * Swaps context gracefully: terminates the previous iteration and scales the new build seamlessly into place.

---

## 📊 Observability & Monitoring Metrics

Monitoring tools run inside independent docker run-time scopes to safely decouple them from the application stack.

### 1. Prometheus Configuration
The host metrics collection layer utilizes a persistent configuration mapping:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'production-node-metrics'
    static_configs:
      - targets: ['localhost:9090']
```
Run the metrics monitoring instance using:
```bash
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v \$(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

### 2. Grafana Dashboards
Grafana handles metric presentation layer visualization and runs on port `4000` to completely mitigate application mapping conflicts on port `3000`:
```bash
docker run -d --name grafana -p 4000:4000 grafana/grafana
```
* **Dashboard Focus:** Preconfigured to observe CPU utilization spikes, total RAM allocation consumption trends, and continuous network packet data movement over time.

---

## 📑 Interview Submission Deliverables

* **GitHub Repository:** `https://github.com<your-username>/devops-cicd-assignment`
* **Dockerfile Location:** `/Dockerfile`
* **Pipeline Infrastructure Specification:** `/Jenkinsfile`
* **Live Application Production Endpoint:** `http://<your-ec2-public-ip>:3000`
* **Live Monitoring Platform Endpoint:** `http://<your-ec2-public-ip>:4000`
