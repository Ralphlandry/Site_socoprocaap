<template>
  <div class="ap">
    <!-- Header -->
    <div class="ap-hd">
      <div>
        <div class="ap-title">Partenaires</div>
        <div class="ap-desc">Gérer les partenaires de commercialisation</div>
      </div>
      <button class="btn btn-primary" @click="openForm()">
        <i class="fas fa-plus"></i> Nouveau partenaire
      </button>
    </div>

    <!-- Modal création/édition -->
    <transition name="mo">
      <div v-if="showForm" class="mo-overlay" @click.self="showForm = false">
        <div class="mo-box">
          <div class="mo-head">
            <h2><i :class="editing ? 'fas fa-link-edit' : 'fas fa-link-plus'"></i>
              {{ editing ? 'Modifier le partenaire' : 'Nouveau partenaire' }}
            </h2>
            <button class="mo-close" @click="showForm = false"><i class="fas fa-times"></i></button>
          </div>
          <form @submit.prevent="save" class="mo-body">
            <div v-if="formError" class="form-err">{{ formError }}</div>
            <div class="field">
              <label>Nom *</label>
              <input v-model="form.nom" required placeholder="Nom du partenaire" />
            </div>
            <div class="field">
              <label>Logo/Image *</label>
              <label class="file-pick">
                <i class="fas fa-image"></i>
                <span>{{ form.imageFile ? form.imageFile.name : 'Choisir une image...' }}</span>
                <input type="file" accept="image/*" @change="form.imageFile = $event.target.files[0]" />
              </label>
              <div v-if="form.imagePreview || editingPartenaire?.image" style="margin-top:8px;">
                <img :src="form.imageFile ? form.imagePreview : editingPartenaire?.image"
                     style="width:80px;height:80px;object-fit:cover;border-radius:8px;border:1px solid #e2e8f0;" />
              </div>
            </div>
            <div class="field">
              <label>Description *</label>
              <textarea v-model="form.description" required placeholder="Décrivez le partenariat..." rows="4" />
            </div>
            <div class="field">
              <label>Ordre d'affichage</label>
              <input v-model.number="form.ordre" type="number" min="0" placeholder="0" />
            </div>
            <div class="mo-foot">
              <button type="button" class="btn btn-ghost" @click="showForm = false">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">
                <i v-if="saving" class="fas fa-spinner fa-spin"></i>
                <span v-else>{{ editing ? 'Enregistrer' : 'Créer le partenaire' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Liste -->
    <div v-if="loadingData" class="state-loading">
      <i class="fas fa-spinner fa-spin"></i> Chargement…
    </div>

    <div v-else-if="!partenaires.length" class="empty-state">
      <i class="fas fa-link"></i>
      <p>Aucun partenaire pour l'instant. Cliquez sur « Nouveau partenaire » pour commencer.</p>
    </div>

    <div v-else class="partenaires-grid">
      <div class="partenaire-card" v-for="p in partenaires" :key="p.id">
        <div class="pc-logo">
          <img v-if="p.image" :src="p.image" :alt="p.nom" />
          <div v-else class="pc-ph"><i class="fas fa-building"></i></div>
        </div>
        <div class="pc-body">
          <div class="pc-name">{{ p.nom }}</div>
          <div class="pc-desc">{{ p.description.substring(0, 60) }}...</div>
        </div>
        <div class="pc-acts">
          <button class="act" title="Modifier" @click="openForm(p)"><i class="fas fa-pen"></i></button>
          <button class="act act-red" title="Supprimer" @click="remove(p.id)"><i class="fas fa-trash"></i></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '../../api'

const partenaires = ref([])
const loadingData = ref(true)
const showForm = ref(false)
const saving = ref(false)
const formError = ref('')
const editing = ref(null)
const editingPartenaire = ref(null)
const form = ref({ nom: '', description: '', ordre: 0, imageFile: null, imagePreview: null })

async function load() {
  loadingData.value = true
  try {
    const { data } = await api.get('/admin/partenaires/')
    partenaires.value = data.results || data
  } finally {
    loadingData.value = false
  }
}

function openForm(p = null) {
  editing.value = p?.id || null
  editingPartenaire.value = p || null
  form.value = p
    ? { nom: p.nom, description: p.description, ordre: p.ordre || 0, imageFile: null, imagePreview: null }
    : { nom: '', description: '', ordre: 0, imageFile: null, imagePreview: null }
  formError.value = ''
  showForm.value = true
}

watch(() => form.value.imageFile, (file) => {
  if (file) {
    const reader = new FileReader()
    reader.onload = e => { form.value.imagePreview = e.target.result }
    reader.readAsDataURL(file)
  }
})

async function save() {
  formError.value = ''
  if (!form.value.nom || !form.value.description) {
    formError.value = 'Nom et description sont requis.'
    return
  }
  saving.value = true
  const fd = new FormData()
  fd.append('nom', form.value.nom)
  fd.append('description', form.value.description)
  fd.append('ordre', form.value.ordre)
  fd.append('actif', 'true')
  if (form.value.imageFile) fd.append('image', form.value.imageFile)
  try {
    if (editing.value) {
      await api.patch(`/admin/partenaires/${editing.value}/`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    } else {
      await api.post('/admin/partenaires/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    }
    showForm.value = false
    await load()
  } catch (e) {
    formError.value = e.response?.data?.detail || 'Erreur lors de l\'enregistrement.'
  } finally {
    saving.value = false
  }
}

async function remove(id) {
  if (!confirm('Supprimer ce partenaire ?')) return
  await api.delete(`/admin/partenaires/${id}/`)
  await load()
}

onMounted(load)
</script>

<style scoped>
.ap { width: 100%; }

.ap-hd {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
}
.ap-title { font-size: 1.4rem; font-weight: 700; color: #0f172a; margin-bottom: 2px; letter-spacing: -0.02em; }
.ap-desc { color: #94a3b8; font-size: 0.82rem; font-weight: 500; }

.btn {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 9px 18px; border-radius: 9px; font-size: 0.85rem; font-weight: 600;
  border: none; cursor: pointer; transition: all 0.15s;
}
.btn-primary { background: #059669; color: #fff; }
.btn-primary:hover { background: #047857; }
.btn-primary:disabled { opacity: 0.55; cursor: not-allowed; }
.btn-ghost { background: #f8fafc; color: #374151; border: 1px solid #e2e8f0; }
.btn-ghost:hover { background: #f1f5f9; }

/* Grid partenaires */
.partenaires-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.partenaire-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: box-shadow 0.2s, transform 0.2s;
}
.partenaire-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.08); transform: translateY(-2px); }

.pc-logo {
  width: 100%;
  aspect-ratio: 1;
  background: #f1f5f9;
  overflow: hidden;
}
.pc-logo img { width: 100%; height: 100%; object-fit: cover; display: block; }
.pc-ph {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  color: #cbd5e1; font-size: 3rem;
}

.pc-body { padding: 12px 14px 8px; }
.pc-name { font-weight: 700; color: #0f172a; font-size: 0.9rem; margin-bottom: 3px; }
.pc-desc { font-size: 0.75rem; color: #64748b; line-height: 1.3; }

.pc-acts {
  display: flex; gap: 6px; padding: 8px 12px 12px;
}
.act {
  width: 30px; height: 30px;
  border: 1px solid #e2e8f0; background: #f8fafc; color: #64748b;
  border-radius: 7px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; transition: all 0.15s;
}
.act:hover { background: #ecfdf5; color: #059669; border-color: #a7f3d0; }
.act-red:hover { background: #fef2f2; color: #dc2626; border-color: #fecaca; }

/* Modal */
.mo-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  backdrop-filter: blur(3px);
  display: flex; align-items: center; justify-content: center;
  z-index: 3000; padding: 20px;
}
.mo-box {
  background: #fff; border-radius: 14px; width: 100%; max-width: 520px;
  max-height: 90vh; overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.mo-head {
  display: flex; justify-content: space-between; align-items: center;
  padding: 18px 24px; border-bottom: 1px solid #e2e8f0;
}
.mo-head h2 { color: #0f172a; font-size: 1rem; font-weight: 700; display: flex; align-items: center; gap: 8px; }
.mo-head h2 i { color: #059669; }
.mo-close {
  background: none; border: none; color: #94a3b8; cursor: pointer;
  font-size: 1.1rem; border-radius: 6px; padding: 4px 8px; transition: background 0.15s;
}
.mo-close:hover { background: #f1f5f9; color: #dc2626; }
.mo-body { padding: 22px; }
.mo-foot { display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px; padding-top: 16px; border-top: 1px solid #e2e8f0; }
.mo-enter-active, .mo-leave-active { transition: opacity 0.2s; }
.mo-enter-from, .mo-leave-to { opacity: 0; }
.mo-enter-active .mo-box { transition: transform 0.2s; }
.mo-enter-from .mo-box { transform: scale(0.96) translateY(10px); }

/* Champs */
.field { margin-bottom: 15px; }
.field > label {
  display: block; font-size: 0.72rem; font-weight: 700; color: #475569;
  margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.05em;
}
.field > input,
.field > textarea {
  width: 100%; padding: 9px 12px; border: 1px solid #e2e8f0; border-radius: 8px;
  font-size: 0.88rem; color: #0f172a; background: #fff;
  transition: border-color 0.15s; box-sizing: border-box;
  font-family: inherit;
}
.field > input:focus,
.field > textarea:focus { outline: none; border-color: #059669; box-shadow: 0 0 0 3px rgba(5,150,105,0.1); }

.file-pick {
  display: flex; align-items: center; gap: 8px; padding: 9px 12px;
  border: 1px dashed #cbd5e1; border-radius: 8px; color: #64748b;
  font-size: 0.84rem; cursor: pointer; background: #f8fafc;
}
.file-pick:hover { border-color: #059669; color: #059669; }
.file-pick input { display: none; }

.form-err {
  background: #fef2f2; border: 1px solid #fca5a5; color: #dc2626;
  padding: 10px 14px; border-radius: 8px; margin-bottom: 16px; font-size: 0.84rem;
}

/* États */
.state-loading { padding: 60px; text-align: center; color: #94a3b8; font-size: 0.9rem; }
.empty-state { text-align: center; padding: 60px 20px; color: #cbd5e1; background: #fff; border-radius: 12px; border: 1px solid #e2e8f0; }
.empty-state i { font-size: 2.5rem; display: block; margin-bottom: 12px; opacity: 0.5; }
.empty-state p { font-size: 0.88rem; color: #94a3b8; }
</style>
