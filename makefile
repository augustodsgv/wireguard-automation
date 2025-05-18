TF_DIR ?= ./terraform
INVENTORY_FILE ?= ./ansible/inventory.yaml
ANSIBLE_PLAYBOOK ?= ./ansible/playbook.yaml
export KUBECONFIG := ./k8s/kubeconfig.yaml
K8S_DIR ?= ./k8s

.PHONY: help deploy destroy terraform inventory ansible clean all

help:
	@echo "Usage: make [terraform|ansible]"
	@echo "  deploy             - Deploy prometheus ring on docker swarm and mimir on k8s [TODO]"
	@echo "  destroy            - Remove running services"
	@echo "  terraform          - Run Terraform initialization and apply"
	@echo "  ansible            - Runs the Ansible playbook"

terraform-init:
	@echo Initializing Terraform project...
	terraform -chdir=$(TF_DIR) init -upgrade

terraform:
	@echo Building Terraform infraestructure...
	terraform -chdir=$(TF_DIR) apply

terraform-destroy:
	@echo Destroying Terraform infraestructure...
	terraform -chdir=$(TF_DIR) destroy

ansible:
	@echo "Running Ansible Playbook..."
	ansible-playbook -i $(INVENTORY_FILE) $(ANSIBLE_PLAYBOOK)
