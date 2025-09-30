# Backend - LLM Key Requestor API

FastAPI backend application for the LLM Key Requestor service, built with UV package manager.

## Features

- FastAPI for high-performance REST API
- UV for fast, reliable dependency management
- YAML-based configuration for LLM models
- LiteLLM backend integration support
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

- `LITELLM_BASE_URL` - LiteLLM backend base URL (default: `http://localhost:4000`)
- `LITELLM_API_KEY` - LiteLLM backend API key
- `CONFIG_FILE` - Path to configuration file (default: `config.yaml`)

Example:
```bash
export LITELLM_BASE_URL="https://api.litellm.ai"
export LITELLM_API_KEY="your-api-key"
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - API status check
- `GET /health` - Health check endpoint
- `GET /api/models` - Get list of available LLM models
- `POST /api/request-key` - Submit key request

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
