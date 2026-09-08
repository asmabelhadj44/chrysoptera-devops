# W1-04 — Kubernetes Basics & kubectl Cheat-Sheet

**Task:** Research Kubernetes basics; create a kubectl cheat-sheet
**Status:** Done
**Context:** Chrysoptera DevOps internship, Week 1

---

## 1. Core concepts (the minimum you need before touching kubectl)

| Concept | What it is | Why it matters for Chrysoptera |
|---|---|---|
| **Cluster** | A set of machines (nodes) running Kubernetes | Would host the FastAPI + Postgres + Redis stack in production instead of one Docker Compose file on one machine |
| **Node** | A single machine (VM or physical) in the cluster | Each node can run many pods |
| **Pod** | The smallest deployable unit — one or more containers that share networking/storage | Your FastAPI container would run inside a pod |
| **Deployment** | Manages a set of identical pods, handles rolling updates and self-healing | Ensures N copies of the API are always running; replaces a crashed pod automatically |
| **Service** | A stable network endpoint that load-balances traffic to a set of pods | Lets the dashboard/frontend always reach "the API" even as pods restart with new IPs |
| **ConfigMap / Secret** | Store non-sensitive / sensitive configuration outside the container image | Database URLs, API keys — same idea as `.env` but Kubernetes-native |
| **Namespace** | A logical partition inside a cluster (e.g. `staging`, `production`) | Keeps environments separate in one cluster |
| **Ingress** | Routes external HTTP(S) traffic into the cluster to the right Service | Public entry point for the solar monitoring dashboard |

**Docker Compose vs Kubernetes, in one line:** Compose runs containers on *one* machine for local dev; Kubernetes orchestrates containers across *many* machines with self-healing, scaling, and rolling updates — which is why it matters once Chrysoptera has real traffic from 100+ solar sites.

---

## 2. kubectl cheat-sheet

### Cluster & context info
```
kubectl cluster-info                   # Show cluster endpoint info
kubectl get nodes                      # List all nodes in the cluster
kubectl config current-context         # Show which cluster you're currently talking to
kubectl config get-contexts            # List all available clusters/contexts
```

### Pods
```
kubectl get pods                       # List pods in current namespace
kubectl get pods -A                    # List pods in ALL namespaces
kubectl describe pod <pod-name>        # Detailed info + recent events (great for debugging)
kubectl logs <pod-name>                # View logs from a pod
kubectl logs -f <pod-name>             # Stream logs live (like `tail -f`)
kubectl exec -it <pod-name> -- bash    # Open a shell inside a running pod
kubectl delete pod <pod-name>          # Delete a pod (Deployment will recreate it)
```

### Deployments
```
kubectl get deployments                        # List deployments
kubectl apply -f deployment.yaml               # Create/update from a YAML file
kubectl rollout status deployment/<name>       # Watch a rollout in progress
kubectl rollout undo deployment/<name>         # Roll back to previous version
kubectl scale deployment/<name> --replicas=3   # Scale to 3 pod copies
```

### Services
```
kubectl get services                   # List services
kubectl describe service <name>        # Show endpoint + port details
```

### ConfigMaps & Secrets
```
kubectl get configmaps
kubectl get secrets
kubectl create secret generic db-secret --from-literal=password=changeme
```

### Namespaces
```
kubectl get namespaces                         # List namespaces
kubectl create namespace staging               # Create one
kubectl get pods -n staging                    # List pods in a specific namespace
```

### Applying & cleaning up
```
kubectl apply -f <file-or-folder>      # Apply one file or a whole folder of manifests
kubectl delete -f <file>               # Delete whatever that file created
kubectl get all                        # Quick overview of everything in current namespace
```

---

## 3. Notes / things worth remembering
- Almost everything follows the pattern: `kubectl <verb> <resource> <name>` (e.g. `get pod my-pod`, `describe deployment my-api`).
- `kubectl describe` is the single most useful debugging command — it shows recent events (crashes, failed pulls, scheduling issues) that `get` doesn't show.
- No cluster was provisioned for this task (no cloud budget) — this is a research + reference deliverable, consistent with the "conceptual/documented" approach used for other Week 3 IaC tasks.
- Natural next step if a real cluster is ever available: try `minikube` or `kind` (Kubernetes-in-Docker) locally, since Docker Desktop is already installed and working.

## 4. Further learning (not run, for reference)
Kubernetes.io hosts a free interactive "Kubernetes Basics" tutorial (browser-based sandbox, no install or cloud account needed) covering six hands-on modules that map directly onto the sections above: creating a cluster, deploying an app, exploring it, exposing it publicly, scaling it, and updating it. Worth working through in a later week if time allows a deeper dive beyond this reference doc.

---
*Chrysoptera — Cloud Computing / DevOps Internship — Week 1*
