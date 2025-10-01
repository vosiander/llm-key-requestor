import { createI18n } from 'vue-i18n'
import de from '../locales/de.js'
import en from '../locales/en.js'
import es from '../locales/es.js'

// Get stored locale from localStorage or detect from browser
function getInitialLocale() {
  // First, check if user has previously selected a language
  const storedLocale = localStorage.getItem('user-locale')
  if (storedLocale && ['de', 'en', 'es'].includes(storedLocale)) {
    return storedLocale
  }

  // Second, try to detect from browser language
  const browserLocale = navigator.language.toLowerCase()
  
  // Check for exact match (e.g., 'de', 'en', 'es')
  if (['de', 'en', 'es'].includes(browserLocale)) {
    return browserLocale
  }
  
  // Check for language prefix (e.g., 'de-DE' -> 'de', 'en-US' -> 'en')
  const languagePrefix = browserLocale.split('-')[0]
  if (['de', 'en', 'es'].includes(languagePrefix)) {
    return languagePrefix
  }

  // Default to German if no match found
  return 'de'
}

const i18n = createI18n({
  legacy: false, // Use Composition API mode
  locale: getInitialLocale(), // Set initial locale
  fallbackLocale: 'de', // Fallback to German if translation is missing
  messages: {
    de,
    en,
    es
  },
  // Additional options
  globalInjection: true, // Inject $t into all components
  missingWarn: false, // Disable missing translation warnings in production
  fallbackWarn: false // Disable fallback warnings in production
})

export default i18n
