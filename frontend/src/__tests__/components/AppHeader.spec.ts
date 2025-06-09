import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import AppHeader from '@/components/layout/AppHeader.vue'
import { useAuthStore } from '@/stores/auth'

// Mock FontAwesome
vi.mock('@fortawesome/vue-fontawesome', () => ({
  FontAwesomeIcon: {
    name: 'FontAwesomeIcon',
    template: '<span><slot /></span>'
  }
}))

// Mock router
vi.mock('vue-router', () => ({
  RouterLink: {
    name: 'RouterLink',
    template: '<a><slot /></a>',
    props: ['to']
  }
}))

describe('AppHeader', () => {
  let wrapper: any
  let authStore: any
  
  beforeEach(() => {
    // Create a fresh pinia instance for each test
    const pinia = createTestingPinia({
      createSpy: vi.fn
    })
    
    // Mount the component
    wrapper = mount(AppHeader, {
      global: {
        plugins: [pinia],
        stubs: {
          FontAwesomeIcon: true,
          RouterLink: true
        }
      }
    })
    
    // Get the auth store
    authStore = useAuthStore()
    
    // Mock the logout method
    authStore.logout = vi.fn()
  })
  
  it('renders correctly', () => {
    expect(wrapper.find('.app-header').exists()).toBe(true)
    expect(wrapper.find('.sidebar-toggle').exists()).toBe(true)
    expect(wrapper.find('.search-box').exists()).toBe(true)
    expect(wrapper.find('.user-menu').exists()).toBe(true)
  })
  
  it('emits toggle-sidebar event when sidebar toggle button is clicked', async () => {
    const toggleButton = wrapper.find('.sidebar-toggle')
    await toggleButton.trigger('click')
    
    expect(wrapper.emitted('toggle-sidebar')).toBeTruthy()
    expect(wrapper.emitted('toggle-sidebar').length).toBe(1)
  })
  
  it('displays username from auth store', async () => {
    // Set user in auth store
    authStore.user = { username: 'testuser' }
    
    // Wait for the component to update
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('.user-name').text()).toBe('testuser')
  })
  
  it('displays default username when user is not set', () => {
    // Auth store user is null by default
    expect(wrapper.find('.user-name').text()).toBe('User')
  })
  
  it('calls logout method when logout button is clicked', async () => {
    // Find and click the logout button
    const logoutButton = wrapper.find('.dropdown-item:last-child')
    await logoutButton.trigger('click')
    
    // Check that logout was called
    expect(authStore.logout).toHaveBeenCalled()
  })
  
  it('has correct navigation links', () => {
    const links = wrapper.findAll('.dropdown-item')
    
    // Check profile link
    expect(links[0].attributes('to')).toBe('/profile')
    expect(links[0].text()).toContain('Profile')
    
    // Check settings link
    expect(links[1].attributes('to')).toBe('/settings')
    expect(links[1].text()).toContain('Settings')
  })
})
