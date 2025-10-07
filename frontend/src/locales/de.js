export default {
  hero: {
    title: 'Optimieren Sie Ihren KI-Modell-Zugang',
    subtitle: 'Erhalten Sie sichere Zugangsschlüssel für führende KI-Modelle mit unserem einfachen, schnellen Genehmigungsverfahren. Verbinden Sie sich mit OpenAI, Anthropic, Google und mehr.',
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
      description: 'Zugang zu Schlüsseln für alle großen KI-Modell-Anbieter einschließlich OpenAI, Anthropic, Google, Meta und mehr.'
    },
      email: {
        title: 'E-Mail-Zustellung',
        description: 'Sichere Schlüsselzustellung direkt in Ihr Postfach mit detaillierten Einrichtungsanweisungen und Nutzungsrichtlinien.'
      }
    }
  },
  timeline: {
    title: 'So funktioniert es',
    subtitle: 'Erhalten Sie Ihren KI-Modell-Zugang in drei einfachen Schritten',
    steps: {
      step1: {
        title: 'Anfrage einreichen',
        description: 'Füllen Sie das Formular mit Ihrem bevorzugten KI-Modell und Ihrer E-Mail-Adresse aus. Wählen Sie aus OpenAI, Anthropic, Google und mehr.'
      },
      step2: {
        title: 'Admin-Genehmigung',
        description: 'Unser Team prüft und genehmigt Ihre Anfrage. Wir verifizieren Ihre Informationen und stellen die Einhaltung der Anbieterbestimmungen sicher.'
      },
      step3: {
        title: 'Zugang erhalten',
        description: 'Erhalten Sie Ihren Zugangsschlüssel sicher per E-Mail mit detaillierten Einrichtungsanweisungen und Nutzungsrichtlinien.'
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
    title: 'Fordern Sie Ihren Zugangsschlüssel an',
    subtitle: 'Wählen Sie ein KI-Modell für Ihre Anforderungen',
    featured: {
      title: 'Empfohlene Modelle',
      subtitle: 'Einfache Auswahl für häufige Anwendungsfälle',
      requestButton: 'Anfragen'
    },
    advanced: {
      title: 'Erweiterte Optionen',
      showButton: 'Erweiterte Optionen anzeigen',
      hideButton: 'Erweiterte Optionen ausblenden'
    },
    provider: {
      title: 'Alle verfügbaren Modelle',
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
      model: {
        label: 'KI-Modell',
        placeholder: 'z.B. OpenAI GPT-4, Claude 3, Gemini Pro, oder wählen Sie aus den Karten',
        tooltip: 'Wählen Sie eine Modellkarte oder geben Sie einen benutzerdefinierten Modellnamen ein'
      },
      email: {
        label: 'E-Mail-Adresse',
        placeholder: 'Geben Sie Ihre E-Mail-Adresse ein'
      }
    },
    validation: {
      modelRequired: 'Bitte wählen Sie ein KI-Modell aus',
      emailRequired: 'E-Mail-Adresse ist erforderlich',
      emailInvalid: 'Bitte geben Sie eine gültige E-Mail-Adresse ein'
    },
    terms: {
      label: 'Ich stimme den {terms} zu und verstehe, dass Zugangsschlüssel den Nutzungsbedingungen des Anbieters unterliegen.',
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
      successMessage: 'Ihre Anfrage wurde erfolgreich übermittelt. Sie erhalten eine Benachrichtigung per E-Mail, sobald Ihr Zugangsschlüssel bereit ist.',
      errorTitle: 'Anfrage fehlgeschlagen',
      errorMessage: 'Beim Verarbeiten Ihrer Anfrage ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.',
      closeButton: 'Schließen'
    }
  },
  termsDialog: {
    title: 'Geschäftsbedingungen',
    heading: 'Bedingungen für Zugangsschlüssel-Anfragen',
    intro: 'Durch das Absenden dieses Formulars erkennen Sie die folgenden Bedingungen an und stimmen ihnen zu:',
    items: {
      legitimateUse: {
        title: 'Legitime Nutzung:',
        description: 'Zugangsschlüssel werden nur für legitime Entwicklungs-, Forschungs- oder Geschäftszwecke bereitgestellt.'
      },
      providerTerms: {
        title: 'Anbieterbestimmungen:',
        description: 'Sie verpflichten sich, die Nutzungsbedingungen des jeweiligen Modell-Anbieters (OpenAI, Anthropic, Google usw.) einzuhalten.'
      },
      security: {
        title: 'Sicherheit:',
        description: 'Sie sind dafür verantwortlich, Ihre Zugangsschlüssel sicher aufzubewahren und sie nicht an unbefugte Personen weiterzugeben.'
      },
      monitoring: {
        title: 'Nutzungsüberwachung:',
        description: 'Die Nutzung kann zu Compliance- und Sicherheitszwecken überwacht werden.'
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
    title: 'Über KI-Modell Zugangsportal',
    intro: 'Das KI-Modell Zugangsportal ist eine sichere Plattform zur Verwaltung von Zugangsschlüssel-Anfragen für führende KI-Modellanbieter. Unser optimierter Prozess gewährleistet schnellen und sicheren Zugang zu den KI-Tools, die Sie benötigen.',
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
    title: 'KI-Modell Zugangsportal',
    description: 'Sichere Zugangsschlüsselverwaltung für führende KI-Modellanbieter',
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
