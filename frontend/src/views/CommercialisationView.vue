<template>
  <div>
    <!-- PAGE HEADER -->
    <div class="page-header">
      <h1>Commercialisation</h1>
      <p>Nos services de commercialisation pour tous nos producteurs</p>
    </div>

    <!-- CONTENU PRINCIPAL -->
    <section class="section commercialisation-section">
      <div class="container">
        <div class="commercialisation-content">
          <div class="comm-text reveal reveal-up">
            <h2 class="section-title">Notre service de commercialisation</h2>
            <p class="intro-text">
              Nous assurons la commercialisation de l'ensemble des produits de nos membres sur les marchés nationaux et internationaux, garantissant des prix justes et compétitifs pour chaque producteur de la coopérative.
            </p>
          </div>

          <div class="comm-images-grid reveal reveal-up" style="--delay:100ms">
            <div class="comm-image-card">
              <img src="/WhatsApp Image 2026-04-14 at 13.41.36.jpeg" alt="Commercialisation 1" class="comm-img" />
            </div>
            <div class="comm-image-card">
              <img src="/WhatsApp Image 2026-04-14 at 13.41.37.jpeg" alt="Commercialisation 2" class="comm-img" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CARACTÉRISTIQUES -->
    <section class="section features-section">
      <div class="container">
        <h2 class="section-title reveal reveal-up">Nos Avantages</h2>
        <div class="features-grid">
          <div class="feature-card reveal reveal-up" style="--delay:0ms">
            <div class="feature-icon">
              <i class="fas fa-handshake"></i>
            </div>
            <h3>Partenariats Directs</h3>
            <p>Nous tissons des relations durables avec les acheteurs locaux et internationaux</p>
          </div>
          <div class="feature-card reveal reveal-up" style="--delay:100ms">
            <div class="feature-icon">
              <i class="fas fa-scale-balanced"></i>
            </div>
            <h3>Prix Justes</h3>
            <p>Nous garantissons des prix rémunérateurs pour chaque producteur membre</p>
          </div>
          <div class="feature-card reveal reveal-up" style="--delay:200ms">
            <div class="feature-icon">
              <i class="fas fa-globe"></i>
            </div>
            <h3>Marchés Diversifiés</h3>
            <p>Accès aux marchés nationaux et internationaux pour vos produits</p>
          </div>
        </div>
      </div>
    </section>

    <!-- PARTENAIRES -->
    <section class="section partenaires-section">
      <div class="container">
        <h2 class="section-title reveal reveal-up">Nos Partenaires</h2>
        <p class="partenaires-intro reveal reveal-up">
          Dans le cadre de nos activités de commercialisation des fèves de cacao, nous collaborons avec un vaste réseau de partenaires engagés dans la valorisation des fèves de cacao. Nous assurons une chaîne d'approvisionnement efficace, garantissant la qualité, la traçabilité et la compétitivité de nos produits sur le marché national et international.
        </p>
        <div class="partenaires-list" v-if="partenaires.length">
          <div class="partenaire-item reveal reveal-up" v-for="(partenaire, i) in partenaires" :key="partenaire.id" :style="'--delay:' + (i * 100) + 'ms'">
            <div class="partenaire-logo">
              <img v-if="partenaire.image" :src="partenaire.image" :alt="partenaire.nom" class="partenaire-img" />
              <div v-else class="partenaire-placeholder"><i class="fas fa-building"></i></div>
            </div>
            <div class="partenaire-info">
              <h3>{{ partenaire.nom }}</h3>
              <p>{{ partenaire.description }}</p>
            </div>
          </div>
        </div>
        <div v-else class="no-partenaires">
          <p>Nos partenaires seront bientôt disponibles</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '../api'

const partenaires = ref([])

let scrollObserver = null

function initScrollAnimations() {
  const els = document.querySelectorAll('.reveal')
  scrollObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target
        const delay = el.style.getPropertyValue('--delay') || '0ms'
        setTimeout(() => {
          el.classList.add('revealed')
        }, parseInt(delay) || 0)
        scrollObserver.unobserve(el)
      }
    })
  }, { threshold: 0.12 })
  els.forEach(el => scrollObserver.observe(el))
}

onMounted(async () => {
  setTimeout(initScrollAnimations, 200)

  try {
    const res = await api.get('/partenaires/')
    partenaires.value = res.data
  } catch {
    // API might not be available yet
  }
})

onUnmounted(() => {
  if (scrollObserver) scrollObserver.disconnect()
})
</script>

<style scoped>
.page-header {
  background: url('/caco3.jpg') center/cover no-repeat;
  color: var(--color-white);
  padding: 120px 0 60px;
  text-align: center;
  position: relative;
  margin-top: 60px;
}

.page-header::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(62, 39, 35, 0.75);
}

.page-header h1,
.page-header p {
  position: relative;
  z-index: 1;
}

