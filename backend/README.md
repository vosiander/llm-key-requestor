# Backend - LLM Key Requestor API

FastAPI backend application for the LLM Key Requestor service, built with UV package manager.

## Features

- FastAPI for high-performance REST API
- UV for fast, reliable dependency management
- Pydantic for data validation
- Email validation
- CORS support for frontend integration
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

## API Endpoints

- `GET /` - API status check
- `GET /health` - Health check endpoint
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
- email-validator - Email validation

## Environment Variables

Currently, no environment variables are required. Future enhancements may include:
- Database connection strings
- Email service credentials
- API keys for LLM providers
