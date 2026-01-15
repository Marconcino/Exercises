<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title> Quasar App </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header> Essential Links </q-item-label>

        <EssentialLink v-for="link in linksList" :key="link.title" v-bind="link" />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import EssentialLink from 'components/EssentialLink.vue'

const linksList = [
  {
    title: 'Appointments',
    caption: 'quasar.dev',
    icon: 'calendar_month',
    link: '',
  },
  {
    title: 'Doctors',
    caption: 'github.com/quasarframework',
    icon: 'healing',
    link: 'https://github.com/quasarframework',
  },
  {
    title: 'Patient',
    caption: 'chat.quasar.dev',
    icon: 'personal_injury',
    link: 'https://chat.quasar.dev',
  },
  {
    title: 'Visiting Rooms',
    caption: 'forum.quasar.dev',
    icon: 'moving_beds',
    link: 'https://forum.quasar.dev',
  }
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
