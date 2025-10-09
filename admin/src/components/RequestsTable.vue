<template>
  <v-data-table
    :headers="headers"
    :items="requests"
    :loading="loading"
    item-value="request_id"
    class="elevation-1"
  >
    <template v-slot:item.state="{ item }">
      <v-chip
        :color="getStateColor(item.state)"
        size="small"
      >
        {{ formatState(item.state) }}
      </v-chip>
    </template>

    <template v-slot:item.created_at="{ item }">
      {{ formatDate(item.created_at) }}
    </template>

    <template v-slot:item.actions="{ item }">
      <v-btn
        icon="mdi-eye"
        size="small"
        variant="text"
        @click="$emit('view-details', item)"
        title="View Details"
      ></v-btn>
      
      <v-btn
        v-if="item.state === 'pending' || item.state === 'in-review'"
        icon="mdi-check"
        size="small"
        variant="text"
        color="success"
        @click="$emit('approve', item.request_id)"
        title="Approve"
      ></v-btn>
      
      <v-btn
        v-if="item.state === 'pending' || item.state === 'in-review'"
        icon="mdi-close"
        size="small"
        variant="text"
        color="error"
        @click="handleDenyClick(item)"
        title="Deny"
      ></v-btn>
    </template>

    <template v-slot:no-data>
      <v-alert type="info" variant="tonal" class="ma-4">
        No requests found
      </v-alert>
    </template>
  </v-data-table>

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
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  requests: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['view-details', 'approve', 'deny', 'refresh'])

const headers = [
  { title: 'Request ID', value: 'request_id', sortable: true },
  { title: 'Email', value: 'email', sortable: true },
  { title: 'Model', value: 'model', sortable: true },
  { title: 'State', value: 'state', sortable: true },
  { title: 'Created At', value: 'created_at', sortable: true },
  { title: 'Actions', value: 'actions', sortable: false, align: 'center' }
]

const denyDialog = ref(false)
const denyReason = ref('')
const selectedRequestId = ref(null)

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

const handleDenyClick = (item) => {
  selectedRequestId.value = item.request_id
  denyReason.value = ''
  denyDialog.value = true
}

const confirmDeny = () => {
  emit('deny', {
    requestId: selectedRequestId.value,
    reason: denyReason.value
  })
  denyDialog.value = false
}
</script>
