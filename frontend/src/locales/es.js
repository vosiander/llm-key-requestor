export default {
  hero: {
    title: 'Optimice su Acceso a Modelos de IA',
    subtitle: 'Obtenga claves de acceso seguras para los principales modelos de IA con nuestro proceso de aprobación simple y rápido. Conéctese con OpenAI, Anthropic, Google y más.',
    cta: 'Solicite su Clave',
    benefitsTitle: '¿Por qué elegir nuestra plataforma?',
    benefitsSubtitle: 'Gestión profesional de claves API simplificada',
    benefits: {
      fast: {
        title: 'Aprobación Rápida',
        description: 'Obtenga sus claves API rápidamente con nuestro proceso de aprobación optimizado. La mayoría de las solicitudes se procesan en 24 horas.'
      },
      secure: {
        title: 'Acceso Seguro',
        description: 'Seguridad de nivel empresarial con entrega de claves cifradas y protocolos seguros de gestión de acceso.'
      },
      multiple: {
        title: 'Múltiples Proveedores',
        description: 'Acceso a claves para todos los principales proveedores de modelos de IA, incluyendo OpenAI, Anthropic, Google, Meta y más.'
      },
      email: {
        title: 'Entrega por Email',
        description: 'Entrega segura de claves directamente a su bandeja de entrada con instrucciones detalladas de configuración y pautas de uso.'
      }
    }
  },
  timeline: {
    title: 'Cómo Funciona',
    subtitle: 'Obtenga su acceso a modelos de IA en tres simples pasos',
    steps: {
      step1: {
        title: 'Enviar Solicitud',
        description: 'Complete el formulario con su modelo de IA preferido y dirección de correo electrónico. Elija entre OpenAI, Anthropic, Google y más.'
      },
      step2: {
        title: 'Aprobación del Admin',
        description: 'Nuestro equipo revisa y aprueba su solicitud. Verificamos su información y garantizamos el cumplimiento de los términos del proveedor.'
      },
      step3: {
        title: 'Recibir Acceso',
        description: 'Reciba su clave de acceso de forma segura por correo electrónico con instrucciones detalladas de configuración y pautas de uso.'
      }
    },
    status: {
      complete: 'Completado',
      current: 'Actual',
      pending: 'Pendiente'
    },
    cta: {
      title: '¿Listo para comenzar?',
      button: 'Inicie su Solicitud'
    }
  },
  form: {
    title: 'Solicite su Clave de Acceso',
    subtitle: 'Elija un modelo de IA para sus necesidades',
    featured: {
      title: 'Modelos Recomendados',
      subtitle: 'Selección fácil para casos de uso comunes',
      requestButton: 'Solicitar'
    },
    advanced: {
      title: 'Opciones Avanzadas',
      showButton: 'Mostrar Opciones Avanzadas',
      hideButton: 'Ocultar Opciones Avanzadas'
    },
    provider: {
      title: 'Todos los Modelos Disponibles',
      retry: 'Reintentar',
      loading: 'Cargando modelos disponibles...',
      error: 'Error al Cargar Modelos',
      models: {
        openai: {
          title: 'OpenAI',
          description: 'GPT-4, GPT-3.5 y más'
        },
        anthropic: {
          title: 'Anthropic',
          description: 'Claude 3 y Claude 2'
        },
        google: {
          title: 'Google',
          description: 'Gemini Pro y PaLM 2'
        },
        meta: {
          title: 'Meta',
          description: 'Modelos Llama 2'
        },
        mistral: {
          title: 'Mistral AI',
          description: 'Modelos Mistral'
        },
        cohere: {
          title: 'Cohere',
          description: 'Command y Embed'
        }
      }
    },
    fields: {
      model: {
        label: 'Modelo de IA',
        placeholder: 'ej., OpenAI GPT-4, Claude 3, Gemini Pro, o seleccione de las tarjetas',
        tooltip: 'Seleccione una tarjeta de modelo o ingrese cualquier nombre de modelo personalizado'
      },
      email: {
        label: 'Dirección de Email',
        placeholder: 'Ingrese su dirección de correo electrónico'
      }
    },
    validation: {
      modelRequired: 'Por favor seleccione un modelo de IA',
      emailRequired: 'La dirección de correo electrónico es obligatoria',
      emailInvalid: 'Por favor ingrese una dirección de correo electrónico válida'
    },
    terms: {
      label: 'Acepto los {terms} y entiendo que las claves de acceso están sujetas a los términos de servicio del proveedor.',
      link: 'Términos y Condiciones',
      required: 'Debe aceptar los términos y condiciones'
    },
    buttons: {
      submit: 'Enviar Solicitud',
      submitting: 'Enviando Solicitud...',
      reset: 'Restablecer Formulario'
    },
    security: {
      encrypted: 'Su información está segura y cifrada',
      processing: 'La mayoría de las solicitudes se procesan en 24 horas'
    },
    messages: {
      successTitle: '¡Solicitud Enviada Exitosamente!',
      successMessage: 'Su solicitud ha sido enviada exitosamente. Recibirá una notificación por correo electrónico una vez que su clave de acceso esté lista.',
      errorTitle: 'Solicitud Fallida',
      errorMessage: 'Ocurrió un error al procesar su solicitud. Por favor, intente nuevamente más tarde.',
      closeButton: 'Cerrar'
    }
  },
  termsDialog: {
    title: 'Términos y Condiciones',
    heading: 'Términos de Solicitud de Clave de Acceso',
    intro: 'Al enviar este formulario, usted reconoce y acepta los siguientes términos:',
    items: {
      legitimateUse: {
        title: 'Uso Legítimo:',
        description: 'Las claves de acceso se proporcionan solo para fines legítimos de desarrollo, investigación o negocios.'
      },
      providerTerms: {
        title: 'Términos del Proveedor:',
        description: 'Usted acepta cumplir con los términos de servicio del respectivo proveedor de modelos (OpenAI, Anthropic, Google, etc.).'
      },
      security: {
        title: 'Seguridad:',
        description: 'Usted es responsable de mantener seguras sus claves de acceso y no compartirlas con partes no autorizadas.'
      },
      monitoring: {
        title: 'Monitoreo de Uso:',
        description: 'El uso puede ser monitoreado con fines de cumplimiento y seguridad.'
      },
      revocation: {
        title: 'Revocación:',
        description: 'Nos reservamos el derecho de revocar el acceso si se violan los términos o se detecta actividad sospechosa.'
      }
    },
    footer: 'Para preguntas sobre estos términos, por favor contacte a nuestro equipo de soporte.',
    button: 'Entiendo'
  },
  aboutDialog: {
    title: 'Acerca del Portal de Acceso a Modelos de IA',
    intro: 'El Portal de Acceso a Modelos de IA es una plataforma segura para gestionar solicitudes de claves de acceso para los principales proveedores de modelos de IA. Nuestro proceso optimizado garantiza un acceso rápido y seguro a las herramientas de IA que necesita.',
    supportedProviders: {
      title: 'Proveedores Soportados',
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
      title: 'Características',
      items: [
        'Proceso de aprobación rápido',
        'Seguridad de nivel empresarial',
        'Soporte de múltiples proveedores',
        'Entrega segura por correo electrónico',
        'Soporte profesional'
      ]
    },
    footer: 'Para soporte técnico o preguntas, por favor contacte a nuestro equipo.',
    button: 'Cerrar'
  },
  footer: {
    title: 'Portal de Acceso a Modelos de IA',
    description: 'Gestión segura de claves de acceso para los principales proveedores de modelos de IA',
    backToTop: 'Volver Arriba',
    copyright: '© {year} LLM Key Requestor. Construido con Vue.js y Vuetify.',
    about: 'Acerca de',
    providers: ['OpenAI', 'Anthropic', 'Google', 'Meta', 'Mistral', 'Cohere']
  },
  common: {
    step: 'Paso',
    loading: 'Cargando...',
    error: 'Error',
    success: 'Éxito',
    close: 'Cerrar',
    cancel: 'Cancelar',
    confirm: 'Confirmar',
    save: 'Guardar'
  },
  language: {
    name: 'Español',
    select: 'Seleccionar Idioma',
    de: 'Alemán',
    en: 'Inglés',
    es: 'Español'
  }
}
