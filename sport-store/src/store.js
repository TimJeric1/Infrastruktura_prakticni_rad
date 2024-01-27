// store.js
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
