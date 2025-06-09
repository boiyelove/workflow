import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Layouts
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

// Views
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/auth/LoginView.vue'
import SignupView from '@/views/auth/SignupView.vue'
import DashboardView from '@/views/DashboardView.vue'
import ProjectsView from '@/views/projects/ProjectsView.vue'
import ProjectDetailView from '@/views/projects/ProjectDetailView.vue'
import TeamsView from '@/views/teams/TeamsView.vue'
import TeamDetailView from '@/views/teams/TeamDetailView.vue'
import ProfileView from '@/views/user/ProfileView.vue'
import NotFoundView from '@/views/NotFoundView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: DefaultLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: DashboardView,
          meta: { requiresAuth: true }
        },
        {
          path: 'projects',
          name: 'projects',
          component: ProjectsView,
          meta: { requiresAuth: true }
        },
        {
          path: 'projects/:id',
          name: 'project-detail',
          component: ProjectDetailView,
          meta: { requiresAuth: true }
        },
        {
          path: 'teams',
          name: 'teams',
          component: TeamsView,
          meta: { requiresAuth: true }
        },
        {
          path: 'teams/:id',
          name: 'team-detail',
          component: TeamDetailView,
          meta: { requiresAuth: true }
        },
        {
          path: 'profile',
          name: 'profile',
          component: ProfileView,
          meta: { requiresAuth: true }
        }
      ]
    },
    {
      path: '/auth',
      component: AuthLayout,
      children: [
        {
          path: 'login',
          name: 'login',
          component: LoginView
        },
        {
          path: 'signup',
          name: 'signup',
          component: SignupView
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundView
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
