<template>
  <section id="request-form" class="key-request-form py-16">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8" lg="6">
          <v-card
            class="form-card pa-8"
            variant="elevated"
            elevation="8"
          >
            <!-- Form Header -->
            <div class="text-center mb-8">
              <v-icon
                size="64"
                color="primary"
                class="mb-4"
              >
                mdi-key-plus
              </v-icon>
              
              <h2 class="text-h4 font-weight-bold mb-3">
                Request Your API Key
              </h2>
              
              <p class="text-body-1 text-medium-emphasis">
                Fill out the form below to get access to your preferred LLM provider
              </p>
            </div>

            <!-- Success Message -->
            <v-alert
              v-if="hasSuccess"
              type="success"
              variant="tonal"
              prominent
              class="mb-6"
            >
              <template #title>
                <div class="d-flex align-center">
                  <v-icon class="me-2">mdi-check-circle</v-icon>
                  Request Submitted Successfully!
                </div>
              </template>
              <p class="mb-0">{{ responseMessage }}</p>
            </v-alert>

            <!-- Error Message -->
            <v-alert
              v-if="hasError"
              type="error"
              variant="tonal"
              prominent
              closable
              class="mb-6"
              @click:close="clearMessages"
            >
              <template #title>
                <div class="d-flex align-center">
                  <v-icon class="me-2">mdi-alert-circle</v-icon>
                  Request Failed
                </div>
              </template>
              <p class="mb-0">{{ error }}</p>
            </v-alert>

            <!-- Form -->
            <v-form
              ref="form"
              v-model="formValid"
              @submit.prevent="handleSubmit"
            >
              <!-- Model Cards Section -->
              <div class="mb-6">
                <div class="d-flex align-center justify-space-between mb-4">
                  <h3 class="text-h6 font-weight-medium">
                    Choose Your LLM Provider
                  </h3>
                  <v-btn
                    v-if="modelsError"
                    size="small"
                    variant="text"
                    color="primary"
                    @click="fetchModels"
                  >
                    <v-icon start>mdi-refresh</v-icon>
                    Retry
                  </v-btn>
                </div>

                <!-- Loading State -->
                <div v-if="isLoadingModels" class="text-center py-8">
                  <v-progress-circular
                    indeterminate
                    color="primary"
                    size="48"
                  />
                  <p class="text-body-2 text-medium-emphasis mt-4">
                    Loading available models...
                  </p>
                </div>

                <!-- Error State -->
                <v-alert
                  v-else-if="modelsError"
                  type="warning"
                  variant="tonal"
                  class="mb-4"
                >
                  <template #title>
                    <div class="d-flex align-center">
                      <v-icon class="me-2">mdi-alert</v-icon>
                      Failed to Load Models
                    </div>
                  </template>
                  <p class="mb-0">{{ modelsError }}</p>
                </v-alert>

                <!-- Model Cards Grid -->
                <v-row v-else class="model-cards-grid">
                  <v-col
                    v-for="model in llmProviders"
                    :key="model.id"
                    cols="12"
                    sm="6"
                    md="4"
                    lg="3"
                  >
                    <v-card
                      class="model-card"
                      :class="{ 'model-card-selected': selectedModelId === model.id }"
                      variant="outlined"
                      hover
                      :disabled="isLoading"
                      @click="selectModel(model)"
                    >
                      <v-card-text class="pa-4">
                        <div class="d-flex flex-column align-center text-center">
                          <!-- Icon -->
                          <div class="model-icon-container mb-3">
                            <Icon
                              :icon="model.icon"
                              :style="{ color: model.color }"
                              width="48"
                              height="48"
                            />
                          </div>
                          
                          <!-- Title -->
                          <h4 class="text-subtitle-1 font-weight-bold mb-2">
                            {{ model.title }}
                          </h4>
                          
                          <!-- Description -->
                          <p class="text-body-2 text-medium-emphasis mb-0">
                            {{ model.description }}
                          </p>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </div>

              <!-- LLM Model Input (Custom Entry) -->
              <v-text-field
                v-model="formData.llm"
                :rules="llmRules"
                label="LLM Model"
                placeholder="e.g., OpenAI GPT-5, Claude 4, Gemini Ultra, or select from cards above"
                variant="outlined"
                prepend-inner-icon="mdi-robot"
                class="mb-4"
                :disabled="isLoading"
                clearable
                @input="onModelInputChange"
              >
                <template #append-inner>
                  <v-tooltip location="top">
                    <template #activator="{ props }">
                      <v-icon
                        v-bind="props"
                        size="20"
                        color="info"
                      >
                        mdi-information-outline
                      </v-icon>
                    </template>
                    <span>Select a model card above or enter any custom model name</span>
                  </v-tooltip>
                </template>
              </v-text-field>

              <!-- Email Input -->
              <v-text-field
                v-model="formData.email"
                :rules="emailRules"
                label="Email Address"
                placeholder="Enter your email address"
                variant="outlined"
                prepend-inner-icon="mdi-email"
                type="email"
                class="mb-6"
                :disabled="isLoading"
                autocomplete="email"
              />

              <!-- Terms and Conditions -->
              <v-checkbox
                v-model="agreeToTerms"
                :rules="[v => !!v || 'You must agree to the terms and conditions']"
                class="mb-4"
                :disabled="isLoading"
              >
                <template #label>
                  <span class="text-body-2">
                    I agree to the 
                    <a href="#" class="text-primary text-decoration-none" @click.prevent="showTerms = true">
                      Terms and Conditions
                    </a>
                    and understand that API keys are subject to provider terms of service.
                  </span>
                </template>
              </v-checkbox>

              <!-- Submit Button -->
              <v-btn
                type="submit"
                size="large"
                color="primary"
                variant="elevated"
                block
                :loading="isLoading"
                :disabled="!formValid || !agreeToTerms"
                class="mb-4"
              >
                <template #prepend>
                  <v-icon>mdi-send</v-icon>
                </template>
                {{ isLoading ? 'Submitting Request...' : 'Submit Request' }}
              </v-btn>

              <!-- Reset Button -->
              <v-btn
                variant="outlined"
                color="secondary"
                block
                :disabled="isLoading"
                @click="handleReset"
              >
                <template #prepend>
                  <v-icon>mdi-refresh</v-icon>
                </template>
                Reset Form
              </v-btn>
            </v-form>

            <!-- Form Footer -->
            <v-divider class="my-6"></v-divider>
            
            <div class="text-center">
              <p class="text-body-2 text-medium-emphasis mb-2">
                <v-icon size="16" class="me-1">mdi-shield-check</v-icon>
                Your information is secure and encrypted
              </p>
              
              <p class="text-body-2 text-medium-emphasis">
                <v-icon size="16" class="me-1">mdi-clock</v-icon>
                Most requests are processed within 24 hours
              </p>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Terms and Conditions Dialog -->
    <v-dialog
      v-model="showTerms"
      max-width="600"
      scrollable
    >
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="me-2">mdi-file-document-outline</v-icon>
          Terms and Conditions
        </v-card-title>
        
        <v-divider></v-divider>
        
        <v-card-text class="py-6">
          <div class="terms-content">
            <h3 class="text-h6 mb-3">API Key Request Terms</h3>
            
            <p class="mb-4">
              By submitting this form, you acknowledge and agree to the following terms:
            </p>
            
            <ul class="mb-4">
              <li class="mb-2">
                <strong>Legitimate Use:</strong> API keys are provided for legitimate development, 
                research, or business purposes only.
              </li>
              <li class="mb-2">
                <strong>Provider Terms:</strong> You agree to comply with the terms of service 
                of the respective LLM provider (OpenAI, Anthropic, Google, etc.).
              </li>
              <li class="mb-2">
                <strong>Security:</strong> You are responsible for keeping your API keys secure 
                and not sharing them with unauthorized parties.
              </li>
              <li class="mb-2">
                <strong>Usage Monitoring:</strong> API usage may be monitored for compliance 
                and security purposes.
              </li>
              <li class="mb-2">
                <strong>Revocation:</strong> We reserve the right to revoke access if terms 
                are violated or suspicious activity is detected.
              </li>
            </ul>
            
            <p class="text-body-2 text-medium-emphasis">
              For questions about these terms, please contact our support team.
            </p>
          </div>
        </v-card-text>
        
        <v-divider></v-divider>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="elevated"
            @click="showTerms = false"
          >
            I Understand
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </section>
</template>

