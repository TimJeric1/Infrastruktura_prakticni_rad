<template>
  <div class="register-form-container">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label>Name:</label>
        <input v-model="name" type="text" required />
      </div>

      <div class="form-group">
        <label>Email:</label>
        <input v-model="email" type="email" required />
      </div>

      <div class="form-group">
        <label>Password:</label>
        <input v-model="password" type="password" required />
      </div>

      <button type="submit">Register</button>
    </form>
    <br />
    <button type="button" @click="toLogin">Go To Login</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useUserStore } from '../store';

const router = useRouter();
const userStore = useUserStore();

const name = ref('');
const email = ref('');
const password = ref('');

// Register method
const register = async () => {
  try {
    const response = await axios.post('http://dujetim.test/express/register', {
      name: name.value,
      email: email.value,
      password: password.value
    });

    // Check the response status and show a message or redirect if needed
    if (response.data.status === 'success') {
      console.log('Registration successful', response.data);

      userStore.login(response.data.user);
      // Redirect
      router.push('/vue/home');
    } else {
      console.error(`Registration failed: ${response.data.message}`);
    }
  } catch (error) {
    console.error(`Error during registration: ${error.message}`);
    // Handle network or other errors
  }
};

const toLogin = () => {
  router.push('/vue/login');
};
</script>

<style scoped>
.register-form-container {
  max-width: 300px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 15px;
}
</style>
