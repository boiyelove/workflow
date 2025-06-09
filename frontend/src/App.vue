<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'

const authStore = useAuthStore()

onMounted(() => {
  // Check if user is already authenticated
  authStore.checkAuth()
})
</script>

<template>
  <RouterView />
</template>

<style>
@import '@/assets/main.css';
</style>
