<template>
  <div>
    <!-- HERO SECTION -->
    <section class="hero">
      <div class="hero-overlay"></div>
      <div class="container hero-content">
        <div class="hero-logo-row">
          <img src="/LOGO (1).png" alt="Logo SOCOPROCAAP" class="hero-logo" />
          <h1>Bienvenue chez <span>SOCOPROCAAP.COOP.CA</span></h1>
        </div>
        <p class="hero-desc">Coopérative agropastorale spécialisée dans la production de cacao, maïs, gombo et l'élevage porcin. De la terre à votre table, nous cultivons l'excellence à Obala.</p>
        <div class="hero-buttons hero-anim-3">
          <router-link to="/productions" class="btn btn-primary">Nos Productions</router-link>
          <router-link to="/contact" class="btn btn-outline">Nous Contacter</router-link>
        </div>
      </div>
    </section>

    <!-- À PROPOS -->
    <section class="section about">
      <div class="container">
        <div class="about-grid">
          <div class="about-image reveal reveal-left">
            <img src="/cacao.jpg" alt="Plantation de cacao SOCOPROCAAP.COOP.CA" class="about-img" />
          </div>
          <div class="about-text reveal reveal-right">
            <h2 class="section-title" style="text-align:left">Qui sommes-nous ?</h2>
            <p>
              SOCOPROCAAP.COOP.CA est une coopérative agropastorale basée à Obala, village Nkolndobo. 
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

    <!-- MISSION VISION VALEURS -->
    <section class="mvv-section">
      <div class="container">
        <div class="mvv-header reveal reveal-up">
          <span class="mvv-badge">Notre ADN</span>
          <h2>Ce qui nous définit</h2>
        </div>
        <div class="mvv-grid">
          <div class="mvv-card reveal reveal-up" style="--delay:0ms">
            <div class="mvv-stripe mvv-stripe--mission"></div>
            <div class="mvv-card-inner">
              <div class="mvv-icon-wrap mvv-icon-wrap--mission">
                <i class="fas fa-bullseye"></i>
              </div>
              <h3>Notre Mission</h3>
              <p>Améliorer les conditions de vie de nos membres en développant une agriculture durable, productive et compétitive. Nous accompagnons chaque producteur du champ au marché, en garantissant un revenu juste et des débouchés fiables.</p>
            </div>
          </div>
          <div class="mvv-card mvv-card--featured reveal reveal-up" style="--delay:120ms">
            <div class="mvv-stripe mvv-stripe--vision"></div>
            <div class="mvv-card-inner">
              <div class="mvv-icon-wrap mvv-icon-wrap--vision">
                <i class="fas fa-binoculars"></i>
              </div>
              <h3>Notre Vision</h3>
              <p>Devenir la coopérative agropastorale de référence en Afrique centrale, reconnue pour la qualité de ses produits, la solidarité de ses membres et son engagement envers le développement rural et la souveraineté alimentaire.</p>
            </div>
          </div>
          <div class="mvv-card reveal reveal-up" style="--delay:240ms">
            <div class="mvv-stripe mvv-stripe--valeurs"></div>
            <div class="mvv-card-inner">
              <div class="mvv-icon-wrap mvv-icon-wrap--valeurs">
                <i class="fas fa-seedling"></i>
              </div>
              <h3>Nos Valeurs</h3>
              <div class="mvv-tags">
                <span><i class="fas fa-check-circle"></i> Solidarité</span>
                <span><i class="fas fa-check-circle"></i> Durabilité</span>
                <span><i class="fas fa-check-circle"></i> Transparence</span>
                <span><i class="fas fa-check-circle"></i> Excellence</span>
                <span><i class="fas fa-check-circle"></i> Respect de la nature</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- PRODUCTIONS APERÇU -->
    <section class="section services-preview" v-if="services.length">
      <div class="container">
        <h2 class="section-title reveal reveal-up">Nos Productions</h2>
        <p class="section-subtitle reveal reveal-up" style="--delay:80ms">Découvrez ce que nous offrons à nos membres et partenaires</p>
        <div class="grid-3">
          <div class="service-card reveal reveal-up" v-for="(service, i) in services.slice(0, 3)" :key="service.id" :style="'--delay:' + (i * 120) + 'ms'">
            <div class="service-icon">
              <i :class="service.icone || 'fas fa-leaf'"></i>
            </div>
            <h3>{{ service.titre }}</h3>
            <p>{{ service.description.substring(0, 120) }}...</p>
          </div>
        </div>
        <div style="text-align:center; margin-top:30px;">
          <router-link to="/productions" class="btn btn-primary">Voir toutes les productions</router-link>
        </div>
      </div>
    </section>

    <!-- DERNIERS ARTICLES -->
    <section class="section latest-blog" v-if="latestPosts.length">
      <div class="container">
        <h2 class="section-title reveal reveal-up">Dernières Actualités</h2>
        <p class="section-subtitle reveal reveal-up" style="--delay:80ms">Restez informé des dernières nouvelles de notre coopérative</p>
        <div class="grid-3">
          <div class="card reveal reveal-up" v-for="(post, i) in latestPosts" :key="post.id" :style="'--delay:' + (i * 130) + 'ms'">
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
        <h2 class="section-title reveal reveal-up">Nos Produits</h2>
        <p class="section-subtitle reveal reveal-up" style="--delay:80ms">Découvrez les filières agropastorales de notre coopérative</p>
        <div class="grid-4">
          <div class="product-card reveal reveal-up" style="--delay:0ms">
            <img src="/cacao4.jpg" alt="Cacao" />
            <div class="product-info">
              <h3>Cacao</h3>
              <p>Fèves de cacao de qualité supérieure</p>
            </div>
          </div>
          <div class="product-card reveal reveal-up" style="--delay:100ms">
            <img src="/mais.jpg" alt="Maïs" />
            <div class="product-info">
              <h3>Maïs</h3>
              <p>Culture céréalière de premier choix</p>
            </div>
          </div>
          <div class="product-card reveal reveal-up" style="--delay:200ms">
            <img src="/gombo.jpg" alt="Gombo" />
            <div class="product-info">
              <h3>Gombo</h3>
              <p>Gombo frais et de qualité</p>
            </div>
          </div>
          <div class="product-card reveal reveal-up" style="--delay:300ms">
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
  // Hero text staggered entrance
  setTimeout(() => document.querySelector('.hero-logo-row')?.classList.add('hero-anim-in'), 100)
  setTimeout(() => document.querySelector('.hero-desc')?.classList.add('hero-anim-in'), 400)
  setTimeout(() => document.querySelector('.hero-anim-3')?.classList.add('hero-anim-in'), 700)

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

  // Scroll reveal
  setTimeout(initScrollAnimations, 200)

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
  if (scrollObserver) scrollObserver.disconnect()
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

