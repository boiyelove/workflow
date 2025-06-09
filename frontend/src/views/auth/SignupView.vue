<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const handleSignup = async () => {
  if (!username.value || !email.value || !password.value) {
    errorMessage.value = 'Please fill in all required fields'
    return
  }
  
  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match'
    return
  }
  
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const success = await authStore.signup(username.value, email.value, password.value)
    
    if (!success) {
      errorMessage.value = 'Registration failed. Please try again.'
    }
  } catch (error) {
    errorMessage.value = 'An error occurred during registration'
    console.error('Signup error:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="signup-view">
    <h2 class="text-center mb-4">Create an account</h2>
    
    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>
    
    <form @submit.prevent="handleSignup">
      <div class="form-group">
        <label for="username" class="form-label">Username</label>
        <input
          id="username"
          v-model="username"
          type="text"
          class="form-control"
          placeholder="Choose a username"
          required
          autofocus
        />
      </div>
      
      <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          class="form-control"
          placeholder="Enter your email"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="password" class="form-label">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          class="form-control"
          placeholder="Create a password"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="confirm-password" class="form-label">Confirm Password</label>
        <input
          id="confirm-password"
          v-model="confirmPassword"
          type="password"
          class="form-control"
          placeholder="Confirm your password"
          required
        />
      </div>
      
      <div class="form-group">
        <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
          {{ isLoading ? 'Creating account...' : 'Sign Up' }}
        </button>
      </div>
    </form>
    
    <div class="text-center mt-3">
      Already have an account?
      <router-link to="/auth/login">Login</router-link>
    </div>
  </div>
</template>

<style scoped>
.signup-view {
  max-width: 400px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1.5rem;
}

.w-100 {
  width: 100%;
}
</style>
