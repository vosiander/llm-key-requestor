<script setup>
import { ref } from 'vue'

const llmProviders = [
  'OpenAI (GPT-4)',
  'Anthropic (Claude)',
  'Google (Gemini)',
  'Meta (Llama)',
  'Mistral AI',
  'Cohere'
]

const selectedLlm = ref('')
const email = ref('')
const isSubmitting = ref(false)
const message = ref('')

const submitRequest = async () => {
  if (!selectedLlm.value || !email.value) {
    message.value = 'Please select an LLM provider and enter your email'
    return
  }

  isSubmitting.value = true
  message.value = ''

  try {
    // TODO: Replace with actual API endpoint
    const response = await fetch('/api/request-key', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        llm: selectedLlm.value,
        email: email.value,
      }),
    })

    if (response.ok) {
      message.value = 'Request submitted successfully! Check your email for the access key.'
      selectedLlm.value = ''
      email.value = ''
    } else {
      message.value = 'Failed to submit request. Please try again.'
    }
  } catch (error) {
    console.error('Error submitting request:', error)
    message.value = 'An error occurred. Please try again later.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-lg shadow-xl p-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2 text-center">LLM Key Requestor</h1>
      <p class="text-gray-600 mb-6 text-center">Request access to your preferred LLM service</p>

      <form @submit.prevent="submitRequest" class="space-y-6">
        <div>
          <label for="llm" class="block text-sm font-medium text-gray-700 mb-2">
            Select LLM Provider
          </label>
          <select
            id="llm"
            v-model="selectedLlm"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            required
          >
            <option value="" disabled>Choose a provider</option>
            <option v-for="provider in llmProviders" :key="provider" :value="provider">
              {{ provider }}
            </option>
          </select>
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
            Email Address
          </label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="your.email@example.com"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            required
          />
        </div>

        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {{ isSubmitting ? 'Submitting...' : 'Request Access Key' }}
        </button>

        <div v-if="message" class="mt-4 p-3 rounded-md" :class="{
          'bg-green-50 text-green-800': message.includes('successfully'),
          'bg-red-50 text-red-800': !message.includes('successfully')
        }">
          {{ message }}
        </div>
      </form>

      <div class="mt-6 text-center text-sm text-gray-500">
        <p>Your access key will be sent to your email address</p>
      </div>
    </div>
  </div>
</template>

