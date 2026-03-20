<template>
  <div>
    <section class="page-header">
      <h1>{{ post?.titre || 'Article' }}</h1>
      <p v-if="post">{{ formatDate(post.date_creation) }}</p>
    </section>

    <section class="section">
      <div class="container">
        <div class="loading" v-if="loading">
          <div class="loading-spinner"></div>
          <p>Chargement...</p>
        </div>

        <article v-else-if="post" class="blog-article">
          <img :src="post.image" :alt="post.titre" class="article-image" />
          <div class="article-content" v-html="formattedContent"></div>
          <router-link to="/blog" class="back-link">
            <i class="fas fa-arrow-left"></i> Retour au blog
          </router-link>
        </article>

        <div v-else class="empty-state">
          <p>Article introuvable.</p>
          <router-link to="/blog" class="btn btn-primary">Retour au blog</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const post = ref(null)
const loading = ref(true)

const formattedContent = computed(() => {
  if (!post.value) return ''
  return post.value.contenu.replace(/\n/g, '<br>')
})

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
}

onMounted(async () => {
  try {
    const res = await api.get(`/blog/${route.params.slug}/`)
    post.value = res.data
  } catch {
    // silent
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.blog-article {
  max-width: 800px;
  margin: 0 auto;
}

.article-image {
  width: 100%;
  border-radius: var(--radius);
  margin-bottom: 30px;
  max-height: 450px;
  object-fit: cover;
}

.article-content {
  font-size: 1.05rem;
  line-height: 1.9;
  color: var(--color-text);
}

.back-link {
  display: inline-block;
  margin-top: 40px;
  color: var(--color-primary);
  font-weight: 600;
}

.back-link:hover {
  color: var(--color-secondary);
}

.empty-state {
  text-align: center;
  padding: 60px 0;
}
</style>
