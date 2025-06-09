<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const authStore = useAuthStore()
const sidebarCollapsed = ref(false)

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}
</script>

<template>
  <div class="layout-default" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
    <AppSidebar :collapsed="sidebarCollapsed" />
    
    <div class="main-content">
      <AppHeader @toggle-sidebar="toggleSidebar" />
      
      <main class="content">
        <div class="container-fluid p-0">
          <RouterView />
        </div>
      </main>
      
      <AppFooter />
    </div>
  </div>
</template>

<style scoped>
.layout-default {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.content {
  flex: 1;
  padding: 1.5rem;
}

.sidebar-collapsed .main-content {
  margin-left: 70px;
}
</style>
