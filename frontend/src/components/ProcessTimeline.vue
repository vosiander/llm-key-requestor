<template>
  <section class="process-timeline py-16">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" class="text-center mb-12">
          <h2 class="text-h3 font-weight-bold mb-4">
            {{ $t('timeline.title') }}
          </h2>
          <p class="text-h6 text-medium-emphasis">
            {{ $t('timeline.subtitle') }}
          </p>
        </v-col>
      </v-row>
      
      <v-row justify="center">
        <v-col cols="12" lg="10" xl="8">
          <!-- Desktop Timeline -->
          <div class="d-none d-md-block">
            <div class="timeline-container">
              <!-- Timeline Line -->
              <div class="timeline-line"></div>
              
              <!-- Timeline Steps -->
              <v-row class="timeline-steps">
                <v-col
                  v-for="(step, index) in steps"
                  :key="step.id"
                  cols="4"
                  class="text-center"
                >
                  <div class="step-container">
                    <!-- Step Circle -->
                    <div 
                      class="step-circle"
                      :class="{ 'active': index === currentStep }"
                    >
                      <v-avatar
                        size="80"
                        :color="index <= currentStep ? 'primary' : 'grey-lighten-2'"
                        class="step-avatar"
                      >
                        <v-icon
                          size="40"
                          :color="index <= currentStep ? 'white' : 'grey'"
                        >
                          {{ step.icon }}
                        </v-icon>
                      </v-avatar>
                    </div>
                    
                    <!-- Step Content -->
                    <div class="step-content mt-6">
                      <div class="step-number mb-2">
                        <span class="text-h5 font-weight-bold text-primary">
                          {{ $t('common.step') }} {{ index + 1 }}
                        </span>
                      </div>
                      
                      <h3 class="text-h5 font-weight-bold mb-3">
                        {{ step.title }}
                      </h3>
                      
                      <p class="text-body-1 text-medium-emphasis">
                        {{ step.description }}
                      </p>
                      
                      <!-- Step Status Badge -->
                      <v-chip
                        v-if="index < currentStep"
                        color="success"
                        variant="tonal"
                        size="small"
                        class="mt-2"
                      >
                        <v-icon start size="16">mdi-check</v-icon>
                        {{ $t('timeline.status.complete') }}
                      </v-chip>
                      
                      <v-chip
                        v-else-if="index === currentStep"
                        color="primary"
                        variant="tonal"
                        size="small"
                        class="mt-2"
                      >
                        <v-icon start size="16">mdi-clock</v-icon>
                        {{ $t('timeline.status.current') }}
                      </v-chip>
                      
                      <v-chip
                        v-else
                        color="grey"
                        variant="tonal"
                        size="small"
                        class="mt-2"
                      >
                        <v-icon start size="16">mdi-circle-outline</v-icon>
                        {{ $t('timeline.status.pending') }}
                      </v-chip>
                    </div>
                  </div>
                </v-col>
              </v-row>
            </div>
          </div>
          
          <!-- Mobile Timeline -->
          <div class="d-md-none">
            <v-timeline
              align="start"
              line-inset="16"
              line-thickness="3"
              line-color="primary"
            >
              <v-timeline-item
                v-for="(step, index) in steps"
                :key="step.id"
                :dot-color="index <= currentStep ? 'primary' : 'grey-lighten-2'"
                size="large"
              >
                <template #icon>
                  <v-icon
                    :color="index <= currentStep ? 'white' : 'grey'"
                    size="24"
                  >
                    {{ step.icon }}
                  </v-icon>
                </template>
                
                <v-card variant="outlined" class="mb-4">
                  <v-card-text>
                    <div class="d-flex align-center mb-2">
                      <span class="text-h6 font-weight-bold text-primary me-3">
                        {{ $t('common.step') }} {{ index + 1 }}
                      </span>
                      
                      <v-chip
                        v-if="index < currentStep"
                        color="success"
                        variant="tonal"
                        size="small"
                      >
                        <v-icon start size="14">mdi-check</v-icon>
                        {{ $t('timeline.status.complete') }}
                      </v-chip>
                      
                      <v-chip
                        v-else-if="index === currentStep"
                        color="primary"
                        variant="tonal"
                        size="small"
                      >
                        <v-icon start size="14">mdi-clock</v-icon>
                        {{ $t('timeline.status.current') }}
                      </v-chip>
                      
                      <v-chip
                        v-else
                        color="grey"
                        variant="tonal"
                        size="small"
                      >
                        <v-icon start size="14">mdi-circle-outline</v-icon>
                        {{ $t('timeline.status.pending') }}
                      </v-chip>
                    </div>
                    
                    <h3 class="text-h6 font-weight-bold mb-2">
                      {{ step.title }}
                    </h3>
                    
                    <p class="text-body-2 text-medium-emphasis">
                      {{ step.description }}
                    </p>
                  </v-card-text>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </div>
        </v-col>
      </v-row>
      
      <!-- Call to Action -->
      <v-row justify="center" class="mt-8">
        <v-col cols="12" class="text-center">
          <p class="text-h6 mb-4">
            {{ $t('timeline.cta.title') }}
          </p>
          <v-btn
            size="large"
            color="primary"
            variant="elevated"
            @click="scrollToForm"
          >
            <v-icon start>mdi-form-select</v-icon>
            {{ $t('timeline.cta.button') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script>
export default {
  name: 'ProcessTimeline',
  props: {
    currentStep: {
      type: Number,
      default: 0,
      validator: (value) => value >= 0 && value <= 2
    }
  },
  computed: {
    steps() {
      return [
        {
          id: 1,
          icon: 'mdi-form-select',
          title: this.$t('timeline.steps.step1.title'),
          description: this.$t('timeline.steps.step1.description')
        },
        {
          id: 2,
          icon: 'mdi-check-circle',
          title: this.$t('timeline.steps.step2.title'),
          description: this.$t('timeline.steps.step2.description')
        },
        {
          id: 3,
          icon: 'mdi-email',
          title: this.$t('timeline.steps.step3.title'),
          description: this.$t('timeline.steps.step3.description')
        }
      ]
    }
  },
  methods: {
    scrollToForm() {
      const formSection = document.querySelector('#request-form')
      if (formSection) {
        formSection.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        })
      } else {
        // Fallback: scroll to bottom of page
        window.scrollTo({
          top: document.body.scrollHeight,
          behavior: 'smooth'
        })
      }
    }
  }
}
</script>

