export default {
  hero: {
    title: 'Streamline Your LLM API Access',
    subtitle: 'Get secure API keys for leading language models with our simple, fast approval process. Connect to OpenAI, Anthropic, Google, and more.',
    cta: 'Request Your Key',
    benefitsTitle: 'Why Choose Our Platform?',
    benefitsSubtitle: 'Professional API key management made simple',
    benefits: {
      fast: {
        title: 'Fast Approval',
        description: 'Get your API keys quickly with our streamlined approval process. Most requests processed within 24 hours.'
      },
      secure: {
        title: 'Secure Access',
        description: 'Enterprise-grade security with encrypted key delivery and secure access management protocols.'
      },
      multiple: {
        title: 'Multiple Providers',
        description: 'Access keys for all major LLM providers including OpenAI, Anthropic, Google, Meta, and more.'
      },
      email: {
        title: 'Email Delivery',
        description: 'Secure key delivery directly to your inbox with detailed setup instructions and usage guidelines.'
      }
    }
  },
  timeline: {
    title: 'How It Works',
    subtitle: 'Get your LLM API key in three simple steps',
    steps: {
      step1: {
        title: 'Submit Request',
        description: 'Fill out the form with your preferred LLM provider and email address. Choose from OpenAI, Anthropic, Google, and more.'
      },
      step2: {
        title: 'Admin Approval',
        description: 'Our team reviews and approves your request. We verify your information and ensure compliance with provider terms.'
      },
      step3: {
        title: 'Receive Key',
        description: 'Get your API key delivered securely via email with detailed setup instructions and usage guidelines.'
      }
    },
    status: {
      complete: 'Complete',
      current: 'Current',
      pending: 'Pending'
    },
    cta: {
      title: 'Ready to get started?',
      button: 'Start Your Request'
    }
  },
  form: {
    title: 'Request Your API Key',
    subtitle: 'Fill out the form below to get access to your preferred LLM provider',
    provider: {
      title: 'Choose Your LLM Provider',
      retry: 'Retry',
      loading: 'Loading available models...',
      error: 'Failed to Load Models',
      models: {
        openai: {
          title: 'OpenAI',
          description: 'GPT-4, GPT-3.5 and more'
        },
        anthropic: {
          title: 'Anthropic',
          description: 'Claude 3 and Claude 2'
        },
        google: {
          title: 'Google',
          description: 'Gemini Pro and PaLM 2'
        },
        meta: {
          title: 'Meta',
          description: 'Llama 2 models'
        },
        mistral: {
          title: 'Mistral AI',
          description: 'Mistral models'
        },
        cohere: {
          title: 'Cohere',
          description: 'Command and Embed'
        }
      }
    },
    fields: {
      llm: {
        label: 'LLM Model',
        placeholder: 'e.g., OpenAI GPT-5, Claude 4, Gemini Ultra, or select from cards above',
        tooltip: 'Select a model card above or enter any custom model name'
      },
      email: {
        label: 'Email Address',
        placeholder: 'Enter your email address'
      }
    },
    validation: {
      llmRequired: 'Please select an LLM model',
      emailRequired: 'Email address is required',
      emailInvalid: 'Please enter a valid email address'
    },
    terms: {
      label: 'I agree to the {terms} and understand that API keys are subject to provider terms of service.',
      link: 'Terms and Conditions',
      required: 'You must agree to the terms and conditions'
    },
    buttons: {
      submit: 'Submit Request',
      submitting: 'Submitting Request...',
      reset: 'Reset Form'
    },
    security: {
      encrypted: 'Your information is secure and encrypted',
      processing: 'Most requests are processed within 24 hours'
    },
    messages: {
      successTitle: 'Request Submitted Successfully!',
      errorTitle: 'Request Failed',
      defaultSuccess: 'Your request has been submitted successfully. You will receive an email soon.'
    }
  },
  termsDialog: {
    title: 'Terms and Conditions',
    heading: 'API Key Request Terms',
    intro: 'By submitting this form, you acknowledge and agree to the following terms:',
    items: {
      legitimateUse: {
        title: 'Legitimate Use:',
        description: 'API keys are provided for legitimate development, research, or business purposes only.'
      },
      providerTerms: {
        title: 'Provider Terms:',
        description: 'You agree to comply with the terms of service of the respective LLM provider (OpenAI, Anthropic, Google, etc.).'
      },
      security: {
        title: 'Security:',
        description: 'You are responsible for keeping your API keys secure and not sharing them with unauthorized parties.'
      },
      monitoring: {
        title: 'Usage Monitoring:',
        description: 'API usage may be monitored for compliance and security purposes.'
      },
      revocation: {
        title: 'Revocation:',
        description: 'We reserve the right to revoke access if terms are violated or suspicious activity is detected.'
      }
    },
    footer: 'For questions about these terms, please contact our support team.',
    button: 'I Understand'
  },
  aboutDialog: {
    title: 'About LLM Key Requestor',
    intro: 'LLM Key Requestor is a secure platform for managing API key requests for leading language model providers. Our streamlined process ensures quick and secure access to the AI tools you need.',
    supportedProviders: {
      title: 'Supported Providers',
      items: [
        'OpenAI (GPT-4, GPT-3.5)',
        'Anthropic (Claude 3, Claude 2)',
        'Google (Gemini Pro, PaLM 2)',
        'Meta (Llama 2)',
        'Mistral AI',
        'Cohere'
      ]
    },
    features: {
      title: 'Features',
      items: [
        'Fast approval process',
        'Enterprise-grade security',
        'Multiple provider support',
        'Secure email delivery',
        'Professional support'
      ]
    },
    footer: 'For technical support or questions, please contact our team.',
    button: 'Close'
  },
  footer: {
    title: 'LLM Key Requestor',
    description: 'Secure API key management for leading language model providers',
    backToTop: 'Back to Top',
    copyright: '© {year} LLM Key Requestor. Built with Vue.js and Vuetify.',
    about: 'About',
    providers: ['OpenAI', 'Anthropic', 'Google', 'Meta', 'Mistral', 'Cohere']
  },
  common: {
    step: 'Step',
    loading: 'Loading...',
    error: 'Error',
    success: 'Success',
    close: 'Close',
    cancel: 'Cancel',
    confirm: 'Confirm',
    save: 'Save'
  },
  language: {
    name: 'English',
    select: 'Select Language',
    de: 'German',
    en: 'English',
    es: 'Spanish'
  }
}
