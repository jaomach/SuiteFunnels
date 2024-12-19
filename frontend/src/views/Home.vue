<template>
  <div>
    <h1 class="text-5xl font-bold">Bem-vinda, <span class="text-primary-color">{{ username }}</span></h1>
  </div>
</template>

<script>
import { useUserStore } from '../stores/user';

export default {
  name: 'Home',
  computed: {
    username() {
      const userStore = useUserStore();
      return userStore.username;
    },
  },
};

</script>
