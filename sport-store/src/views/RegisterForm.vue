<template>
    <div>
      <h2>Register</h2>
      <form @submit.prevent="register">
        <label>Name:
          <input v-model="name" type="text" required>
        </label>
        <label>Email:
          <input v-model="email" type="email" required>
        </label>
        <label>Password:
          <input v-model="password" type="password" required>
        </label>
        <button type="submit">Register</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import { useUserStore } from '../store';

  const router = useRouter();
  const userStore = useUserStore();
  // Using refs for reactive properties
  const name = ref('');
  const email = ref('');
  const password = ref('');
  
  // Register method
  const register = async () => {
    try {
      const response = await axios.post('http://dujetim.test/express/register', {
        name: name.value,
        email: email.value,
        password: password.value,
      });
  
      // Check the response status and show a message or redirect if needed
      if (response.data.status === 'success') {
        console.log('Registration successful', response.data);

        userStore.login(response.data.user);
        // Redirect
        router.push('/vue/home');
      } else {
        console.error(`Registration failed: ${response.data.message}`);
        // Show an error message to the user
      }
    } catch (error) {
      console.error(`Error during registration: ${error.message}`);
      // Handle network or other errors
    }
  };
  </script>
  