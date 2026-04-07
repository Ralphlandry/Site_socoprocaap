<template>
  <div>
    <section class="page-header">
      <div class="page-header-content">
        <span class="page-badge">Nos Membres</span>
        <h1>Les hommes et les femmes<br>qui font avancer SOCOPROCAAP</h1>
        <p>Une équipe passionnée, engagée pour l'agriculture durable et le développement de nos membres.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">

        <div v-if="loading" class="state-loading">
          <div class="spinner"></div>
          <p>Chargement...</p>
        </div>

        <div v-else-if="membres.length" class="equipe-grid">
          <div class="membre-card" v-for="m in membres" :key="m.id">
            <div class="mc-photo-wrap">
              <div class="mc-photo">
                <img v-if="m.image" :src="m.image" :alt="m.prenom + ' ' + m.nom" />
                <div v-else class="mc-ph"><i class="fas fa-user"></i></div>
              </div>
              <div class="mc-deco"></div>
            </div>
            <div class="mc-info">
              <h3>{{ m.nom }} {{ m.prenom }}</h3>
              <span class="mc-fonction">{{ m.fonction }}</span>
              <div class="mc-line"></div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="fas fa-users"></i>
          <p>Les membres de l'équipe seront bientôt présentés.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const membres = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await api.get('/equipe/')
    membres.value = res.data
  } catch {
    // handle silently
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* ---- Header ---- */
.page-header {
  background: linear-gradient(135deg, #1e0e04 0%, #3d1f0a 60%, #5c2e0e 100%);
  text-align: center;
  padding: 90px 20px 80px;
  position: relative;
  overflow: hidden;
}
.page-header::before {
  content: '';
  position: absolute;
  width: 420px; height: 420px;
  border-radius: 50%;
  background: rgba(255,255,255,0.03);
  top: -120px; right: -80px;
  pointer-events: none;
}
.page-header-content { position: relative; z-index: 1; }
.page-badge {
  display: inline-block;
  background: rgba(255,255,255,0.1);
  color: #e8c07a;
  font-size: 0.72rem; font-weight: 700;
  letter-spacing: 0.12em; text-transform: uppercase;
  padding: 5px 16px; border-radius: 100px;
  border: 1px solid rgba(200,137,26,0.4);
  margin-bottom: 18px;
}
.page-header h1 {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 800;
  color: #fff;
  line-height: 1.25;
  margin-bottom: 16px;
}
.page-header p {
  font-size: 1.05rem;
  color: rgba(255,255,255,0.7);
  max-width: 520px;
  margin: 0 auto;
  line-height: 1.7;
}

/* ---- Section ---- */
.section {
  padding: 80px 20px;
  background: #fdf8f0;
}
.container {
  max-width: 1100px;
  margin: 0 auto;
}

/* ---- Grid ---- */
.equipe-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 36px;
}

/* ---- Card ---- */
.membre-card {
  background: #fff;
  border-radius: 20px;
  padding: 36px 24px 28px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(61,31,10,0.08);
  transition: transform 0.25s, box-shadow 0.25s;
  border: 1px solid #f0e4d0;
}
.membre-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 48px rgba(61,31,10,0.14);
}

/* ---- Photo ---- */
.mc-photo-wrap {
  position: relative;
  width: 110px;
  height: 110px;
  margin: 0 auto 20px;
}
.mc-deco {
  position: absolute;
  inset: -5px;
  border-radius: 50%;
  border: 3px solid transparent;
  background: linear-gradient(135deg, #c8891a, #7b3f10) border-box;
  -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: destination-out;
  mask-composite: exclude;
}
.mc-photo {
  width: 110px; height: 110px;
  border-radius: 50%;
  overflow: hidden;
  background: #f5edd6;
  position: relative;
  z-index: 1;
}
.mc-photo img {
  width: 100%; height: 100%;
  object-fit: cover; display: block;
}
.mc-ph {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  color: #c8891a; font-size: 2.8rem;
}

/* ---- Info ---- */
.mc-info { }
.mc-info h3 {
  font-size: 1.05rem;
  font-weight: 700;
  color: #2c1a08;
  margin-bottom: 6px;
  letter-spacing: -0.01em;
}
.mc-fonction {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  color: #7b3f10;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  background: #fdf0dc;
  padding: 3px 12px;
  border-radius: 20px;
}
.mc-line {
  width: 40px; height: 3px;
  background: linear-gradient(90deg, #c8891a, #7b3f10);
  border-radius: 2px;
  margin: 14px auto 0;
}

/* ---- États ---- */
.state-loading {
  text-align: center; padding: 60px; color: #94a3b8;
}
.spinner {
  width: 36px; height: 36px;
  border: 3px solid #f0e4d0;
  border-top-color: #c8891a;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 14px;
}
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state {
  text-align: center; padding: 80px 20px; color: #bbb;
}
.empty-state i { font-size: 3rem; display: block; margin-bottom: 14px; }
.empty-state p { font-size: 1rem; }

@media (max-width: 600px) {
  .equipe-grid { grid-template-columns: repeat(2, 1fr); gap: 20px; }
  .membre-card { padding: 24px 14px 20px; }
}
@media (max-width: 380px) {
  .equipe-grid { grid-template-columns: 1fr; }
}
</style>

