# Frontend - LLM Key Requestor

Vue.js 3 frontend application with Tailwind CSS for the LLM Key Requestor service.

## Features

- Clean, minimal single-page interface
- Tailwind CSS for modern, responsive design
- Form validation for email and LLM selection
- Integration with FastAPI backend
- Dockerized for easy deployment

## Development

Install dependencies:
```bash
npm install
```

Run development server:
```bash
npm run dev
```

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## Docker

Build:
```bash
docker build -t llm-key-requestor-frontend .
```

Run:
```bash
docker run -p 80:80 llm-key-requestor-frontend
```

## Configuration

The application expects the backend API to be available at `/api/request-key`. 

For development with a separate backend server, you may need to configure a proxy in `vite.config.js`.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).
