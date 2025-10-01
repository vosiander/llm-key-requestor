import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify.js'
import './assets/main.css'

const app = createApp(App)

// Disable Vue devtools in production
app.config.devtools = false

// Use Vuetify plugin
app.use(vuetify)

// Mount the app
app.mount('#app')
