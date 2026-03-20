<template>
  <div>
    <!-- HERO SECTION -->
    <section class="hero">
      <div class="hero-overlay"></div>
      <div class="container hero-content">
        <h1>Bienvenue chez <span>SOCOPROCAAP</span></h1>
        <p>Coopérative agropastorale spécialisée dans la production de cacao, maïs, gombo et l'élevage porcin. De la terre à votre table, nous cultivons l'excellence à Obala.</p>
        <div class="hero-buttons">
          <router-link to="/services" class="btn btn-primary">Nos Services</router-link>
          <router-link to="/contact" class="btn btn-outline">Nous Contacter</router-link>
        </div>
      </div>
    </section>

    <!-- À PROPOS -->
    <section class="section about">
      <div class="container">
        <div class="about-grid">
          <div class="about-image">
            <img src="/cacao.jpg" alt="Plantation de cacao SOCOPROCAAP" class="about-img" />
          </div>
          <div class="about-text">
            <h2 class="section-title" style="text-align:left">Qui sommes-nous ?</h2>
            <p>
              SOCOPROCAAP est une coopérative agropastorale basée à Obala, village Nkolndobo. 
              Nous sommes spécialisés dans la production de fèves de cacao, la culture du maïs et du gombo, 
              ainsi que l'élevage porcin. Fondée sur les valeurs de solidarité et de durabilité, 
              notre coopérative regroupe des centaines de producteurs passionnés.
            </p>
            <p>
              Nous accompagnons nos membres dans toutes les filières agropastorales, 
              de la plantation à la commercialisation, pour garantir des produits d'exception 
              reconnus sur les marchés locaux et internationaux.
            </p>
            <div class="stats" ref="statsRef">
              <div class="stat">
                <span class="stat-number">{{ animatedProducteurs }}+</span>
                <span class="stat-label">Producteurs</span>
              </div>
              <div class="stat">
                <span class="stat-number">{{ animatedTonnes }}</span>
                <span class="stat-label">Tonnes/an</span>
              </div>
              <div class="stat">
                <span class="stat-number">{{ animatedAnnees }}</span>
                <span class="stat-label">Ans d'expérience</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SERVICES APERÇU -->
    <section class="section services-preview" v-if="services.length">
      <div class="container">
        <h2 class="section-title">Nos Services</h2>
        <p class="section-subtitle">Découvrez ce que nous offrons à nos membres et partenaires</p>
        <div class="grid-3">
          <div class="service-card" v-for="service in services.slice(0, 3)" :key="service.id">
            <div class="service-icon">
              <i :class="service.icone || 'fas fa-leaf'"></i>
            </div>
            <h3>{{ service.titre }}</h3>
            <p>{{ service.description.substring(0, 120) }}...</p>
          </div>
        </div>
        <div style="text-align:center; margin-top:30px;">
          <router-link to="/services" class="btn btn-primary">Voir tous les services</router-link>
        </div>
      </div>
    </section>

    <!-- DERNIERS ARTICLES -->
    <section class="section latest-blog" v-if="latestPosts.length">
      <div class="container">
        <h2 class="section-title">Dernières Actualités</h2>
        <p class="section-subtitle">Restez informé des dernières nouvelles de notre coopérative</p>
        <div class="grid-3">
          <div class="card" v-for="post in latestPosts" :key="post.id">
            <img :src="post.image" :alt="post.titre" class="card-img" />
            <div class="card-body">
              <span class="card-date">{{ formatDate(post.date_creation) }}</span>
              <h3>{{ post.titre }}</h3>
              <p>{{ post.extrait }}</p>
              <router-link :to="`/blog/${post.slug}`" class="card-link">
                Lire la suite <i class="fas fa-arrow-right"></i>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- NOS PRODUITS -->
    <section class="section products">
      <div class="container">
        <h2 class="section-title">Nos Produits</h2>
        <p class="section-subtitle">Découvrez les filières agropastorales de notre coopérative</p>
        <div class="grid-4">
          <div class="product-card">
            <img src="/cacao4.jpg" alt="Cacao" />
            <div class="product-info">
              <h3>Cacao</h3>
              <p>Fèves de cacao de qualité supérieure</p>
            </div>
          </div>
          <div class="product-card">
            <img src="/mais.jpg" alt="Maïs" />
            <div class="product-info">
              <h3>Maïs</h3>
              <p>Culture céréalière de premier choix</p>
            </div>
          </div>
          <div class="product-card">
            <img src="/gombo.jpg" alt="Gombo" />
            <div class="product-info">
              <h3>Gombo</h3>
              <p>Gombo frais et de qualité</p>
            </div>
          </div>
          <div class="product-card">
            <img src="/porc.jpg" alt="Élevage porcin" />
            <div class="product-info">
              <h3>Élevage Porcin</h3>
              <p>Élevage de porcs en conditions optimales</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="container cta-content">
        <h2>Rejoignez notre coopérative</h2>
        <p>Ensemble, développons une agriculture d'excellence pour un avenir durable.</p>
        <router-link to="/contact" class="btn btn-primary">Contactez-nous</router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '../api'

