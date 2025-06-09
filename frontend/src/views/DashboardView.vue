<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isLoading = ref(true)
const stats = ref({
  projects: 0,
  tasks: 0,
  completedTasks: 0,
  teams: 0
})

onMounted(async () => {
  try {
    // Fetch dashboard data from API
    // This is a placeholder - replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 500))
    
    stats.value = {
      projects: 12,
      tasks: 48,
      completedTasks: 32,
      teams: 5
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="dashboard-view">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="mb-0">Dashboard</h1>
      <div>
        <button class="btn btn-primary">
          <font-awesome-icon icon="plus" class="me-2" />
          New Project
        </button>
      </div>
    </div>
    
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading dashboard data...</p>
    </div>
    
    <div v-else>
      <!-- Stats Cards -->
      <div class="row">
        <div class="col-md-3">
          <div class="card stat-card">
            <div class="card-body">
              <h5 class="card-title">Projects</h5>
              <div class="stat-value">{{ stats.projects }}</div>
              <div class="stat-icon">
                <font-awesome-icon icon="project-diagram" />
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-3">
          <div class="card stat-card">
            <div class="card-body">
              <h5 class="card-title">Tasks</h5>
              <div class="stat-value">{{ stats.tasks }}</div>
              <div class="stat-icon">
                <font-awesome-icon icon="tasks" />
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-3">
          <div class="card stat-card">
            <div class="card-body">
              <h5 class="card-title">Completed</h5>
              <div class="stat-value">{{ stats.completedTasks }}</div>
              <div class="stat-icon">
                <font-awesome-icon icon="check-circle" />
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-3">
          <div class="card stat-card">
            <div class="card-body">
              <h5 class="card-title">Teams</h5>
              <div class="stat-value">{{ stats.teams }}</div>
              <div class="stat-icon">
                <font-awesome-icon icon="users" />
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Recent Projects -->
      <div class="card mt-4">
        <div class="card-header">
          <h5 class="mb-0">Recent Projects</h5>
        </div>
        <div class="card-body">
          <table class="table">
            <thead>
              <tr>
                <th>Project Name</th>
                <th>Status</th>
                <th>Progress</th>
                <th>Due Date</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Website Redesign</td>
                <td><span class="badge bg-success">In Progress</span></td>
                <td>
                  <div class="progress">
                    <div class="progress-bar" role="progressbar" style="width: 75%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>
                  </div>
                </td>
                <td>Jun 15, 2025</td>
              </tr>
              <tr>
                <td>Mobile App Development</td>
                <td><span class="badge bg-warning">Planning</span></td>
                <td>
                  <div class="progress">
                    <div class="progress-bar" role="progressbar" style="width: 30%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"></div>
                  </div>
                </td>
                <td>Aug 20, 2025</td>
              </tr>
              <tr>
                <td>Marketing Campaign</td>
                <td><span class="badge bg-info">Review</span></td>
                <td>
                  <div class="progress">
                    <div class="progress-bar" role="progressbar" style="width: 60%" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100"></div>
                  </div>
                </td>
                <td>Jul 5, 2025</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Upcoming Tasks -->
      <div class="card mt-4">
        <div class="card-header">
          <h5 class="mb-0">Your Tasks</h5>
        </div>
        <div class="card-body">
          <ul class="list-group">
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <h6 class="mb-0">Design homepage mockup</h6>
                <small class="text-muted">Website Redesign</small>
              </div>
              <span class="badge bg-danger">Due Today</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <h6 class="mb-0">Create user flow diagrams</h6>
                <small class="text-muted">Mobile App Development</small>
              </div>
              <span class="badge bg-warning">Due in 3 days</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <h6 class="mb-0">Review content strategy</h6>
                <small class="text-muted">Marketing Campaign</small>
              </div>
              <span class="badge bg-info">Due in 1 week</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-view {
  padding: 1.5rem;
}

.stat-card {
  position: relative;
  overflow: hidden;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 600;
  margin-top: 0.5rem;
}

.stat-icon {
  position: absolute;
  right: 1rem;
  bottom: 1rem;
  font-size: 3rem;
  opacity: 0.2;
}

.progress {
  height: 8px;
  margin-top: 0.5rem;
}

.badge {
  padding: 0.5em 0.75em;
}

.list-group-item {
  padding: 1rem;
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

.me-2 {
  margin-right: 0.5rem;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin-right: -0.75rem;
  margin-left: -0.75rem;
}

.col-md-3 {
  flex: 0 0 25%;
  max-width: 25%;
  padding-right: 0.75rem;
  padding-left: 0.75rem;
}

@media (max-width: 768px) {
  .col-md-3 {
    flex: 0 0 50%;
    max-width: 50%;
    margin-bottom: 1.5rem;
  }
}

@media (max-width: 576px) {
  .col-md-3 {
    flex: 0 0 100%;
    max-width: 100%;
  }
}
</style>
