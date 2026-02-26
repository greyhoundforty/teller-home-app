# Kubernetes Manifests — Teller Home App

Deploys the app into a `teller-home` namespace on a k3s cluster.
SQLite is used for persistence; the database file lives in a PersistentVolumeClaim
backed by k3s's built-in `local-path` provisioner.

## Prerequisites

- `kubectl` configured to talk to your k3s cluster
- The Docker image built and pushed to a registry (see below)
- Your Teller mTLS cert files: `certificate.pem` and `private_key.pem`

---

## 1. Build and push the Docker image

```bash
# From the repo root — build the production image
docker build -t ghcr.io/greyhoundforty/teller-home-app:latest .

# Push to GitHub Container Registry (or swap for any registry your k3s node can pull from)
docker push ghcr.io/greyhoundforty/teller-home-app:latest
```

If you prefer to load the image directly into k3s without a registry:

```bash
# Build and export
docker build -t teller-home-app:latest .
docker save teller-home-app:latest | gzip > teller-home-app.tar.gz

# Copy to each k3s node and import into containerd
scp teller-home-app.tar.gz user@k3s-node:~
ssh user@k3s-node "sudo k3s ctr images import teller-home-app.tar.gz"
```

Then update the `image:` field in `deployment.yaml` to `teller-home-app:latest`
and set `imagePullPolicy: Never`.

---

## 2. Create the namespace

```bash
kubectl apply -f kubes/namespace.yaml
```

---

## 3. Create the Secrets

### App secrets (SECRET_KEY)

```bash
kubectl create secret generic teller-home-secrets \
  --namespace teller-home \
  --from-literal=SECRET_KEY='your-secret-key-here'
```

### Teller mTLS certificates

The app uses mutual TLS to authenticate with the Teller API.
Create the secret directly from your local cert files:

```bash
kubectl create secret generic teller-certs \
  --namespace teller-home \
  --from-file=certificate.pem=./authentication/certificate.pem \
  --from-file=private_key.pem=./authentication/private_key.pem
```

The secret keys (`certificate.pem`, `private_key.pem`) match the filenames
the app expects under `/app/authentication/`, so no code changes are needed.

To verify the secret was created correctly:

```bash
kubectl get secret teller-certs -n teller-home -o jsonpath='{.data}' | python3 -m json.tool
```

---

## 4. Apply the remaining manifests

```bash
kubectl apply -f kubes/pvc.yaml
kubectl apply -f kubes/deployment.yaml
kubectl apply -f kubes/service.yaml
kubectl apply -f kubes/ingress.yaml
```

Or all at once:

```bash
kubectl apply -f kubes/
```

---

## 5. Verify the deployment

```bash
# Watch the pod come up
kubectl get pods -n teller-home -w

# Check logs
kubectl logs -n teller-home -l app=teller-home-app -f

# Confirm the health endpoint responds
kubectl exec -n teller-home deploy/teller-home-app -- \
  python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5001/api/health').read())"
```

---

## 6. Accessing the app

### Via ingress (recommended)

`ingress.yaml` uses host `teller.home`. Point that hostname at your k3s node's IP
in your local DNS (Pi-hole, AdGuard Home, or `/etc/hosts`):

```
192.168.x.x   teller.home
```

Then open `http://teller.home` in your browser.

### Via port-forward (quick test)

```bash
kubectl port-forward -n teller-home svc/teller-home-app 5001:5001
# App is now available at http://localhost:5001
```

---

## Exposing via Tailscale (tailnet-only access)

The `ingress-tailscale.yaml` manifest uses the Tailscale Kubernetes Operator
to expose the app exclusively to devices on your tailnet. It is **not** a
Funnel setup — there is no public internet exposure.

### 1. Create a Tailscale OAuth client

In the Tailscale admin panel → **Settings → OAuth clients**, create a client
with `Auth Keys (write)` and `Devices (write)` scopes. Save the client ID and secret.

### 2. Install the Tailscale Kubernetes Operator

```bash
helm repo add tailscale https://pkgs.tailscale.com/helmcharts
helm repo update

helm upgrade \
  --install tailscale-operator \
  tailscale/tailscale-operator \
  --namespace tailscale \
  --create-namespace \
  --set-string oauth.clientId=<CLIENT_ID> \
  --set-string oauth.clientSecret=<CLIENT_SECRET> \
  --wait
```

### 3. Apply the Tailscale ingress

```bash
kubectl apply -f kubes/ingress-tailscale.yaml
```

After a minute or two the operator will register a new machine on your tailnet.
You can watch it appear:

```bash
kubectl get ingress -n teller-home
# NAME                     CLASS       HOSTS          ADDRESS
# teller-home-tailscale    tailscale   teller-home    100.x.x.x
```

The app will be available at:

```
https://teller-home.<tailnet-name>.ts.net
```

Tailscale provisions the HTTPS certificate automatically — no cert-manager needed.

### Funnel vs tailnet-only

| Mode | What it does | How to enable |
|---|---|---|
| Tailnet only (default) | Reachable only by devices on your tailnet | Just apply `ingress-tailscale.yaml` as-is |
| Funnel (public) | Reachable from the open internet via Tailscale | Add annotation `tailscale.com/funnel: "true"` — **not recommended** for this app |

---

## Updating the app

```bash
# Build and push a new image
docker build -t ghcr.io/greyhoundforty/teller-home-app:latest .
docker push ghcr.io/greyhoundforty/teller-home-app:latest

# Roll out the new image (imagePullPolicy: Always handles the pull)
kubectl rollout restart deployment/teller-home-app -n teller-home

# Watch the rollout
kubectl rollout status deployment/teller-home-app -n teller-home
```

---

## Manifest overview

| File | What it creates |
|---|---|
| `namespace.yaml` | `teller-home` namespace |
| `pvc.yaml` | 1Gi PersistentVolumeClaim for the SQLite DB (k3s `local-path`) |
| `deployment.yaml` | Single-replica Deployment with health probes and volume mounts |
| `service.yaml` | ClusterIP Service on port 5001 |
| `ingress.yaml` | Traefik Ingress for `teller.home` hostname |

> **Note:** Keep `replicas: 1` in the Deployment. SQLite does not support
> concurrent writes from multiple processes, so running more than one pod
> will corrupt the database.
