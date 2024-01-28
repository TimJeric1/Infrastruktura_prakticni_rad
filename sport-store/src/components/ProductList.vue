<template>
  <div>
    <h2>Product List</h2>
    <div class="product-list">
      <ProductCard
        v-for="product in products"
        :key="product.key"
        :product="product"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import ProductCard from './ProductCard.vue';
const props = defineProps(['products']);

console.log(props.products)

onMounted(()=>{
  console.log(props.products)
})
</script>

<style scoped>
.product-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  justify-content: center;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}
</style>
