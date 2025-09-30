FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Install ca-certificates for certificate handling
RUN apk add --no-cache ca-certificates bash

# Set working directory
WORKDIR /app

# Copy application files
COPY pyproject.toml uv.lock* ./
COPY main.py ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create volume mount point for certificates
VOLUME /certs

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
