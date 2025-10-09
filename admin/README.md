# LLM Key Requestor - Admin Panel

Admin panel for managing LLM API key requests. Built with Vue 3, Vuetify, and Vite.

## Features

- Basic authentication with environment-based credentials
- View pending, in-review, and all key requests
- Approve or deny key requests with optional reasons
- Real-time request status updates

## Development

```bash
# Install dependencies
npm install

# Start dev server (port 5174)
npm run dev

# Build for production
npm run build
```

## Environment Variables

The admin panel connects to the backend API which requires the following environment variables:

- `ADMIN_USERNAME` - Admin username for authentication
- `ADMIN_PASSWORD` - Admin password for authentication

These should be configured in the backend service.

## Docker

```bash
# Build image
docker build -t llm-key-requestor-admin .

# Run container
docker run -p 5174:80 llm-key-requestor-admin
```

## Authentication

The admin panel uses Basic Authentication. Credentials are verified against environment variables configured in the backend service.
