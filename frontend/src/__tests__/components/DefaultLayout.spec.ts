import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

// Mock child components
vi.mock('@/components/layout/AppSidebar.vue', () => ({
  default: {
    name: 'AppSidebar',
    template: '<div class="mock-sidebar"><slot /></div>',
    props: ['collapsed']
  }
}))

vi.mock('@/components/layout/AppHeader.vue', () => ({
  default: {
    name: 'AppHeader',
    template: '<div class="mock-header"><slot /></div>',
    emits: ['toggle-sidebar']
  }
}))

vi.mock('@/components/layout/AppFooter.vue', () => ({
  default: {
    name: 'AppFooter',
    template: '<div class="mock-footer"><slot /></div>'
  }
}))

// Mock vue-router
vi.mock('vue-router', () => ({
  RouterView: {
    name: 'RouterView',
    template: '<div class="mock-router-view">Page Content</div>'
  }
}))

describe('DefaultLayout', () => {
  let wrapper: any
  
  beforeEach(() => {
    // Create a fresh pinia instance for each test
    const pinia = createTestingPinia({
      createSpy: vi.fn
    })
    
    // Mount the component
    wrapper = mount(DefaultLayout, {
      global: {
        plugins: [pinia],
        stubs: {
          RouterView: true
        }
      }
    })
  })
  
  it('renders correctly', () => {
    expect(wrapper.find('.layout-default').exists()).toBe(true)
    expect(wrapper.find('.mock-sidebar').exists()).toBe(true)
    expect(wrapper.find('.mock-header').exists()).toBe(true)
    expect(wrapper.find('.mock-footer').exists()).toBe(true)
    expect(wrapper.find('.mock-router-view').exists()).toBe(true)
  })
  
  it('initializes with sidebar not collapsed', () => {
    expect(wrapper.classes()).not.toContain('sidebar-collapsed')
    
    // Check that AppSidebar receives correct props
    const sidebar = wrapper.findComponent({ name: 'AppSidebar' })
    expect(sidebar.props('collapsed')).toBe(false)
  })
  
  it('toggles sidebar when header emits toggle-sidebar event', async () => {
    // Initially not collapsed
    expect(wrapper.classes()).not.toContain('sidebar-collapsed')
    
    // Trigger toggle-sidebar event from header
    const header = wrapper.findComponent({ name: 'AppHeader' })
    await header.vm.$emit('toggle-sidebar')
    
    // Should be collapsed now
    expect(wrapper.classes()).toContain('sidebar-collapsed')
    
    // Check that AppSidebar receives updated props
    const sidebar = wrapper.findComponent({ name: 'AppSidebar' })
    expect(sidebar.props('collapsed')).toBe(true)
    
    // Toggle again
    await header.vm.$emit('toggle-sidebar')
    
    // Should be not collapsed again
    expect(wrapper.classes()).not.toContain('sidebar-collapsed')
    expect(sidebar.props('collapsed')).toBe(false)
  })
})
