import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

// Mock axios
vi.mock('axios')

// Mock router
vi.mock('@/router', () => ({
  default: {
    push: vi.fn(),
    currentRoute: {
      value: {
        query: {}
      }
    }
  }
}))

describe('Auth Store', () => {
  beforeEach(() => {
    // Create a fresh pinia instance for each test
    setActivePinia(createPinia())
    
    // Clear localStorage before each test
    localStorage.clear()
    
    // Reset axios mocks
    vi.mocked(axios.post).mockReset()
    vi.mocked(axios.get).mockReset()
  })
  
  afterEach(() => {
    vi.clearAllMocks()
  })
  
  it('initializes with correct state', () => {
    const store = useAuthStore()
    
    expect(store.user).toBeNull()
    expect(store.token).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })
  
  it('initializes with token from localStorage', () => {
    // Set token in localStorage
    localStorage.setItem('token', 'test-token')
    
    const store = useAuthStore()
    
    expect(store.token).toBe('test-token')
    expect(store.isAuthenticated).toBe(false) // Still false until checkAuth is called
  })
  
  it('successfully logs in a user', async () => {
    const store = useAuthStore()
    
    // Mock successful login response
    vi.mocked(axios.post).mockResolvedValueOnce({
      data: {
        token: 'test-token',
        user: {
          id: 1,
          username: 'testuser',
          email: 'test@example.com'
        }
      }
    })
    
    const result = await store.login('testuser', 'password')
    
    // Verify axios was called correctly
    expect(axios.post).toHaveBeenCalledWith('/api/auth/login/', {
      username: 'testuser',
      password: 'password'
    })
    
    // Verify store state was updated
    expect(store.token).toBe('test-token')
    expect(store.user).toEqual({
      id: 1,
      username: 'testuser',
      email: 'test@example.com'
    })
    expect(store.isAuthenticated).toBe(true)
    
    // Verify token was saved to localStorage
    expect(localStorage.getItem('token')).toBe('test-token')
    
    // Verify result
    expect(result).toBe(true)
  })
  
  it('handles login failure', async () => {
    const store = useAuthStore()
    
    // Mock failed login response
    vi.mocked(axios.post).mockRejectedValueOnce(new Error('Invalid credentials'))
    
    const result = await store.login('testuser', 'wrong-password')
    
    // Verify axios was called correctly
    expect(axios.post).toHaveBeenCalledWith('/api/auth/login/', {
      username: 'testuser',
      password: 'wrong-password'
    })
    
    // Verify store state was not updated
    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    
    // Verify token was not saved to localStorage
    expect(localStorage.getItem('token')).toBeNull()
    
    // Verify result
    expect(result).toBe(false)
  })
  
  it('successfully signs up a user', async () => {
    const store = useAuthStore()
    
    // Mock successful signup response
    vi.mocked(axios.post).mockResolvedValueOnce({
      data: {
        success: true
      }
    })
    
    const result = await store.signup('newuser', 'new@example.com', 'password')
    
    // Verify axios was called correctly
    expect(axios.post).toHaveBeenCalledWith('/api/auth/register/', {
      username: 'newuser',
      email: 'new@example.com',
      password: 'password'
    })
    
    // Verify result
    expect(result).toBe(true)
  })
  
  it('handles signup failure', async () => {
    const store = useAuthStore()
    
    // Mock failed signup response
    vi.mocked(axios.post).mockRejectedValueOnce(new Error('Username already exists'))
    
    const result = await store.signup('existinguser', 'existing@example.com', 'password')
    
    // Verify axios was called correctly
    expect(axios.post).toHaveBeenCalledWith('/api/auth/register/', {
      username: 'existinguser',
      email: 'existing@example.com',
      password: 'password'
    })
    
    // Verify result
    expect(result).toBe(false)
  })
  
  it('successfully logs out a user', async () => {
    const store = useAuthStore()
    
    // Set initial authenticated state
    store.token = 'test-token'
    store.user = { id: 1, username: 'testuser', email: 'test@example.com' }
    store.isAuthenticated = true
    localStorage.setItem('token', 'test-token')
    
    // Mock successful logout response
    vi.mocked(axios.post).mockResolvedValueOnce({})
    
    await store.logout()
    
    // Verify axios was called correctly
    expect(axios.post).toHaveBeenCalledWith('/api/auth/logout/')
    
    // Verify store state was updated
    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    
    // Verify token was removed from localStorage
    expect(localStorage.getItem('token')).toBeNull()
  })
  
  it('handles logout API failure but still clears user data', async () => {
    const store = useAuthStore()
    
    // Set initial authenticated state
    store.token = 'test-token'
    store.user = { id: 1, username: 'testuser', email: 'test@example.com' }
    store.isAuthenticated = true
    localStorage.setItem('token', 'test-token')
    
    // Mock failed logout response
    vi.mocked(axios.post).mockRejectedValueOnce(new Error('Network error'))
    
    await store.logout()
    
    // Verify axios was called correctly
    expect(axios.post).toHaveBeenCalledWith('/api/auth/logout/')
    
    // Verify store state was still updated despite API failure
    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    
    // Verify token was removed from localStorage
    expect(localStorage.getItem('token')).toBeNull()
  })
  
  it('successfully validates a token', async () => {
    const store = useAuthStore()
    
    // Set initial token
    store.token = 'test-token'
    localStorage.setItem('token', 'test-token')
    
    // Mock successful user data response
    vi.mocked(axios.get).mockResolvedValueOnce({
      data: {
        id: 1,
        username: 'testuser',
        email: 'test@example.com'
      }
    })
    
    const result = await store.checkAuth()
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/api/auth/user/')
    expect(axios.defaults.headers.common['Authorization']).toBe('Token test-token')
    
    // Verify store state was updated
    expect(store.user).toEqual({
      id: 1,
      username: 'testuser',
      email: 'test@example.com'
    })
    expect(store.isAuthenticated).toBe(true)
    
    // Verify result
    expect(result).toBe(true)
  })
  
  it('handles invalid token', async () => {
    const store = useAuthStore()
    
    // Set initial token
    store.token = 'invalid-token'
    localStorage.setItem('token', 'invalid-token')
    
    // Mock failed user data response
    vi.mocked(axios.get).mockRejectedValueOnce(new Error('Invalid token'))
    
    const result = await store.checkAuth()
    
    // Verify axios was called correctly
    expect(axios.get).toHaveBeenCalledWith('/api/auth/user/')
    
    // Verify store state was updated
    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    
    // Verify token was removed from localStorage
    expect(localStorage.getItem('token')).toBeNull()
    
    // Verify result
    expect(result).toBe(false)
  })
  
  it('returns false when no token exists', async () => {
    const store = useAuthStore()
    
    const result = await store.checkAuth()
    
    // Verify axios was not called
    expect(axios.get).not.toHaveBeenCalled()
    
    // Verify store state remains unchanged
    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    
    // Verify result
    expect(result).toBe(false)
  })
})
