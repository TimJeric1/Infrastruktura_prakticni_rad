<template>
  <div>
    <h1>Data from Express Server:</h1>
    <ul>
      <li v-for="item in data" :key="item.id">{{ item.name }}</li>
    </ul>
  </div>
</template>



<script setup>
import { ref, onMounted } from 'vue';
import axios from 'redaxios';

const data = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get('http://dujetim.test/express/read-categories');
    data.value = response.data;
  } catch (error) {
    console.error('Error fetching data:', error.message);
  }
});
</script>

<style scoped>
</style>
