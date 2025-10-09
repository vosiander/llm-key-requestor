<template>
  <v-app-bar color="primary" elevation="4">
    <v-app-bar-title>
      <v-icon icon="mdi-key-variant" class="mr-2"></v-icon>
      LLM Key Requestor - Admin
    </v-app-bar-title>

    <v-spacer></v-spacer>

    <div class="d-flex align-center mr-4">
      <v-icon icon="mdi-account-circle" class="mr-2"></v-icon>
      <span class="text-body-1">{{ username }}</span>
    </div>

    <v-btn
      icon="mdi-logout"
      @click="handleLogout"
      title="Logout"
    ></v-btn>
  </v-app-bar>
</template>

<script setup>
import { computed } from 'vue'
import { authService } from '@/services/auth'

const emit = defineEmits(['logout'])

const username = computed(() => {
  const creds = authService.getCredentials()
  return creds?.username || 'Admin'
})

const handleLogout = () => {
  if (confirm('Are you sure you want to logout?')) {
    emit('logout')
  }
}
</script>
