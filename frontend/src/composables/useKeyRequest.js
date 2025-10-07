// Vue 3 composable for key request state management
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { apiService, ApiError } from '../services/api.js'

export function useKeyRequest() {
  // i18n instance
  const { t } = useI18n()
  
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
  
  // Featured models (fetched from API)
  const featuredModels = ref([])
  const isLoadingFeatured = ref(false)
  const featuredError = ref(null)
  
  // Modal state
  const showSuccessModal = ref(false)
  const showErrorModal = ref(false)
  const modalMessage = ref('')

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

  // Email validation rules for Vuetify (with i18n)
  const emailRules = [
    (value) => !!value || t('form.validation.emailRequired'),
    (value) => isValidEmail(value) || t('form.validation.emailInvalid')
  ]

  const llmRules = [
    (value) => !!value || t('form.validation.llmRequired')
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
  
  // Fetch featured models from API
  async function fetchFeaturedModels() {
    try {
      isLoadingFeatured.value = true
      featuredError.value = null
      
      const models = await apiService.getFeaturedModels()
      featuredModels.value = models
      
      return true
    } catch (err) {
      console.error('Failed to fetch featured models:', err)
      featuredError.value = err instanceof ApiError ? err.message : 'Failed to load featured models'
      
      // Fallback to empty array if fetch fails
      featuredModels.value = []
      
      return false
    } finally {
      isLoadingFeatured.value = false
    }
  }

  // Submit request with modal handling
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
      responseMessage.value = response.message || t('form.messages.successMessage')
      
      // Show success modal
      modalMessage.value = responseMessage.value
      showSuccessModal.value = true
      
      return true

    } catch (err) {
      console.error('Request submission failed:', err)
      
      if (err instanceof ApiError) {
        error.value = err.message
      } else {
        error.value = t('form.messages.errorMessage')
      }
      
      // Show error modal
      modalMessage.value = error.value
      showErrorModal.value = true
      
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
    showSuccessModal.value = false
    showErrorModal.value = false
    modalMessage.value = ''
  }
  
  function closeModal() {
    showSuccessModal.value = false
    showErrorModal.value = false
    modalMessage.value = ''
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
    fetchFeaturedModels()
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
    featuredModels,
    isLoadingFeatured,
    featuredError,
    showSuccessModal,
    showErrorModal,
    modalMessage,
    
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
    closeModal,
    validateForm,
    isValidEmail,
    checkBackendHealth,
    fetchModels,
    fetchFeaturedModels
  }
}
