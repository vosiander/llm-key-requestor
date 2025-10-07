// API service layer for backend communication
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiError extends Error {
  constructor(message, status, details = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.details = details
  }
}

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`
        let errorDetails = null
        
        try {
          const errorData = await response.json()
          errorMessage = errorData.message || errorData.detail || errorMessage
          errorDetails = errorData
        } catch (parseError) {
          // If error response is not JSON, use default message
          console.warn('Failed to parse error response as JSON')
        }
        
        throw new ApiError(errorMessage, response.status, errorDetails)
      }

      const data = await response.json()
      return data
    } catch (error) {
      if (error instanceof ApiError) {
        throw error
      }
      
      // Handle network errors, timeout, etc.
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new ApiError('Unable to connect to server. Please check your connection.', 0, error)
      }
      
      throw new ApiError('An unexpected error occurred', 0, error)
    }
  }

  // GET request helper
  async get(endpoint, params = {}) {
    const searchParams = new URLSearchParams(params)
    const queryString = searchParams.toString()
    const url = queryString ? `${endpoint}?${queryString}` : endpoint
    
    return this.request(url, { method: 'GET' })
  }

  // POST request helper
  async post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  // Health check endpoint
  async checkHealth() {
    try {
      const response = await this.get('/health')
      return response.status === 'healthy'
    } catch (error) {
      console.error('Health check failed:', error)
      return false
    }
  }

  // Get available LLM models
  async getModels() {
    try {
      const response = await this.get('/api/models')
      return response.models || []
    } catch (error) {
      console.error('Failed to fetch models:', error)
      throw error
    }
  }

  // Get featured models
  async getFeaturedModels() {
    try {
      const response = await this.get('/api/featured-models')
      return response.models || []
    } catch (error) {
      console.error('Failed to fetch featured models:', error)
      throw error
    }
  }

  // Submit key request
  async submitKeyRequest(request) {
    if (!request.llm || !request.email) {
      throw new ApiError('LLM provider and email are required', 400)
    }

    // Validate email format on client side
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(request.email)) {
      throw new ApiError('Please enter a valid email address', 400)
    }

    try {
      const response = await this.post('/api/request-key', {
        llm: request.llm.trim(),
        email: request.email.trim().toLowerCase()
      })
      
      return response
    } catch (error) {
      console.error('Key request failed:', error)
      throw error
    }
  }

  // Get server info
  async getServerInfo() {
    try {
      return await this.get('/')
    } catch (error) {
      console.error('Failed to get server info:', error)
      throw error
    }
  }
}

// Export singleton instance
export const apiService = new ApiService()

// Export ApiError for error handling in components
export { ApiError }

// Export default for convenience
export default apiService
