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
   - Calls approval service with plugin chain
   - For approved requests:
     - Generates API key via LiteLLM
     - Updates secret with `approved` state and API key
     - Sends approval email with API key
   - For denied requests:
     - Updates secret with `denied` state
     - Sends denial email with reason

## Approval Plugins

The system uses a plugin-based approval mechanism that evaluates requests through a chain of responsibility pattern. Configure plugins in `config.yaml` under the `approvals` section.

### How It Works

- Plugins are evaluated in the order they are configured
- Each plugin returns: `APPROVE`, `DENY`, or `CONTINUE`
- If a plugin returns `APPROVE` or `DENY`, evaluation stops immediately
- If all plugins return `CONTINUE`, the request is **denied by default**

### Available Plugins

#### HTTP Plugin

Query an external HTTP endpoint for approval decisions. Useful for integrating with existing approval systems or custom workflows.

**Configuration:**
```yaml
approval_plugins:
  - name: http
    config:
      endpoint: "https://example.com/api/approve"
```

**Endpoint Requirements:**
- Method: POST
- Request Body: `{"email": "user@example.com", "model": "gpt-4", "request_id": "abc123"}`
- Response: `{"decision": "APPROVE"}` or `{"decision": "DENY"}` or `{"decision": "CONTINUE"}`
- On error or timeout (5s default), returns `CONTINUE`

#### Blacklist Plugin

Deny requests for models matching specified patterns. Useful for blocking access to expensive or restricted models.

**Configuration:**
```yaml
approval_plugins:
  - name: blacklist
    config:
      list:
        - "anthropic/*"      # Block all Anthropic models
        - "google/*"         # Block all Google models
        - "gpt-4*"           # Block GPT-4 variants
```

**Behavior:**
- Match: Returns `DENY`
- No match: Returns `CONTINUE`
- Supports wildcards: `*` (any characters), `?` (single character)

#### Whitelist Plugin

Approve requests for models matching specified patterns. Useful for auto-approving access to specific models.

**Configuration:**
```yaml
approval_plugins:
  - name: whitelist
    config:
      list:
        - "ollama/*"         # Auto-approve all Ollama models
        - "llama-*"          # Auto-approve all Llama models
        - "mistral-7b"       # Auto-approve specific model
```

**Behavior:**
- Match: Returns `APPROVE`
- No match: Returns `CONTINUE`
- Supports wildcards: `*` (any characters), `?` (single character)

#### Email Plugin

Approve or deny requests based on email domain pattern matching. Useful for allowing access only to specific domains.

**Configuration:**
```yaml
approval_plugins:
  - name: email
    config:
      pattern: "*@example.com"
```

**Behavior:**
- Match: Returns `APPROVE`
- No match: Returns `DENY`
- Supports wildcards: `*` (any characters), `?` (single character)

### Example Configurations

**Simple Whitelist:**
```yaml
approval_plugins:
  # Only approve Ollama models
  - name: whitelist
    config:
      list:
        - "ollama/*"
```

**Combined Approach:**
```yaml
approval_plugins:
  # First, check external approval system
  - name: http
    config:
      endpoint: "https://approval-service.company.com/api/approve"
  
  # Block expensive models
  - name: blacklist
    config:
      list:
        - "gpt-4"
        - "claude-3"
  
  # Auto-approve cheap models
  - name: whitelist
    config:
      list:
        - "ollama/*"
        - "mistral-7b"
  
  # Require company email for any remaining requests
  - name: email
    config:
      pattern: "*@company.com"
```

**Email-based Access Control:**
```yaml
approval_plugins:
  # Only allow company employees
  - name: email
    config:
      pattern: "*@company.com"
```

### Plugin Evaluation Example

Given this configuration:
```yaml
approval_plugins:
  - name: blacklist
    config:
      list: ["gpt-4*"]
  - name: whitelist
    config:
      list: ["ollama/*"]
  - name: email
    config:
      pattern: "*@company.com"
```

Request: `email="user@company.com", model="gpt-4"`
1. Blacklist plugin: model matches "gpt-4*" → **DENY** → Request denied

Request: `email="user@company.com", model="ollama/llama2"`
1. Blacklist plugin: no match → CONTINUE
2. Whitelist plugin: model matches "ollama/*" → **APPROVE** → Request approved

Request: `email="user@company.com", model="claude-3"`
1. Blacklist plugin: no match → CONTINUE
2. Whitelist plugin: no match → CONTINUE
3. Email plugin: email matches "*@company.com" → **APPROVE** → Request approved

Request: `email="user@gmail.com", model="claude-3"`
1. Blacklist plugin: no match → CONTINUE
2. Whitelist plugin: no match → CONTINUE
3. Email plugin: email doesn't match "*@company.com" → **DENY** → Request denied

### No Plugins Configured

If no plugins are configured in `config.yaml`, **all requests will be denied by default** with the reason "No approval plugins configured".

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
