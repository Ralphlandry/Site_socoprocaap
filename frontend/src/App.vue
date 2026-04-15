<template>
  <div id="app">
    <AppHeader v-if="!isAdmin" />
    <main>
      <router-view />
    </main>
    <AppFooter v-if="!isAdmin" />
    <WhatsAppButton v-if="!isAdmin" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import WhatsAppButton from './components/WhatsAppButton.vue'

const route = useRoute()
const isAdmin = computed(() => route.path.startsWith('/admin'))
</script>
