# devops-mini-service

Mini backend Flask pour le projet DevOps.

## Description

Cette application Flask permet de calculer :  
- Le carréd’un nombre  
- La racine carrée d’un nombre (uniquement si positif)  

Elle expose également :  
- Un endpoint /metrics pour les métriques basiques  
- Des logs structurés et un trace ID pour chaque requête  


## Prerequisites

- Python 3.10+
- pip
- Docker
- Kubernetes (Kind ou minikube)
- Git


## Setup Instructions

1. Cloner le repo :  
git clone https://github.com/ilef713/devops-mini-service.git
cd devops-mini-service

2.Installer les dépendances Python :
python -m pip install --upgrade pip
pip install -r requirements.txt

3.Lancer les tests :
pytest -q

4.exécuter le service localement :
python app.py
Le service sera accessible sur :
 http://localhost:5000
Metrics : http://localhost:5000/metrics

5.Docker Usage
docker build -t ilef7103/devops-mini-service:latest .

docker run -p 5000:5000 ilef7103/devops-mini-service:latest

6.Kubernetes Deployment (Kind)
-Créer un cluster KIND :
kind create cluster --name devops-mini --config kind-config.yaml

-Appliquer les manifests Kubernetes :
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

-Vérifier que le pod est prêt :
kubectl get pods
kubectl get svc

-Accéder au service via NodePort :
kubectl port-forward svc/devops-mini-service 5000:5000
curl http://localhost:5000

7.API Examples
GET /
Accède à la page HTML principale.

POST /
Formulaire pour calculer le carré et la racine 

GET /metrics