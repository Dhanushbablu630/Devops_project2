pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "your-dockerhub-username/myapp"
        AWS_REGION = "ap-south-1"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-username/my-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $DOCKER_IMAGE:$BUILD_NUMBER'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withAWS(credentials: 'aws-creds', region: "$AWS_REGION") {
                    sh 'kubectl set image deployment/myapp-deployment myapp=$DOCKER_IMAGE:$BUILD_NUMBER --record || kubectl apply -f k8s-deployment.yaml'
                }
            }
        }
    }
}

