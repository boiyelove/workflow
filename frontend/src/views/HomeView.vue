<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  // If user is already authenticated, redirect to dashboard
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
})
</script>

<template>
  <div class="home-view">
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1>Manage your projects with ease</h1>
          <p class="lead">
            Workflow is a comprehensive project management solution for teams of all sizes.
            Track projects, manage tasks, and collaborate with your team all in one place.
          </p>
          <div class="hero-buttons">
            <router-link to="/auth/signup" class="btn btn-primary btn-lg">Get Started</router-link>
            <router-link to="/auth/login" class="btn btn-outline-primary btn-lg">Login</router-link>
          </div>
        </div>
        <div class="hero-image">
          <img src="@/assets/hero-image.png" alt="Workflow Dashboard" />
        </div>
      </div>
    </section>
    
    <section class="features">
      <div class="container">
        <h2 class="section-title">Key Features</h2>
        
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <font-awesome-icon icon="project-diagram" />
            </div>
            <h3>Project Management</h3>
            <p>Create and manage projects with customizable workflows, milestones, and deadlines.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <font-awesome-icon icon="tasks" />
            </div>
            <h3>Task Tracking</h3>
            <p>Break down projects into manageable tasks and subtasks with assignees and due dates.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <font-awesome-icon icon="users" />
            </div>
            <h3>Team Collaboration</h3>
            <p>Work together with your team, assign tasks, and track progress in real-time.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <font-awesome-icon icon="chart-line" />
            </div>
            <h3>Analytics & Reporting</h3>
            <p>Gain insights into project performance with detailed analytics and custom reports.</p>
          </div>
        </div>
      </div>
    </section>
    
    <section class="cta">
      <div class="container">
        <h2>Ready to streamline your workflow?</h2>
        <p>Join thousands of teams already using Workflow to manage their projects efficiently.</p>
        <router-link to="/auth/signup" class="btn btn-primary btn-lg">Start Free Trial</router-link>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-view {
  margin-top: -70px; /* Offset the header height */
}

.hero {
  background-color: #f8f9fa;
  padding: 120px 0 80px;
}

.hero .container {
  display: flex;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.hero-content {
  flex: 1;
  padding-right: 2rem;
}

.hero-image {
  flex: 1;
  text-align: center;
}

.hero-image img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.hero h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #212529;
}

.lead {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  color: #6c757d;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
}

.features {
  padding: 80px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.section-title {
  text-align: center;
  margin-bottom: 3rem;
  font-size: 2.5rem;
  font-weight: 600;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 2.5rem;
  color: var(--primary-color);
  margin-bottom: 1.5rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #6c757d;
}

.cta {
  background-color: var(--primary-color);
  color: #fff;
  padding: 80px 0;
  text-align: center;
}

.cta h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.cta p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta .btn {
  background-color: #fff;
  color: var(--primary-color);
  border: none;
}

.cta .btn:hover {
  background-color: #f8f9fa;
}

@media (max-width: 992px) {
  .hero .container {
    flex-direction: column;
  }
  
  .hero-content {
    padding-right: 0;
    margin-bottom: 3rem;
    text-align: center;
  }
  
  .hero-buttons {
    justify-content: center;
  }
  
  .hero h1 {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .cta h2 {
    font-size: 2rem;
  }
}
</style>
