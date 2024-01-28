<template>
  <div class="app">
    <Header :user="currentUser" @toggle="toggleCart" />
    <div v-if="showCart" class="overlay" @click="closeCart">
      <Cart @click.stop @dont-show="closeCart" />
    </div>
    <ProductList :products="products" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCartStore } from '../store';
import axios from 'axios';
import ProductList from '../components/ProductList.vue';
import Header from '../components/Header.vue';
import Cart from '../components/Cart.vue';

const products = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get(
      'http://dujetim.test/express/read-products'
    );
    products.value = response.data;
  } catch (error) {
    console.error('Error fetching products:', error.message);
  }
});

const showCart = ref(false);

const toggleCart = () => {
  // Open the cart only if there are items in the cart
  if (useCartStore().cartItems.length > 0) {
    showCart.value = !showCart.value;
  }
};

const closeCart = () => {
  showCart.value = false;
};
</script>

<style lang="scss">
body,
html {
  margin: 0;
  padding: 0;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
