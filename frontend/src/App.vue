<template>
  <v-app>
    <v-main>
      <!-- Hero Section -->
      <HeroSection />
      
      <!-- Process Timeline -->
      <ProcessTimeline />
      
      <!-- Key Request Form -->
      <KeyRequestForm />
      
      <!-- Footer -->
      <footer class="footer py-8">
        <v-container>
          <v-row justify="center">
            <v-col cols="12" class="text-center">
              <v-divider class="mb-6"></v-divider>
              
              <div class="mb-4">
                <v-icon color="primary" size="32" class="mb-2">
                  mdi-key-variant
                </v-icon>
                <h3 class="text-h6 font-weight-bold">
                  LLM Key Requestor
                </h3>
              </div>
              
              <p class="text-body-2 text-medium-emphasis mb-4">
                Secure API key management for leading language model providers
              </p>
              
              <div class="d-flex justify-center align-center flex-wrap ga-4 mb-4">
                <v-chip
                  v-for="provider in featuredProviders"
                  :key="provider"
                  variant="tonal"
                  size="small"
                  color="primary"
                >
                  <v-icon start size="16">mdi-robot</v-icon>
                  {{ provider }}
                </v-chip>
              </div>
              
              <v-row justify="center" class="mt-6">
                <v-col cols="auto">
                  <v-btn
                    variant="text"
                    color="primary"
                    size="small"
                    @click="scrollToTop"
                  >
                    <v-icon start>mdi-arrow-up</v-icon>
                    Back to Top
                  </v-btn>
                </v-col>
              </v-row>
              
              <v-divider class="my-4"></v-divider>
              
              <p class="text-body-2 text-medium-emphasis">
                &copy; {{ currentYear }} LLM Key Requestor. Built with Vue.js and Vuetify.
              </p>
              
              <div class="mt-2">
                <v-btn
                  variant="text"
                  size="small"
                  color="primary"
                  @click="showAbout = true"
                >
                  <v-icon start size="16">mdi-information</v-icon>
                  About
                </v-btn>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </footer>
    </v-main>

    <!-- About Dialog -->
    <v-dialog
      v-model="showAbout"
      max-width="500"
      scrollable
    >
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="me-2">mdi-information</v-icon>
          About LLM Key Requestor
        </v-card-title>
        
        <v-divider></v-divider>
        
        <v-card-text class="py-6">
          <div class="about-content">
            <p class="mb-4">
              LLM Key Requestor is a secure platform for managing API key requests 
              for leading language model providers. Our streamlined process ensures 
              quick and secure access to the AI tools you need.
            </p>
            
            <h4 class="text-h6 mb-3">Supported Providers</h4>
            <ul class="mb-4">
              <li>OpenAI (GPT-4, GPT-3.5)</li>
              <li>Anthropic (Claude 3, Claude 2)</li>
              <li>Google (Gemini Pro, PaLM 2)</li>
              <li>Meta (Llama 2)</li>
              <li>Mistral AI</li>
              <li>Cohere</li>
            </ul>
            
            <h4 class="text-h6 mb-3">Features</h4>
            <ul class="mb-4">
              <li>Fast approval process</li>
              <li>Enterprise-grade security</li>
              <li>Multiple provider support</li>
              <li>Secure email delivery</li>
              <li>Professional support</li>
            </ul>
            
            <p class="text-body-2 text-medium-emphasis">
              For technical support or questions, please contact our team.
            </p>
          </div>
        </v-card-text>
        
        <v-divider></v-divider>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="elevated"
            @click="showAbout = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Scroll to top FAB -->
    <v-fab
      v-show="showScrollTop"
      icon="mdi-arrow-up"
      location="bottom end"
      size="small"
      color="primary"
      @click="scrollToTop"
    ></v-fab>
  </v-app>
</template>

<script>
import HeroSection from './components/HeroSection.vue'
import ProcessTimeline from './components/ProcessTimeline.vue'
import KeyRequestForm from './components/KeyRequestForm.vue'

export default {
  name: 'App',
  components: {
    HeroSection,
    ProcessTimeline,
    KeyRequestForm
  },
  data() {
    return {
      showAbout: false,
      showScrollTop: false,
      featuredProviders: ['OpenAI', 'Anthropic', 'Google', 'Meta', 'Mistral', 'Cohere'],
      currentYear: new Date().getFullYear()
    }
  },
  mounted() {
    // Add scroll listener for scroll-to-top button
    window.addEventListener('scroll', this.handleScroll)
    
    // Optional: Log app startup
    console.log('LLM Key Requestor application started')
  },
  beforeUnmount() {
    // Clean up scroll listener
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      // Show scroll-to-top button after scrolling down 300px
      this.showScrollTop = window.pageYOffset > 300
    },
    
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    }
  }
}
</script>

<style scoped>
/* Footer styling */
.footer {
  background-color: #fafafa;
  border-top: 1px solid #e0e0e0;
}

/* About dialog content styling */
.about-content ul {
  padding-left: 1.5rem;
}

.about-content li {
  list-style-type: disc;
  margin-bottom: 0.5rem;
}

/* Global app styling */
:deep(.v-application) {
  font-family: 'Roboto', sans-serif;
}

/* Smooth scroll behavior */
html {
  scroll-behavior: smooth;
}

/* Custom scrollbar for webkit browsers */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

/* Ensure full height layout */
.v-application {
  min-height: 100vh;
}

/* Loading animation for components */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .footer {
    padding: 2rem 0;
  }
}
</style>
