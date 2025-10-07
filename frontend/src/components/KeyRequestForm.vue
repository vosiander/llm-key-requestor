<template>
  <section id="request-form" class="key-request-form py-16">
    <v-container>
      <v-row justify="center">
        <v-col>
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
                {{ $t('form.title') }}
              </h2>
              
              <p class="text-body-1 text-medium-emphasis">
                {{ $t('form.subtitle') }}
              </p>
            </div>

            <!-- Form -->
            <v-form
              ref="form"
              v-model="formValid"
              @submit.prevent="handleSubmit"
            >
              <!-- Featured Models Section (Always Visible) -->
              <div class="mb-8">
                <h3 class="text-h6 font-weight-medium mb-2">
                  {{ $t('form.featured.title') }}
                </h3>
                <p class="text-body-2 text-medium-emphasis mb-4">
                  {{ $t('form.featured.subtitle') }}
                </p>

                <!-- Loading State for Featured Models -->
                <div v-if="isLoadingFeatured" class="text-center py-8">
                  <v-progress-circular
                    indeterminate
                    color="primary"
                    size="48"
                  />
                  <p class="text-body-2 text-medium-emphasis mt-4">
                    {{ $t('common.loading') }}
                  </p>
                </div>

                <!-- Featured Model Cards -->
                <v-row v-else>
                  <v-col
                    v-for="model in featuredModels"
                    :key="model.id"
                    cols="12"
                    md="4"
                  >
                    <v-card
                      class="featured-card"
                      :class="{ 'featured-card-selected': selectedModelId === model.id }"
                      variant="outlined"
                      hover
                      height="100%"
                    >
                      <v-card-text class="pa-4">
                        <div class="d-flex flex-column h-100 position-relative">
                          <!-- Info Button - Top Right -->
                          <v-btn
                            icon
                            variant="text"
                            size="small"
                            :href="model.documentation_link"
                            target="_blank"
                            class="info-btn-featured"
                            @click.stop
                          >
                            <v-icon size="20">mdi-help-circle-outline</v-icon>
                          </v-btn>
                          
                          <!-- Icon -->
                          <div class="featured-icon-container mb-3">
                            <Icon
                              :icon="model.icon"
                              :style="{ color: model.color }"
                              width="40"
                              height="40"
                            />
                          </div>
                          
                          <!-- Title -->
                          <h4 class="text-h6 font-weight-bold mb-2">
                            {{ model.title }}
                          </h4>
                          
                          <!-- Subtitle -->
                          <p class="text-subtitle-2 text-primary mb-2">
                            {{ model.subtitle }}
                          </p>
                          
                          <!-- Description -->
                          <p class="text-body-2 text-medium-emphasis mb-4 flex-grow-1">
                            {{ model.description }}
                          </p>
                          
                          <!-- Actions -->
                          <v-btn
                            color="primary"
                            variant="elevated"
                            size="default"
                            :disabled="isLoading"
                            :loading="isLoading && selectedModelId === model.id"
                            @click="selectFeaturedModel(model)"
                            block
                          >
                            <v-icon start>mdi-check-circle</v-icon>
                            {{ $t('form.featured.requestButton') }}
                          </v-btn>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </div>

              <!-- Advanced Options Accordion -->
              <v-expansion-panels class="mb-6">
                <v-expansion-panel>
                  <v-expansion-panel-title>
                    <div class="d-flex align-center">
                      <v-icon class="me-2">mdi-cog</v-icon>
                      <span class="text-h6">{{ $t('form.advanced.title') }}</span>
                    </div>
                  </v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <!-- Model Input Field -->
                    <v-text-field
                      v-model="formData.llm"
                      :rules="llmRules"
                      :label="$t('form.fields.model.label')"
                      :placeholder="$t('form.fields.model.placeholder')"
                      variant="outlined"
                      prepend-inner-icon="mdi-robot"
                      class="mb-4 mt-4"
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
                          <span>{{ $t('form.fields.model.tooltip') }}</span>
                        </v-tooltip>
                      </template>
                    </v-text-field>

                    <!-- API-Fetched Model Cards Section -->
                    <div>
                      <div class="d-flex align-center justify-space-between mb-4">
                        <h4 class="text-subtitle-1 font-weight-medium">
                          {{ $t('form.provider.title') }}
                        </h4>
                        <v-btn
                          v-if="modelsError"
                          size="small"
                          variant="text"
                          color="primary"
                          @click="fetchModels"
                        >
                          <v-icon start>mdi-refresh</v-icon>
                          {{ $t('form.provider.retry') }}
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
                          {{ $t('form.provider.loading') }}
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
                            {{ $t('form.provider.error') }}
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
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>

              <!-- Email Input -->
              <v-text-field
                v-model="formData.email"
                :rules="emailRules"
                :label="$t('form.fields.email.label')"
                :placeholder="$t('form.fields.email.placeholder')"
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
                :rules="[v => !!v || $t('form.terms.required')]"
                class="mb-4"
                :disabled="isLoading"
              >
                <template #label>
                  <span class="text-body-2">
                    {{ $t('form.terms.label', { terms: '' }) }}
                    <a href="#" class="text-primary text-decoration-none" @click.prevent="showTerms = true">
                      {{ $t('form.terms.link') }}
                    </a>
                    {{ $t('form.terms.label', { terms: '' }).split('{terms}')[1] }}
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
                {{ isLoading ? $t('form.buttons.submitting') : $t('form.buttons.submit') }}
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
                {{ $t('form.buttons.reset') }}
              </v-btn>
            </v-form>

            <!-- Form Footer -->
            <v-divider class="my-6"></v-divider>
            
            <div class="text-center">
              <p class="text-body-2 text-medium-emphasis mb-2">
                <v-icon size="16" class="me-1">mdi-shield-check</v-icon>
                {{ $t('form.security.encrypted') }}
              </p>
              
              <p class="text-body-2 text-medium-emphasis">
                <v-icon size="16" class="me-1">mdi-clock</v-icon>
                {{ $t('form.security.processing') }}
              </p>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Success Modal -->
    <v-dialog
      v-model="showSuccessModal"
      max-width="500"
    >
      <v-card>
        <v-card-title class="d-flex align-center bg-success pa-4">
          <v-icon size="32" class="me-2" color="white">mdi-check-circle</v-icon>
          <span class="text-white">{{ $t('form.messages.successTitle') }}</span>
        </v-card-title>
        
        <v-card-text class="py-6">
          <p class="text-body-1 mb-0">
            {{ modalMessage }}
          </p>
        </v-card-text>
        
        <v-divider></v-divider>
        
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="success"
            variant="elevated"
            @click="closeModal"
          >
            {{ $t('form.messages.closeButton') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Error Modal -->
    <v-dialog
      v-model="showErrorModal"
      max-width="500"
    >
      <v-card>
        <v-card-title class="d-flex align-center bg-error pa-4">
          <v-icon size="32" class="me-2" color="white">mdi-alert-circle</v-icon>
          <span class="text-white">{{ $t('form.messages.errorTitle') }}</span>
        </v-card-title>
        
        <v-card-text class="py-6">
          <p class="text-body-1 mb-0">
            {{ modalMessage }}
          </p>
        </v-card-text>
        
        <v-divider></v-divider>
        
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="error"
            variant="elevated"
            @click="closeModal"
          >
            {{ $t('form.messages.closeButton') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Terms and Conditions Dialog -->
    <v-dialog
      v-model="showTerms"
      max-width="600"
      scrollable
    >
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="me-2">mdi-file-document-outline</v-icon>
          {{ $t('termsDialog.title') }}
        </v-card-title>
        
        <v-divider></v-divider>
        
        <v-card-text class="py-6">
          <div class="terms-content">
            <h3 class="text-h6 mb-3">{{ $t('termsDialog.heading') }}</h3>
            
            <p class="mb-4">
              {{ $t('termsDialog.intro') }}
            </p>
            
            <ul class="mb-4">
              <li class="mb-2">
                <strong>{{ $t('termsDialog.items.legitimateUse.title') }}</strong> {{ $t('termsDialog.items.legitimateUse.description') }}
              </li>
              <li class="mb-2">
                <strong>{{ $t('termsDialog.items.providerTerms.title') }}</strong> {{ $t('termsDialog.items.providerTerms.description') }}
              </li>
              <li class="mb-2">
                <strong>{{ $t('termsDialog.items.security.title') }}</strong> {{ $t('termsDialog.items.security.description') }}
              </li>
              <li class="mb-2">
                <strong>{{ $t('termsDialog.items.monitoring.title') }}</strong> {{ $t('termsDialog.items.monitoring.description') }}
              </li>
              <li class="mb-2">
                <strong>{{ $t('termsDialog.items.revocation.title') }}</strong> {{ $t('termsDialog.items.revocation.description') }}
              </li>
            </ul>
            
            <p class="text-body-2 text-medium-emphasis">
              {{ $t('termsDialog.footer') }}
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
            {{ $t('termsDialog.button') }}
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
      featuredModels,
      isLoadingFeatured,
      featuredError,
      showSuccessModal,
      showErrorModal,
      modalMessage,
      isFormValid,
      hasError,
      hasSuccess,
      emailRules,
      llmRules,
      submitRequest,
      resetForm,
      clearMessages,
      closeModal,
      fetchModels,
      fetchFeaturedModels
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
      featuredModels,
      isLoadingFeatured,
      featuredError,
      showSuccessModal,
      showErrorModal,
      modalMessage,
      isFormValid,
      hasError,
      hasSuccess,
      emailRules,
      llmRules,
      submitRequest,
      resetForm,
      clearMessages,
      closeModal,
      fetchModels,
      fetchFeaturedModels
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
    
    async selectFeaturedModel(model) {
      this.formData.llm = model.id
      this.selectedModelId = model.id
      
      // Auto-submit if email and terms are valid
      if (this.formData.email && this.agreeToTerms && this.$refs.form.validate()) {
        await this.handleSubmit()
      }
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
        return
      }

      try {
        await this.submitRequest()
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

/* Featured Model Cards Styling */
.featured-card {
  border-radius: 16px;
  border-width: 2px;
  transition: all 0.3s ease;
}

.featured-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.featured-card-selected {
  border-color: rgb(var(--v-theme-primary)) !important;
  background-color: rgba(var(--v-theme-primary), 0.05);
}

.featured-icon-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  border-radius: 12px;
  background-color: rgba(var(--v-theme-primary), 0.1);
}

/* Info button positioning for featured cards */
.info-btn-featured {
  position: absolute !important;
  top: 8px;
  right: 8px;
  z-index: 1;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

.info-btn-featured:hover {
  opacity: 1;
}

/* Model Cards Styling (Advanced Options) */
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

/* Expansion Panel Styling */
:deep(.v-expansion-panel) {
  border-radius: 12px !important;
  overflow: hidden;
}

:deep(.v-expansion-panel-title) {
  border-radius: 12px !important;
}

/* Modal Styling */
:deep(.v-dialog .v-card) {
  border-radius: 16px;
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
