
# devops-mini-service

A mini backend service built with Flask to demonstrate an end-to-end DevOps workflow including CI/CD, security, observability, containerization, and Kubernetes deployment.

---

## Project Overview

This project is an individual DevOps mini-project designed to practice real-world DevOps concepts:

- Backend development
- CI/CD automation
- Static & dynamic security scanning
- Docker & Kubernetes
- Observability with metrics

The application performs simple numerical computations and exposes monitoring metrics.

---

##  Features

- Compute:
  - Square of a number
  - Square root (only for non-negative values)
- HTML user interface (Flask + Bootstrap)
- REST endpoints
- Structured logging with request trace ID
- Prometheus-ready `/metrics` endpoint
- Automated CI/CD pipeline (GitHub Actions)
- SAST with Semgrep
- DAST with OWASP ZAP
- Docker container (Gunicorn + Flask)
- Kubernetes deployment using Kind
- Automation via Makefile

##  Prerequisites

- Python 3.10+
- pip
- Docker & Docker Compose
- Git
- kubectl
- Kind
- Make

---

##  Local Setup

### Clone the repository

```bash
git clone https://github.com/ilef713/devops-mini-service.git
cd devops-mini-service

Install dependencies
make install

Run tests
make test

Run the application locally
make run

Access:

 App: http://localhost:5000

 Metrics: http://localhost:5000/metrics


Docker

Build Docker image
make docker-build

Run Docker container
make docker-run

Push to Docker Hub
make docker-push


Security Scanning
Static Application Security Testing (SAST)

Uses Semgrep to analyze source code.
make sast

Dynamic Application Security Testing (DAST)
Uses OWASP ZAP to scan the running service.
make dast

Prometheus & Grafana
Start monitoring stack:
make obs-up

Access:
 Prometheus: http://localhost:9090
 Grafana: http://localhost:3000

Stop services:
make obs-down

Kubernetes Deployment (Kind)
Create Kind cluster
make kind-create

Deploy application
make k8s-deploy

Check status
make k8s-status

Access application
make k8s-port-forward

Then open:
http://localhost:5000
