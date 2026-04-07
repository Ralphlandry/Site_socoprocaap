<template>
  <div class="page">
    <!-- Header -->
    <div class="page-head">
      <div>
        <h1>Campagnes</h1>
        <p>Gestion des enregistrements de production</p>
      </div>
      <button class="btn-primary" @click="openForm()">
        <i class="fas fa-plus"></i> Nouvelle entrée
      </button>
    </div>

    <!-- Filtres -->
    <div class="filters-bar">
      <select v-model="filterProduit" class="f-select">
        <option value="">Tous les produits</option>
        <option v-for="p in PRODUITS" :key="p" :value="p">{{ p }}</option>
      </select>
      <select v-model="filterSession" class="f-select">
        <option value="">Toutes les sessions</option>
        <option v-for="s in sessions" :key="s" :value="s">{{ s }}</option>
      </select>
    </div>

    <!-- Tableau -->
    <div class="table-card">
      <div v-if="loading" class="state-msg">
        <div class="spinner"></div><span>Chargement...</span>
      </div>
      <div v-else-if="!filtered.length" class="state-msg empty">
        <i class="fas fa-seedling"></i> Aucune entrée
      </div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Produit</th>
            <th>Nom du producteur</th>
            <th>Tonnage (T)</th>
            <th>Superficie (ha)</th>
            <th>Session</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in filtered" :key="c.id">
            <td><span class="badge" :class="badgeClass(c.produit)">{{ c.produit }}</span></td>
            <td class="td-bold">{{ c.nom_producteur }}</td>
            <td class="td-num">{{ c.tonnage }}</td>
            <td class="td-num">{{ c.superficie ?? '—' }}</td>
            <td>{{ c.session }}</td>
            <td class="td-actions">
              <button class="btn-icon edit" @click="openForm(c)" title="Modifier">
                <i class="fas fa-pen"></i>
              </button>
              <button class="btn-icon del" @click="confirmDelete(c)" title="Supprimer">
                <i class="fas fa-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal formulaire -->
    <transition name="mo">
      <div v-if="showForm" class="mo-overlay" @click.self="showForm = false">
        <div class="mo-box">
          <div class="mo-head">
            <h2><i class="fas fa-seedling"></i> {{ editing ? 'Modifier' : 'Nouvelle entrée' }}</h2>
            <button class="mo-close" @click="showForm = false"><i class="fas fa-times"></i></button>
          </div>
          <form class="mo-body" @submit.prevent="save">
            <div class="form-grid">
              <div class="form-group span2">
                <label>Produit *</label>
                <select v-model="form.produit" required class="form-control">
                  <option value="" disabled>Choisir un produit</option>
                  <option v-for="p in PRODUITS" :key="p" :value="p">{{ p }}</option>
                </select>
              </div>
              <div class="form-group span2">
                <label>Nom du producteur *</label>
                <input v-model="form.nom_producteur" type="text" class="form-control" required placeholder="Ex: Jean Kouamé" />
              </div>
              <div class="form-group">
                <label>Tonnage (T) *</label>
                <input v-model="form.tonnage" type="number" step="0.01" min="0" class="form-control" required placeholder="0.00" />
              </div>
              <div class="form-group">
                <label>Superficie cultivable (ha)</label>
                <input v-model="form.superficie" type="number" step="0.01" min="0" class="form-control" placeholder="0.00" />
              </div>
              <div class="form-group span2">
                <label>Session *</label>
                <input v-model="form.session" type="text" class="form-control" required placeholder="Ex: 2025" maxlength="20" />
              </div>
            </div>
            <div class="mo-footer">
              <button type="button" class="btn-cancel" @click="showForm = false">Annuler</button>
              <button type="submit" class="btn-primary" :disabled="saving">
                <i class="fas fa-save"></i> {{ saving ? 'Enregistrement...' : 'Enregistrer' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Modal confirmation suppression -->
    <transition name="mo">
      <div v-if="showConfirm" class="mo-overlay" @click.self="showConfirm = false">
        <div class="mo-box mo-sm">
          <div class="mo-head danger">
            <h2><i class="fas fa-exclamation-triangle"></i> Confirmer la suppression</h2>
            <button class="mo-close" @click="showConfirm = false"><i class="fas fa-times"></i></button>
          </div>
          <div class="mo-body">
            <p>Supprimer <strong>{{ toDelete?.nom_producteur }}</strong> ({{ toDelete?.produit }}, session {{ toDelete?.session }}) ?</p>
            <p class="warn-text">Cette action est irréversible.</p>
          </div>
          <div class="mo-footer">
            <button class="btn-cancel" @click="showConfirm = false">Annuler</button>
            <button class="btn-danger" @click="doDelete" :disabled="saving">
              <i class="fas fa-trash"></i> Supprimer
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const PRODUITS = ['Cacao', 'Maïs', 'Gombo', 'Élevage Porcin']

const campagnes = ref([])
const loading = ref(true)
const saving = ref(false)
const showForm = ref(false)
const showConfirm = ref(false)
const editing = ref(null)
const toDelete = ref(null)
const filterProduit = ref('')
const filterSession = ref('')

const form = ref({ produit: '', nom_producteur: '', tonnage: '', superficie: '', session: '' })

onMounted(fetchAll)

async function fetchAll() {
  loading.value = true
  try {
    const { data } = await api.get('/admin/campagnes/')
    campagnes.value = data
  } finally {
    loading.value = false
  }
}

const sessions = computed(() => [...new Set(campagnes.value.map(c => c.session))].sort().reverse())

const filtered = computed(() => {
  return campagnes.value.filter(c => {
    if (filterProduit.value && c.produit !== filterProduit.value) return false
    if (filterSession.value && c.session !== filterSession.value) return false
    return true
  })
})

function openForm(c = null) {
  editing.value = c
  form.value = c
    ? { produit: c.produit, nom_producteur: c.nom_producteur, tonnage: c.tonnage, superficie: c.superficie, session: c.session }
    : { produit: '', nom_producteur: '', tonnage: '', superficie: '', session: '' }
  showForm.value = true
}

async function save() {
  saving.value = true
  try {
    const payload = {
      produit: form.value.produit,
      nom_producteur: form.value.nom_producteur,
      tonnage: parseFloat(form.value.tonnage),
      superficie: form.value.superficie !== '' && form.value.superficie !== null ? parseFloat(form.value.superficie) : null,
      session: form.value.session,
    }
    if (editing.value) {
      const { data } = await api.patch(`/admin/campagnes/${editing.value.id}/`, payload)
      const idx = campagnes.value.findIndex(c => c.id === editing.value.id)
      if (idx !== -1) campagnes.value[idx] = data
    } else {
      const { data } = await api.post('/admin/campagnes/', payload)
      campagnes.value.unshift(data)
    }
    showForm.value = false
  } finally {
    saving.value = false
  }
}

function confirmDelete(c) {
  toDelete.value = c
  showConfirm.value = true
}

async function doDelete() {
  saving.value = true
  try {
    await api.delete(`/admin/campagnes/${toDelete.value.id}/`)
    campagnes.value = campagnes.value.filter(c => c.id !== toDelete.value.id)
    showConfirm.value = false
  } finally {
    saving.value = false
  }
}

const BADGE_CLASSES = {
  'Cacao': 'badge-cacao',
  'Maïs': 'badge-mais',
  'Gombo': 'badge-gombo',
  'Élevage Porcin': 'badge-elevage',
}
function badgeClass(p) { return BADGE_CLASSES[p] || '' }
</script>

<style scoped>
.page { padding: 28px 24px; }
.page-head {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 24px; gap: 16px; flex-wrap: wrap;
}
.page-head h1 { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0 0 4px; }
.page-head p { font-size: 0.85rem; color: #64748b; margin: 0; }

/* Filters */
.filters-bar { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.f-select {
  padding: 9px 14px; border: 1px solid #e2e8f0; border-radius: 8px;
  font-size: 0.85rem; color: #374151; background: #fff; cursor: pointer;
}

/* Table card */
.table-card {
  background: #fff; border-radius: 12px;
  box-shadow: 0 1px 8px rgba(0,0,0,0.06); overflow: hidden;
  border: 1px solid #e2e8f0;
}
.state-msg {
  display: flex; align-items: center; justify-content: center; gap: 12px;
  padding: 48px; color: #94a3b8; font-size: 0.9rem;
}
.state-msg.empty { gap: 8px; }
.spinner {
  width: 22px; height: 22px; border: 2px solid #e2e8f0; border-top-color: #059669;
  border-radius: 50%; animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.data-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.data-table thead tr { background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
.data-table thead th {
  padding: 12px 16px; text-align: left;
  color: #475569; font-size: 0.75rem; font-weight: 700;
  letter-spacing: 0.06em; text-transform: uppercase;
}
.data-table tbody tr { border-bottom: 1px solid #f1f5f9; transition: background 0.12s; }
.data-table tbody tr:last-child { border-bottom: none; }
.data-table tbody tr:hover { background: #f8fafc; }
.data-table tbody td { padding: 13px 16px; color: #334155; }
.td-bold { font-weight: 600; color: #0f172a; }
.td-num { font-weight: 700; }
.td-actions { display: flex; gap: 8px; padding: 10px 16px; }

/* Badge */
.badge {
  display: inline-block; padding: 3px 10px; border-radius: 20px;
  font-size: 0.75rem; font-weight: 700;
}
.badge-cacao  { background: #f5edd6; color: #7b3f10; }
.badge-mais   { background: #fef3c7; color: #92400e; }
.badge-gombo  { background: #d1fae5; color: #065f46; }
.badge-elevage { background: #fee2e2; color: #991b1b; }

/* Buttons */
.btn-primary {
  display: inline-flex; align-items: center; gap: 7px;
  background: #059669; color: #fff; border: none;
  padding: 10px 18px; border-radius: 8px; font-weight: 700; font-size: 0.85rem;
  cursor: pointer; transition: background 0.15s;
}
.btn-primary:hover:not(:disabled) { background: #047857; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-cancel {
  background: #f1f5f9; color: #64748b; border: 1px solid #e2e8f0;
  padding: 9px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 600;
  cursor: pointer; transition: background 0.15s;
}
.btn-cancel:hover { background: #e2e8f0; }

.btn-danger {
  display: inline-flex; align-items: center; gap: 7px;
  background: #dc2626; color: #fff; border: none;
  padding: 9px 16px; border-radius: 8px; font-weight: 700; font-size: 0.85rem;
  cursor: pointer;
}
.btn-danger:disabled { opacity: 0.6; }

.btn-icon {
  background: none; border: none; cursor: pointer;
  width: 32px; height: 32px; border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; transition: all 0.15s;
}
.btn-icon.edit { color: #059669; background: #d1fae5; }
.btn-icon.edit:hover { background: #059669; color: #fff; }
.btn-icon.del { color: #dc2626; background: #fee2e2; }
.btn-icon.del:hover { background: #dc2626; color: #fff; }

/* Modal */
.mo-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  backdrop-filter: blur(3px); display: flex; align-items: center; justify-content: center;
  z-index: 3000; padding: 20px;
}
.mo-box {
  background: #fff; border-radius: 14px; width: 100%; max-width: 560px;
  max-height: 90vh; overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.18);
}
.mo-sm { max-width: 460px; }
.mo-head {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 20px; border-bottom: 1px solid #e2e8f0; background: #f8fafc;
  border-radius: 14px 14px 0 0;
}
.mo-head.danger { background: #fef2f2; }
.mo-head h2 { font-size: 0.95rem; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 8px; }
.mo-head h2 i { color: #059669; }
.mo-head.danger h2 i { color: #dc2626; }
.mo-close { background: none; border: none; cursor: pointer; color: #94a3b8; font-size: 1rem; padding: 4px 8px; border-radius: 6px; }
.mo-close:hover { color: #0f172a; background: #e2e8f0; }
.mo-body { padding: 20px; }
.mo-footer {
  display: flex; justify-content: flex-end; gap: 10px;
  padding: 16px 20px; border-top: 1px solid #f1f5f9;
}

/* Form */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.span2 { grid-column: span 2; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 0.8rem; font-weight: 700; color: #374151; }
.form-control {
  padding: 9px 12px; border: 1px solid #d1d5db; border-radius: 8px;
  font-size: 0.88rem; color: #0f172a; background: #fff; transition: border-color 0.15s;
}
.form-control:focus { outline: none; border-color: #059669; box-shadow: 0 0 0 3px rgba(5,150,105,0.12); }

.warn-text { color: #dc2626; font-size: 0.82rem; margin-top: 4px; }

.mo-enter-active, .mo-leave-active { transition: opacity 0.2s; }
.mo-enter-from, .mo-leave-to { opacity: 0; }

@media (max-width: 500px) {
  .form-grid { grid-template-columns: 1fr; }
  .span2 { grid-column: span 1; }
}
</style>