<script>
import { ref } from 'vue'
import { Icon } from '@iconify/vue'
import { useKeyRequest } from '../composables/useKeyRequest.js'

export default {
  name: 'KeyRequestForm',
  components: {
    Icon
  },
  setup() {
    // Use the composable for all key request functionality
    const {
      formData,
      isLoading,
      error,
      success,
      responseMessage,
      llmProviders,
      isLoadingModels,
      modelsError,
      isFormValid,
      hasError,
      hasSuccess,
      emailRules,
      llmRules,
      submitRequest,
      resetForm,
      clearMessages,
      fetchModels
    } = useKeyRequest()

    return {
      formData,
      isLoading,
      error,
      success,
      responseMessage,
      llmProviders,
      isLoadingModels,
      modelsError,
      isFormValid,
      hasError,
      hasSuccess,
      emailRules,
      llmRules,
      submitRequest,
      resetForm,
      clearMessages,
      fetchModels
    }
  },
  data() {
    return {
      formValid: false,
      agreeToTerms: false,
      showTerms: false,
      selectedModelId: null
    }
  },
  methods: {
    selectModel(model) {
      this.formData.llm = model.id
      this.selectedModelId = model.id
    },
    
    onModelInputChange() {
      // Clear selection if user manually types
      const matchingModel = this.llmProviders.find(
        provider => provider.title.toLowerCase() === this.formData.llm.toLowerCase()
      )
      this.selectedModelId = matchingModel ? matchingModel.id : null
    },
    
    async handleSubmit() {
      // Validate the form first
      if (!this.$refs.form.validate()) {
        return
      }

      if (!this.agreeToTerms) {
        // This should be caught by form validation, but just in case
        return
      }

      try {
        const success = await this.submitRequest()
        
        if (success) {
          // Scroll to top of form to show success message
          this.$nextTick(() => {
            const formElement = document.getElementById('request-form')
            if (formElement) {
              formElement.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
              })
            }
          })
        }
      } catch (err) {
        console.error('Form submission error:', err)
      }
    },
    
    handleReset() {
      // Reset the form validation
      this.$refs.form.resetValidation()
      
      // Reset the composable data
      this.resetForm()
      
      // Reset local form state
      this.agreeToTerms = false
      this.formValid = false
      this.selectedModelId = null
    }
  }
}
</script>

