1. Local Setup
2. Git & GitHub
3. Docker Setup
4. Terraform Setup
5. Kubernetes Setup
6. Start Commands
7. Stop Commands
8. Cleanup Commands
9. Security Notes
10. Common Errors

<!-- VERY IMPORTANT
INCLUDE THESE COMMANDS

DOCKER START
docker run -p 8501:8501 ai-resume-analyzer


DOCKER STOP
docker stop CONTAINER_ID

MINIKUBE START
minikube start


MINIKUBE STOP
minikube stop


KUBERNETES DEPLOY
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml


KUBERNETES DELETE
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/service.yaml


TERRAFORM APPLY
terraform apply


TERRAFORM DESTROY
terraform destroy


SECURITY SECTION MUST INCLUDE
NEVER PUSH:
.aws/
.env
terraform.tfstate
venv/


ALSO INCLUDE
COST SAFETY NOTES

Example:
Always stop Minikube and Docker containers when not using.
Always destroy unused cloud infrastructure.
Avoid keeping EC2 instances running unnecessarily. -->