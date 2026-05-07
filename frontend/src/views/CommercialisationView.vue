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

    <!-- IMMATRICULATION -->
    <section class="section immatriculation-section">
      <div class="container">
        <div class="immatriculation-content reveal reveal-up">
          <div class="immatriculation-image">
            <img src="/immatriculation.jpeg" alt="Immatriculation SOCOPROCAAP" class="immatriculation-img" />
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
        
        <div v-if="partenaires.length" class="partenaires-list">
          <div
            class="partenaire-item"
            v-for="(partenaire, index) in partenaires"
            :key="partenaire.id"
            :class="{ reverse: index % 2 !== 0 }"
          >
            <div class="partenaire-visual">
              <img v-if="partenaire.image" :src="partenaire.image" :alt="partenaire.nom" />
              <div v-else class="partenaire-placeholder"><i class="fas fa-building"></i></div>
            </div>
            <div class="partenaire-info">
              <div class="partenaire-number">{{ String(index + 1).padStart(2, '0') }}</div>
              <h2>{{ partenaire.nom }}</h2>
              <p>{{ partenaire.description }}</p>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="fas fa-building"></i>
          <p>Nos partenaires seront bientôt disponibles.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
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
  try {
    const res = await api.get('/partenaires/')
    partenaires.value = res.data
    await nextTick()
    setTimeout(initScrollAnimations, 300)
  } catch {
    // API might not be available yet
    await nextTick()
    setTimeout(initScrollAnimations, 300)
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
  margin-top: 0;
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

.immatriculation-section {
  background: var(--color-white);
  padding: 60px 20px;
}

.immatriculation-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.immatriculation-image {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  transition: transform 0.3s ease;
}

.immatriculation-image:hover {
  transform: translateY(-8px);
}

.immatriculation-img {
  width: 100%;
  height: auto;
  max-height: 500px;
  object-fit: contain;
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

/* Immatriculation responsive */
@media (max-width: 768px) {
  .immatriculation-section {
    padding: 40px 20px;
  }

  .immatriculation-img {
    max-height: 300px;
  }
}

@media (max-width: 480px) {
  .immatriculation-section {
    padding: 30px 15px;
  }

  .immatriculation-img {
    max-height: 250px;
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
}

.partenaires-list {
  display: flex;
  flex-direction: column;
  gap: 60px;
  max-width: 1000px;
  margin: 0 auto;
}

.partenaire-item {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 50px;
  align-items: center;
}

.partenaire-item.reverse {
  direction: rtl;
}

.partenaire-item.reverse > * {
  direction: ltr;
}

.partenaire-visual img {
  width: 100%;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  height: 350px;
  object-fit: cover;
}

.partenaire-visual {
  overflow: hidden;
}

.partenaire-placeholder {
  width: 100%;
  height: 350px;
  background: #f0f4f8;
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #cbd5e1;
  font-size: 3rem;
  box-shadow: var(--shadow);
}

.partenaire-number {
  font-family: var(--font-heading);
  font-size: 3rem;
  color: var(--color-secondary);
  opacity: 0.5;
  font-weight: 700;
  margin-bottom: 5px;
}

.partenaire-info h2 {
  font-family: var(--font-heading);
  font-size: 1.8rem;
  color: var(--color-primary-dark);
  margin-bottom: 15px;
}

.partenaire-info p {
  color: var(--color-text-light);
  line-height: 1.8;
  font-size: 1rem;
}

.empty-state {
  text-align: center;
  padding: 60px 0;
  color: var(--color-text-light);
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 15px;
  color: var(--color-primary-light);
}

@media (max-width: 900px) {
  .partenaire-item,
  .partenaire-item.reverse {
    grid-template-columns: 1fr;
    direction: ltr;
  }

  .partenaire-visual img {
    height: 280px;
  }

  .partenaire-number {
    font-size: 2.5rem;
  }

  .partenaire-info h2 {
    font-size: 1.5rem;
  }
}

@media (max-width: 900px) {
  .partenaire-visual img {
    height: 220px;
  }

  .partenaire-number {
    font-size: 2rem;
  }

  .partenaire-info h2 {
    font-size: 1.3rem;
  }

  .partenaire-info p {
    font-size: 0.9rem;
  }
}

@media (max-width: 768px) {
  .partenaires-list {
    gap: 40px;
  }

  .partenaire-item,
  .partenaire-item.reverse {
    grid-template-columns: 1fr;
    direction: ltr;
    gap: 30px;
  }

  .partenaire-visual img {
    height: 250px;
  }

  .partenaire-number {
    font-size: 2.2rem;
  }

  .partenaire-info h2 {
    font-size: 1.4rem;
  }

  .partenaires-intro {
    text-align: left;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1.8rem;
  }

  .partenaires-list {
    gap: 30px;
  }

  .partenaire-visual img {
    height: 200px;
  }

  .partenaire-number {
    font-size: 1.8rem;
  }

  .partenaire-info h2 {
    font-size: 1.2rem;
  }

  .partenaire-info p {
    font-size: 0.85rem;
  }
}</style>