<style scoped>
.key-request-form {
  background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
}

.form-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.form-card:hover {
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
}

/* Custom styles for form elements */
:deep(.v-field--variant-outlined) {
  border-radius: 12px;
}

:deep(.v-btn) {
  border-radius: 12px;
  font-weight: 600;
}

/* Terms content styling */
.terms-content ul {
  padding-left: 1.5rem;
}

.terms-content li {
  list-style-type: disc;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .key-request-form {
    padding: 2rem 0;
  }
  
  .form-card {
    margin: 1rem;
    border-radius: 12px;
  }
}

/* Loading state styling */
:deep(.v-btn--loading .v-btn__content) {
  opacity: 0.8;
}

/* Success/Error alert animations */
.v-alert {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Model Cards Styling */
.model-cards-grid {
  margin-bottom: 0;
}

.model-card {
  height: 100%;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 12px;
  border-width: 2px;
}

.model-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.model-card-selected {
  border-color: rgb(var(--v-theme-primary)) !important;
  background-color: rgba(var(--v-theme-primary), 0.05);
  box-shadow: 0 4px 16px rgba(var(--v-theme-primary), 0.2);
}

.model-card-selected:hover {
  box-shadow: 0 8px 24px rgba(var(--v-theme-primary), 0.3);
}

.model-icon-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 12px;
  background-color: rgba(0, 0, 0, 0.03);
  transition: all 0.3s ease;
}

.model-card:hover .model-icon-container {
  background-color: rgba(0, 0, 0, 0.06);
  transform: scale(1.05);
}

.model-card-selected .model-icon-container {
  background-color: rgba(var(--v-theme-primary), 0.1);
}

/* Responsive model cards */
@media (max-width: 960px) {
  .model-card {
    margin-bottom: 0.5rem;
  }
}

@media (max-width: 600px) {
  .model-icon-container {
    width: 56px;
    height: 56px;
  }
  
  .model-card-selected {
    border-width: 2px;
  }
}
</style>
