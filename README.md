# Sindhu Vastra Vedika

Production-style Python/Flask e-commerce starter for women's and girls' clothing, with Azure DevOps, Docker, Terraform and AKS deployment structure.

## Stack

- Python 3.12 / Flask
- SQLAlchemy
- Gunicorn
- Docker
- Kubernetes / AKS
- Azure Container Registry
- Terraform / AzureRM
- Azure Key Vault
- Azure DevOps YAML CI/CD

## Repository

```text
app/                         Application source (3-tier)
  business/                  Business/services layer
  data/                      Models/repositories/data layer
  presentation/              HTTP/auth/presentation layer
  templates/                 UI templates
  static/                    CSS
k8s/                         Kubernetes manifests
terraform/                   Azure infrastructure
  bootstrap-state/           One-time remote state bootstrap
scripts/                     Helper scripts
tests/                       Automated tests
Dockerfile                   Production container
azure-pipelines.yml         CI/CD pipeline
requirements.txt             Python dependencies
```

See `docs/SETUP.md` for the exact deployment process.
