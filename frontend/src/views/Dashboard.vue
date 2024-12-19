<template>
  <div v-if="username">
    <h1 class="text-5xl font-bold">Bem-vinda, <span class="text-primary-color">{{ username }}</span></h1>
  </div>
  <div v-else>
    <p>Carregando...</p>
  </div>
</template>

<script>
import { useClienteStore } from '../stores/cliente';
import Cookies from 'js-cookie';

export default {
  name: 'Dashboard',
  computed: {
    username() {
      const clienteStore = useClienteStore();
      return clienteStore.username;
    },
  },
  watch: {
    '$route'(to, from) {
      this.checkPermission(to);
    },
  },
  async mounted() {
    await this.checkPermission(this.$route);
  },
  methods: {
    async checkPermission(route) {
      const tokenFromUrl = route.params.token;
      const tokenFromCookie = Cookies.get('token');
      const clienteStore = useClienteStore();
  
      if (!tokenFromCookie || !tokenFromUrl) {
        console.error('Tokens não encontrados');
        this.$router.push('/login');
        return;
      }
  
      try {
        const response = await fetch("/api/check_cliente", {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${tokenFromCookie} ${tokenFromUrl}`,
          },
        });
        const data = await response.json();
        if (response.ok && data.valid) {
          clienteStore.setUsername(data.username_cliente);
        } else {
          this.$router.push('/login');
        }
      } catch (error) {
        console.error("Erro ao verificar o token:", error);
        this.$router.push('/login');
      }
    },
  },
};
</script>
