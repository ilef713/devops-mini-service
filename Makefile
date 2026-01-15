# ===============================
# Project configuration
# ===============================
APP_NAME=devops-mini-service
IMAGE_NAME=ilef7103/$(APP_NAME)
TAG=latest
CLUSTER_NAME=devops-mini
K8S_DIR=k8s

# ===============================
# Local Python
# ===============================
.PHONY: install test run

install:
	pip install -r requirements.txt

test:
	pytest -q

run:
	python app.py

# ===============================
# Docker
# ===============================
.PHONY: docker-build docker-run docker-push

docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

docker-run:
	docker run -p 5000:5000 $(IMAGE_NAME):$(TAG)

docker-push:
	docker push $(IMAGE_NAME):$(TAG)

# ===============================
# Security
# ===============================
.PHONY: sast dast

sast:
	semgrep --config p/ci

dast:
	docker run --network="host" \
		-v $(PWD):/zap/wrk:rw \
		ghcr.io/zaproxy/zaproxy:stable \
		zap-baseline.py \
		-t http://127.0.0.1:5000 \
		-r zap_report.html || true

# ===============================
# Observability (Docker Compose)
# ===============================
.PHONY: obs-up obs-down

obs-up:
	docker compose up -d

obs-down:
	docker compose down

# ===============================
# Kubernetes (Kind)
# ===============================
.PHONY: kind-create kind-delete k8s-deploy k8s-status k8s-port-forward

kind-create:
	kind create cluster --name $(CLUSTER_NAME) --config kind-config.yaml

kind-delete:
	kind delete cluster --name $(CLUSTER_NAME)

k8s-deploy:
	kubectl apply -f $(K8S_DIR)/deployment.yaml
	kubectl apply -f $(K8S_DIR)/service.yaml

k8s-status:
	kubectl get pods
	kubectl get svc

k8s-port-forward:
	kubectl port-forward svc/devops-mini-service 5000:5000

# ===============================
# Clean
# ===============================
.PHONY: clean

clean:
	docker system prune -f
