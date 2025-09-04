# Jenkins + Docker + EKS CI/CD Project

## Project Overview

This project demonstrates a **complete CI/CD pipeline** where an application is automatically built, containerized, pushed to Amazon ECR, and deployed to an Amazon EKS cluster using Kubernetes.  

**Key Achievements:**
- Automated building and deployment of applications using **Jenkins pipelines**.
- Dockerized the application for portability.
- Deployed the application to **AWS Elastic Kubernetes Service (EKS)**.
- Configured **Kubernetes Deployment and Service manifests** for scalable application deployment.
- Learned integration between **AWS, Docker, Kubernetes, and Jenkins**.

---

## Architecture
GitHub → Jenkins → Docker → Amazon ECR → EKS → LoadBalancer → Browser

- **GitHub**: Hosts the application source code and Jenkinsfile.
- **Jenkins**: Orchestrates the CI/CD pipeline.
- **Docker**: Packages the application into a container.
- **Amazon ECR**: Stores the Docker image.
- **Amazon EKS**: Runs the application in Kubernetes pods.
- **LoadBalancer**: Exposes the application publicly.

---

## Steps & Commands

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Build Docker image
```
docker build -t <image-name>:latest .
```
### 3. Push Docker image to ECR
```
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<region>.amazonaws.com
docker tag <image-name>:latest <aws-account-id>.dkr.ecr.<region>.amazonaws.com/<repository-name>:latest
docker push <aws-account-id>.dkr.ecr.<region>.amazonaws.com/<repository-name>:latest
```
### 4. Create EKS cluster (using eksctl)
```
eksctl create cluster \
  --name my-eks-cluster \
  --region <region> \
  --nodes 2 \
  --node-type t3.small
```
### 5. Configure kubectl for EKS
```
aws eks --region <region> update-kubeconfig --name my-eks-cluster
kubectl get nodes
```

### 6. Deploy application to Kubernetes
```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get svc
```

### 7. Access the application

- Open the EXTERNAL-IP of the LoadBalancer service in a browser.

---

# Learning Outcomes

- Hands-on experience with CI/CD pipelines using Jenkins.

- Containerizing applications using Docker.

- Managing AWS resources like ECR and EKS.

- Deploying applications in Kubernetes using manifests.

- Understanding cluster, node, pod, service concepts in Kubernetes.

- Managing pipeline automation for continuous deployment.
---

# Notes

- This project was implemented using AWS Free Tier (t2.micro/t3.small for nodes).

- For multiple pods or larger applications, node size must be increased due to resource limitations.

- Manual changes inside running pods are ephemeral and will be reset on redeployment.


