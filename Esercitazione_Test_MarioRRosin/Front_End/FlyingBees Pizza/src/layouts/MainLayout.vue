<template>
  <q-layout view="lHh Lpr lFf">
    <BeeBackground />

    <q-header elevated class="app-header">
      <q-toolbar>
        <q-toolbar-title>FlyingBees Pizza</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container class="app-foreground">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import BeeBackground from "src/components/BeeBackground.vue";
</script>

<style scoped>
.app-header { z-index: 2; }
.app-foreground { position: relative; z-index: 1; }
</style>




<!--  
<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn flat dense round icon = "menu" aria-label = "Menu" @click = "toggleLeftDrawer" />

        <q-toolbar-title> FlyingBees Pizza </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model = "leftDrawerOpen" show-if-above bordered>
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
    title: 'Book Your Table',
    caption: 'Try our pizzas',
    icon: 'local_pizza',
    link: '',
  },
  {
    title: 'About Our Bees',
    caption: 'Read our History',
    icon: 'emoji_nature',
    link: '',
  },
  {
    title: '',
    caption: 'chat.quasar.dev',
    icon: 'chat',
    link: '',
  }
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>

--> 
