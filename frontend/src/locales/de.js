export default {
  hero: {
    title: 'Optimieren Sie Ihren LLM-API-Zugang',
    subtitle: 'Erhalten Sie sichere API-Schlüssel für führende Sprachmodelle mit unserem einfachen, schnellen Genehmigungsverfahren. Verbinden Sie sich mit OpenAI, Anthropic, Google und mehr.',
    cta: 'Fordern Sie Ihren Schlüssel an',
    benefitsTitle: 'Warum unsere Plattform wählen?',
    benefitsSubtitle: 'Professionelles API-Schlüsselmanagement leicht gemacht',
    benefits: {
      fast: {
        title: 'Schnelle Genehmigung',
        description: 'Erhalten Sie Ihre API-Schlüssel schnell mit unserem optimierten Genehmigungsverfahren. Die meisten Anfragen werden innerhalb von 24 Stunden bearbeitet.'
      },
      secure: {
        title: 'Sicherer Zugang',
        description: 'Sicherheit auf Unternehmensniveau mit verschlüsselter Schlüsselzustellung und sicheren Zugriffsverwaltungsprotokollen.'
      },
      multiple: {
        title: 'Mehrere Anbieter',
        description: 'Zugang zu Schlüsseln für alle großen LLM-Anbieter einschließlich OpenAI, Anthropic, Google, Meta und mehr.'
      },
      email: {
        title: 'E-Mail-Zustellung',
        description: 'Sichere Schlüsselzustellung direkt in Ihr Postfach mit detaillierten Einrichtungsanweisungen und Nutzungsrichtlinien.'
      }
    }
  },
  timeline: {
    title: 'So funktioniert es',
    subtitle: 'Erhalten Sie Ihren LLM-API-Schlüssel in drei einfachen Schritten',
    steps: {
      step1: {
        title: 'Anfrage einreichen',
        description: 'Füllen Sie das Formular mit Ihrem bevorzugten LLM-Anbieter und Ihrer E-Mail-Adresse aus. Wählen Sie aus OpenAI, Anthropic, Google und mehr.'
      },
      step2: {
        title: 'Admin-Genehmigung',
        description: 'Unser Team prüft und genehmigt Ihre Anfrage. Wir verifizieren Ihre Informationen und stellen die Einhaltung der Anbieterbestimmungen sicher.'
      },
      step3: {
        title: 'Schlüssel erhalten',
        description: 'Erhalten Sie Ihren API-Schlüssel sicher per E-Mail mit detaillierten Einrichtungsanweisungen und Nutzungsrichtlinien.'
      }
    },
    status: {
      complete: 'Abgeschlossen',
      current: 'Aktuell',
      pending: 'Ausstehend'
    },
    cta: {
      title: 'Bereit loszulegen?',
      button: 'Starten Sie Ihre Anfrage'
    }
  },
  form: {
    title: 'Fordern Sie Ihren API-Schlüssel an',
    subtitle: 'Füllen Sie das folgende Formular aus, um Zugang zu Ihrem bevorzugten LLM-Anbieter zu erhalten',
    provider: {
      title: 'Wählen Sie Ihren LLM-Anbieter',
      retry: 'Erneut versuchen',
      loading: 'Verfügbare Modelle werden geladen...',
      error: 'Fehler beim Laden der Modelle',
      models: {
        openai: {
          title: 'OpenAI',
          description: 'GPT-4, GPT-3.5 und mehr'
        },
        anthropic: {
          title: 'Anthropic',
          description: 'Claude 3 und Claude 2'
        },
        google: {
          title: 'Google',
          description: 'Gemini Pro und PaLM 2'
        },
        meta: {
          title: 'Meta',
          description: 'Llama 2 Modelle'
        },
        mistral: {
          title: 'Mistral AI',
          description: 'Mistral Modelle'
        },
        cohere: {
          title: 'Cohere',
          description: 'Command und Embed'
        }
      }
    },
    fields: {
      llm: {
        label: 'LLM-Modell',
        placeholder: 'z.B. OpenAI GPT-5, Claude 4, Gemini Ultra, oder wählen Sie aus den Karten oben',
        tooltip: 'Wählen Sie eine Modellkarte oben oder geben Sie einen benutzerdefinierten Modellnamen ein'
      },
      email: {
        label: 'E-Mail-Adresse',
        placeholder: 'Geben Sie Ihre E-Mail-Adresse ein'
      }
    },
    validation: {
      llmRequired: 'Bitte wählen Sie ein LLM-Modell aus',
      emailRequired: 'E-Mail-Adresse ist erforderlich',
      emailInvalid: 'Bitte geben Sie eine gültige E-Mail-Adresse ein'
    },
    terms: {
      label: 'Ich stimme den {terms} zu und verstehe, dass API-Schlüssel den Nutzungsbedingungen des Anbieters unterliegen.',
      link: 'Geschäftsbedingungen',
      required: 'Sie müssen den Geschäftsbedingungen zustimmen'
    },
    buttons: {
      submit: 'Anfrage absenden',
      submitting: 'Anfrage wird gesendet...',
      reset: 'Formular zurücksetzen'
    },
    security: {
      encrypted: 'Ihre Informationen sind sicher und verschlüsselt',
      processing: 'Die meisten Anfragen werden innerhalb von 24 Stunden bearbeitet'
    },
    messages: {
      successTitle: 'Anfrage erfolgreich gesendet!',
      errorTitle: 'Anfrage fehlgeschlagen',
      defaultSuccess: 'Ihre Anfrage wurde erfolgreich gesendet. Sie erhalten bald eine E-Mail.'
    }
  },
  termsDialog: {
    title: 'Geschäftsbedingungen',
    heading: 'Bedingungen für API-Schlüsselanfragen',
    intro: 'Durch das Absenden dieses Formulars erkennen Sie die folgenden Bedingungen an und stimmen ihnen zu:',
    items: {
      legitimateUse: {
        title: 'Legitime Nutzung:',
        description: 'API-Schlüssel werden nur für legitime Entwicklungs-, Forschungs- oder Geschäftszwecke bereitgestellt.'
      },
      providerTerms: {
        title: 'Anbieterbestimmungen:',
        description: 'Sie verpflichten sich, die Nutzungsbedingungen des jeweiligen LLM-Anbieters (OpenAI, Anthropic, Google usw.) einzuhalten.'
      },
      security: {
        title: 'Sicherheit:',
        description: 'Sie sind dafür verantwortlich, Ihre API-Schlüssel sicher aufzubewahren und sie nicht an unbefugte Personen weiterzugeben.'
      },
      monitoring: {
        title: 'Nutzungsüberwachung:',
        description: 'Die API-Nutzung kann zu Compliance- und Sicherheitszwecken überwacht werden.'
      },
      revocation: {
        title: 'Widerruf:',
        description: 'Wir behalten uns das Recht vor, den Zugang zu widerrufen, wenn die Bedingungen verletzt werden oder verdächtige Aktivitäten festgestellt werden.'
      }
    },
    footer: 'Bei Fragen zu diesen Bedingungen wenden Sie sich bitte an unser Support-Team.',
    button: 'Ich verstehe'
  },
  aboutDialog: {
    title: 'Über LLM Key Requestor',
    intro: 'LLM Key Requestor ist eine sichere Plattform zur Verwaltung von API-Schlüsselanfragen für führende Sprachmodellanbieter. Unser optimierter Prozess gewährleistet schnellen und sicheren Zugang zu den KI-Tools, die Sie benötigen.',
    supportedProviders: {
      title: 'Unterstützte Anbieter',
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
      title: 'Funktionen',
      items: [
        'Schneller Genehmigungsprozess',
        'Sicherheit auf Unternehmensniveau',
        'Unterstützung mehrerer Anbieter',
        'Sichere E-Mail-Zustellung',
        'Professioneller Support'
      ]
    },
    footer: 'Für technischen Support oder Fragen wenden Sie sich bitte an unser Team.',
    button: 'Schließen'
  },
  footer: {
    title: 'LLM Key Requestor',
    description: 'Sichere API-Schlüsselverwaltung für führende Sprachmodellanbieter',
    backToTop: 'Zurück nach oben',
    copyright: '© {year} LLM Key Requestor. Erstellt mit Vue.js und Vuetify.',
    about: 'Über',
    providers: ['OpenAI', 'Anthropic', 'Google', 'Meta', 'Mistral', 'Cohere']
  },
  common: {
    step: 'Schritt',
    loading: 'Wird geladen...',
    error: 'Fehler',
    success: 'Erfolg',
    close: 'Schließen',
    cancel: 'Abbrechen',
    confirm: 'Bestätigen',
    save: 'Speichern'
  },
  language: {
    name: 'Deutsch',
    select: 'Sprache wählen',
    de: 'Deutsch',
    en: 'Englisch',
    es: 'Spanisch'
  }
}
