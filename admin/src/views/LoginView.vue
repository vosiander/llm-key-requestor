<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="12">
          <v-card-title class="text-h5 text-center pa-6 bg-primary">
            <v-icon icon="mdi-shield-lock" size="large" class="mr-2"></v-icon>
            Admin Login
          </v-card-title>
          
          <v-card-text class="pa-6">
            <v-form @submit.prevent="handleSubmit" ref="formRef">
              <v-text-field
                v-model="username"
                label="Username"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                :rules="[rules.required]"
                :disabled="loading"
                class="mb-3"
              ></v-text-field>
              
              <v-text-field
                v-model="password"
                label="Password"
                type="password"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                :rules="[rules.required]"
                :disabled="loading"
                class="mb-3"
              ></v-text-field>

              <v-alert
                v-if="error"
                type="error"
                variant="tonal"
                class="mb-4"
              >
                {{ error }}
              </v-alert>

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
              >
                Login
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { authService } from '@/services/auth'

const emit = defineEmits(['login'])

const formRef = ref(null)
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const rules = {
  required: value => !!value || 'This field is required'
}

const handleSubmit = async () => {
  const { valid } = await formRef.value.validate()
  
  if (!valid) return

  error.value = ''
  loading.value = true

  try {
    const success = await authService.login(username.value, password.value)
    
    if (success) {
      emit('login')
    } else {
      error.value = 'Invalid username or password'
    }
  } catch (err) {
    error.value = 'Login failed. Please try again.'
    console.error('Login error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
