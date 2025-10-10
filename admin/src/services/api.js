// API service layer for admin panel
import { authService } from './auth'

const API_BASE_URL = import.meta.env.VITE_ADMIN_API_URL || 'http://localhost:8000'
const API_BASE = `${API_BASE_URL}/api`

/**
 * Make an authenticated API request
 * @param {string} endpoint - API endpoint
 * @param {object} options - Fetch options
 * @returns {Promise<any>} - Response data
 */
async function authenticatedFetch(endpoint, options = {}) {
  const authHeader = authService.getAuthHeader()
  
  if (!authHeader) {
    throw new Error('Not authenticated')
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': authHeader,
      'Content-Type': 'application/json',
      ...options.headers
    }
  })

  if (response.status === 401) {
    // Unauthorized - clear auth and redirect to login
    authService.logout()
    window.location.href = '/'
    throw new Error('Unauthorized')
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }))
    throw new Error(error.message || 'Request failed')
  }

  return response.json()
}

export const apiService = {
  /**
   * Fetch key requests with optional filter
   * @param {string} filter - Filter by state: 'pending', 'review', 'all'
   * @returns {Promise<Array>} - Array of key requests
   */
  async fetchRequests(filter = 'pending') {
    return authenticatedFetch(`/admin/requests?filter=${filter}`)
  },

  /**
   * Get details for a specific request
   * @param {string} requestId - Request ID
   * @returns {Promise<object>} - Request details
   */
  async getRequestDetails(requestId) {
    return authenticatedFetch(`/admin/requests/${requestId}`)
  },

  /**
   * Approve a key request
   * @param {string} requestId - Request ID to approve
   * @returns {Promise<object>} - Action response
   */
  async approveRequest(requestId) {
    return authenticatedFetch(`/admin/requests/${requestId}/approve`, {
      method: 'POST'
    })
  },

  /**
   * Deny a key request with reason
   * @param {string} requestId - Request ID to deny
   * @param {string} reason - Reason for denial
   * @returns {Promise<object>} - Action response
   */
  async denyRequest(requestId, reason) {
    return authenticatedFetch(`/admin/requests/${requestId}/deny`, {
      method: 'POST',
      body: JSON.stringify({ reason })
    })
  }
}
