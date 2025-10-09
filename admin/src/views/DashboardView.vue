<template>
  <v-main>
    <v-container fluid>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title class="d-flex align-center">
              <span class="text-h5">Key Requests Dashboard</span>
              <v-spacer></v-spacer>
              <v-btn
                icon="mdi-refresh"
                @click="loadRequests"
                :loading="loading"
                title="Refresh"
              ></v-btn>
            </v-card-title>

            <v-card-text>
              <v-tabs v-model="currentFilter" class="mb-4">
                <v-tab value="pending">
                  <v-icon icon="mdi-clock-outline" class="mr-2"></v-icon>
                  Pending
                  <v-chip v-if="stats.pending > 0" size="small" class="ml-2">
                    {{ stats.pending }}
                  </v-chip>
                </v-tab>
                <v-tab value="review">
                  <v-icon icon="mdi-eye-outline" class="mr-2"></v-icon>
                  In Review
                  <v-chip v-if="stats.review > 0" size="small" class="ml-2">
                    {{ stats.review }}
                  </v-chip>
                </v-tab>
                <v-tab value="all">
                  <v-icon icon="mdi-format-list-bulleted" class="mr-2"></v-icon>
                  All Requests
                </v-tab>
              </v-tabs>

              <RequestsTable
                :requests="requests"
                :loading="loading"
                @view-details="handleViewDetails"
                @approve="handleApprove"
                @deny="handleDeny"
                @refresh="loadRequests"
              />
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <RequestDetailDialog
      v-model="detailDialog"
      :request="selectedRequest"
      @approve="handleApprove"
      @deny="handleDeny"
    />

    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
    >
      {{ snackbar.message }}
    </v-snackbar>
  </v-main>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { apiService } from '@/services/api'
import RequestsTable from '@/components/RequestsTable.vue'
import RequestDetailDialog from '@/components/RequestDetailDialog.vue'

const currentFilter = ref('pending')
const requests = ref([])
const loading = ref(false)
const detailDialog = ref(false)
const selectedRequest = ref(null)

const snackbar = ref({
  show: false,
  message: '',
  color: 'success'
})

const stats = computed(() => {
  return {
    pending: requests.value.filter(r => r.state === 'pending').length,
    review: requests.value.filter(r => r.state === 'in-review').length,
    total: requests.value.length
  }
})

watch(currentFilter, () => {
  loadRequests()
})

onMounted(() => {
  loadRequests()
})

const loadRequests = async () => {
  loading.value = true
  try {
    requests.value = await apiService.fetchRequests(currentFilter.value)
  } catch (error) {
    showSnackbar('Failed to load requests', 'error')
    console.error('Load requests error:', error)
  } finally {
    loading.value = false
  }
}

const handleViewDetails = (request) => {
  selectedRequest.value = request
  detailDialog.value = true
}

const handleApprove = async (requestId) => {
  try {
    await apiService.approveRequest(requestId)
    showSnackbar('Request approved successfully', 'success')
    detailDialog.value = false
    await loadRequests()
  } catch (error) {
    showSnackbar('Failed to approve request', 'error')
    console.error('Approve error:', error)
  }
}

const handleDeny = async ({ requestId, reason }) => {
  try {
    await apiService.denyRequest(requestId, reason)
    showSnackbar('Request denied successfully', 'success')
    detailDialog.value = false
    await loadRequests()
  } catch (error) {
    showSnackbar('Failed to deny request', 'error')
    console.error('Deny error:', error)
  }
}

const showSnackbar = (message, color = 'success') => {
  snackbar.value = {
    show: true,
    message,
    color
  }
}
</script>
