<template>
  <header class="app-header">
    <div class="left-section">
      <button @click="logout">Logout</button>
    </div>
    <div class="center-section">
      <h1>Sport Store</h1>
    </div>
    <div class="right-section">
      <button @click="toggleCart">Cart</button>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useUserStore } from '../store';

const emit = defineEmits(['toggle']);

const userStore = useUserStore();
const router = useRouter();

// Logout method
const logout = () => {
  userStore.logout();
  router.push('/vue/login'); // Navigate back to the login page
};

const toggleCart = () => {
  emit('toggle');
};
</script>

<style scoped>
.app-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #242424;
  color: rgba(255, 255, 255, 0.87);
  margin: 0;
  box-sizing: border-box;
}

.left-section,
.right-section {
  display: flex;
  align-items: center;
}

.center-section {
  flex-grow: 1;
  text-align: center;
}
</style>
