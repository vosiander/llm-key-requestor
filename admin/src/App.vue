<template>
  <v-app>
    <LoginView v-if="!isAuthenticated" @login="handleLogin" />
    <template v-else>
      <AppHeader @logout="handleLogout" />
      <DashboardView />
    </template>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authService } from './services/auth'
import LoginView from './views/LoginView.vue'
import DashboardView from './views/DashboardView.vue'
import AppHeader from './components/AppHeader.vue'

const isAuthenticated = ref(false)

onMounted(() => {
  isAuthenticated.value = authService.isAuthenticated()
})

const handleLogin = () => {
  isAuthenticated.value = true
}

const handleLogout = () => {
  authService.logout()
  isAuthenticated.value = false
}
</script>

<style scoped>
/* Global styles can be added here */
</style>
