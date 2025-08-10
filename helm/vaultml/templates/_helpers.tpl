{{/*
Expand the name of the chart.
*/}}
{{- define "vaultml.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "vaultml.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "vaultml.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "vaultml.labels" -}}
helm.sh/chart: {{ include "vaultml.chart" . }}
{{ include "vaultml.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/component: vaultml
app.kubernetes.io/part-of: vaultml-ce
{{- end }}

{{/*
Selector labels
*/}}
{{- define "vaultml.selectorLabels" -}}
app.kubernetes.io/name: {{ include "vaultml.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "vaultml.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "vaultml.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Database URL
*/}}
{{- define "vaultml.databaseUrl" -}}
{{- if .Values.postgresql.enabled }}
{{- printf "postgresql+asyncpg://%s:%s@%s-postgresql:5432/%s" .Values.postgresql.auth.username .Values.postgresql.auth.password .Release.Name .Values.postgresql.auth.database }}
{{- else }}
{{- printf "postgresql+asyncpg://%s:%s@%s:%s/%s" .Values.externalDatabase.username .Values.externalDatabase.password .Values.externalDatabase.host (.Values.externalDatabase.port | toString) .Values.externalDatabase.database }}
{{- end }}
{{- end }}

{{/*
S3 Endpoint
*/}}
{{- define "vaultml.s3Endpoint" -}}
{{- if .Values.minio.enabled }}
{{- printf "http://%s-minio:9000" .Release.Name }}
{{- else }}
{{- .Values.externalS3.endpoint }}
{{- end }}
{{- end }}

{{/*
S3 Region
*/}}
{{- define "vaultml.s3Region" -}}
{{- if .Values.minio.enabled }}
{{- "us-east-1" }}
{{- else }}
{{- .Values.externalS3.region }}
{{- end }}
{{- end }}

{{/*
S3 Bucket
*/}}
{{- define "vaultml.s3Bucket" -}}
{{- if .Values.minio.enabled }}
{{- .Values.minio.defaultBuckets }}
{{- else }}
{{- .Values.externalS3.bucket }}
{{- end }}
{{- end }}