import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../stores/user';
import { useClienteStore } from '../stores/cliente';
import Home from '../views/Home.vue';
import Dashboard from '../views/Dashboard.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Cookies from 'js-cookie';
import Pipelines from '../views/Pipelines.vue';

const routes = [
  {
    path: '/dashboard',
    name: 'DashboardAll',
    meta: { noSidebar: false },
    component: Home,
    beforeEnter: async (to, from, next) => {
      const token = Cookies.get('token');
      const userStore = useUserStore(); // Instancia a store
      if (token) {
        try {
          const response = await fetch("/api/token_check", {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });
          const data = await response.json();
          if (data.valid) {
            console.log('Token validado');
            userStore.setUsername(data.username); // Salva o username na store
            next();
          } else {
            next('/login');
          }
        } catch (error) {
          console.error("Erro ao verificar o token:", error);
          next('/login');
        }
      } else {
        next('/login');
      }
    },
  },
  {
    path: '/dashboard/:token',
    name: 'Dashboard',
    meta: { noSidebar: false },
    component: Dashboard,
  },  
  {
    path: '/dashboard/:token/pipelines',
    name: 'Pipelines',
    meta: { noSidebar: false },
    component: Pipelines,
  },  
  {
    path: '/login',
    name: 'Login',
    meta: { noSidebar: true },
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    meta: { noSidebar: true },
    component: Register,
  },
];

const router = createRouter({
  history: createWebHistory("/"),
  routes,
});

export default router;