.page-header h1 {
  font-family: var(--font-heading);
  font-size: 2.8rem;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.commercialisation-section {
  background: linear-gradient(135deg, #f5edd6 0%, #fdf8f0 100%);
}

.commercialisation-content {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.comm-text {
  max-width: 800px;
  margin: 0 auto;
}

.section-title {
  font-family: var(--font-heading);
  font-size: 2.5rem;
  color: var(--color-primary-dark);
  text-align: center;
  margin-bottom: 20px;
}

.intro-text {
  font-size: 1.1rem;
  color: var(--color-text-light);
  line-height: 1.8;
  text-align: center;
  background: var(--color-white);
  padding: 30px;
  border-radius: 12px;
  box-shadow: var(--shadow);
  border-left: 5px solid var(--color-secondary);
}

.comm-images-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  max-width: 900px;
  margin: 0 auto;
}

.comm-image-card {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  transition: transform 0.3s ease;
}

.comm-image-card:hover {
  transform: translateY(-8px);
}

.comm-img {
  width: 100%;
  height: 300px;
  object-fit: cover;
  display: block;
}

.features-section {
  background: var(--color-white);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 50px;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

.feature-card {
  background: linear-gradient(135deg, #f5edd6 0%, #fdf8f0 100%);
  padding: 30px;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s;
  border: 1px solid rgba(200, 137, 26, 0.2);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
  border-color: var(--color-secondary);
}

.feature-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-secondary), var(--color-secondary-light));
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  font-size: 2rem;
  color: var(--color-white);
}

.feature-card h3 {
  font-family: var(--font-heading);
  font-size: 1.3rem;
  color: var(--color-primary-dark);
  margin-bottom: 12px;
}

.feature-card p {
  color: var(--color-text-light);
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Animations */
.reveal {
  opacity: 0;
  transition: opacity 0.65s ease, transform 0.65s ease;
}

.reveal-up {
  transform: translateY(40px);
}

.reveal.revealed {
  opacity: 1;
  transform: none;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    padding: 80px 0 50px;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .comm-images-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .comm-img {
    height: 250px;
  }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }

  .feature-card {
    padding: 20px;
  }

  .feature-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }

  .feature-card h3 {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .page-header {
    padding: 60px 0 40px;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .comm-img {
    height: 200px;
  }
}

/* PARTENAIRES SECTION */
.partenaires-section {
  background: var(--color-white);
  padding: 80px 20px;
}

.partenaires-intro {
  max-width: 900px;
  margin: 0 auto 60px;
  font-size: 1rem;
  color: var(--color-text-light);
  line-height: 1.8;
  text-align: justify;
  opacity: 0;
}

.partenaires-list {
  display: flex;
  flex-direction: column;
  gap: 30px;
  max-width: 1000px;
  margin: 0 auto;
}

.partenaire-item {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 30px;
  align-items: flex-start;
  background: var(--color-white);
  border: 1px solid rgba(200, 137, 26, 0.15);
  border-radius: 14px;
  padding: 25px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: all 0.3s ease;
  opacity: 0;
}

.partenaire-item:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  border-color: var(--color-secondary);
  transform: translateY(-4px);
}

.partenaire-logo {
  width: 220px;
  height: 140px;
  background: #f0f4f8;
  border-radius: 10px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.partenaire-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.partenaire-item:hover .partenaire-img {
  transform: scale(1.05);
}

.partenaire-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #cbd5e1;
  font-size: 2.5rem;
}

.partenaire-info {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.partenaire-info h3 {
  font-family: var(--font-heading);
  font-size: 1.4rem;
  color: var(--color-primary-dark);
  margin-bottom: 15px;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.partenaire-info p {
  color: var(--color-text-light);
  font-size: 0.95rem;
  line-height: 1.7;
  text-align: justify;
  margin: 0;
}

.no-partenaires {
  text-align: center;
  padding: 60px 20px;
  color: var(--color-text-light);
  font-size: 1.1rem;
}

@media (max-width: 900px) {
  .partenaire-item {
    grid-template-columns: 150px 1fr;
    gap: 20px;
    padding: 20px;
  }

  .partenaire-logo {
    width: 150px;
    height: 120px;
  }

  .partenaire-info h3 {
    font-size: 1.2rem;
  }

  .partenaire-info p {
    font-size: 0.9rem;
  }
}

@media (max-width: 768px) {
  .partenaires-list {
    gap: 20px;
  }

  .partenaire-item {
    grid-template-columns: 1fr;
    gap: 15px;
    padding: 18px;
  }

  .partenaire-logo {
    width: 100%;
    height: 200px;
  }

  .partenaire-info h3 {
    font-size: 1.1rem;
  }

  .partenaire-info p {
    font-size: 0.9rem;
  }

  .partenaires-intro {
    font-size: 0.95rem;
  }
}

@media (max-width: 480px) {
  .partenaire-item {
    padding: 15px;
    gap: 12px;
  }

  .partenaire-logo {
    height: 160px;
  }

  .partenaire-info h3 {
    font-size: 1rem;
    margin-bottom: 10px;
  }

  .partenaire-info p {
    font-size: 0.85rem;
  }
}</style>
