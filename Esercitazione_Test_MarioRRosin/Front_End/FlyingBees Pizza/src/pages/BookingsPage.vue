<template>
  <q-page class="q-pa-lg">
    <!-- Header -->
    <div class="row items-center q-col-gutter-md">
      <div class="col">
        <div class="text-h5 text-weight-bold">Bookings</div>
        <div class="text-grey-7">Create and manage reservations</div>
      </div>

      <div class = "col-auto">
        <q-btn
          color = "primary"
          icon = "add"
          label = "New booking"
          unelevated
          @click = "openCreate"
        />
      </div>
    </div>

    <!-- Table -->
    <q-card class="q-mt-md" bordered>
      <q-card-section>
        <q-table
          :rows="rows"
          :columns="columns"
          row-key="id"
          :loading="loading"
          flat
        >
          <template #body-cell-status="props">
            <q-td :props="props">
              <q-badge :color="statusBadgeColor(props.row.status)" outline>
                {{ props.row.status }}
              </q-badge>
            </q-td>
          </template>

          <template #body-cell-actions="props">
            <q-td :props="props" class="text-right">
              <q-btn
                flat
                round
                icon="delete"
                color="negative"
                @click="confirmDelete(props.row.id)"
              />
            </q-td>
          </template>

          <template #no-data>
            <div class="full-width row flex-center q-gutter-sm q-pa-md">
              <q-icon name="event_busy" size="28px" />
              <div class="text-grey-7">No bookings found.</div>
              <q-btn color="primary" unelevated label="Create one" @click="openCreate" />
            </div>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- Create Dialog -->
    <q-dialog v-model="createDialog">
      <q-card style="width: 520px; max-width: 95vw" class="q-pa-sm">
        <q-card-section>
          <div class="text-h6 text-weight-bold">New booking</div>
          <div class="text-caption text-grey-7">Fill the fields and save.</div>
        </q-card-section>

        <q-separator />

        <q-card-section>
          <q-form @submit.prevent="submitCreate">
            <q-input
              v-model.number="form.client_id"
              type="number"
              label="Client ID"
              filled
              class="q-mb-md"
              :rules="[val => !!val || 'Client ID is required']"
            />

            <q-input
              v-model.number="form.table_id"
              type="number"
              label="Table ID"
              filled
              class="q-mb-md"
              :rules="[val => !!val || 'Table ID is required']"
            />

            <q-input
              v-model="form.reservation_date"
              type="date"
              label="Reservation date"
              filled
              class="q-mb-md"
              :rules="[val => !!val || 'Reservation date is required']"
            />

            <q-input
              v-model="form.reservation_time"
              type="time"
              label="Reservation time"
              filled
              class="q-mb-md"
              :rules="[val => !!val || 'Reservation time is required']"
            />

            <q-input
              v-model.number="form.guest_count"
              type="number"
              label="Guests"
              filled
              class="q-mb-md"
              :rules="[
                val => !!val || 'Guests is required',
                val => Number(val) > 0 || 'Guests must be greater than 0'
              ]"
            />

            <q-select
              v-model="form.status"
              :options="statusOptions"
              label="Status"
              filled
              class="q-mb-md"
              emit-value
              map-options
            />

            <div class="row justify-end q-gutter-sm">
              <q-btn flat label="Cancel" v-close-popup />
              <q-btn
                color="primary"
                label="Save"
                type="submit"
                unelevated
                :loading="saving"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Notify, Dialog } from 'quasar'
import { api } from 'src/boot/axios'

const rows = ref([])
const loading = ref(false)

const columns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left', sortable: true },
  { name: 'client_id', label: 'Client', field: 'client_id', sortable: true },
  { name: 'table_id', label: 'Table', field: 'table_id', sortable: true },
  { name: 'reservation_date', label: 'Date', field: 'reservation_date', sortable: true },
  { name: 'reservation_time', label: 'Time', field: 'reservation_time', sortable: true },
  { name: 'guest_count', label: 'Guests', field: 'guest_count', sortable: true },
  { name: 'status', label: 'Status', field: 'status', sortable: true },
  { name: 'actions', label: '', field: 'actions', align: 'right' }
]

const statusOptions = [
  { label: 'Pending', value: 'pending' },
  { label: 'Confirmed', value: 'confirmed' },
  { label: 'Completed', value: 'completed' },
  { label: 'Cancelled', value: 'cancelled' }
]

function statusBadgeColor(status) {
  switch (status) {
    case 'confirmed':
      return 'positive'
    case 'pending':
      return 'warning'
    case 'completed':
      return 'info'
    case 'cancelled':
      return 'negative'
    default:
      return 'grey'
  }
}

function load() {
  loading.value = true

  api.get('/bookings')
    .then((res) => {
      rows.value = res.data
    })
    .catch(() => {
      Notify.create({ type: 'negative', message: 'Failed to load bookings' })
    })
    .finally(() => {
      loading.value = false
    })
}

onMounted(() => {
  load()
})

const createDialog = ref(false)
const saving = ref(false)

const form = ref({
  client_id: 1,
  table_id: 1,
  reservation_date: '',
  reservation_time: '',
  guest_count: 2,
  status: 'pending'
})

function openCreate() {
  createDialog.value = true
}

function submitCreate() {
  saving.value = true

  api.post('/bookings', form.value)
    .then(() => {
      Notify.create({ type: 'positive', message: 'Booking created' })
      createDialog.value = false
      load()
    })
    .catch((e) => {
      const response = e && e.response
      const status = response && response.status
      const detail = response && response.data && response.data.detail

      if (status === 409) {
        Notify.create({
          type: 'warning',
          message: detail || 'Double booking detected'
        })
        return
      }

      Notify.create({ type: 'negative', message: 'Failed to create booking' })
    })
    .finally(() => {
      saving.value = false
    })
}

function confirmDelete(id) {
  Dialog.create({
    title: 'Delete booking',
    message: `Are you sure you want to delete booking #${id}?`,
    cancel: true,
    persistent: true
  }).onOk(() => {
    api.delete(`/bookings/${id}`)
      .then(() => {
        Notify.create({ type: 'positive', message: 'Booking deleted' })
        load()
      })
      .catch(() => {
        Notify.create({ type: 'negative', message: 'Failed to delete booking' })
      })
  })
}
</script>
