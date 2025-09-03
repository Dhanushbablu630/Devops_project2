pipeline {
    agent any

    environment {
        AWS_REGION     = "us-east-1"  
        ECR_ACCOUNT_ID = "842871321276"  
        ECR_REPO_NAME  = "devops_2"  
        ECR_REPO       = "${ECR_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/Dhanushbablu630/Devops_project2.git'  
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $ECR_REPO:$BUILD_NUMBER .'
            }
        }

        stage('Push to ECR') {
            steps {
                withAWS(credentials: 'aws-creds', region: "$AWS_REGION") {
                    sh '''
                        aws ecr get-login-password --region $AWS_REGION \
                        | docker login --username AWS --password-stdin ${ECR_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    '''
                    sh 'docker push $ECR_REPO:$BUILD_NUMBER'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withAWS(credentials: 'aws-creds', region: "$AWS_REGION") {
                    sh '''
                        kubectl set image deployment/myapp-deployment myapp=$ECR_REPO:$BUILD_NUMBER --record \
                        || kubectl apply -f k8s-deployment.yaml
                    '''
                }
            }
        }
    }
}
