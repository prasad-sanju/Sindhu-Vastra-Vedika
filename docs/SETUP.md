# Sindhu Vastra Vedika - Real Project Setup

## 1. Local application

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python seed.py
python run.py
```

Open http://localhost:5000

## 2. Git - push the complete repository

```powershell
git init
git branch -M main
git add .
git commit -m "Initial commit - Sindhu Vastra Vedika"
git remote add origin <GITHUB_REPO_URL>
git remote add ado <AZURE_DEVOPS_REPO_URL>
git push -u origin main
git push -u ado main
```

## 3. One-time Terraform state bootstrap

The remote backend cannot create the storage account it needs before the backend exists. Run this one time from your workstation:

```powershell
az login
cd terraform/bootstrap-state
terraform init
terraform apply
terraform output storage_account_name
```

Copy the output value. Example:

```text
svvtfstate12345678
```

Then create the Azure DevOps variable:

```text
TF_STATE_STORAGE_ACCOUNT = svvtfstate12345678
```

The Azure DevOps service connection must have `Storage Blob Data Contributor` on the `svv-tfstate-rg` storage account/container.

## 4. Main Terraform

Copy `terraform/terraform.tfvars.example` to `terraform/terraform.tfvars` for local testing and replace the globally unique ACR/Key Vault names.

For local Terraform state migration, copy `terraform/backend.tf.example` to `terraform/backend.tf`, then run:

```powershell
cd terraform
terraform init -migrate-state \
  -backend-config="resource_group_name=svv-tfstate-rg" \
  -backend-config="storage_account_name=<STATE_STORAGE_ACCOUNT>" \
  -backend-config="container_name=tfstate" \
  -backend-config="key=svv-dev.tfstate" \
  -backend-config="use_azuread_auth=true"
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

## 5. Azure DevOps service connections

Create:

- `SVV-Azure-Service-Connection` - Azure Resource Manager connection for Terraform/AKS.
- `SVV-ACR-Service-Connection` - Docker Registry connection to the ACR.

Update the names in `azure-pipelines.yml` if your names differ.

Update `acrName` in `azure-pipelines.yml` to exactly match the Terraform ACR name.

Create Azure DevOps Environment:

```text
SVV-DEV
```

Optionally configure an approval/check on that environment before production use.

## 6. Pipeline flow

CI -> Python tests -> Terraform -> Docker build/push -> AKS deployment

The Docker image is tagged with `Build.BuildId`, not `latest`, so each deployment is traceable.

## 7. Security

Never commit:

- `.env`
- passwords/API keys
- kubeconfig
- `terraform.tfstate`
- `terraform.tfvars` if it contains secrets

Key Vault and AKS Workload Identity are enabled in the infrastructure. Wire application runtime secrets through Key Vault + Secrets Store CSI Driver before adding production credentials.
