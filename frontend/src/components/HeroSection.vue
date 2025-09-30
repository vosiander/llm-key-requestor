<template>
  <section class="hero-section">
    <v-container class="py-16">
      <v-row align="center" justify="center">
        <!-- Hero Content -->
        <v-col cols="12" md="8" lg="6" class="text-center">
          <h1 class="hero-title text-h2 text-md-h1 font-weight-bold mb-6">
            Streamline Your LLM API Access
          </h1>
          
          <p class="hero-subtitle text-h6 text-md-h5 mb-8 text-medium-emphasis">
            Get secure API keys for leading language models with our simple, 
            fast approval process. Connect to OpenAI, Anthropic, Google, and more.
          </p>
          
          <v-btn
            size="x-large"
            color="primary"
            variant="elevated"
            class="hero-cta px-8 py-4"
            @click="scrollToForm"
          >
            <v-icon start>mdi-rocket-launch</v-icon>
            Request Your Key
          </v-btn>
        </v-col>
      </v-row>
      
      <!-- Benefits Grid -->
      <v-row class="mt-16" justify="center">
        <v-col cols="12" class="text-center mb-8">
          <h2 class="text-h4 font-weight-bold mb-4">
            Why Choose Our Platform?
          </h2>
          <p class="text-h6 text-medium-emphasis">
            Professional API key management made simple
          </p>
        </v-col>
        
        <v-col
          v-for="benefit in benefits"
          :key="benefit.icon"
          cols="12"
          sm="6"
          md="3"
          class="d-flex"
        >
          <v-card
            class="benefit-card flex-grow-1 pa-6 text-center"
            variant="outlined"
            hover
          >
            <v-avatar
              size="64"
              color="primary"
              class="mb-4"
            >
              <v-icon size="32" color="white">{{ benefit.icon }}</v-icon>
            </v-avatar>
            
            <h3 class="text-h6 font-weight-bold mb-3">
              {{ benefit.title }}
            </h3>
            
            <p class="text-body-2 text-medium-emphasis">
              {{ benefit.description }}
            </p>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script>
export default {
  name: 'HeroSection',
  data() {
    return {
      benefits: [
        {
          icon: 'mdi-clock-fast',
          title: 'Fast Approval',
          description: 'Get your API keys quickly with our streamlined approval process. Most requests processed within 24 hours.'
        },
        {
          icon: 'mdi-shield-check',
          title: 'Secure Access',
          description: 'Enterprise-grade security with encrypted key delivery and secure access management protocols.'
        },
        {
          icon: 'mdi-server-network',
          title: 'Multiple Providers',
          description: 'Access keys for all major LLM providers including OpenAI, Anthropic, Google, Meta, and more.'
        },
        {
          icon: 'mdi-email-fast',
          title: 'Email Delivery',
          description: 'Secure key delivery directly to your inbox with detailed setup instructions and usage guidelines.'
        }
      ]
    }
  },
  methods: {
    scrollToForm() {
      // Smooth scroll to the form section
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
.hero-section {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  color: white;
  min-height: 80vh;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>');
  background-size: 50px 50px;
  opacity: 0.3;
  pointer-events: none;
}

.hero-title {
  position: relative;
  z-index: 1;
}

.hero-subtitle {
  position: relative;
  z-index: 1;
}

.hero-cta {
  position: relative;
  z-index: 1;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2) !important;
  transition: all 0.3s ease !important;
}

.hero-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3) !important;
}

.benefit-card {
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.12);
  height: 100%;
}

.benefit-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.benefit-card .v-avatar {
  transition: all 0.3s ease;
}

.benefit-card:hover .v-avatar {
  transform: scale(1.1);
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .hero-section {
    min-height: 70vh;
  }
  
  .hero-title {
    font-size: 2.5rem !important;
  }
  
  .hero-subtitle {
    font-size: 1.2rem !important;
  }
}
</style>
