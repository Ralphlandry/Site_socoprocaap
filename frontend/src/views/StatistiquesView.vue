<template>
  <div>
    <section class="page-header">
      <h1>Statistiques de Production</h1>
      <p>Tonnages cumulés par filière — coopérative SOCOPROCAAP</p>
    </section>

    <section class="section">
      <div class="container">
        <div v-if="loading" class="state-loading">
          <div class="spinner"></div><p>Chargement...</p>
        </div>

        <template v-else>
          <!-- En-tête tableau -->
          <div class="table-header">
            <span class="table-label"><i class="fas fa-seedling"></i> Campagne</span>
            <select v-model="filterSession" class="session-select">
              <option value="">Toutes les sessions</option>
              <option v-for="s in sessions" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>

          <!-- Tableau des tonnages par produit -->
          <div class="table-wrap">
            <table class="prod-table">
              <thead>
                <tr>
                  <th><i class="fas fa-leaf"></i> Produit</th>
                  <th><i class="fas fa-weight-hanging"></i> Tonnage total (T)</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="!produitStats.length">
                  <td colspan="3" class="empty-row">
                    <i class="fas fa-chart-bar"></i> Aucune donnée disponible
                  </td>
                </tr>
                <tr v-for="p in produitStats" :key="p.produit">
                  <td class="td-produit">
                    <span class="produit-dot" :style="{ background: produitColor(p.produit) }"></span>
                    {{ p.produit }}
                  </td>
                  <td class="td-tonnage">{{ formatTonnage(p.tonnage_total) }} T</td>
                  <td class="td-action">
                    <button class="btn-detail" @click="openDetail(p.produit)">
                      <i class="fas fa-eye"></i> Détail
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
      </div>
    </section>

    <!-- Modal détail -->
    <transition name="mo">
      <div v-if="showModal" class="mo-overlay" @click.self="showModal = false">
        <div class="mo-box">
          <div class="mo-head">
            <h2><i class="fas fa-seedling"></i> {{ modalProduit }} — Détail des producteurs</h2>
            <button class="mo-close" @click="showModal = false"><i class="fas fa-times"></i></button>
          </div>
          <div class="mo-body">
            <table class="detail-table">
              <thead>
                <tr>
                  <th>Nom du Producteur</th>
                  <th>Tonnage (T)</th>
                  <th>Superficie (ha)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="c in modalRows" :key="c.id">
                  <td>{{ c.nom_producteur }}</td>
                  <td class="td-num">{{ formatTonnage(c.tonnage) }}</td>
                  <td class="td-num">{{ c.superficie != null ? formatTonnage(c.superficie) : '—' }}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <td><strong>Total</strong></td>
                  <td class="td-num"><strong>{{ formatTonnage(modalRows.reduce((s,r) => s + parseFloat(r.tonnage), 0)) }}</strong></td>
                  <td class="td-num"><strong>{{ formatTonnage(modalRows.reduce((s,r) => s + (r.superficie != null ? parseFloat(r.superficie) : 0), 0)) }}</strong></td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'

const campagnes = ref([])
const loading = ref(true)
const showModal = ref(false)
const modalProduit = ref('')
const filterSession = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get('/campagnes/')
    campagnes.value = data
  } finally {
    loading.value = false
  }
})

const PRODUIT_COLORS = {
  'Cacao': '#7b3f10',
  'Maïs': '#c8891a',
  'Gombo': '#4a7c59',
  'Élevage Porcin': '#9b4444',
}
function produitColor(p) { return PRODUIT_COLORS[p] || '#64748b' }

const sessions = computed(() =>
  [...new Set(campagnes.value.map(c => c.session))].sort().reverse()
)

const filtered = computed(() =>
  filterSession.value ? campagnes.value.filter(c => c.session === filterSession.value) : campagnes.value
)

const produitStats = computed(() => {
  const map = {}
  filtered.value.forEach(c => {
    if (!map[c.produit]) map[c.produit] = 0
    map[c.produit] += parseFloat(c.tonnage)
  })
  return Object.entries(map).map(([produit, tonnage_total]) => ({ produit, tonnage_total }))
})

const modalRows = computed(() =>
  filtered.value.filter(c => c.produit === modalProduit.value)
)

function openDetail(produit) {
  modalProduit.value = produit
  showModal.value = true
}

function formatTonnage(v) {
  const n = parseFloat(v)
  return Number.isInteger(n) ? n.toString() : n.toFixed(2).replace(/\.?0+$/, '')
}
</script>

