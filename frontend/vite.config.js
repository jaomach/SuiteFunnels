import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path'; // Certifique-se de incluir esta importação

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:5000',
    },
  },
  build: {
    outDir: '../backend/static/dist',  // Salva o build no diretório estático do Flask
    emptyOutDir: true,
  },
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
});
