# VaultML CE - Machine Learning Model Repository

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=flat&logo=kubernetes&logoColor=white)](https://kubernetes.io)
![Docker – Build & Push to GHCR](https://github.com/All-Day-Developer/VaultML-CE/actions/workflows/docker-publish.yml/badge.svg)

**VaultML CE** is an open-source machine learning model repository system that provides versioning, aliasing, and S3-compatible storage for ML artifacts. Built with FastAPI backend and Nuxt4 frontend, it offers a complete solution for managing machine learning models in both development and production environments.

## ✨ Features

- **Model Versioning**: Track and manage different versions of your ML models
- **Model Aliasing**: Create named pointers to specific versions (e.g., "latest", "production", "staging")
- **S3-Compatible Storage**: Store large model artifacts using MinIO or any S3-compatible backend
- **Authentication**: JWT-based user authentication with secure session management
- **Web Interface**: Modern, responsive web UI built with Nuxt4 and Tailwind CSS
- **API-First**: Complete REST API for programmatic access
- **Container Ready**: Docker and Kubernetes deployment support
- **Helm Charts**: Production-ready Kubernetes deployment

## 🏗 Architecture

VaultML CE consists of three main components:

### Backend (`app/`)
- **FastAPI server** - Main application with CORS, license middleware, and static file serving
- **Database models** - SQLAlchemy async models for User, Model, ModelVersion, ModelAlias with PostgreSQL
- **API routes** - Authentication, model CRUD, versioning, and alias management endpoints  
- **S3 integration** - MinIO/S3-compatible storage with presigned upload URLs

### Frontend (`frontend/`)
- **Nuxt4** application with TypeScript, Tailwind CSS, and Pinia state management
- **API proxy** configured to forward `/api` requests to FastAPI backend
- **Authentication** using JWT cookies and Pinia store

### Infrastructure
- **PostgreSQL** for metadata storage
- **MinIO** for S3-compatible object storage
- **Docker Compose** for local development environment

## 📋 Prerequisites

- **Docker** and **Docker Compose** (for containerized deployment)
- **Python 3.11+** (for local development)
- **Node.js 20+** and **pnpm** (for frontend development)
- **PostgreSQL** (for database)
- **MinIO or S3-compatible storage** (for model artifacts)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/All-Day-Developer/VaultML-CE.git
   cd VaultML-CE
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Web UI: http://localhost:3000
   - API: http://localhost:8000
   - Default credentials: `default/default`

### Manual Setup

#### Backend Development

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start PostgreSQL and MinIO** (using Docker)
   ```bash
   docker-compose up -d postgres minio
   ```

4. **Source environment variables and run the FastAPI server**
   ```bash
   # Source .env file to export all variables
   set -a && source .env && set +a
   
   # Run the server
   python -m app.server
   # or
   uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Frontend Development

1. **Install dependencies**
   ```bash
   cd frontend
   pnpm install
   ```

2. **Start development server**
   ```bash
   pnpm dev
   ```

3. **Build for production**
   ```bash
   pnpm build
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://vaultml:vaultmlpass@localhost:5432/vaultml

# JWT Configuration
JWT_SECRET=your-super-secure-jwt-secret-key

# S3/MinIO Configuration
S3_ENDPOINT=http://localhost:9000
S3_BUCKET=models
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_REGION=us-east-1

# Application
CORS_ORIGINS=http://localhost:3000
```

### Loading Environment Variables

When running the Python application locally (without Docker), you need to export the environment variables from the `.env` file:

```bash
# Export all variables from .env file
set -a && source .env && set +a

# Now run your Python application
python -m app.server
```

**Explanation:**
- `set -a` enables automatic export of all variables
- `source .env` loads the variables from the file
- `set +a` disables automatic export for subsequent variables

### Database Schema

The application uses these main entities:
- **User** - Authentication and user management
- **Model** - Top-level model container with unique names
- **ModelVersion** - Versioned model artifacts stored in S3 with integer versions
- **ModelAlias** - Named pointers to specific versions (e.g., "latest", "production")

## 🔌 API Usage

### Authentication

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login   -H "Content-Type: application/json"   -d '{"username": "default", "password": "default"}'
```

### Model Management

```bash
# List models
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/models

# Create model
curl -X POST http://localhost:8000/api/models   -H "Authorization: Bearer <token>"   -H "Content-Type: application/json"   -d '{"name": "my-model", "description": "My ML model"}'

# Upload model version
curl -X POST http://localhost:8000/api/models/my-model/versions   -H "Authorization: Bearer <token>"   -F "file=@model.pkl"

# Resolve model (by version or alias)
curl -H "Authorization: Bearer <token>"   "http://localhost:8000/api/models/my-model/resolve?version=1"
```

## ☸️ Kubernetes Deployment

VaultML CE includes production-ready Helm charts for Kubernetes deployment.

### Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+

### Installation

1. **Add Bitnami repository**
   ```bash
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
   ```

2. **Install VaultML CE**
   ```bash
   # Development setup
   helm install vaultml ./helm/vaultml

   # Production setup with custom values
   helm install vaultml ./helm/vaultml -f production-values.yaml
   ```

3. **Access the application**
   ```bash
   kubectl port-forward svc/vaultml 8000:8000
   ```

See [helm/vaultml/README.md](helm/vaultml/README.md) for detailed configuration options.

## 🛠 Development

### Project Structure

```
VaultML-CE/
├── app/             # FastAPI backend
├── frontend/        # Nuxt4 frontend
├── helm/            # Helm charts
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```
