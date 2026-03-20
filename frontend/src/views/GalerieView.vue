<template>
  <div>
    <section class="page-header">
      <h1>Galerie</h1>
      <p>Découvrez notre coopérative en images</p>
    </section>

    <section class="section">
      <div class="container">
        <!-- Filtres catégories -->
        <div class="gallery-filters" v-if="categories.length">
          <button
            :class="{ active: activeCategory === null }"
            @click="filterCategory(null)"
          >Tout</button>
          <button
            v-for="cat in categories"
            :key="cat.id"
            :class="{ active: activeCategory === cat.id }"
            @click="filterCategory(cat.id)"
          >{{ cat.nom }}</button>
        </div>

        <div class="loading" v-if="loading">
          <div class="loading-spinner"></div>
          <p>Chargement...</p>
        </div>

        <div v-else-if="images.length" class="gallery-grid">
          <div
            class="gallery-item"
            v-for="img in images"
            :key="img.id"
            @click="openLightbox(img)"
          >
            <img :src="img.image" :alt="img.titre" />
            <div class="gallery-overlay">
              <h4>{{ img.titre }}</h4>
              <span v-if="img.categorie_nom">{{ img.categorie_nom }}</span>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="fas fa-images"></i>
          <p>Aucune image disponible pour le moment.</p>
        </div>

        <div class="pagination" v-if="totalPages > 1">
          <button :disabled="currentPage <= 1" @click="loadImages(currentPage - 1)">
            <i class="fas fa-chevron-left"></i> Précédent
          </button>
          <span>Page {{ currentPage }} / {{ totalPages }}</span>
          <button :disabled="currentPage >= totalPages" @click="loadImages(currentPage + 1)">
            Suivant <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- Lightbox -->
    <div class="lightbox" v-if="lightboxImage" @click="lightboxImage = null">
      <div class="lightbox-content" @click.stop>
        <button class="lightbox-close" @click="lightboxImage = null">
          <i class="fas fa-times"></i>
        </button>
        <img :src="lightboxImage.image" :alt="lightboxImage.titre" />
        <div class="lightbox-info">
          <h3>{{ lightboxImage.titre }}</h3>
          <p v-if="lightboxImage.description">{{ lightboxImage.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const images = ref([])
const categories = ref([])
const loading = ref(true)
const activeCategory = ref(null)
const lightboxImage = ref(null)
const currentPage = ref(1)
const totalPages = ref(1)

function openLightbox(img) {
  lightboxImage.value = img
}

async function loadImages(page = 1) {
  loading.value = true
  try {
    let url = `/galerie/?page=${page}`
    if (activeCategory.value) {
      url += `&categorie=${activeCategory.value}`
    }
    const res = await api.get(url)
    images.value = res.data.results || res.data
    const count = res.data.count || images.value.length
    totalPages.value = Math.ceil(count / 12)
    currentPage.value = page
  } catch {
    // silent
  } finally {
    loading.value = false
  }
}

function filterCategory(catId) {
  activeCategory.value = catId
  loadImages(1)
}

onMounted(async () => {
  try {
    const res = await api.get('/galerie/categories/')
    categories.value = res.data
  } catch {
    // silent
  }
  loadImages(1)
})
</script>

<style scoped>
.gallery-filters {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.gallery-filters button {
  padding: 8px 22px;
  border: 2px solid var(--color-primary-light);
  background: transparent;
  color: var(--color-primary);
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s;
}

.gallery-filters button.active,
.gallery-filters button:hover {
  background: var(--color-primary);
  color: var(--color-white);
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.gallery-item {
  position: relative;
  border-radius: var(--radius);
  overflow: hidden;
  cursor: pointer;
  aspect-ratio: 1;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.gallery-item:hover img {
  transform: scale(1.1);
}

.gallery-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 15px;
  opacity: 0;
  transition: opacity 0.3s;
}

.gallery-item:hover .gallery-overlay {
  opacity: 1;
}

.gallery-overlay h4 {
  color: var(--color-white);
  font-size: 1rem;
  margin-bottom: 3px;
}

.gallery-overlay span {
  color: var(--color-secondary);
  font-size: 0.85rem;
}

/* Lightbox */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.9);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.lightbox-content {
  max-width: 900px;
  width: 100%;
  position: relative;
}

.lightbox-content img {
  width: 100%;
  border-radius: 8px;
  max-height: 80vh;
  object-fit: contain;
}

.lightbox-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: var(--color-white);
  font-size: 1.5rem;
  cursor: pointer;
}

.lightbox-info {
  color: var(--color-white);
  padding: 15px 0;
}

.lightbox-info h3 {
  font-family: var(--font-heading);
  margin-bottom: 5px;
}

.lightbox-info p {
  opacity: 0.8;
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

@media (max-width: 992px) {
  .gallery-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .gallery-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
