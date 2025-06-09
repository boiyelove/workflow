<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.back()
}
</script>

<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The page you are looking for doesn't exist or has been moved.</p>
      <div class="not-found-actions">
        <button @click="goBack" class="btn btn-secondary">
          <font-awesome-icon icon="arrow-left" class="me-2" />
          Go Back
        </button>
        <router-link to="/" class="btn btn-primary">
          <font-awesome-icon icon="home" class="me-2" />
          Go Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 140px); /* Subtract header and footer height */
  text-align: center;
  padding: 2rem;
}

.not-found-content {
  max-width: 500px;
}

.not-found h1 {
  font-size: 6rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 1rem;
}

.not-found h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.not-found p {
  font-size: 1.25rem;
  color: #6c757d;
  margin-bottom: 2rem;
}

.not-found-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.me-2 {
  margin-right: 0.5rem;
}
</style>