<style scoped>
.page-header {
  background: linear-gradient(135deg, #1e0e04 0%, #3d1f0a 60%, #5c2e0e 100%);
  color: #fff; text-align: center;
  padding: 80px 20px 70px;
}
.page-header h1 { font-size: clamp(1.8rem, 4vw, 2.6rem); font-weight: 800; margin-bottom: 10px; }
.page-header p { font-size: 1rem; opacity: 0.75; }

.section { padding: 60px 20px; background: #fdf8f0; }
.container { max-width: 860px; margin: 0 auto; }

/* En-tête tableau */
.table-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 0; padding: 14px 20px;
  background: #fff; border: 1px solid #f0e4d0;
  border-radius: 16px 16px 0 0; border-bottom: none;
  flex-wrap: wrap; gap: 10px;
}
.table-label {
  font-size: 0.85rem; font-weight: 800; color: #3d1f0a;
  display: flex; align-items: center; gap: 7px; text-transform: uppercase; letter-spacing: 0.07em;
}
.table-label i { color: #c8891a; }
.session-select {
  padding: 7px 14px; border: 1px solid #e8c07a; border-radius: 8px;
  font-size: 0.82rem; color: #3d1f0a; background: #fff8ee; cursor: pointer;
  font-weight: 600;
}
.session-select:focus { outline: none; border-color: #c8891a; }

/* Table */
.table-wrap {
  background: #fff;
  border-radius: 0 0 16px 16px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(61,31,10,0.08);
  border: 1px solid #f0e4d0;
  border-top: none;
}
.prod-table { width: 100%; border-collapse: collapse; }
.prod-table thead tr { background: #3d1f0a; }
.prod-table thead th {
  padding: 16px 20px; text-align: left;
  color: #f5edd6; font-size: 0.78rem;
  font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase;
}
.prod-table thead th i { margin-right: 6px; opacity: 0.75; }
.prod-table tbody tr { border-bottom: 1px solid #f5edd6; transition: background 0.15s; }
.prod-table tbody tr:last-child { border-bottom: none; }
.prod-table tbody tr:hover { background: #fdf5e8; }

.td-produit {
  padding: 16px 20px;
  font-weight: 700; color: #2c1a08; font-size: 0.95rem;
  display: flex; align-items: center; gap: 10px;
}
.produit-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.td-tonnage {
  padding: 16px 20px;
  font-size: 1.1rem; font-weight: 800; color: #7b3f10;
}
.td-action { padding: 12px 20px; }
.btn-detail {
  display: inline-flex; align-items: center; gap: 6px;
  background: #fff8ee; color: #7b3f10; border: 1px solid #e8c07a;
  padding: 7px 14px; border-radius: 8px; font-size: 0.8rem; font-weight: 700;
  cursor: pointer; transition: all 0.15s;
}
.btn-detail:hover { background: #7b3f10; color: #fff; border-color: #7b3f10; }

.empty-row { padding: 50px; text-align: center; color: #94a3b8; font-size: 0.9rem; }
.empty-row i { margin-right: 8px; }

/* Modal */
.mo-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45);
  backdrop-filter: blur(3px); display: flex; align-items: center; justify-content: center;
  z-index: 3000; padding: 20px;
}
.mo-box {
  background: #fff; border-radius: 16px; width: 100%; max-width: 680px;
  max-height: 85vh; overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.mo-head {
  display: flex; justify-content: space-between; align-items: center;
  padding: 18px 24px; border-bottom: 1px solid #f0e4d0;
  background: #3d1f0a;
}
.mo-head h2 { color: #f5edd6; font-size: 0.95rem; font-weight: 700; display: flex; align-items: center; gap: 8px; }
.mo-head h2 i { color: #c8891a; }
.mo-close {
  background: none; border: none; color: rgba(255,255,255,0.6);
  cursor: pointer; font-size: 1.1rem; padding: 4px 8px; border-radius: 6px; transition: color 0.15s;
}
.mo-close:hover { color: #fff; }
.mo-body { padding: 20px; }

/* Detail table */
.detail-table { width: 100%; border-collapse: collapse; }
.detail-table thead tr { background: #f5edd6; }
.detail-table thead th {
  padding: 12px 16px; text-align: left;
  color: #5c2e0e; font-size: 0.75rem;
  font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
}
.detail-table tbody tr { border-bottom: 1px solid #f5edd6; font-size: 0.88rem; }
.detail-table tbody tr:hover { background: #fdf5e8; }
.detail-table tbody td { padding: 11px 16px; color: #2c1a08; }
.detail-table tfoot tr { background: #fdf5e8; border-top: 2px solid #c8891a; }
.detail-table tfoot td { padding: 11px 16px; font-size: 0.88rem; }
.td-num { text-align: right; font-weight: 700; color: #7b3f10; }

/* Spinner */
.state-loading { text-align: center; padding: 60px; color: #94a3b8; }
.spinner {
  width: 36px; height: 36px;
  border: 3px solid #f0e4d0; border-top-color: #c8891a;
  border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 14px;
}
@keyframes spin { to { transform: rotate(360deg); } }

.mo-enter-active, .mo-leave-active { transition: opacity 0.2s; }
.mo-enter-from, .mo-leave-to { opacity: 0; }

@media (max-width: 600px) {
  .td-produit { padding: 12px; }
  .td-tonnage, .td-action { padding: 12px; }
}
</style>


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
