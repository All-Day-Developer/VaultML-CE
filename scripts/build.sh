#!/bin/bash

# VaultML CE Build Script
# Copyright (C) 2025 All-Day Developer Marcin Wawrzków
# Licensed under AGPL-3.0-or-later

set -e

REPO_NAME="vaultml/vaultml-ce"
VERSION=${1:-"latest"}

echo "🏗️  Building VaultML CE v$VERSION"

# Build the Docker image
docker build -t $REPO_NAME:$VERSION .
docker tag $REPO_NAME:$VERSION $REPO_NAME:latest

echo "✅ Build complete!"
echo "🐳 Image: $REPO_NAME:$VERSION"

echo ""
echo "Next steps:"
echo "  • Run locally: docker run -p 8000:8000 $REPO_NAME:$VERSION"
echo "  • Push to registry: docker push $REPO_NAME:$VERSION"
echo "  • Deploy with Helm: helm install vaultml ./helm/vaultml --set image.tag=$VERSION"