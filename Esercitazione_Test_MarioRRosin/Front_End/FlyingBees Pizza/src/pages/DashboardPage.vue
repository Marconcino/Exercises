<template>
  <q-page class = "q-pa-lg">
    <div class = "row items-center q-col-gutter-md">
      <div class = "col-12 col-md-8">
        <div class = "text-h5 text-weight-bold">Welcome to FlyingBees Pizza</div>
        <div class = "text-grey-7">Get your spot Today</div>
      </div>
      <div class = "col-12 col-md-4 flex justify-end">
        <q-btn color = "primary" icon = "add" label = "New booking" to = "/bookings" unelevated />
      </div>
    </div>

    <div class = "row q-col-gutter-md q-mt-md">
      <div class = "col-12 col-sm-6 col-lg-3" v-for = "c in cards" :key="c.title">
        <q-card class = "my-card" bordered>
          <q-card-section>
            <div class = "row items-center no-wrap">
              <q-icon :name = "c.icon" size = "28px" class = "q-mr-sm" />
              <div>
                <div class = "text-caption text-grey-7">{{ c.title }}</div>
                <div class = "text-h6 text-weight-bold">{{ c.value }}</div>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <q-card class = "q-mt-lg" bordered>
      <q-card-section>
        <div class="text-subtitle1 text-weight-bold">Next steps</div>
        <div class="text-grey-7">
          Start by adding a couple of tables and clients, then create bookings.
        </div>
      </q-card-section>
      <q-separator />
      <q-card-actions align="right">
        <q-btn flat label="Go to Tables" to = "/tables" />
        <q-btn flat label="Go to Clients" to = "/clients" />
        <q-btn color = "primary" unelevated label = "Go to Bookings" to = "/bookings" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const cards = computed(() => ([
  { title: 'Today bookings', value: 0, icon: 'event' },
  { title: 'Pending', value: 0, icon: 'hourglass_empty' },
  { title: 'Tables', value: 0, icon: 'table_restaurant' },
  { title: 'Clients', value: 0, icon: 'people' }
]))
</script>

<style scoped>
.my-card {
  border-radius: 26px;
}
</style>
