# VaultML CE Helm Chart

This Helm chart deploys VaultML CE (Community Edition) - a machine learning model repository system.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+

## Installation

### Add Bitnami repository for dependencies

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Install VaultML CE

```bash
# Install with default values
helm install vaultml ./helm/vaultml

# Install with custom values
helm install vaultml ./helm/vaultml -f custom-values.yaml

# Install in specific namespace
helm install vaultml ./helm/vaultml -n vaultml --create-namespace
```

## Configuration

The following table lists the configurable parameters and their default values.

### Application Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of VaultML replicas | `1` |
| `image.repository` | VaultML image repository | `vaultml/vaultml-ce` |
| `image.tag` | VaultML image tag | `""` (uses Chart appVersion) |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `config.jwtSecret` | JWT secret key | `"supersecretjwtkey"` |

### Database Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `postgresql.enabled` | Deploy PostgreSQL | `true` |
| `postgresql.auth.username` | PostgreSQL username | `"vaultml"` |
| `postgresql.auth.password` | PostgreSQL password | `"vaultmlpass"` |
| `postgresql.auth.database` | PostgreSQL database | `"vaultml"` |
| `externalDatabase.host` | External DB host (when postgresql.enabled=false) | `localhost` |

### Storage Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `minio.enabled` | Deploy MinIO for S3 storage | `true` |
| `minio.auth.rootUser` | MinIO root username | `"minioadmin"` |
| `minio.auth.rootPassword` | MinIO root password | `"minioadmin"` |
| `minio.defaultBuckets` | Default bucket name | `"models"` |
| `externalS3.endpoint` | External S3 endpoint (when minio.enabled=false) | `"http://localhost:9000"` |

### Service Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `service.type` | Kubernetes service type | `ClusterIP` |
| `service.port` | Service port | `8000` |
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.hosts[0].host` | Hostname | `vaultml.local` |

## Examples

### Production Setup with External Database and S3

```yaml
# production-values.yaml
replicaCount: 3

config:
  jwtSecret: "your-super-secure-jwt-secret"

postgresql:
  enabled: false

externalDatabase:
  host: "postgres.example.com"
  port: 5432
  username: "vaultml"
  password: "secure-password"
  database: "vaultml"

minio:
  enabled: false

externalS3:
  endpoint: "https://s3.amazonaws.com"
  region: "us-west-2"
  bucket: "my-models-bucket"
  accessKey: "AKIAIOSFODNN7EXAMPLE"
  secretKey: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY"

ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: vaultml.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: vaultml-tls
      hosts:
        - vaultml.example.com

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi
```

### Development Setup

```yaml
# dev-values.yaml
replicaCount: 1

postgresql:
  enabled: true
  auth:
    postgresPassword: "dev-postgres"
    username: "vaultml"
    password: "dev-password"
    database: "vaultml"

minio:
  enabled: true
  auth:
    rootUser: "dev-admin"
    rootPassword: "dev-password"

service:
  type: NodePort

resources:
  requests:
    cpu: 100m
    memory: 128Mi
```

## Upgrading

```bash
helm upgrade vaultml ./helm/vaultml
```

## Uninstalling

```bash
helm uninstall vaultml
```

## License

VaultML CE is licensed under AGPL-3.0-or-later.

**Copyright (C) 2025 All-Day Developer Marcin Wawrzków**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## Support

- GitHub: https://github.com/All-Day-Developer/VaultML-CE
- Issues: https://github.com/All-Day-Developer/VaultML-CE/issues