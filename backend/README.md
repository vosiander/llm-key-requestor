# Backend - LLM Key Requestor API

FastAPI backend application for the LLM Key Requestor service, built with UV package manager.

## Features

- FastAPI for high-performance REST API
- UV for fast, reliable dependency management
- YAML-based configuration for LLM models
- LiteLLM backend integration support
- **Kubernetes-based key request state management**
- **Automated approval workflow with background processing**
- **Email notifications via SMTP**
- Pydantic for data validation
- Email validation
- CORS support for frontend integration
- Environment variable overrides for deployment flexibility
- Custom certificate support via volume mount
- Dockerized for easy deployment

## Development

Install dependencies:
```bash
uv sync
```

Run development server:
```bash
uv run python main.py
```

Or using uvicorn directly:
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## Configuration

The API uses a YAML-based configuration system for managing LLM models and backend settings. See [CONFIG.md](CONFIG.md) for detailed configuration instructions.

### Quick Configuration

Edit `config.yaml` to:
- Add or modify available LLM models
- Configure LiteLLM backend URL and API key

### Environment Variables

Override configuration using environment variables:

**LiteLLM Configuration:**
- `LITELLM_BASE_URL` - LiteLLM backend base URL (default: `http://localhost:4000`)
- `LITELLM_API_KEY` - LiteLLM backend API key
- `CONFIG_FILE` - Path to configuration file (default: `config.yaml`)

**SMTP Configuration:**
- `SMTP_HOST` - SMTP server host (default: `localhost`)
- `SMTP_PORT` - SMTP server port (default: `587`)
- `SMTP_USER` - SMTP username
- `SMTP_PASSWORD` - SMTP password
- `SMTP_FROM` - From email address (default: `noreply@example.com`)
- `SMTP_USE_TLS` - Use TLS for SMTP (default: `true`)

**Approval Queue Configuration:**
- `APPROVAL_QUEUE_INTERVAL` - Queue processing interval (default: `30s`)

**Kubernetes Configuration:**
- `KUBERNETES_NAMESPACE` - Kubernetes namespace for secrets (default: current namespace or `default`)

Example:
```bash
export LITELLM_BASE_URL="https://api.litellm.ai"
export LITELLM_API_KEY="your-api-key"
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export APPROVAL_QUEUE_INTERVAL="30s"
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## Key Request System

The backend implements a Kubernetes-based key request system with automated approval and email notifications.

### Architecture

1. **State Management**: Uses Kubernetes secrets to store request state
   - Each request creates a secret with labels and annotations
   - State tracked via labels: `pending`, `approved`, `denied`
   - Request metadata stored in secret annotations

2. **Approval Workflow**: Background queue processor runs every 30 seconds (configurable)
   - Fetches all pending requests from Kubernetes
   - Processes each request through approval service
   - Generates API keys via LiteLLM for approved requests
   - Updates secret state and sends email notifications

3. **Email Notifications**: SMTP-based notifications
   - Approval emails include the generated API key
   - Denial emails include the reason for denial
   - HTML and plain text email formats

### Workflow

1. User submits key request via `POST /api/request-key`
2. System checks for existing request by email
3. If new request:
   - Creates Kubernetes secret with `pending` state
   - Returns request ID to user
4. Background processor (every 30s):
   - Fetches all `pending` requests
   - Calls approval service (currently auto-approves)
   - For approved requests:
     - Generates API key via LiteLLM
     - Updates secret with `approved` state and API key
     - Sends approval email with API key
   - For denied requests:
     - Updates secret with `denied` state
     - Sends denial email with reason

### Manual Intervention

View all key requests:
```bash
kubectl get secrets -l app.kubernetes.io/component=llm-key-request
```

View request details:
```bash
kubectl describe secret llm-key-request-<request-id>
```

Manually approve a request:
```bash
kubectl label secret llm-key-request-<request-id> request-state=approved --overwrite
kubectl annotate secret llm-key-request-<request-id> state=approved --overwrite
```

## API Endpoints

- `GET /` - API status check
- `GET /health` - Health check endpoint
- `GET /api/models` - Get list of available LLM models
- `POST /api/request-key` - Submit key request
  - Body: `{"email": "user@example.com", "llm": "model-id"}`
  - Returns: Request status and request ID

## Docker

Build:
```bash
docker build -t llm-key-requestor-backend .
```

Run:
```bash
docker run -p 8000:8000 llm-key-requestor-backend
```

### Custom Certificates

Mount a directory with certificate files:
```bash
docker run -p 8000:8000 -v /path/to/certs:/certs llm-key-requestor-backend
```

The entrypoint script will automatically add `.crt` and `.pem` files to the system trust store.

## Dependencies

- FastAPI - Web framework
- Uvicorn - ASGI server
- Pydantic - Data validation
- Pydantic Settings - Environment variable management
- PyYAML - YAML configuration parsing
- email-validator - Email validation
- kubernetes - Official Kubernetes Python client
- aiosmtplib - Async SMTP client for email notifications
- requests - HTTP library for LiteLLM integration
- injector - Dependency injection framework
