Random Forest MLOps Project

Project Overview

This project demonstrates a simple end-to-end MLOps workflow using:

FastAPI
Docker
GitHub Actions
AWS ECR
AWS ECS Fargate
Terraform

The application uses a trained Random Forest model to predict handwritten digits from the MNIST dataset.

The goal of this project was to:

containerize the application
automate CI/CD pipeline
push Docker images to AWS ECR
provision infrastructure using Terraform
deploy the application into ECS Fargate

Architecture
Developer Push
      ↓
GitHub Actions CI
      ↓
Run Tests + Lint
      ↓
Build Docker Image
      ↓
Push Image to AWS ECR
      ↓
GitHub Actions Deploy Workflow
      ↓
Terraform Apply
      ↓
AWS ECS Fargate Deployment
      ↓
Public API Endpoint

Technologies Used
| Tool            | Purpose                 |
| --------------- | ----------------------- |
| Python          | Application development |
| FastAPI         | REST API                |
| Scikit-learn    | ML model                |
| Docker          | Containerization        |
| GitHub Actions  | CI/CD                   |
| Terraform       | Infrastructure as Code  |
| AWS ECR         | Docker image registry   |
| AWS ECS Fargate | Container deployment    |
| Flake8          | Linting                 |
| Pytest          | Testing                 |


Project Structure

.
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
│
├── app/
│   ├── api/
│   ├── models/
│   └── services/
│
├── terraform/
│   ├── provider.tf
│   ├── main.tf
│   └── outputs.tf
│
├── tests/
├── Dockerfile
├── requirements.txt
└── README.md


Application Workflow
1. Model Training

The Random Forest model is trained using the MNIST dataset.

After training:

model artifacts are stored locally
FastAPI loads the trained model during startup


2. API Service

FastAPI exposes prediction endpoints.

Example:

POST /predict

The API receives image input and returns predicted digit output.


3. Docker Containerization

The application is packaged into a Docker image.

Main steps:

install dependencies
copy source code
expose FastAPI port
start uvicorn server

The container runs using:
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]


CI Pipeline

GitHub Actions CI pipeline performs:

dependency installation
lint checks using flake8
unit testing using pytest
Docker image build
image push to AWS ECR

The image is tagged using:

latest
timestamp tag

example
latest
20260524-171756


AWS Deployment
ECR

Docker images are stored in:
146713999197.dkr.ecr.ap-south-2.amazonaws.com/mnist-random-forest/random

ECS Fargate

Terraform creates:

ECS Cluster
ECS Service
Task Definition
Security Group
IAM Roles

The application is deployed as a Fargate task with public IP enabled.
Terraform Workflow

Terraform is used for Infrastructure as Code.

Deployment flow:

terraform init
terraform plan
terraform apply


Public Access

After deployment:

ECS task receives a public IP
application becomes accessible through: http://40.192.38.14:8000/docs
