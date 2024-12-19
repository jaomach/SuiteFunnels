<template>
  <div v-if="username">
    <h2 class="text-s mb-1 opacity-40">Visualizando pipelines de: {{ username }}</h2>
    <h1 class="text-5xl font-bold mb-8">Suas <span class="text-primary-color">Pipelines</span></h1>
    <ul role="list" class="space-y-3">
      <li v-if="pipelines && pipelines.length === 0" class="text-gray-500">
        Nenhuma pipeline encontrada.
      </li>
      <li v-for="pipeline in pipelines" :key="pipeline.id" class="flex flex-col overflow-hidden rounded-md bg-white px-6 py-8 border-gray-200 border">
        <span>{{ pipeline.nome }}</span>
        <a class="w-min text-primary-color" :href="`${pipeline.id}`">Acessar</a>
      </li>
    </ul>
  </div>
  <div v-else>
    <p>Carregando...</p>
  </div>
</template>

<script>
import { useClienteStore } from '../stores/cliente';
import Cookies from 'js-cookie';

export default {
  name: 'Pipelines',
  data() {
    return {
      pipelines: [],
    }
  },
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
    await this.callPipelines(this.$route);
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

    async callPipelines(route) {
      const tokenFromUrl = route.params.token;
  
      if (!tokenFromUrl) {
        console.error('Tokens não encontrados');
        this.$router.push('/login');
        return;
      }
  
      try {
        const response = await fetch("/api/call_pipelines", {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${tokenFromUrl}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          if (data.pipelines && Array.isArray(data.pipelines)) {
            this.pipelines = data.pipelines.map(pipeline => {
              return {
                id: pipeline[0],
                nome: pipeline[2],
              };
            })
          }
        } else {
        }
      } catch (error) {
        console.error("Erro ao verificar o token:", error);
      }
    },
  },
};
</script>
