<template>
  <div class="language-switcher">
    <v-menu offset-y>
      <template #activator="{ props }">
        <v-btn
          v-bind="props"
          variant="outlined"
          size="small"
          class="language-btn"
        >
          <v-icon start size="20">mdi-translate</v-icon>
          {{ currentLanguageName }}
          <v-icon end size="20">mdi-chevron-down</v-icon>
        </v-btn>
      </template>

      <v-list density="compact">
        <v-list-item
          v-for="lang in languages"
          :key="lang.code"
          :active="currentLocale === lang.code"
          @click="changeLanguage(lang.code)"
        >
          <template #prepend>
            <v-icon :color="currentLocale === lang.code ? 'primary' : ''">
              {{ currentLocale === lang.code ? 'mdi-check-circle' : 'mdi-circle-outline' }}
            </v-icon>
          </template>
          
          <v-list-item-title>
            {{ lang.flag }} {{ lang.name }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script>
import { useI18n } from 'vue-i18n'
import { useLocale } from 'vuetify'
import { computed } from 'vue'

export default {
  name: 'LanguageSwitcher',
  setup() {
    const { locale, t } = useI18n()
    const { current: vuetifyLocale } = useLocale()

    const languages = [
      { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
      { code: 'en', name: 'English', flag: '🇬🇧' },
      { code: 'es', name: 'Español', flag: '🇪🇸' }
    ]

    const currentLocale = computed(() => locale.value)

    const currentLanguageName = computed(() => {
      const currentLang = languages.find(lang => lang.code === currentLocale.value)
      return currentLang ? `${currentLang.flag} ${currentLang.name}` : ''
    })

    const changeLanguage = (langCode) => {
      // Update Vue I18n locale
      locale.value = langCode
      
      // Update Vuetify locale
      vuetifyLocale.value = langCode
      
      // Store the selected language in localStorage for persistence
      localStorage.setItem('user-locale', langCode)
      
      // Update document language attribute for accessibility
      document.documentElement.setAttribute('lang', langCode)
      
      // Optional: Emit event for parent components
      console.log(`Language changed to: ${langCode}`)
    }

    // Set initial document language
    document.documentElement.setAttribute('lang', currentLocale.value)

    return {
      languages,
      currentLocale,
      currentLanguageName,
      changeLanguage
    }
  }
}
</script>

<style scoped>
.language-switcher {
  display: inline-block;
}

.language-btn {
  text-transform: none;
  font-weight: 500;
}

/* Ensure flags display properly */
:deep(.v-list-item-title) {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
