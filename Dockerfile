# Copyright (C) 2025 All-Day Developer Marcin Wawrzków
# contributor: Marcin Wawrzków
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

FROM node:20 AS frontend-builder

LABEL maintainer="All-Day Developer Marcin Wawrzków"
LABEL description="VaultML CE - Machine Learning Model Repository"
LABEL license="AGPL-3.0-or-later"

# Build frontend
WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install -g pnpm
RUN pnpm install --ignore-scripts

COPY frontend/ .
RUN pnpm build --ignore-scripts || pnpm run build

# Python backend stage
FROM python:3.11-slim

LABEL maintainer="All-Day Developer Marcin Wawrzków"
LABEL description="VaultML CE - Machine Learning Model Repository"
LABEL license="AGPL-3.0-or-later"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app/ ./app/

# Copy built frontend from builder stage
COPY --from=frontend-builder /frontend/.output/public ./static/

# Create directory for chunk uploads and ensure proper permissions
RUN mkdir -p /tmp/vaultml_chunks

# Create non-root user
RUN groupadd -r vaultml && useradd -r -g vaultml vaultml
RUN chown -R vaultml:vaultml /app
RUN chown -R vaultml:vaultml /tmp/vaultml_chunks
USER vaultml

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=10)" || exit 1

# Run the application
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]