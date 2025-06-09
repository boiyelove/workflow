<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps<{
  collapsed: boolean
}>()

const route = useRoute()

const isActive = (path: string) => {
  return route.path === path || route.path.startsWith(`${path}/`)
}

const sidebarClass = computed(() => {
  return {
    'sidebar-collapsed': props.collapsed
  }
})
</script>

<template>
  <aside class="app-sidebar" :class="sidebarClass">
    <div class="sidebar-header">
      <router-link to="/" class="logo">
        <img src="@/assets/logo.svg" alt="Workflow Logo" />
        <span v-if="!collapsed" class="logo-text">Workflow</span>
      </router-link>
    </div>
    
    <div class="sidebar-content">
      <nav class="sidebar-nav">
        <ul>
          <li>
            <router-link to="/dashboard" :class="{ active: isActive('/dashboard') }">
              <font-awesome-icon icon="home" />
              <span v-if="!collapsed">Dashboard</span>
            </router-link>
          </li>
          <li>
            <router-link to="/projects" :class="{ active: isActive('/projects') }">
              <font-awesome-icon icon="project-diagram" />
              <span v-if="!collapsed">Projects</span>
            </router-link>
          </li>
          <li>
            <router-link to="/teams" :class="{ active: isActive('/teams') }">
              <font-awesome-icon icon="users" />
              <span v-if="!collapsed">Teams</span>
            </router-link>
          </li>
          <li>
            <router-link to="/calendar" :class="{ active: isActive('/calendar') }">
              <font-awesome-icon icon="calendar-alt" />
              <span v-if="!collapsed">Calendar</span>
            </router-link>
          </li>
          <li>
            <router-link to="/analytics" :class="{ active: isActive('/analytics') }">
              <font-awesome-icon icon="chart-line" />
              <span v-if="!collapsed">Analytics</span>
            </router-link>
          </li>
        </ul>
      </nav>
    </div>
    
    <div class="sidebar-footer">
      <router-link to="/settings" :class="{ active: isActive('/settings') }">
        <font-awesome-icon icon="cog" />
        <span v-if="!collapsed">Settings</span>
      </router-link>
    </div>
  </aside>
</template>

<style scoped>
.app-sidebar {
  width: 250px;
  height: 100vh;
  background-color: #2c3e50;
  color: #fff;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
}

.sidebar-collapsed {
  width: 70px;
}

.sidebar-header {
  height: 70px;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #fff;
}

.logo img {
  width: 32px;
  height: 32px;
}

.logo-text {
  margin-left: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-nav li {
  margin: 0;
}

.sidebar-nav a {
  display: flex;
  align-items: center;
  padding: 1rem;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.3s ease;
}

.sidebar-nav a:hover,
.sidebar-nav a.active {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-nav a svg {
  width: 20px;
  text-align: center;
  margin-right: 1rem;
}

.sidebar-collapsed .sidebar-nav a svg {
  margin-right: 0;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-footer a {
  display: flex;
  align-items: center;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.3s ease;
}

.sidebar-footer a:hover,
.sidebar-footer a.active {
  color: #fff;
}

.sidebar-footer a svg {
  width: 20px;
  text-align: center;
  margin-right: 1rem;
}

.sidebar-collapsed .sidebar-footer a svg {
  margin-right: 0;
}
</style>
