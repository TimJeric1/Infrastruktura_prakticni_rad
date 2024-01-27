<template>
    <div>
      <h2>Login</h2>
      <form @submit.prevent="login">
        <label>Email:
          <input v-model="email" type="email" required>
        </label>
        <label>Password:
          <input v-model="password" type="password" required>
        </label>
        <button type="submit">Login</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import { useUserStore } from '../store';

  const router = useRouter();
  // Using refs for reactive properties
  const email = ref('');
  const password = ref('');

  const userStore = useUserStore();
  
  // Login method
  const login = () => {
    // Example API call using axios
    axios.post('http://dujetim.test/express/login', {
      email: email.value,
      password: password.value,
    })
      .then(response => {
        // Check the response
        console.log('Login successful', response.data);
        // Set user in store
        userStore.login(response.data.user);
        // Redirect
        router.push('/vue/home');
      })
      .catch(error => {
        console.error('Error during login', error.response.data);
      });
  };
  </script>
  