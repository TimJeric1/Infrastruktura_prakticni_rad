import { createRouter, createWebHistory } from 'vue-router';
import Login from './views/LoginForm.vue';
import Register from './views/RegisterForm.vue';
import Home from './views/Home.vue';
import { useUserStore } from './store';

const routes = [
  { path: '/vue/', redirect: '/vue/login' },
  { path: '/vue/login', component: Login },
  { path: '/vue/register', component: Register },
  {
    path: '/vue/home',
    component: Home,
    // Add a beforeEnter guard to check if the user is logged in
    beforeEnter: (to, from, next) => {
      const userStore = useUserStore();
      if (userStore.isLoggedIn) {
        // User is logged in, allow access to the route
        next();
      } else {
        // User is not logged in, redirect to login page
        next('/vue/login');
      }
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
