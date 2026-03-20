<template>
  <div>
    <section class="page-header">
      <h1>Blog</h1>
      <p>Actualités et articles sur le cacao et notre coopérative</p>
    </section>

    <section class="section">
      <div class="container">
        <div class="loading" v-if="loading">
          <div class="loading-spinner"></div>
          <p>Chargement...</p>
        </div>

        <div v-else-if="posts.length">
          <div class="grid-3">
            <div class="card" v-for="post in posts" :key="post.id">
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

          <div class="pagination" v-if="totalPages > 1">
            <button :disabled="currentPage <= 1" @click="loadPage(currentPage - 1)">
              <i class="fas fa-chevron-left"></i> Précédent
            </button>
            <span>Page {{ currentPage }} / {{ totalPages }}</span>
            <button :disabled="currentPage >= totalPages" @click="loadPage(currentPage + 1)">
              Suivant <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>

        <div v-else class="empty-state">
          <i class="fas fa-newspaper"></i>
          <p>Aucun article pour le moment.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const posts = ref([])
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(1)

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
}

async function loadPage(page) {
  loading.value = true
  try {
    const res = await api.get(`/blog/?page=${page}`)
    posts.value = res.data.results || res.data
    const count = res.data.count || posts.value.length
    totalPages.value = Math.ceil(count / 12)
    currentPage.value = page
  } catch {
    // silent
  } finally {
    loading.value = false
  }
}

onMounted(() => loadPage(1))
</script>

<style scoped>
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
</style>
