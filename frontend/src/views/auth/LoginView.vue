<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  if (!username.value || !password.value) {
    errorMessage.value = 'Please enter both username and password'
    return
  }
  
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const success = await authStore.login(username.value, password.value)
    
    if (!success) {
      errorMessage.value = 'Invalid username or password'
    }
  } catch (error) {
    errorMessage.value = 'An error occurred during login'
    console.error('Login error:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-view">
    <h2 class="text-center mb-4">Login to your account</h2>
    
    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>
    
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username" class="form-label">Username</label>
        <input
          id="username"
          v-model="username"
          type="text"
          class="form-control"
          placeholder="Enter your username"
          required
          autofocus
        />
      </div>
      
      <div class="form-group">
        <label for="password" class="form-label">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          class="form-control"
          placeholder="Enter your password"
          required
        />
      </div>
      
      <div class="form-group">
        <div class="d-flex justify-content-between align-items-center">
          <div class="form-check">
            <input id="remember" type="checkbox" class="form-check-input" />
            <label for="remember" class="form-check-label">Remember me</label>
          </div>
          <div>
            <router-link to="/auth/forgot-password">Forgot password?</router-link>
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
          {{ isLoading ? 'Logging in...' : 'Login' }}
        </button>
      </div>
    </form>
    
    <div class="text-center mt-3">
      Don't have an account?
      <router-link to="/auth/signup">Sign up</router-link>
    </div>
  </div>
</template>

<style scoped>
.login-view {
  max-width: 400px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1.5rem;
}

.d-flex {
  display: flex;
}

.justify-content-between {
  justify-content: space-between;
}

.align-items-center {
  align-items: center;
}

.w-100 {
  width: 100%;
}

.form-check {
  display: flex;
  align-items: center;
}

.form-check-input {
  margin-right: 0.5rem;
}
</style>
