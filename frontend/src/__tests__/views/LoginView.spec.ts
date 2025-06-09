import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import LoginView from '@/views/auth/LoginView.vue'
import { useAuthStore } from '@/stores/auth'

// Mock router
vi.mock('vue-router', () => ({
  useRoute: vi.fn(() => ({
    query: {}
  })),
  useRouter: vi.fn(() => ({
    push: vi.fn()
  }))
}))

describe('LoginView', () => {
  let wrapper: any
  let authStore: any
  
  beforeEach(() => {
    // Create a fresh pinia instance for each test with stubbed actions
    const pinia = createTestingPinia({
      createSpy: vi.fn,
      stubActions: false
    })
    
    // Mount the component
    wrapper = mount(LoginView, {
      global: {
        plugins: [pinia],
        stubs: {
          RouterLink: true
        }
      }
    })
    
    // Get the auth store
    authStore = useAuthStore()
    
    // Mock the login method
    authStore.login = vi.fn()
  })
  
  it('renders correctly', () => {
    expect(wrapper.find('h2').text()).toBe('Login to your account')
    expect(wrapper.find('form').exists()).toBe(true)
    expect(wrapper.find('input[type="text"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').text()).toBe('Login')
  })
  
  it('initializes with empty form fields', () => {
    const usernameInput = wrapper.find('input[type="text"]')
    const passwordInput = wrapper.find('input[type="password"]')
    
    expect(usernameInput.element.value).toBe('')
    expect(passwordInput.element.value).toBe('')
  })
  
  it('updates form fields when user types', async () => {
    const usernameInput = wrapper.find('input[type="text"]')
    const passwordInput = wrapper.find('input[type="password"]')
    
    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')
    
    expect(usernameInput.element.value).toBe('testuser')
    expect(passwordInput.element.value).toBe('password123')
  })
  
  it('shows error when form is submitted with empty fields', async () => {
    const form = wrapper.find('form')
    
    await form.trigger('submit')
    
    // Check that error message is displayed
    expect(wrapper.find('.alert-danger').exists()).toBe(true)
    expect(wrapper.find('.alert-danger').text()).toContain('Please enter both username and password')
    
    // Check that login action was not called
    expect(authStore.login).not.toHaveBeenCalled()
  })
  
  it('calls login action when form is submitted with valid data', async () => {
    // Set form values
    const usernameInput = wrapper.find('input[type="text"]')
    const passwordInput = wrapper.find('input[type="password"]')
    
    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')
    
    // Mock successful login
    authStore.login.mockResolvedValue(true)
    
    // Submit the form
    const form = wrapper.find('form')
    await form.trigger('submit')
    
    // Check that login action was called with correct arguments
    expect(authStore.login).toHaveBeenCalledWith('testuser', 'password123')
    
    // No error message should be displayed
    expect(wrapper.find('.alert-danger').exists()).toBe(false)
  })
  
  it('shows error message when login fails', async () => {
    // Set form values
    const usernameInput = wrapper.find('input[type="text"]')
    const passwordInput = wrapper.find('input[type="password"]')
    
    await usernameInput.setValue('testuser')
    await passwordInput.setValue('wrong-password')
    
    // Mock failed login
    authStore.login.mockResolvedValue(false)
    
    // Submit the form
    const form = wrapper.find('form')
    await form.trigger('submit')
    
    // Check that login action was called
    expect(authStore.login).toHaveBeenCalledWith('testuser', 'wrong-password')
    
    // Error message should be displayed
    expect(wrapper.find('.alert-danger').exists()).toBe(true)
    expect(wrapper.find('.alert-danger').text()).toContain('Invalid username or password')
  })
  
  it('disables the submit button while loading', async () => {
    // Set form values
    const usernameInput = wrapper.find('input[type="text"]')
    const passwordInput = wrapper.find('input[type="password"]')
    
    await usernameInput.setValue('testuser')
    await passwordInput.setValue('password123')
    
    // Create a promise that doesn't resolve immediately
    let resolveLogin: any
    const loginPromise = new Promise(resolve => {
      resolveLogin = resolve
    })
    
    // Mock login to return the promise
    authStore.login.mockReturnValue(loginPromise)
    
    // Submit the form
    const form = wrapper.find('form')
    await form.trigger('submit')
    
    // Check that button is disabled and shows loading text
    const button = wrapper.find('button[type="submit"]')
    expect(button.attributes('disabled')).toBeDefined()
    expect(button.text()).toBe('Logging in...')
    
    // Resolve the login promise
    resolveLogin(true)
    
    // Wait for the next tick to let the component update
    await wrapper.vm.$nextTick()
    
    // Button should be enabled again
    expect(button.attributes('disabled')).toBeUndefined()
    expect(button.text()).toBe('Login')
  })
})
