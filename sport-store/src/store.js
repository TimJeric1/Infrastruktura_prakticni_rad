import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isLoggedIn: false
  }),

  actions: {
    login(user) {
      this.user = user;
      this.isLoggedIn = true;
    },

    logout() {
      this.user = null;
      this.isLoggedIn = false;
    }
  }
});

export const useCartStore = defineStore('cart', {
  state: () => ({
    cartItems: []
  }),

  actions: {
    addToCart(product) {
      const existingProduct = this.cartItems.find(
        (item) => item.id === product.key
      );

      if (existingProduct) {
        existingProduct.quantity += 1;
      } else {
        this.cartItems.push({
          id: product.key,
          name: product.values.name,
          quantity: 1,
          price: product.values.price
        });
      }
    },

    removeFromCart(productId) {
      const index = this.cartItems.findIndex((item) => item.id === productId);

      if (index !== -1) {
        this.cartItems.splice(index, 1);
      }
    },

    emptyCart() {
      this.cartItems = [];
    }
  }
});
