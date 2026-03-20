<template>
  <div>
    <section class="page-header">
      <h1>Nos Statistiques</h1>
      <p>Les chiffres clés de la coopérative SOCOPROCAAP</p>
    </section>

    <section class="section">
      <div class="container">
        <div class="loading" v-if="loading">
          <div class="loading-spinner"></div>
          <p>Chargement...</p>
        </div>

        <div v-else-if="stats.length" class="stats-grid">
          <div class="stat-card" v-for="stat in stats" :key="stat.id">
            <div class="stat-icon">
              <i :class="stat.icone || 'fas fa-chart-line'"></i>
            </div>
            <div class="stat-value">{{ stat.valeur }} <span v-if="stat.unite" class="stat-unite">{{ stat.unite }}</span></div>
            <h3 class="stat-title">{{ stat.titre }}</h3>
            <p v-if="stat.description" class="stat-desc">{{ stat.description }}</p>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="fas fa-chart-bar"></i>
          <p>Les statistiques seront bientôt disponibles.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const stats = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await api.get('/statistiques/')
    stats.value = data
  } catch (e) {
    console.error('Erreur chargement statistiques:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 30px;
  padding: 20px 0;
}

.stat-card {
  background: var(--color-white);
  border-radius: 16px;
  padding: 36px 28px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.stat-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 18px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-white);
  font-size: 1.5rem;
}

.stat-value {
  font-size: 2.4rem;
  font-weight: 800;
  color: var(--color-primary-dark);
  line-height: 1.1;
  margin-bottom: 8px;
  font-family: var(--font-heading);
}

.stat-unite {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-secondary);
}

.stat-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-dark);
  margin-bottom: 6px;
}

.stat-desc {
  font-size: 0.88rem;
  color: var(--color-text-light);
  line-height: 1.5;
  margin-top: 6px;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  .stat-card { padding: 24px 16px; }
  .stat-value { font-size: 1.8rem; }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
