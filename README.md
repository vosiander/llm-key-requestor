# llm-key-requestor

A simple one-page web app where users pick their preferred LLM from a list, enter their email, and instantly request an access key. Clean and minimal, it streamlines onboarding by making key requests quick, transparent, and hassle-free—no extra steps, just select, submit, and receive.

## Architecture

This project consists of two main components:

### Frontend
- **Framework**: Vue.js 3
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Features**: 
  - Single-page application with clean, minimal UI
  - Responsive design with gradient background
  - Form validation for LLM selection and email input
  - Real-time feedback on form submission

### Backend
- **Framework**: FastAPI
- **Package Manager**: UV (modern Python package manager)
- **Features**:
  - RESTful API for key requests
  - CORS enabled for frontend integration
  - Email validation using Pydantic
  - Health check endpoint
  - Custom certificate support

## Development

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Development

```bash
cd backend
uv sync
uv run python main.py
```

The backend API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## Docker

### Frontend Docker

Build and run the frontend:

```bash
cd frontend
docker build -t llm-key-requestor-frontend .
docker run -p 80:80 llm-key-requestor-frontend
```

### Backend Docker

Build and run the backend:

```bash
cd backend
docker build -t llm-key-requestor-backend .
docker run -p 8000:8000 llm-key-requestor-backend
```

#### Custom Certificates

The backend supports custom certificates through a volume mount:

```bash
docker run -p 8000:8000 -v /path/to/certs:/certs llm-key-requestor-backend
```

Place your `.crt` or `.pem` certificate files in the mounted directory. The entrypoint script will automatically add them to the system trust store during container startup.

## CI/CD

GitHub Actions workflows are configured to automatically build and push Docker images to GitHub Container Registry (ghcr.io) on:
- Pushes to `main` branch
- Git tags (e.g., `v1.0.0`)
- Pull requests (build only, no push)

### Workflows

- **Frontend**: `.github/workflows/frontend-docker.yml`
- **Backend**: `.github/workflows/backend-docker.yml`

Both workflows support semantic versioning tags and will automatically tag images with:
- Branch name
- Git SHA
- Semantic version tags (for tagged releases)

## API Endpoints

### `GET /`
Health check - returns API status

### `GET /health`
Detailed health check

### `POST /api/request-key`
Submit a key request

**Request Body:**
```json
{
  "llm": "OpenAI (GPT-4)",
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Key request for OpenAI (GPT-4) received. Check your email at user@example.com",
  "success": true,
  "request_id": "demo-request-id"
}
```

## Environment Variables

### Frontend
No environment variables required for basic functionality.

### Backend
The backend can be configured through environment variables if needed (to be implemented based on requirements).

## License

Apache License 2.0 - see LICENSE file for details
