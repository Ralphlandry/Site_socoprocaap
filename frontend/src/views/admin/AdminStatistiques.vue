<template>
  <div class="page">
    <div class="page-head">
      <div>
        <h1>Statistiques de production</h1>
        <p>Tonnages et superficies par produit et par session</p>
      </div>
    </div>

    <!-- Filtres -->
    <div class="camp-filters">
      <select v-model="campFilterProduit" class="f-select">
        <option value="">Tous les produits</option>
        <option v-for="p in PRODUITS" :key="p" :value="p">{{ p }}</option>
      </select>
      <select v-model="campFilterSession" class="f-select">
        <option value="">Toutes les sessions</option>
        <option v-for="s in campSessions" :key="s" :value="s">{{ s }}</option>
      </select>
    </div>

    <!-- Tableau agrégé -->
    <div class="tbl-card">
      <div class="tbl-top">
        <span class="tbl-count">{{ campStats.length }} produit{{ campStats.length > 1 ? 's' : '' }}</span>
      </div>
      <div v-if="campLoading" class="state-loading">
        <div class="spinner"></div> Chargement...
      </div>
      <div v-else class="tbl-wrap">
        <table>
          <thead>
            <tr>
              <th>PRODUIT</th>
              <th>NB PRODUCTEURS</th>
              <th>TONNAGE TOTAL (T)</th>
              <th>SUPERFICIE TOTALE (ha)</th>
              <th>DÉTAIL</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in campStats" :key="p.produit">
              <td><span class="camp-badge" :class="campBadgeClass(p.produit)">{{ p.produit }}</span></td>
              <td>{{ p.count }}</td>
              <td class="cell-val">{{ p.tonnage_total }}</td>
              <td>{{ p.superficie_total }}</td>
              <td>
                <button class="btn-detail" @click="openCampDetail(p.produit)">
                  <i class="fas fa-eye"></i> Voir
                </button>
              </td>
            </tr>
            <tr v-if="!campStats.length">
              <td colspan="5" class="tbl-empty">
                <i class="fas fa-seedling"></i>
                <span>Aucune campagne enregistrée</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal détail -->
    <Teleport to="body">
      <transition name="mo">
        <div v-if="showCampDetail" class="mo-overlay" @click.self="showCampDetail = false">
          <div class="mo-box">
            <div class="mo-head">
              <h2><i class="fas fa-seedling"></i> {{ campDetailProduit }} — Producteurs</h2>
              <button class="mo-close" @click="showCampDetail = false"><i class="fas fa-times"></i></button>
            </div>
            <div class="mo-body">
              <div v-if="campFilterSession" class="mo-filter-info">
                Session : <strong>{{ campFilterSession }}</strong>
              </div>
              <div class="tbl-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>NOM DU PRODUCTEUR</th>
                      <th>TONNAGE (T)</th>
                      <th>SUPERFICIE (ha)</th>
                      <th>SESSION</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="c in campDetailRows" :key="c.id">
                      <td class="cell-bold">{{ c.nom_producteur }}</td>
                      <td class="cell-val">{{ c.tonnage }}</td>
                      <td>{{ c.superficie ?? '—' }}</td>
                      <td>{{ c.session }}</td>
                    </tr>
                  </tbody>
                  <tfoot>
                    <tr class="tfoot-total">
                      <td><strong>Total</strong></td>
                      <td class="cell-val"><strong>{{ fmt(campDetailRows.reduce((s,r) => s + parseFloat(r.tonnage), 0)) }}</strong></td>
                      <td><strong>{{ fmt(campDetailRows.reduce((s,r) => s + (r.superficie != null ? parseFloat(r.superficie) : 0), 0)) }}</strong></td>
                      <td></td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const PRODUITS = ['Cacao', 'Maïs', 'Gombo', 'Élevage Porcin']

const campagnes = ref([])
const campLoading = ref(true)
const campFilterProduit = ref('')
const campFilterSession = ref('')
const showCampDetail = ref(false)
const campDetailProduit = ref('')

onMounted(async () => {
  campLoading.value = true
  try {
    const { data } = await api.get('/admin/campagnes/')
    campagnes.value = data
  } finally { campLoading.value = false }
})

const campSessions = computed(() =>
  [...new Set(campagnes.value.map(c => c.session))].sort().reverse()
)

const campFiltered = computed(() =>
  campagnes.value.filter(c => {
    if (campFilterProduit.value && c.produit !== campFilterProduit.value) return false
    if (campFilterSession.value && c.session !== campFilterSession.value) return false
    return true
  })
)

const campStats = computed(() => {
  const map = {}
  campFiltered.value.forEach(c => {
    if (!map[c.produit]) map[c.produit] = { produit: c.produit, count: 0, tonnage_total: 0, superficie_total: 0 }
    map[c.produit].count++
    map[c.produit].tonnage_total += parseFloat(c.tonnage)
    map[c.produit].superficie_total += c.superficie != null ? parseFloat(c.superficie) : 0
  })
  return Object.values(map).map(p => ({
    ...p,
    tonnage_total: fmt(p.tonnage_total),
    superficie_total: fmt(p.superficie_total),
  }))
})

