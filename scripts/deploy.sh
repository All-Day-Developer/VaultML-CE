#!/bin/bash

# VaultML CE Deployment Script
# Copyright (C) 2025 All-Day Developer Marcin Wawrzków
# Licensed under AGPL-3.0-or-later

set -e

RELEASE_NAME=${1:-"vaultml"}
NAMESPACE=${2:-"default"}
VALUES_FILE=${3:-""}

echo "🚀 Deploying VaultML CE"
echo "   Release: $RELEASE_NAME"
echo "   Namespace: $NAMESPACE"

# Add Bitnami repo for dependencies
echo "📦 Adding Bitnami repository..."
helm repo add bitnami https://charts.bitnami.com/bitnami >/dev/null 2>&1 || true
helm repo update

# Update dependencies
echo "🔄 Updating chart dependencies..."
cd helm/vaultml
helm dependency update
cd ../..

# Deploy
echo "⚙️  Deploying..."
HELM_CMD="helm upgrade --install $RELEASE_NAME ./helm/vaultml --namespace $NAMESPACE --create-namespace"

if [ -n "$VALUES_FILE" ]; then
    HELM_CMD="$HELM_CMD -f $VALUES_FILE"
fi

eval $HELM_CMD

echo "✅ Deployment complete!"
echo ""
echo "🔍 Check status:"
echo "   kubectl get pods -n $NAMESPACE"
echo "   helm status $RELEASE_NAME -n $NAMESPACE"
echo ""
echo "🌐 Access VaultML:"
echo "   kubectl port-forward -n $NAMESPACE svc/$RELEASE_NAME 8000:8000"
echo "   http://localhost:8000"