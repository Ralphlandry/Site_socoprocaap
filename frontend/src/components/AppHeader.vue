<template>
  <header class="header" :class="{ scrolled: isScrolled }">
    <div class="container header-inner">
      <router-link to="/" class="logo">
        <img src="/LOGO (1).png" alt="SOCOPROCAAP" class="logo-img" />
        <span class="logo-text">SOCOPROCAAP</span>
      </router-link>

      <button class="menu-toggle" @click="menuOpen = !menuOpen" :aria-label="menuOpen ? 'Fermer le menu' : 'Ouvrir le menu'">
        <i :class="menuOpen ? 'fas fa-times' : 'fas fa-bars'"></i>
      </button>

      <nav class="nav" :class="{ open: menuOpen }">
        <router-link to="/" @click="menuOpen = false">Accueil</router-link>
        <router-link to="/equipe" @click="menuOpen = false">Équipe</router-link>
        <router-link to="/productions" @click="menuOpen = false">Productions</router-link>
        <router-link to="/blog" @click="menuOpen = false">Blog</router-link>
        <router-link to="/galerie" @click="menuOpen = false">Galerie</router-link>
        <router-link to="/statistiques" @click="menuOpen = false">Statistiques</router-link>
        <router-link to="/contact" @click="menuOpen = false">Contact</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isScrolled = ref(false)
const menuOpen = ref(false)

function onScroll() {
  isScrolled.value = window.scrollY > 50
}

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: transparent;
  transition: all 0.3s ease;
  padding: 15px 0;
}

.header.scrolled {
  background: var(--color-primary-dark);
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  padding: 10px 0;
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--color-white);
  font-family: var(--font-heading);
  font-size: 1.6rem;
  font-weight: 700;
}

.logo-img {
  width: 42px;
  height: 42px;
  object-fit: contain;
}

.nav {
  display: flex;
  align-items: center;
  gap: 30px;
}

.nav a {
  color: var(--color-white);
  font-weight: 600;
  font-size: 0.95rem;
  padding: 5px 0;
  position: relative;
  transition: opacity 0.3s;
}

.nav a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-secondary);
  transition: width 0.3s;
}

.nav a:hover::after,
.nav a.router-link-active::after {
  width: 100%;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  color: var(--color-white);
  font-size: 1.5rem;
  cursor: pointer;
}

@media (max-width: 768px) {
  .menu-toggle {
    display: block;
  }

  .nav {
    position: fixed;
    top: 0;
    right: -100%;
    width: 70%;
    height: 100vh;
    background: var(--color-primary-dark);
    flex-direction: column;
    justify-content: center;
    gap: 25px;
    transition: right 0.3s ease;
  }

  .nav.open {
    right: 0;
  }

  .nav a {
    font-size: 1.2rem;
  }
}
</style>
