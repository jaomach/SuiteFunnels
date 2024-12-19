<template>
  <div class="form-container">
    <h2>Login</h2>
    <form id="loginForm">
      <div class="error-message" id="errorMessage"></div>
      <label for="email">E-mail</label>
      <input autocomplete="email" type="email" id="email" name="email" placeholder="Digite seu e-mail" required>

      <label for="password">Senha</label>
      <input autocomplete="current-password" type="password" id="password" name="password" placeholder="Digite sua senha" required>

      <button type="button" @click="loginUser">Entrar</button>
    </form>
  </div>
</template>

<script>
import { loginUser } from '../assets/js/loginUtils'; // Ajuste o caminho, se necessário
export default {
  name: 'Login',
  methods: {
    loginUser,
  },
};
</script>

<style scoped>
@import '../assets/styles/form.css';
</style>
