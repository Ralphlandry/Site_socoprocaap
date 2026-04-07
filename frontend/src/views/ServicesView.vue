<template>
  <div>
    <section class="page-header">
      <h1>Nos Productions</h1>
      <p>Ce que nous offrons à nos membres et partenaires dans les filières agropastorales</p>
    </section>

    <section class="section">
      <div class="container">
        <div class="loading" v-if="loading">
          <div class="loading-spinner"></div>
          <p>Chargement...</p>
        </div>

        <div v-else-if="services.length" class="services-list">
          <div
            class="service-item"
            v-for="(service, index) in services"
            :key="service.id"
            :class="{ reverse: index % 2 !== 0 }"
          >
            <div class="service-visual">
              <img v-if="service.image" :src="service.image" :alt="service.titre" />
              <img v-else :src="fallbackImages[index % fallbackImages.length]" :alt="service.titre" />
            </div>
            <div class="service-info">
              <div class="service-number">{{ String(index + 1).padStart(2, '0') }}</div>
              <h2>{{ service.titre }}</h2>
              <p>{{ service.description }}</p>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="fas fa-seedling"></i>
          <p>Les productions seront bientôt disponibles.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const services = ref([])
const loading = ref(true)

const fallbackImages = [
  '/cacao.jpg',
  '/mais.jpg',
  '/gombo.jpg',
  '/porc.jpg',
  '/cacao4.jpg',
  '/mais%201.jpg',
]

onMounted(async () => {
  try {
    const res = await api.get('/services/')
    services.value = res.data
  } catch {
    // handle silently
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.services-list {
  display: flex;
  flex-direction: column;
  gap: 60px;
}

.service-item {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 50px;
  align-items: center;
}

.service-item.reverse {
  direction: rtl;
}

.service-item.reverse > * {
  direction: ltr;
}

.service-visual img {
  width: 100%;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  height: 350px;
  object-fit: cover;
}

.service-number {
  font-family: var(--font-heading);
  font-size: 3rem;
  color: var(--color-secondary);
  opacity: 0.5;
  font-weight: 700;
  margin-bottom: 5px;
}

.service-info h2 {
  font-family: var(--font-heading);
  font-size: 1.8rem;
  color: var(--color-primary-dark);
  margin-bottom: 15px;
}

.service-info p {
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

@media (max-width: 768px) {
  .service-item,
  .service-item.reverse {
    grid-template-columns: 1fr;
    direction: ltr;
  }
}
</style>
