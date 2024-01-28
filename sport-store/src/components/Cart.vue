<template>
  <div class="cart">
    <h2>Your Cart</h2>
    <ul>
      <li v-for="item in cartItems" :key="item.id">
        {{ item.quantity }} x {{ item.name }} - ${{
          item.price * item.quantity
        }}
        <span class="remove" @click="removeItem(item.id)">X</span>
      </li>
    </ul>
    <p>Total: ${{ total }}</p>
    <button @click="createOrder">Create Order</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCartStore, useUserStore } from '../store';
import axios from 'axios';
const emit = defineEmits(['dont-show']);

const currentUser = useUserStore().user;
const cartItems = useCartStore().cartItems;
const cartStore = useCartStore();


// Computed property to calculate the total cost of items in the cart
const total = computed(() => {
  return cartItems.reduce((acc, item) => acc + item.price * item.quantity, 0);
});

const removeItem = (productId) => {
  cartStore.removeFromCart(productId);
  if (useCartStore().cartItems.length == 0) {
    emit('dont-show');
  }
};

// Method to create an order
const createOrder = async () => {
  try {
    console.log(cartItems)
    const user_id = currentUser.user_id;
    const products = cartItems.map((item) => ({
      product_id: item.id,
      quantity: item.quantity,
      price: Number(item.price)
    }));

    // Call the Express endpoint to create an order
    const response = await axios.post(
      'http://dujetim.test/express/create-order',
      { user_id, products }
    );
    console.log('Order created successfully:', response.data);
    emit('dont-show');
    cartStore.emptyCart();
  } catch (error) {
    console.error('Error creating order:', error.message);
  }
};
</script>

<style scoped>
.cart {
  border: 1px solid #ddd;
  padding: 10px;
  width: 500px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 5px;
}

.remove {
  cursor: pointer;
}
</style>