<style scoped>
.process-timeline {
  background-color: #f8f9fa;
}

/* Desktop Timeline Styles */
.timeline-container {
  position: relative;
  padding: 2rem 0;
}

.timeline-line {
  position: absolute;
  top: 40px;
  left: 16.67%;
  width: 66.66%;
  height: 4px;
  background: linear-gradient(to right, #1976d2 0%, #1976d2 50%, #e0e0e0 50%, #e0e0e0 100%);
  border-radius: 2px;
  z-index: 1;
}

.timeline-steps {
  position: relative;
  z-index: 2;
}

.step-container {
  position: relative;
}

.step-circle {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  width: 80px;
  height: 80px;
}

.step-avatar {
  border: 4px solid white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.step-circle.active .step-avatar {
  transform: scale(1.1);
  box-shadow: 0 6px 12px rgba(25, 118, 210, 0.3);
}

.step-content {
  max-width: 280px;
  margin: 0 auto;
}

.step-number {
  opacity: 0.8;
}

/* Animation for step completion */
.step-circle .step-avatar {
  transition: all 0.5s ease;
}

/* Responsive adjustments */
@media (max-width: 960px) {
  .timeline-line {
    display: none;
  }
  
  .step-content {
    max-width: 100%;
  }
}

/* Mobile specific styles */
@media (max-width: 600px) {
  .process-timeline {
    padding: 3rem 0;
  }
}

/* Hover effects */
.step-container:hover .step-avatar {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}
</style>
