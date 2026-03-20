<template>
  <div class="ap">
    <div class="ap-hd">
      <div>
        <h1 class="ap-title">Statistiques</h1>
        <p class="ap-desc">Gérez les chiffres clés affichés sur le site public</p>
      </div>
      <button class="btn btn-primary" @click="openForm()">
        <i class="fas fa-plus"></i> Nouvelle statistique
      </button>
    </div>

    <!-- Preview -->
    <div v-if="actives.length" class="preview-grid">
      <div v-for="s in actives" :key="s.id" class="preview-card">
        <div class="preview-icon"><i :class="s.icone || 'fas fa-chart-line'"></i></div>
        <div class="preview-val">{{ s.valeur }}<span v-if="s.unite"> {{ s.unite }}</span></div>
        <div class="preview-name">{{ s.titre }}</div>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <transition name="mo">
        <div v-if="showForm" class="mo-overlay" @click.self="showForm = false">
          <div class="mo-box">
            <div class="mo-head">
              <h2>{{ editing ? 'Modifier la statistique' : 'Nouvelle statistique' }}</h2>
              <button class="mo-close" @click="showForm = false"><i class="fas fa-times"></i></button>
            </div>
            <form @submit.prevent="save" class="mo-body">
              <div class="field"><label>Titre *</label><input v-model="form.titre" required placeholder="ex: Membres actifs" /></div>
              <div class="field-row">
                <div class="field"><label>Valeur *</label><input v-model="form.valeur" required placeholder="ex: 350" /></div>
                <div class="field"><label>Unité</label><input v-model="form.unite" placeholder="ex: membres, ha, %" /></div>
              </div>
              <div class="field">
                <label>Icône FontAwesome</label>
                <input v-model="form.icone" placeholder="ex: fas fa-users" />
                <div v-if="form.icone" class="icon-preview"><i :class="form.icone"></i> <span>Aperçu de l'icône</span></div>
              </div>
              <div class="field"><label>Description</label><textarea v-model="form.description" rows="3" placeholder="Explication optionnelle..."></textarea></div>
              <div class="field-row">
                <div class="field"><label>Ordre d'affichage</label><input v-model.number="form.ordre" type="number" /></div>
                <div class="field">
                  <label>Visibilité</label>
                  <label class="tgl">
                    <input type="checkbox" v-model="form.actif" />
                    <span class="tgl-track"></span>
                    <span class="tgl-lbl">{{ form.actif ? 'Visible' : 'Masqué' }}</span>
                  </label>
                </div>
              </div>
              <div class="mo-foot">
                <button type="button" class="btn btn-ghost" @click="showForm = false">Annuler</button>
                <button type="submit" class="btn btn-primary" :disabled="saving">
                  <i v-if="saving" class="fas fa-spinner fa-spin"></i>
                  {{ saving ? 'Enregistrement...' : 'Enregistrer' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </transition>
    </Teleport>

    <!-- Table -->
    <div class="tbl-card">
      <div class="tbl-top">
        <span class="tbl-count">{{ stats.length }} statistique{{ stats.length > 1 ? 's' : '' }}</span>
      </div>
      <div class="tbl-wrap">
        <table>
          <thead>
            <tr>
              <th>ICÔNE</th>
              <th>TITRE</th>
              <th>VALEUR</th>
              <th>UNITÉ</th>
              <th>ORDRE</th>
              <th>VISIBLE</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in stats" :key="s.id">
              <td><div class="icon-cell"><i :class="s.icone || 'fas fa-chart-bar'"></i></div></td>
              <td><span class="cell-bold">{{ s.titre }}</span></td>
              <td class="cell-val">{{ s.valeur }}</td>
              <td class="cell-unit">{{ s.unite || '—' }}</td>
              <td class="cell-order">{{ s.ordre }}</td>
              <td>
                <span class="badge" :class="s.actif ? 'badge-ok' : 'badge-muted'">
                  {{ s.actif ? 'Oui' : 'Non' }}
                </span>
              </td>
              <td>
                <div class="cell-acts">
                  <button class="act" @click="openForm(s)" title="Modifier"><i class="fas fa-pen"></i></button>
                  <button class="act act-red" @click="remove(s.id)" title="Supprimer"><i class="fas fa-trash-alt"></i></button>
                </div>
              </td>
            </tr>
            <tr v-if="!stats.length">
              <td colspan="7" class="tbl-empty">
                <i class="fas fa-chart-bar"></i><span>Aucune statistique enregistrée</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const stats = ref([])
const showForm = ref(false)
const editing = ref(null)
const saving = ref(false)
const form = ref({ titre: '', valeur: '', unite: '', icone: '', description: '', ordre: 0, actif: true })
const actives = computed(() => stats.value.filter(s => s.actif))

async function load() {
  const { data } = await api.get('/admin/statistiques/')
  stats.value = data.results || data
}

function openForm(s = null) {
  editing.value = s?.id || null
  form.value = s
    ? { titre: s.titre, valeur: s.valeur, unite: s.unite || '', icone: s.icone || '', description: s.description || '', ordre: s.ordre || 0, actif: s.actif }
    : { titre: '', valeur: '', unite: '', icone: '', description: '', ordre: 0, actif: true }
  showForm.value = true
}

async function save() {
  saving.value = true
  try {
    const payload = { ...form.value }
    if (editing.value) {
      await api.put(`/admin/statistiques/${editing.value}/`, payload)
    } else {
      await api.post('/admin/statistiques/', payload)
    }
    showForm.value = false
    await load()
  } finally { saving.value = false }
}

async function remove(id) {
  if (!confirm('Supprimer cette statistique ?')) return
  await api.delete(`/admin/statistiques/${id}/`)
  await load()
}

onMounted(load)
</script>

<style scoped>
.ap { width: 100%; }
.ap-hd { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }
.ap-title { font-size: 1.4rem; font-weight: 700; color: #0f172a; margin-bottom: 2px; letter-spacing: -0.02em; }
.ap-desc { color: #94a3b8; font-size: 0.82rem; font-weight: 500; }

.btn { display: inline-flex; align-items: center; gap: 7px; padding: 9px 18px; border-radius: 9px; font-size: 0.85rem; font-weight: 600; border: none; cursor: pointer; transition: all 0.15s; }
.btn-primary { background: #059669; color: #fff; }
.btn-primary:hover { background: #047857; }
.btn-primary:disabled { opacity: 0.55; cursor: not-allowed; }
.btn-ghost { background: #f8fafc; color: #374151; border: 1px solid #e2e8f0; }
.btn-ghost:hover { background: #f1f5f9; }

/* Preview */
.preview-grid { display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 24px; }
.preview-card {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 16px 20px;
  display: flex; align-items: center; gap: 12px; min-width: 180px;
  border-left: 4px solid #059669; box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: box-shadow 0.2s;
}
.preview-card:hover { box-shadow: 0 4px 16px rgba(5,150,105,0.1); }
.preview-icon { width: 36px; height: 36px; background: #ecfdf5; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #059669; font-size: 0.95rem; flex-shrink: 0; }
.preview-val { font-size: 1.2rem; font-weight: 700; color: #0f172a; letter-spacing: -0.02em; }
.preview-name { font-size: 0.78rem; color: #94a3b8; font-weight: 500; }

/* Modal */
.mo-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(3px); display: flex; align-items: center; justify-content: center; z-index: 3000; padding: 20px; }
.mo-box { background: #fff; border-radius: 14px; width: 100%; max-width: 540px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.mo-head { display: flex; justify-content: space-between; align-items: center; padding: 18px 24px; border-bottom: 1px solid #e2e8f0; }
.mo-head h2 { color: #0f172a; font-size: 1rem; font-weight: 700; }
.mo-close { background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 1.1rem; border-radius: 6px; padding: 4px 8px; transition: background 0.15s; }
.mo-close:hover { background: #f1f5f9; color: #dc2626; }
.mo-body { padding: 22px; }
.mo-foot { display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px; padding-top: 16px; border-top: 1px solid #e2e8f0; }
.mo-enter-active, .mo-leave-active { transition: opacity 0.2s; }
.mo-enter-from, .mo-leave-to { opacity: 0; }
.mo-enter-active .mo-box { transition: transform 0.2s; }
.mo-enter-from .mo-box { transform: scale(0.96) translateY(10px); }

.field { margin-bottom: 15px; }
.field > label { display: block; font-size: 0.72rem; font-weight: 700; color: #475569; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.05em; }
.field input, .field textarea, .field select { width: 100%; padding: 9px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.88rem; color: #0f172a; background: #fff; transition: border-color 0.15s; box-sizing: border-box; }
.field input:focus, .field textarea:focus { outline: none; border-color: #059669; box-shadow: 0 0 0 3px rgba(5,150,105,0.1); }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

.icon-preview { margin-top: 6px; padding: 8px 12px; background: #ecfdf5; border-radius: 8px; color: #059669; font-size: 0.9rem; display: flex; align-items: center; gap: 8px; }

.tgl { display: flex !important; align-items: center; gap: 10px; cursor: pointer; margin-top: 8px; }
.tgl input { display: none; }
.tgl-track { width: 40px; height: 22px; background: #cbd5e1; border-radius: 11px; position: relative; transition: background 0.2s; flex-shrink: 0; }
.tgl-track::after { content: ''; position: absolute; top: 3px; left: 3px; width: 16px; height: 16px; background: #fff; border-radius: 50%; transition: transform 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.25); }
.tgl input:checked + .tgl-track { background: #059669; }
.tgl input:checked + .tgl-track::after { transform: translateX(18px); }
.tgl-lbl { color: #64748b; font-size: 0.84rem; font-weight: 500; }

/* Table */
.tbl-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.tbl-top { padding: 12px 20px; border-bottom: 1px solid #e2e8f0; }
.tbl-count { color: #94a3b8; font-size: 0.78rem; font-weight: 600; }
.tbl-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 10px 16px; font-size: 0.65rem; font-weight: 700; color: #94a3b8; letter-spacing: 0.08em; border-bottom: 1px solid #e2e8f0; background: #f8fafc; text-transform: uppercase; }
td { padding: 11px 16px; color: #334155; font-size: 0.84rem; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
tr:last-child td { border-bottom: none; }
tr:hover td { background: #f8fafc; }

.icon-cell { width: 32px; height: 32px; background: #ecfdf5; border-radius: 7px; display: flex; align-items: center; justify-content: center; color: #059669; font-size: 0.85rem; }
.cell-bold { font-weight: 600; color: #0f172a; }
.cell-val { font-weight: 700; color: #059669; }
.cell-unit { color: #94a3b8; }
.cell-order { color: #cbd5e1; }

.badge { display: inline-flex; align-items: center; padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }
.badge-ok { background: #d1fae5; color: #065f46; }
.badge-muted { background: #f1f5f9; color: #64748b; }

.cell-acts { display: flex; gap: 6px; }
.act { width: 30px; height: 30px; border: 1px solid #e2e8f0; background: #f8fafc; color: #64748b; border-radius: 7px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; transition: all 0.15s; }
.act:hover { background: #ecfdf5; color: #059669; border-color: #a7f3d0; }
.act-red:hover { background: #fef2f2; color: #dc2626; border-color: #fecaca; }

.tbl-empty { text-align: center; padding: 40px; color: #b8d4c4; }
.tbl-empty i { font-size: 2rem; display: block; margin-bottom: 8px; }
.tbl-empty span { font-size: 0.88rem; display: block; }

@media (max-width: 700px) {
  .preview-grid { display: grid; grid-template-columns: 1fr 1fr; }
  th:nth-child(5), td:nth-child(5) { display: none; }
  .ap-hd { flex-direction: column; align-items: flex-start; }
}
@media (max-width: 500px) {
  .field-row { grid-template-columns: 1fr; }
  th:nth-child(4), td:nth-child(4) { display: none; }
}
</style>
