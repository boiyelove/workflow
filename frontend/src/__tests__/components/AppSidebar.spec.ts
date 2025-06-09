import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import AppSidebar from '@/components/layout/AppSidebar.vue'

// Mock FontAwesome
vi.mock('@fortawesome/vue-fontawesome', () => ({
  FontAwesomeIcon: {
    name: 'FontAwesomeIcon',
    template: '<span><slot /></span>'
  }
}))

// Mock vue-router
vi.mock('vue-router', () => ({
  RouterLink: {
    name: 'RouterLink',
    template: '<a class="router-link" :class="{ active: to === \'/dashboard\' }" :to="to"><slot /></a>',
    props: ['to']
  },
  useRoute: vi.fn(() => ({
    path: '/dashboard'
  }))
}))

describe('AppSidebar', () => {
  let wrapper: any
  
  beforeEach(() => {
    // Mount the component with default props
    wrapper = mount(AppSidebar, {
      props: {
        collapsed: false
      },
      global: {
        stubs: {
          FontAwesomeIcon: true,
          RouterLink: {
            template: '<a class="router-link" :class="{ active: to === \'/dashboard\' }" :to="to"><slot /></a>',
            props: ['to']
          }
        }
      }
    })
  })
  
  it('renders correctly', () => {
    expect(wrapper.find('.app-sidebar').exists()).toBe(true)
    expect(wrapper.find('.sidebar-header').exists()).toBe(true)
    expect(wrapper.find('.sidebar-content').exists()).toBe(true)
    expect(wrapper.find('.sidebar-footer').exists()).toBe(true)
  })
  
  it('adds collapsed class when collapsed prop is true', async () => {
    // Initially not collapsed
    expect(wrapper.classes()).not.toContain('sidebar-collapsed')
    
    // Update props to collapsed
    await wrapper.setProps({ collapsed: true })
    
    expect(wrapper.classes()).toContain('sidebar-collapsed')
  })
  
  it('renders navigation links', () => {
    const navLinks = wrapper.findAll('.router-link')
    expect(navLinks.length).toBeGreaterThan(0)
  })
  
  it('shows dashboard link', () => {
    const dashboardLink = wrapper.findAll('.router-link').find(link => link.attributes('to') === '/dashboard')
    expect(dashboardLink).toBeDefined()
  })
  
  it('shows projects link', () => {
    const projectsLink = wrapper.findAll('.router-link').find(link => link.attributes('to') === '/projects')
    expect(projectsLink).toBeDefined()
  })
})
