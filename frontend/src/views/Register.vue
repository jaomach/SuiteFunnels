<template>
  <div class="form-container">
      <h2>Cadastro</h2>
      <form id="registerForm">
          <div class="error-message" id="errorMessage"></div>
          <label for="username">Nome</label>
          <input type="text" id="username" name="username" placeholder="Digite seu nome" required>

          <label for="email">E-mail</label>
          <input type="email" id="email" name="email" placeholder="Digite seu e-mail" required>

          <label for="password">Senha</label>
          <input type="password" id="password" name="password" placeholder="Digite sua senha" required>

          <button type="button" @click="registerUser">Cadastrar</button>
      </form>
  </div>
</template>

<script>
import { registerUser } from '../assets/js/registerUtils'; // Ajuste o caminho, se necessário
export default {
  name: 'Register',
  methods: {
    registerUser,
  },
};
</script>

<style scoped>
@import '../assets/styles/form.css';
</style>
