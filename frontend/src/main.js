import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify.js'
import i18n from './plugins/i18n.js'
import './assets/main.css'

const app = createApp(App)

// Disable Vue devtools in production
app.config.devtools = false

// Use plugins
app.use(vuetify)
app.use(i18n)

// Mount the app
app.mount('#app')
