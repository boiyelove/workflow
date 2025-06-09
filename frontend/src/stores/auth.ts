import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

interface User {
  id: number
  username: string
  email: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false
  }),
  
  actions: {
    async login(username: string, password: string) {
      try {
        const response = await axios.post('/api/auth/login/', {
          username,
          password
        })
        
        const { token, user } = response.data
        
        this.token = token
        this.user = user
        this.isAuthenticated = true
        
        localStorage.setItem('token', token)
        
        // Set default Authorization header for all requests
        axios.defaults.headers.common['Authorization'] = `Token ${token}`
        
        // Redirect to dashboard or requested page
        const redirectPath = router.currentRoute.value.query.redirect as string || '/dashboard'
        router.push(redirectPath)
        
        return true
      } catch (error) {
        console.error('Login failed:', error)
        return false
      }
    },
    
    async signup(username: string, email: string, password: string) {
      try {
        await axios.post('/api/auth/register/', {
          username,
          email,
          password
        })
        
        // Redirect to login page after successful signup
        router.push('/auth/login')
        
        return true
      } catch (error) {
        console.error('Signup failed:', error)
        return false
      }
    },
    
    async logout() {
      try {
        await axios.post('/api/auth/logout/')
      } catch (error) {
        console.error('Logout API call failed:', error)
      }
      
      // Clear user data regardless of API success
      this.token = null
      this.user = null
      this.isAuthenticated = false
      
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
      
      router.push('/auth/login')
    },
    
    async checkAuth() {
      if (!this.token) {
        this.isAuthenticated = false
        return false
      }
      
      try {
        // Set the token in axios headers
        axios.defaults.headers.common['Authorization'] = `Token ${this.token}`
        
        // Verify the token by fetching user data
        const response = await axios.get('/api/auth/user/')
        
        this.user = response.data
        this.isAuthenticated = true
        return true
      } catch (error) {
        console.error('Token validation failed:', error)
        this.token = null
        this.user = null
        this.isAuthenticated = false
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
        return false
      }
    }
  }
})
