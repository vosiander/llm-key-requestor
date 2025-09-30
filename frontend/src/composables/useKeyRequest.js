// Vue 3 composable for key request state management
import { ref, computed, onMounted } from 'vue'
import { apiService, ApiError } from '../services/api.js'

export function useKeyRequest() {
  // Reactive state
  const formData = ref({
    llm: '',
    email: ''
  })
  
  const isLoading = ref(false)
  const error = ref(null)
  const success = ref(false)
  const responseMessage = ref('')
  
  // Available LLM providers (fetched from API)
  const llmProviders = ref([])
  const isLoadingModels = ref(false)
  const modelsError = ref(null)

  // Computed properties
  const isFormValid = computed(() => {
    return formData.value.llm && 
           formData.value.email && 
           isValidEmail(formData.value.email)
  })

  const hasError = computed(() => !!error.value)
  const hasSuccess = computed(() => success.value)

  // Validation functions
  function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  function validateForm() {
    const errors = []

    if (!formData.value.llm) {
      errors.push('Please select an LLM provider')
    }

    if (!formData.value.email) {
      errors.push('Please enter your email address')
    } else if (!isValidEmail(formData.value.email)) {
      errors.push('Please enter a valid email address')
    }

    return errors
  }

  // Email validation rules for Vuetify
  const emailRules = [
    (value) => !!value || 'Email is required',
    (value) => isValidEmail(value) || 'Please enter a valid email address'
  ]

  const llmRules = [
    (value) => !!value || 'Please select an LLM provider'
  ]

  // Fetch models from API
  async function fetchModels() {
    try {
      isLoadingModels.value = true
      modelsError.value = null
      
      const models = await apiService.getModels()
      llmProviders.value = models
      
      return true
    } catch (err) {
      console.error('Failed to fetch models:', err)
      modelsError.value = err instanceof ApiError ? err.message : 'Failed to load models'
      
      // Fallback to empty array if fetch fails
      llmProviders.value = []
      
      return false
    } finally {
      isLoadingModels.value = false
    }
  }

  // Actions
  async function submitRequest() {
    try {
      // Reset previous states
      clearMessages()
      
      // Validate form
      const validationErrors = validateForm()
      if (validationErrors.length > 0) {
        error.value = validationErrors[0]
        return false
      }

      isLoading.value = true

      // Submit request
      const response = await apiService.submitKeyRequest({
        llm: formData.value.llm,
        email: formData.value.email
      })

      // Handle successful response
      success.value = true
      responseMessage.value = response.message || 'Request submitted successfully!'
      
      // Optionally reset form after successful submission
      // resetForm()
      
      return true

    } catch (err) {
      console.error('Request submission failed:', err)
      
      if (err instanceof ApiError) {
        error.value = err.message
      } else {
        error.value = 'An unexpected error occurred. Please try again.'
      }
      
      return false
    } finally {
      isLoading.value = false
    }
  }

  function resetForm() {
    formData.value.llm = ''
    formData.value.email = ''
    clearMessages()
  }

  function clearMessages() {
    error.value = null
    success.value = false
    responseMessage.value = ''
  }

  // Health check for backend connectivity
  async function checkBackendHealth() {
    try {
      const isHealthy = await apiService.checkHealth()
      return isHealthy
    } catch (err) {
      console.error('Backend health check failed:', err)
      return false
    }
  }

  // Load models on mount
  onMounted(() => {
    fetchModels()
  })

  // Return reactive state and methods
  return {
    // State
    formData,
    isLoading,
    error,
    success,
    responseMessage,
    llmProviders,
    isLoadingModels,
    modelsError,
    
    // Computed
    isFormValid,
    hasError,
    hasSuccess,
    
    // Validation rules for Vuetify
    emailRules,
    llmRules,
    
    // Methods
    submitRequest,
    resetForm,
    clearMessages,
    validateForm,
    isValidEmail,
    checkBackendHealth,
    fetchModels
  }
}
