<template>
  <div class="product-card">
    <h3>{{ product.values.name }}</h3>
    <p class="description">
      {{ truncateDescription(product.values.description, 100) }}
    </p>
    <p>Price: ${{ product.values.price }}</p>
    <button @click="addToCart(product)">Add to Cart</button>
  </div>
</template>

<script setup>
import { useCartStore } from '../store';
const props = defineProps(['product']);

const truncateDescription = (description, maxLength) => {
  if (description.length > maxLength) {
    return `${description.slice(0, maxLength)}...`;
  }
  return description;
};

const addToCart = (product) => {
  // Emit an event to notify the parent component about the product being added to the cart
  useCartStore().addToCart(product);
};
</script>

<style scoped>
.product-card {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.description {
  max-height: 3em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

button {
  margin-top: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 15px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
}
</style>
