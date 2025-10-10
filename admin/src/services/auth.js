// Authentication service for admin panel using Basic Auth
const AUTH_KEY = 'admin_auth'
const API_BASE_URL = import.meta.env.VITE_ADMIN_API_URL || 'http://localhost:8000'
const API_BASE = `${API_BASE_URL}/api`

export const authService = {
  /**
   * Attempt to login with username and password
   * @param {string} username - Admin username
   * @param {string} password - Admin password
   * @returns {Promise<boolean>} - Success status
   */
  async login(username, password) {
    try {
      const credentials = btoa(`${username}:${password}`)
      
      // Verify credentials with backend
      const response = await fetch(`${API_BASE}/admin/verify`, {
        method: 'POST',
        headers: {
          'Authorization': `Basic ${credentials}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        // Store credentials in sessionStorage (more secure than localStorage)
        sessionStorage.setItem(AUTH_KEY, credentials)
        return true
      }
      
      return false
    } catch (error) {
      console.error('Login error:', error)
      return false
    }
  },

  /**
   * Logout and clear session
   */
  logout() {
    sessionStorage.removeItem(AUTH_KEY)
  },

  /**
   * Check if user is authenticated
   * @returns {boolean} - Authentication status
   */
  isAuthenticated() {
    return sessionStorage.getItem(AUTH_KEY) !== null
  },

  /**
   * Get Authorization header for API requests
   * @returns {string} - Basic Auth header value
   */
  getAuthHeader() {
    const credentials = sessionStorage.getItem(AUTH_KEY)
    return credentials ? `Basic ${credentials}` : ''
  },

  /**
   * Get stored credentials (for display purposes)
   * @returns {object|null} - Decoded credentials or null
   */
  getCredentials() {
    const credentials = sessionStorage.getItem(AUTH_KEY)
    if (!credentials) return null

    try {
      const decoded = atob(credentials)
      const [username] = decoded.split(':')
      return { username }
    } catch {
      return null
    }
  }
}
