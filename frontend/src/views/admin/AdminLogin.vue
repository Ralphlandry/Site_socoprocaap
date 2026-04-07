<template>
  <div class="login-page">
    <!-- Background decoration -->
    <div class="bg-deco">
      <div class="bg-circle bg-circle-1"></div>
      <div class="bg-circle bg-circle-2"></div>
    </div>

    <div class="login-card">
      <div class="login-brand">
        <img src="/LOGO (1).png" alt="SOCOPROCAAP" class="brand-logo" />
        <h1>SOCOPROCAAP</h1>
        <p>Espace d'administration</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <transition name="alert">
          <div v-if="error" class="login-error">
            <i class="fas fa-exclamation-circle"></i> {{ error }}
          </div>
        </transition>

        <div class="field">
          <label for="username">Identifiant</label>
          <div class="input-wrap">
            <i class="fas fa-user input-icon"></i>
            <input id="username" v-model="username" type="text" required placeholder="Nom d'utilisateur" autocomplete="username" />
          </div>
        </div>

        <div class="field">
          <label for="password">Mot de passe</label>
          <div class="input-wrap">
            <i class="fas fa-lock input-icon"></i>
            <input id="password" v-model="password" type="password" required placeholder="••••••••" autocomplete="current-password" />
          </div>
        </div>

        <button type="submit" class="btn-login" :disabled="loading">
          <i v-if="loading" class="fas fa-spinner fa-spin"></i>
          <span v-else><i class="fas fa-sign-in-alt"></i> Se connecter</span>
        </button>
      </form>

      <router-link to="/" class="back-link">
        <i class="fas fa-arrow-left"></i> Retour au site public
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push('/admin')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Identifiants incorrects. Vérifiez vos informations.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.bg-deco { position: absolute; inset: 0; pointer-events: none; }
.bg-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.08;
}
.bg-circle-1 {
  width: 500px; height: 500px;
  background: #059669;
  top: -150px; right: -100px;
}
.bg-circle-2 {
  width: 350px; height: 350px;
  background: #0f172a;
  bottom: -100px; left: -80px;
}

.login-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 40px 36px;
  width: 100%;
  max-width: 400px;
  position: relative;
  z-index: 1;
  box-shadow: 0 10px 40px rgba(0,0,0,0.08);
}

.login-brand {
  text-align: center;
  margin-bottom: 32px;
}
.brand-logo {
  width: 64px; height: 64px;
  border-radius: 16px;
  object-fit: cover;
  border: 3px solid #d1fae5;
  margin-bottom: 14px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
.login-brand h1 {
  font-size: 1.3rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 4px;
  letter-spacing: -0.02em;
}
.login-brand p {
  color: #94a3b8;
  font-size: 0.85rem;
}

.login-error {
  background: #fef2f2;
  border: 1px solid #fca5a5;
  color: #dc2626;
  padding: 10px 14px;
  border-radius: 10px;
  margin-bottom: 18px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.field { margin-bottom: 18px; }
.field label {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  color: #475569;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.input-wrap { position: relative; }
.input-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #cbd5e1;
  font-size: 0.85rem;
  pointer-events: none;
}
.input-wrap input {
  width: 100%;
  padding: 11px 14px 11px 36px;
  border: 1px solid #e2e8f0;
  border-radius: 9px;
  font-size: 0.95rem;
  color: #0f172a;
  background: #fff;
  transition: border-color 0.15s, box-shadow 0.15s;
  box-sizing: border-box;
}
.input-wrap input:focus {
  outline: none;
  border-color: #059669;
  box-shadow: 0 0 0 3px rgba(5,150,105,0.1);
}
.input-wrap input::placeholder { color: #cbd5e1; }

.btn-login {
  width: 100%;
  padding: 13px;
  background: #059669;
  color: #fff;
  border: none;
  border-radius: 9px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s, transform 0.1s;
  margin-top: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.btn-login:hover { background: #047857; }
.btn-login:active { transform: scale(0.98); }
.btn-login:disabled { opacity: 0.55; cursor: not-allowed; }

.back-link {
  display: block;
  text-align: center;
  margin-top: 22px;
  color: #94a3b8;
  font-size: 0.82rem;
  text-decoration: none;
  transition: color 0.15s;
}
.back-link:hover { color: #059669; }

.alert-enter-active, .alert-leave-active { transition: opacity 0.2s, transform 0.2s; }
.alert-enter-from, .alert-leave-to { opacity: 0; transform: translateY(-6px); }

@media (max-width: 440px) {
  .login-card { padding: 28px 20px; }
}
</style>
