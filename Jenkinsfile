pipeline {
    agent any

    environment {
        AWS_REGION     = "us-east-1"
        ECR_ACCOUNT_ID = "842871321276"
        ECR_REPO_NAME  = "devops_2"
        ECR_REPO       = "${ECR_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"
        CLUSTER_NAME   = "eks-cluster-devops"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Dhanushbablu630/Devops_project2.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build -t $ECR_REPO:$BUILD_NUMBER .
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                withAWS(credentials: 'aws-creds', region: "$AWS_REGION") {
                    sh '''
                        echo "Logging in to Amazon ECR..."
                        aws ecr get-login-password --region $AWS_REGION \
                        | docker login --username AWS --password-stdin ${ECR_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                        
                        echo "Pushing Docker image to ECR..."
                        docker push $ECR_REPO:$BUILD_NUMBER
                    '''
                }
            }
        }

        stage('Debug AWS Identity') {
            steps {
                withAWS(credentials: 'aws-creds', region: "$AWS_REGION") {
                    sh '''
                        echo "Checking which IAM identity Jenkins is using..."
                        aws sts get-caller-identity
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withAWS(credentials: 'aws-creds', region: "$AWS_REGION") {
                    sh '''
                        echo "Setting up kubeconfig..."
                        aws eks --region $AWS_REGION update-kubeconfig --name $CLUSTER_NAME --alias $CLUSTER_NAME

                        echo "Testing Kubernetes access..."
                        kubectl get nodes

                        echo "Applying deployment manifest..."
                        kubectl apply -f k8s-deployment.yaml

                        echo "Updating Kubernetes deployment..."
                        kubectl set image deployment/myapp-deployment myapp=$ECR_REPO:$BUILD_NUMBER || true
                    '''
                }
            }
        }
    }
}
