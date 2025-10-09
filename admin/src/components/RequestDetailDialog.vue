<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" max-width="700">
    <v-card v-if="request">
      <v-card-title class="d-flex align-center bg-primary">
        <v-icon icon="mdi-file-document-outline" class="mr-2"></v-icon>
        Request Details
        <v-spacer></v-spacer>
        <v-btn
          icon="mdi-close"
          variant="text"
          @click="$emit('update:modelValue', false)"
        ></v-btn>
      </v-card-title>

      <v-card-text class="pt-4">
        <v-row>
          <v-col cols="12" md="6">
            <div class="text-subtitle-2 text-grey-darken-1 mb-1">Request ID</div>
            <div class="text-body-1 mb-3">{{ request.request_id }}</div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="text-subtitle-2 text-grey-darken-1 mb-1">Status</div>
            <v-chip :color="getStateColor(request.state)" size="small">
              {{ formatState(request.state) }}
            </v-chip>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="6">
            <div class="text-subtitle-2 text-grey-darken-1 mb-1">Email</div>
            <div class="text-body-1 mb-3">{{ request.email }}</div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="text-subtitle-2 text-grey-darken-1 mb-1">Model</div>
            <div class="text-body-1 mb-3">{{ request.model }}</div>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="6">
            <div class="text-subtitle-2 text-grey-darken-1 mb-1">Created At</div>
            <div class="text-body-1 mb-3">{{ formatDate(request.created_at) }}</div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="text-subtitle-2 text-grey-darken-1 mb-1">Updated At</div>
            <div class="text-body-1 mb-3">{{ formatDate(request.updated_at) }}</div>
          </v-col>
        </v-row>

        <v-row v-if="request.api_key">
          <v-col cols="12">
            <div class="text-subtitle-2 text-grey-darken-1 mb-1">API Key</div>
            <v-text-field
              :model-value="request.api_key"
              readonly
              variant="outlined"
              density="compact"
              append-inner-icon="mdi-content-copy"
              @click:append-inner="copyToClipboard(request.api_key)"
            ></v-text-field>
          </v-col>
        </v-row>

        <v-divider class="my-4"></v-divider>

        <div v-if="request.state === 'pending' || request.state === 'in-review'" class="d-flex justify-end ga-2">
          <v-btn
            color="error"
            variant="outlined"
            prepend-icon="mdi-close"
            @click="handleDenyClick"
          >
            Deny
          </v-btn>
          <v-btn
            color="success"
            variant="elevated"
            prepend-icon="mdi-check"
            @click="$emit('approve', request.request_id)"
          >
            Approve
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>

  <v-dialog v-model="denyDialog" max-width="500">
    <v-card>
      <v-card-title>Deny Request</v-card-title>
      <v-card-text>
        <v-textarea
          v-model="denyReason"
          label="Reason for denial"
          rows="3"
          variant="outlined"
          placeholder="Please provide a reason for denying this request..."
        ></v-textarea>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="denyDialog = false">Cancel</v-btn>
        <v-btn
          color="error"
          @click="confirmDeny"
          :disabled="!denyReason.trim()"
        >
          Deny Request
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-snackbar v-model="copySnackbar" color="success" :timeout="2000">
    API key copied to clipboard
  </v-snackbar>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  request: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'approve', 'deny'])

const denyDialog = ref(false)
const denyReason = ref('')
const copySnackbar = ref(false)

const getStateColor = (state) => {
  const colors = {
    'pending': 'warning',
    'in-review': 'info',
    'approved': 'success',
    'denied': 'error'
  }
  return colors[state] || 'grey'
}

const formatState = (state) => {
  return state.split('-').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleString()
}

const handleDenyClick = () => {
  denyReason.value = ''
  denyDialog.value = true
}

const confirmDeny = () => {
  emit('deny', {
    requestId: props.request.request_id,
    reason: denyReason.value
  })
  denyDialog.value = false
}

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    copySnackbar.value = true
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}
</script>
