<script setup lang="ts">
// Auth layout for login, signup, etc.
</script>

<template>
  <div class="auth-layout">
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-logo">
          <img src="@/assets/logo.svg" alt="Workflow Logo" />
          <h1>Workflow</h1>
        </div>
        
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fb;
}

.auth-container {
  width: 100%;
  max-width: 400px;
  padding: 1rem;
}

.auth-card {
  background-color: #fff;
  border-radius: 0.5rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  padding: 2rem;
}

.auth-logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}

.auth-logo img {
  width: 64px;
  height: 64px;
}

.auth-logo h1 {
  margin-top: 1rem;
  font-size: 1.5rem;
  font-weight: 600;
}
</style>
