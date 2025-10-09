FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source files
COPY . .

# Expose port 5174
EXPOSE 5174

# Start development server
CMD ["npm", "run", "dev"]
