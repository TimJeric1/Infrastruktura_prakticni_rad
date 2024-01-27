<template>
    <div>
      <h2>User Profile</h2>
      <p>Name: {{ currentUser.name }}</p>
      <p>Email: {{ currentUser.email }}</p>
      <!-- Add more fields as needed -->
      
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useUserStore } from '../store';
  import { useRouter } from 'vue-router'; // Import the useRouter function
  
  const userStore = useUserStore();
  const router = useRouter(); // Create a router instance
  
  // Use a ref to track the current user
  const currentUser = ref(userStore.user);
  
  // Logout method
  const logout = () => {
    userStore.logout();
    router.push('/vue/login'); // Navigate back to the login page
  };
  </script>
  
  <style lang="scss" scoped>
  /* Add your styles here */
  </style>
  