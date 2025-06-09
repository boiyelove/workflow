<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="app-footer">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-6">
          <p class="mb-0">
            &copy; {{ currentYear }} Workflow. All rights reserved.
          </p>
        </div>
        <div class="col-md-6 text-md-end">
          <p class="mb-0">
            <a href="#">Terms</a>
            <span class="mx-2">·</span>
            <a href="#">Privacy</a>
            <span class="mx-2">·</span>
            <a href="#">Help</a>
          </p>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  padding: 1rem 1.5rem;
  background-color: #fff;
  border-top: 1px solid #e9ecef;
}

.app-footer a {
  color: #495057;
  text-decoration: none;
}

.app-footer a:hover {
  color: #0d6efd;
}
</style>
