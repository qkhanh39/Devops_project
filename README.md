# Devops_project

* Contents:
    * [Introduction](#introduction)
    * [Tech stack](#techstack)
    * [CI/CD workflow summary](#workflow)
    * [Setup instructions](#setup)


## Introduction
This project is part of a course assignment focused on learning and applying DevOps practices. It demonstrates the implementation of a complete CI/CD pipeline using modern DevOps tools and cloud infrastructure.
The pipeline automates key stages such as code testing, quality analysis, security scanning, containerization, and deployment to a Kubernetes cluster on AWS. The main goal of this project is to gain hands-on experience with setting up automated pipelines and managing cloud-based deployments.

## Tech stack
- **CI/CD**: [Jenkins](https://www.jenkins.io/)
- **Code Quality**: [SonarQube](https://www.sonarqube.org/)
- **Security Scanning**: [Trivy](https://github.com/aquasecurity/trivy)
- **Container Orchestration**: [Kubernetes](https://kubernetes.io/)
- **Cloud Provider**: [Amazon Web Services (AWS)](https://aws.amazon.com/)
- **Infrastructure as Code**: [Terraform](https://developer.hashicorp.com/terraform)

## CI/CD Workflow Summary
1. **Code Push**: Developer pushes code to the `main` branch on GitHub.
2. **Jenkins Trigger**: Jenkins automatically pulls the latest code and starts the pipeline.
3. **Code Quality & Security**: SonarQube analyzes the code quality, and Trivy scans for vulnerabilities.
4. **Docker Build & Push**: A Docker image is built and pushed to Docker Hub.
5. **Deployment**: Jenkins deploys the application and database to a Kubernetes cluster on AWS (EKS).

## ⚙️ Setup Instructions

### Prerequisites
- AWS CLI and kubectl configured with access to EKS
- Docker installed and logged in to Docker Hub
- Jenkins with required plugins: Git, Docker, SonarQube, Kubernetes CLI, Trivy
- SonarQube server running and configured in Jenkins
- Jenkins credentials set:
  - `mysql-root-password` (Secret text)
  - `dockerhub` (Username + password)
  - `sonarqube-token` (Secret text)
  - `kubernetes` (Kubeconfig file)

### Steps

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/qkhanh39/Devops_project.git
   cd Devops_project

2. **Use Terraform to Create an EC2 Instance**

- Create a new IAM user in AWS with programmatic access and EC2 permissions.
- Generate Access Key and Secret Access Key.
- Configure your AWS CLI:
  
  ```bash
  aws configure
- Then run the following Terraform commands:
    ```bash
    terraform init
    terraform plan
    terraform apply -auto-approve

3. **Jenkins configuration**
- Go to the AWS Console and copy the Public IPv4 of your EC2 instance.
- Access Jenkins via:
    ```bash
    http://<public-ipv4>:8080
- Complete Jenkins setup and install the suggested plugins.
- Create an admin user.

3. **Sonarqube configuration**
- Access SonarQube via:
    ```bash
    http://<public-ipv4>:9000
- Generate a project token to use in Jenkins (SonarQube > My Account > Security).
- In SonarQube, go to Administration > Webhooks and add a webhook with the private IPv4 of your EC2 instance.

4. **Create Jenkins pipeline to build and push Docker Image to Dockerhub**
- In Jenkins, click New Item > select Pipeline.
- In the Pipeline script section, paste the contents of your Jenkinsfile (adjust credentials, Docker image name, etc.).
- Add DockerHub credentials in Manage Jenkins > Credentials.
5. **Create AWS EKS Cluster and Download the secret file for EKS Cluster**
- Generate and download a key pair from AWS
- On your local machine:    
    ```bash
    chmod 400 <your-key-pair-name>.pem
    ssh -i ~/.ssh/<your-key-pair-name>.pem ubuntu@<public-ipv4>
- Install pre-requisites
    ```bash
    sudo apt update
    sudo apt install curl
    sudo api install unzip
    curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
- Check the version of kubectl via:
    ```bash
    kubectl version --client
- Now install AWS CLI
    ```bash
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
- Check the version
    ```bash
    aws --version
- Install eks
    ```bash
    curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
    cd /tmp
    sudo mv /tmp/eksctl /bin
- Check the version
    ```bash 
    eksctl version
- Follow the instruction to create IAM role and attach that to EC2 instance
- Create eks cluster
    ```bash
    eksctl create cluster --name <your-cluster-name> --region <your-region> --note-type <your-node-type> --managed --nodes <number-of-your-nodes>
- You can check all nodes and services via
    ```bash
    kubectl get nodes
    kubectl get svc
- Copy the config file in the .kube folder

6. **Configure the Jenkins pipeline to deploy application on AWS EKS**
- Click on Manage Jenkins -> Credentials -> Add credentials and upload the config file
7. **Set the trigger and verify CI/CD pipeline**
- Choose configure -> Github project and paste the url of your github project
- Tick on the Github hook trigger for GITScm polling
- Navigate to your github project and choose Settings -> Webhooks -> Add webhook -> paste your Jenkins url to Payload URL and set:
    ```bash
    https://<your-jenkins-url>/github-webhook/
- You can choose the events to trigger (in my case is just the push event)
- Click on Add webhook
8. **Testing**
- You can change any file in you repo and push on the main branch, then Jenkins will trigger automatically
- In the EC2 terminal, run
    ```bash 
    kubectl get svc
- Copy the External-IP of our app and access it via browser.
## Demo
[Watch the demo on Google Drive](https://drive.google.com/file/d/1B2w5OM01WinL2lyND0XpwCbVKRKN4w0u/view?usp=sharing)
