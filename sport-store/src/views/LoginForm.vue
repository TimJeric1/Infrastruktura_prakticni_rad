<template>
  <div class="login-form-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label>Email:</label>
        <input v-model="email" type="email" required />
      </div>

      <div class="form-group">
        <label>Password:</label>
        <input v-model="password" type="password" required />
      </div>

      <button type="submit">Login</button>
      <br />
      <br />

      <button type="button" @click="toRegister">Go To Register</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useUserStore } from '../store';

const router = useRouter();

const email = ref('');
const password = ref('');

const userStore = useUserStore();

// Login method
const login = () => {
  axios
    .post('http://dujetim.test/express/login', {
      email: email.value,
      password: password.value
    })
    .then((response) => {
      // Check the response
      console.log('Login successful', response.data);
      // Set user in store
      userStore.login(response.data.user);
      // Redirect
      router.push('/vue/home');
    })
    .catch((error) => {
      console.error('Error during login', error.response.data);
    });
};

const toRegister = () => {
  router.push('/vue/register');
};
</script>

<style scoped>
.login-form-container {
  max-width: 300px; /* Adjust the width as needed */
  margin: 0 auto; /* Center the form on the page */
}

.form-group {
  margin-bottom: 15px; /* Add some spacing between form groups */
}
</style>