/* ---- Hero entrance animations ---- */
.hero-logo-row,
.hero-desc,
.hero-anim-3 {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}
.hero-logo-row.hero-anim-in,
.hero-desc.hero-anim-in,
.hero-anim-3.hero-anim-in {
  opacity: 1;
  transform: translateY(0);
}

/* ---- Scroll reveal ---- */
.reveal {
  opacity: 0;
  transition: opacity 0.65s ease, transform 0.65s ease;
}
.reveal-up    { transform: translateY(40px); }
.reveal-left  { transform: translateX(-50px); }
.reveal-right { transform: translateX(50px); }
.reveal.revealed {
  opacity: 1;
  transform: none;
}

.hero-content {
  position: relative;
  z-index: 1;
  color: var(--color-white);
  max-width: 700px;
}

.hero-logo-row {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.hero-logo {
  width: 160px;
  height: 160px;
  object-fit: contain;
  filter: drop-shadow(0 6px 24px rgba(0,0,0,0.5));
  flex-shrink: 0;
  animation: logoEntrance 1s ease-out both, logoPulse 3s ease-in-out 1s infinite;
  transform-origin: center;
}

@keyframes logoEntrance {
  0% {
    opacity: 0;
    transform: scale(0.5) rotate(-15deg);
    filter: drop-shadow(0 0 0 rgba(0,0,0,0));
  }
  60% {
    transform: scale(1.1) rotate(4deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
    filter: drop-shadow(0 6px 24px rgba(0,0,0,0.5));
  }
}

@keyframes logoPulse {
  0%, 100% {
    transform: scale(1);
    filter: drop-shadow(0 6px 24px rgba(0,0,0,0.5));
  }
  50% {
    transform: scale(1.07);
    filter: drop-shadow(0 8px 32px rgba(255,255,255,0.25)) drop-shadow(0 0 20px rgba(255,200,50,0.3));
  }
}

.hero-content h1 {
  font-family: var(--font-heading);
  font-size: 3.5rem;
  line-height: 1.2;
  margin-bottom: 0;
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

/* MISSION VISION VALEURS */
.mvv-section {
  background: linear-gradient(160deg, #0f2a1a 0%, #1a3d28 100%);
  padding: 80px 0;
  position: relative;
  overflow: hidden;
}
.mvv-section::before {
  content: '';
  position: absolute;
  width: 500px; height: 500px;
  border-radius: 50%;
  background: rgba(255,255,255,0.03);
  top: -150px; right: -100px;
  pointer-events: none;
}

.mvv-header {
  text-align: center;
  margin-bottom: 50px;
}
.mvv-badge {
  display: inline-block;
  background: rgba(255,255,255,0.1);
  color: #86efac;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 5px 16px;
  border-radius: 100px;
  border: 1px solid rgba(134,239,172,0.3);
  margin-bottom: 12px;
}
.mvv-header h2 {
  font-family: var(--font-heading);
  font-size: 2rem;
  color: #fff;
  margin: 0;
}

.mvv-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.mvv-card {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  overflow: hidden;
  transition: transform 0.25s, background 0.25s, box-shadow 0.25s;
  backdrop-filter: blur(6px);
}
.mvv-card:hover {
  transform: translateY(-6px);
  background: rgba(255,255,255,0.1);
  box-shadow: 0 20px 50px rgba(0,0,0,0.3);
}
.mvv-card--featured {
  background: rgba(255,255,255,0.12);
  border-color: rgba(134,239,172,0.35);
  box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}

.mvv-stripe {
  height: 5px;
}
.mvv-stripe--mission { background: linear-gradient(90deg, #4ade80, #22c55e); }
.mvv-stripe--vision  { background: linear-gradient(90deg, #fbbf24, #f59e0b); }
.mvv-stripe--valeurs { background: linear-gradient(90deg, #34d399, #10b981); }

.mvv-card-inner {
  padding: 32px 28px;
  text-align: center;
}

.mvv-icon-wrap {
  width: 68px; height: 68px;
  border-radius: 18px;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 20px;
  font-size: 1.7rem;
}
.mvv-icon-wrap--mission { background: rgba(74,222,128,0.15); color: #4ade80; }
.mvv-icon-wrap--vision  { background: rgba(251,191,36,0.15);  color: #fbbf24; }
.mvv-icon-wrap--valeurs { background: rgba(52,211,153,0.15);  color: #34d399; }

.mvv-card h3 {
  font-family: var(--font-heading);
  font-size: 1.2rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 14px;
}
.mvv-card p {
  font-size: 0.9rem;
  line-height: 1.8;
  color: rgba(255,255,255,0.7);
}

.mvv-tags {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.mvv-tags span {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 0.88rem;
  color: rgba(255,255,255,0.85);
  font-weight: 600;
}
.mvv-tags span i {
  color: #34d399;
  font-size: 0.8rem;
}

@media (max-width: 900px) {
  .mvv-grid { grid-template-columns: 1fr; }
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
