<template>
  <div class="dash">
    <div class="dash-head">
      <div>
        <h1 class="dash-title">Bonjour, {{ auth.user?.username }}</h1>
        <p class="dash-sub">{{ todayDate }}</p>
      </div>
    </div>

    <!-- Stat cards -->
    <div class="stat-grid">
      <div v-for="s in stats" :key="s.label" class="stat-card" :style="{ '--c': s.color }">
        <div class="stat-icon"><i :class="s.icon"></i></div>
        <div class="stat-info">
          <span class="stat-val">{{ s.value }}</span>
          <span class="stat-lbl">{{ s.label }}</span>
          <span v-if="s.sub" class="stat-sub">{{ s.sub }}</span>
        </div>
      </div>
    </div>

    <div class="bottom-row">
      <!-- Quick actions -->
      <div class="panel">
        <h2 class="panel-title"><i class="fas fa-bolt"></i> Actions rapides</h2>
        <div class="actions-grid">
          <router-link to="/admin/blog" class="action-item">
            <i class="fas fa-pencil-alt"></i><span>Nouvel article</span>
          </router-link>
          <router-link to="/admin/galerie" class="action-item">
            <i class="fas fa-image"></i><span>Ajouter image</span>
          </router-link>
          <router-link to="/admin/services" class="action-item">
            <i class="fas fa-seedling"></i><span>Gérer services</span>
          </router-link>
          <router-link to="/admin/statistiques" class="action-item">
            <i class="fas fa-chart-line"></i><span>Statistiques</span>
          </router-link>
        </div>
      </div>

      <!-- Recent messages -->
      <div class="panel">
        <h2 class="panel-title"><i class="fas fa-envelope"></i> Messages récents</h2>
        <div v-if="contacts.length" class="msg-list">
          <div v-for="c in contacts" :key="c.id" class="msg-row" :class="{ unread: !c.lu }">
            <div class="msg-avatar">{{ c.nom.charAt(0).toUpperCase() }}</div>
            <div class="msg-body">
              <div class="msg-top">
                <strong>{{ c.nom }}</strong>
                <span class="msg-date">{{ fmtDate(c.date_envoi) }}</span>
              </div>
              <span class="msg-sub">{{ c.sujet }}</span>
            </div>
            <span v-if="!c.lu" class="unread-dot"></span>
          </div>
        </div>
        <div v-else class="empty-msg">
          <i class="fas fa-inbox"></i><p>Aucun message reçu</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import api from '../../api'

const auth = useAuthStore()
const stats = ref([])
const contacts = ref([])
const todayDate = new Date().toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })

function fmtDate(d) {
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' })
}

onMounted(async () => {
  try {
    const { data } = await api.get('/admin/stats/')
    stats.value = [
      { label: 'Services', value: data.services, icon: 'fas fa-seedling', color: '#2d7d46' },
      { label: 'Articles', value: data.blog_posts, icon: 'fas fa-newspaper', color: '#0284c7', sub: `${data.blog_published} publiés` },
      { label: 'Images', value: data.galerie_images, icon: 'fas fa-images', color: '#d97706' },
      { label: 'Messages', value: data.contacts, icon: 'fas fa-envelope', color: '#dc2626', sub: `${data.contacts_non_lus} non lus` },
      { label: 'Catégories', value: data.galerie_categories, icon: 'fas fa-folder-open', color: '#7c3aed' },
      { label: 'Statistiques', value: data.statistiques, icon: 'fas fa-chart-bar', color: '#0891b2' },
    ]
  } catch { /* */ }

  try {
    const { data } = await api.get('/admin/contacts/')
    contacts.value = (data.results || data).slice(0, 5)
  } catch { /* */ }
})
</script>

<style scoped>
.dash { width: 100%; }

.dash-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
}
.dash-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 3px;
  letter-spacing: -0.02em;
}
.dash-sub { color: #94a3b8; font-size: 0.82rem; font-weight: 500; }

/* Stat grid */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  border: 1px solid #e2e8f0;
  border-left: 4px solid var(--c);
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: box-shadow 0.2s, transform 0.2s;
}
.stat-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); transform: translateY(-2px); }
.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: color-mix(in srgb, var(--c) 12%, transparent);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c);
  font-size: 1.1rem;
  flex-shrink: 0;
}
.stat-val { display: block; font-size: 1.7rem; font-weight: 700; color: #0f172a; line-height: 1; letter-spacing: -0.02em; }
.stat-lbl { display: block; color: #475569; font-size: 0.78rem; font-weight: 600; margin-top: 3px; }
.stat-sub { display: block; font-size: 0.7rem; color: #94a3b8; margin-top: 2px; font-weight: 500; }

/* Bottom row */
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.panel {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 22px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.panel-title {
  font-size: 0.82rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.panel-title i { color: #059669; }

/* Actions */
.actions-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 16px 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #059669;
  font-size: 0.76rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.15s;
  cursor: pointer;
  text-align: center;
}
.action-item i { font-size: 1.1rem; }
.action-item:hover { background: #ecfdf5; border-color: #a7f3d0; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(5,150,105,0.1); }

/* Messages */
.msg-list { display: flex; flex-direction: column; gap: 8px; }
.msg-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 8px;
  background: #f8fafc;
  position: relative;
  transition: background 0.15s;
}
.msg-row:hover { background: #f1f5f9; }
.msg-row.unread { background: #f0fdf9; }
.msg-avatar {
  width: 34px;
  height: 34px;
  background: #059669;
  color: #fff;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.82rem;
  flex-shrink: 0;
}
.msg-body { flex: 1; min-width: 0; }
.msg-top { display: flex; justify-content: space-between; align-items: center; gap: 6px; }
.msg-top strong { color: #0f172a; font-size: 0.82rem; font-weight: 600; }
.msg-date { color: #94a3b8; font-size: 0.7rem; }
.msg-sub { display: block; color: #64748b; font-size: 0.76rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 2px; }
.unread-dot { width: 7px; height: 7px; background: #059669; border-radius: 50%; flex-shrink: 0; }

.empty-msg { text-align: center; padding: 28px; color: #94a3b8; }
.empty-msg i { font-size: 2rem; display: block; margin-bottom: 8px; opacity: 0.5; }
.empty-msg p { font-size: 0.84rem; }

@media (max-width: 700px) {
  .stat-grid { grid-template-columns: 1fr 1fr; }
  .bottom-row { grid-template-columns: 1fr; }
  .actions-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 400px) {
  .stat-grid { grid-template-columns: 1fr; }
}
</style>
