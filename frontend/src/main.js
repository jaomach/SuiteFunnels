import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import './tailwind.css';

const app = createApp(App);
app.use(createPinia());
app.use(router); // Registre o roteador no app
app.mount('#app');