const campDetailRows = computed(() =>
  campFiltered.value.filter(c => c.produit === campDetailProduit.value)
)

function openCampDetail(produit) {
  campDetailProduit.value = produit
  showCampDetail.value = true
}

function fmt(v) {
  const n = parseFloat(v)
  return Number.isInteger(n) ? n.toString() : n.toFixed(2).replace(/\.?0+$/, '')
}

const CAMP_BADGE = {
  'Cacao': 'badge-cacao',
  'Maïs': 'badge-mais',
  'Gombo': 'badge-gombo',
  'Élevage Porcin': 'badge-elevage',
}
function campBadgeClass(p) { return CAMP_BADGE[p] || '' }
</script>

<style scoped>
.page { padding: 28px 24px; }
.page-head { margin-bottom: 24px; }
.page-head h1 { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0 0 4px; }
.page-head p { font-size: 0.85rem; color: #64748b; margin: 0; }

/* Filtres */
.camp-filters { display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }
.f-select {
  padding: 9px 14px; border: 1px solid #e2e8f0; border-radius: 8px;
  font-size: 0.85rem; color: #374151; background: #fff; cursor: pointer;
}

/* Table card */
.tbl-card {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
  overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.tbl-top { padding: 12px 20px; border-bottom: 1px solid #e2e8f0; }
.tbl-count { color: #94a3b8; font-size: 0.78rem; font-weight: 600; }
.tbl-wrap { overflow-x: auto; }

table { width: 100%; border-collapse: collapse; }
th {
  text-align: left; padding: 10px 16px;
  font-size: 0.65rem; font-weight: 700; color: #94a3b8;
  letter-spacing: 0.08em; border-bottom: 1px solid #e2e8f0;
  background: #f8fafc; text-transform: uppercase;
}
td {
  padding: 13px 16px; color: #334155; font-size: 0.85rem;
  border-bottom: 1px solid #f1f5f9; vertical-align: middle;
}
tr:last-child td { border-bottom: none; }
tr:hover td { background: #f8fafc; }

.cell-bold { font-weight: 600; color: #0f172a; }
.cell-val { font-weight: 700; color: #059669; }

.tfoot-total { background: #f8fafc; border-top: 2px solid #e2e8f0; }
.tfoot-total td { border-bottom: none; }

/* Badges */
.camp-badge {
  display: inline-block; padding: 3px 10px; border-radius: 20px;
  font-size: 0.75rem; font-weight: 700;
}
.badge-cacao   { background: #f5edd6; color: #7b3f10; }
.badge-mais    { background: #fef3c7; color: #92400e; }
.badge-gombo   { background: #d1fae5; color: #065f46; }
.badge-elevage { background: #fee2e2; color: #991b1b; }

/* Bouton détail */
.btn-detail {
  display: inline-flex; align-items: center; gap: 6px;
  background: #f8fafc; color: #059669; border: 1px solid #a7f3d0;
  padding: 6px 12px; border-radius: 7px; font-size: 0.78rem; font-weight: 700;
  cursor: pointer; transition: all 0.15s;
}
.btn-detail:hover { background: #059669; color: #fff; border-color: #059669; }

/* Empty/loading */
.state-loading {
  padding: 40px; text-align: center; color: #94a3b8;
  font-size: 0.88rem; display: flex; align-items: center; justify-content: center; gap: 10px;
}
.spinner {
  width: 18px; height: 18px; border: 2px solid #e2e8f0;
  border-top-color: #059669; border-radius: 50%; animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.tbl-empty { text-align: center; padding: 48px; color: #b8d4c4; }
.tbl-empty i { font-size: 2rem; display: block; margin-bottom: 10px; }
.tbl-empty span { font-size: 0.88rem; display: block; }

/* Modal */
.mo-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  backdrop-filter: blur(3px); display: flex; align-items: center; justify-content: center;
  z-index: 3000; padding: 20px;
}
.mo-box {
  background: #fff; border-radius: 14px; width: 100%; max-width: 680px;
  max-height: 88vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.mo-head {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 20px; border-bottom: 1px solid #e2e8f0; background: #f8fafc;
  border-radius: 14px 14px 0 0;
}
.mo-head h2 { font-size: 0.95rem; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 8px; }
.mo-head h2 i { color: #059669; }
.mo-close { background: none; border: none; cursor: pointer; color: #94a3b8; font-size: 1rem; padding: 4px 8px; border-radius: 6px; }
.mo-close:hover { color: #0f172a; background: #e2e8f0; }
.mo-body { padding: 20px; }
.mo-filter-info { margin-bottom: 12px; font-size: 0.82rem; color: #64748b; }

.mo-enter-active, .mo-leave-active { transition: opacity 0.2s; }
.mo-enter-from, .mo-leave-to { opacity: 0; }
</style>