const services = ref([])
const latestPosts = ref([])

// Animated counters
const statsRef = ref(null)
const animatedProducteurs = ref(0)
const animatedTonnes = ref(0)
const animatedAnnees = ref(0)
let statsObserver = null
let hasAnimated = false

function animateCounter(targetRef, target, duration = 2000) {
  const start = performance.now()
  const step = (now) => {
    const elapsed = now - start
    const progress = Math.min(elapsed / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)
    targetRef.value = Math.floor(eased * target)
    if (progress < 1) {
      requestAnimationFrame(step)
    } else {
      targetRef.value = target
    }
  }
  requestAnimationFrame(step)
}

function startCounters() {
  if (hasAnimated) return
  hasAnimated = true
  animateCounter(animatedProducteurs, 500, 2000)
  animateCounter(animatedTonnes, 1000, 2500)
  animateCounter(animatedAnnees, 15, 1500)
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
}

onMounted(async () => {
  // Intersection Observer for animated counters
  if (statsRef.value) {
    statsObserver = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          startCounters()
        }
      },
      { threshold: 0.3 }
    )
    statsObserver.observe(statsRef.value)
  }

  try {
    const [servRes, blogRes] = await Promise.all([
      api.get('/services/'),
      api.get('/blog/?page_size=3'),
    ])
    services.value = servRes.data
    latestPosts.value = (blogRes.data.results || blogRes.data).slice(0, 3)
  } catch {
    // API might not be available yet
  }
})

onUnmounted(() => {
  if (statsObserver) statsObserver.disconnect()
})
</script>

<style scoped>
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: url('/caco3.jpg') center/cover no-repeat;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(62, 39, 35, 0.7);
}

.hero-content {
  position: relative;
  z-index: 1;
  color: var(--color-white);
  max-width: 700px;
}

.hero-content h1 {
  font-family: var(--font-heading);
  font-size: 3.5rem;
  line-height: 1.2;
  margin-bottom: 20px;
}

.hero-content h1 span {
  color: var(--color-secondary);
}

.hero-content p {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 35px;
  line-height: 1.8;
}

.hero-buttons {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

/* About */
.about-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.about-img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
}

.about-text p {
  color: var(--color-text-light);
  margin-bottom: 20px;
  line-height: 1.8;
}

.stats {
  display: flex;
  gap: 40px;
  margin-top: 30px;
}

.stat {
  text-align: center;
}

.stat-number {
  display: block;
  font-family: var(--font-heading);
  font-size: 2.5rem;
  color: var(--color-secondary);
  font-weight: 700;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--color-text-light);
}

/* Services Preview */
.services-preview {
  background: var(--color-white);
}

.service-card {
  text-align: center;
  padding: 40px 30px;
  border-radius: var(--radius);
  transition: all 0.3s;
  border: 1px solid var(--color-border);
}

.service-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-5px);
}

.service-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-secondary), var(--color-secondary-light));
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.service-icon i {
  font-size: 2rem;
  color: var(--color-white);
}

.service-card h3 {
  font-family: var(--font-heading);
  font-size: 1.3rem;
  color: var(--color-primary-dark);
  margin-bottom: 10px;
}

.service-card p {
  color: var(--color-text-light);
  font-size: 0.95rem;
}

/* Blog */
.card-date {
  font-size: 0.85rem;
  color: var(--color-secondary);
  display: block;
  margin-bottom: 8px;
}

.card-link {
  display: inline-block;
  margin-top: 12px;
  color: var(--color-primary);
  font-weight: 600;
  font-size: 0.95rem;
}

.card-link i {
  margin-left: 5px;
  transition: margin-left 0.3s;
}

.card-link:hover i {
  margin-left: 10px;
}

/* Products */
.product-card {
  border-radius: var(--radius);
  overflow: hidden;
  position: relative;
  aspect-ratio: 3/4;
  cursor: pointer;
}

.product-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.product-card:hover img {
  transform: scale(1.1);
}

.product-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
  color: var(--color-white);
}

.product-info h3 {
  font-family: var(--font-heading);
  font-size: 1.2rem;
  margin-bottom: 4px;
}

.product-info p {
  font-size: 0.85rem;
  opacity: 0.85;
}

/* CTA */
.cta-section {
  background: url('/cacao%201.jpg') center/cover no-repeat;
  padding: 80px 0;
  text-align: center;
  position: relative;
}

.cta-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(46, 125, 50, 0.85);
}

.cta-content {
  position: relative;
  z-index: 1;
}

.cta-content h2 {
  font-family: var(--font-heading);
  font-size: 2.5rem;
  color: var(--color-white);
  margin-bottom: 15px;
}

.cta-content p {
  color: rgba(255,255,255,0.9);
  font-size: 1.15rem;
  margin-bottom: 30px;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2.2rem;
  }
  .about-grid {
    grid-template-columns: 1fr;
  }
  .stats {
    gap: 20px;
  }
}
</style>
