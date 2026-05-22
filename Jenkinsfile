pipeline {
    agent any

    environment {
        IMAGE_NAME = "YOUR_DOCKERHUB_USERNAME/flask-devops-app"
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo 'Cloning repository...'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER .'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push $IMAGE_NAME:$BUILD_NUMBER'
            }
        }

        stage('Deploy Container') {
            steps {

                sh '''
                docker stop flask-app || true
                docker rm flask-app || true

                docker run -d \
                --name flask-app \
                -p 5000:5000 \
                $IMAGE_NAME:$BUILD_NUMBER
                '''
            }
        }
    }
}
