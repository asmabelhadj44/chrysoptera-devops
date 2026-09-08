# W1-02 — Terraform Install & Getting-Started Tutorial

## Objective
Install Terraform and complete a getting-started tutorial to learn the core Infrastructure-as-Code workflow (`init` → `plan` → `apply` → `destroy`), documenting the process.

## Why Docker as the provider
No paid cloud account (AWS/Azure/GCP) was available, so instead of the standard cloud-based tutorial, I used Terraform's **Docker provider** (`kreuzwerker/docker`). This teaches the exact same core workflow — write a `.tf` file describing desired infrastructure, then let Terraform create and destroy it — but runs entirely locally and for free using Docker Desktop.

## Installation
- Attempted `winget install Hashicorp.Terraform` — failed with an `msstore` source error (`0x8a15000f : Data required by the source is missing`), a known winget/Microsoft Store source issue unrelated to Terraform itself.
- **Fix:** downloaded the Windows `.zip` directly from developer.hashicorp.com, extracted `terraform.exe` to `C:\terraform`, and added that folder to the Windows user PATH via Environment Variables.
- Verified with `terraform -version` → `Terraform v1.15.8 on windows_amd64`.

## The configuration (main.tf)
```hcl
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}

resource "docker_image" "nginx" {
  name = "nginx:latest"
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "tutorial"
  ports {
    internal = 80
    external = 8000
  }
}
```

This declares two resources: an nginx Docker image, and a container running that image with port 8000 (host) mapped to port 80 (container).

## Workflow executed
1. `terraform init` — downloaded and installed the Docker provider plugin.
2. `terraform plan` — previewed the 2 resources to be created (image + container) with no changes applied yet.
3. `terraform apply` — created the resources. **Hit an error here on the first attempt** (see Troubleshooting below).
4. Verified the container was running via `http://localhost:8000` (nginx welcome page) and in Docker Desktop's Containers tab.
5. `terraform destroy` — cleanly removed both the container and image, confirming Terraform can tear down infrastructure as reliably as it builds it.

## Troubleshooting encountered

**Problem 1 — Docker client connection error on `terraform apply`:**
```
Error: failed to create Docker client: Error pinging Docker server, please make sure that
npipe:////./pipe/docker_engine is reachable...500 Internal Server Error
```
This is a known Windows-specific issue with the `kreuzwerker/docker` provider: it doesn't always auto-detect Docker Desktop's named pipe correctly. **Fix:** explicitly declared the pipe path in the provider block (`host = "npipe:////./pipe/docker_engine"`) instead of leaving `provider "docker" {}` empty.

**Problem 2 — root cause: outdated WSL2 kernel:**
While restarting Docker Desktop to retry, it displayed a **"WSL needs updating"** screen — the actual underlying cause of the connection error above. **Fix:** ran `wsl --update` in an administrator PowerShell, restarted the machine, and Docker Desktop started cleanly afterward ("Engine running").

**Problem 3 — wrong working directory for `terraform apply`:**
Got `Error: No configuration files` because the terminal wasn't in the folder containing `main.tf`. **Fix:** used `Get-ChildItem -Path . -Filter main.tf -Recurse` from the user home directory to locate the actual project folder, then `cd`'d into it before rerunning Terraform commands.

## Outcome
- Terraform fully installed and verified on Windows.
- Successfully ran the complete `init → plan → apply → destroy` lifecycle against a local Docker container.
- Verified the container was live via browser and Docker Desktop before tearing it down.
- Documented three real Windows-specific issues and their fixes, which will be useful reference for later weeks when writing actual Dockerfiles and docker-compose configs for the project.

*(Screenshots of `terraform plan`, `terraform apply`, the running nginx page, and `terraform destroy` are kept alongside this doc.)*
