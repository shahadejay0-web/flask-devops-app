pipeline {
    agent any

    environment {
        IMAGE_NAME = "jayshahade/devops-monitoring-app"
        CONTAINER_NAME = "flask-app"
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo 'Cloning GitHub repository...'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME:$BUILD_NUMBER .
                '''
            }
        }

        stage('Docker Login') {
            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-cred',
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

                sh '''
                docker push $IMAGE_NAME:$BUILD_NUMBER

                docker tag $IMAGE_NAME:$BUILD_NUMBER $IMAGE_NAME:latest

                docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Deploy Container') {
            steps {

                sh '''
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true

                docker run -d \
                --name $CONTAINER_NAME \
                -p 5000:5000 \
                $IMAGE_NAME:$BUILD_NUMBER
                '''
            }
        }

        stage('Show Running Containers') {
            steps {
                sh 'docker ps'
            }
        }
    }

    post {

        success {
            echo 'Pipeline executed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}
