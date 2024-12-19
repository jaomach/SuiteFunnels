import { defineStore } from 'pinia';

export const useClienteStore = defineStore('cliente', {
  state: () => ({
    username: null,
  }),
  actions: {
    setUsername(username) {
      this.username = username;
    },
  },
});