<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

defineEmits(['toggle-sidebar'])
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <button class="sidebar-toggle" @click="$emit('toggle-sidebar')">
        <font-awesome-icon icon="bars" />
      </button>
      <div class="search-box">
        <font-awesome-icon icon="search" />
        <input type="text" placeholder="Search..." />
      </div>
    </div>
    
    <div class="header-right">
      <div class="notifications">
        <font-awesome-icon icon="bell" />
        <span class="badge">3</span>
      </div>
      
      <div class="user-menu dropdown">
        <button class="dropdown-toggle">
          <div class="avatar">
            <img src="https://ui-avatars.com/api/?name=User&background=0D8ABC&color=fff" alt="User" />
          </div>
          <span class="user-name">{{ authStore.user?.username || 'User' }}</span>
        </button>
        <div class="dropdown-menu">
          <router-link to="/profile" class="dropdown-item">
            <font-awesome-icon icon="user" />
            Profile
          </router-link>
          <router-link to="/settings" class="dropdown-item">
            <font-awesome-icon icon="cog" />
            Settings
          </router-link>
          <div class="dropdown-divider"></div>
          <button @click="authStore.logout()" class="dropdown-item">
            <font-awesome-icon icon="sign-out-alt" />
            Logout
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
  padding: 0 1.5rem;
  background-color: #fff;
  border-bottom: 1px solid #e9ecef;
}

.header-left {
  display: flex;
  align-items: center;
}

.sidebar-toggle {
  background: none;
  border: none;
  font-size: 1.25rem;
  margin-right: 1rem;
  cursor: pointer;
  color: #495057;
}

.search-box {
  position: relative;
  margin-left: 1rem;
}

.search-box input {
  padding: 0.5rem 0.5rem 0.5rem 2rem;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  width: 200px;
}

.search-box svg {
  position: absolute;
  left: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
}

.header-right {
  display: flex;
  align-items: center;
}

.notifications {
  position: relative;
  margin-right: 1.5rem;
  font-size: 1.25rem;
  color: #495057;
  cursor: pointer;
}

.badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #dc3545;
  color: #fff;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-menu {
  position: relative;
}

.dropdown-toggle {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  cursor: pointer;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 0.5rem;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-name {
  font-weight: 500;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: 100%;
  background-color: #fff;
  border: 1px solid #e9ecef;
  border-radius: 0.25rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  min-width: 200px;
  z-index: 1000;
  display: none;
}

.dropdown:hover .dropdown-menu {
  display: block;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  color: #212529;
  text-decoration: none;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.dropdown-item svg {
  margin-right: 0.5rem;
  width: 16px;
}

.dropdown-divider {
  height: 0;
  margin: 0.5rem 0;
  overflow: hidden;
  border-top: 1px solid #e9ecef;
}
</style>
