<template>
  <q-page padding>
    <q-card flat bordered>
      <q-card-section>
        <div class="text-h6">Clients</div>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <q-table
          :rows="rows"
          :columns="columns"
          row-key="id"
          :loading="loading"
          no-data-label="No clients found"
        />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'src/boot/axios'

const loading = ref(false)
const rows = ref([])

const columns = [
  {
    name: 'id',
    label: 'ID',
    field: 'id',
    align: 'left'
  },
  {
    name: 'name',
    label: 'Name',
    field: 'name',
    align: 'left'
  },
  {
    name: 'phone',
    label: 'Phone',
    field: 'phone',
    align: 'left'
  },
  {
    name: 'email',
    label: 'Email',
    field: 'email',
    align: 'left'
  }
]

const loadClients = async () => {
  loading.value = true
  try {
    const res = await api.get('/clients')
    rows.value = res.data
  } catch {
    rows.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadClients()
})
</script>
