<template>
  <div :class="appClass" id="app">
    <Sidebar v-if="!$route.meta.noSidebar" />
    <div id="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';

export default {
  components: {
    Sidebar,
  },
  computed: {
    appClass() {
      return this.$route.meta.noSidebar ? 'no-sidebar' : 'with-sidebar';
    },
  },
};
</script>

<style scoped>
#app {
  display: flex;
  min-height: 100vh;
}

.with-sidebar #main-content {
  flex: 1;
  padding: 40px 50px;
  margin-left: 290px; /* Remove o espaço reservado */
}

.no-sidebar #main-content {
  margin-left: 0; /* Remove o espaço reservado */
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0px;
}
</style>
