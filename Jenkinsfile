pipeline {
    agent any

    environment {
        IMAGE_NAME = "jayshahade/devops-monitoring-app"
        CONTAINER_NAME = "flask-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
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

        stage('Push Image to Docker Hub') {
            steps {
                sh """
                echo "Pushing images..."
                docker push $IMAGE_NAME:$IMAGE_TAG
                docker push $IMAGE_NAME:latest
                """
            }
        }

        stage('Deploy Application') {
            steps {
                sh """
                echo "Stopping old container if exists..."
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true

                echo "Running new container..."
                docker run -d \
                    --name $CONTAINER_NAME \
                    -p 5000:5000 \
                    $IMAGE_NAME:$IMAGE_TAG
                """
            }
        }

        stage('Verify Deployment') {
            steps {
                sh """
                echo "Checking running containers..."
                docker ps
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline SUCCESS: Application deployed successfully 🚀"
        }

        failure {
            echo "Pipeline FAILED ❌ Check logs"
        }
    }
}
