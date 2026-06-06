pipeline {
    agent any

    environment {
        IMAGE_NAME = "jayshahade/devops-monitoring-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Checking out source code..."
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                echo "Building Docker image..."
                docker build -t $IMAGE_NAME:$IMAGE_TAG .
                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
                """
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    """
                }
            }
        }

        stage('Push Image') {
            steps {
                sh """
                echo "Pushing Docker images..."
                docker push $IMAGE_NAME:$IMAGE_TAG
                docker push $IMAGE_NAME:latest
                """
            }
        }

        stage('Deploy Stack (Docker Compose)') {
            steps {
                sh """
                echo "Deploying monitoring stack using docker compose..."

                # Use Jenkins workspace (IMPORTANT FIX)
                cd $WORKSPACE

                # Stop old stack
                docker compose down || true

                # Pull latest images
                docker compose pull || true

                # Start stack
                docker compose up -d --build

                echo "Containers running:"
                docker ps
                """
            }
        }

        stage('Verify Deployment') {
            steps {
                sh """
                echo "Checking service status..."

                docker ps

                echo "Flask App:"
                curl -s http://localhost:5000 || true

                echo "Prometheus:"
                curl -s http://localhost:9090 || true

                echo "Grafana:"
                curl -s http://localhost:3000 || true
                """
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline SUCCESS: Full monitoring stack deployed!"
        }

        failure {
            echo "❌ Pipeline FAILED: Check logs for errors"
        }
    }
}
