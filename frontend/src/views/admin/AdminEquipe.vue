<template>
  <div class="ap">
    <!-- Header -->
    <div class="ap-hd">
      <div>
        <div class="ap-title">Équipe</div>
        <div class="ap-desc">Gérer les membres de l'équipe affichés sur le site</div>
      </div>
      <button class="btn btn-primary" @click="openForm()">
        <i class="fas fa-plus"></i> Nouveau membre
      </button>
    </div>

    <!-- Modal création/édition -->
    <transition name="mo">
      <div v-if="showForm" class="mo-overlay" @click.self="showForm = false">
        <div class="mo-box">
          <div class="mo-head">
            <h2><i :class="editing ? 'fas fa-user-edit' : 'fas fa-user-plus'"></i>
              {{ editing ? 'Modifier le membre' : 'Nouveau membre' }}
            </h2>
            <button class="mo-close" @click="showForm = false"><i class="fas fa-times"></i></button>
          </div>
          <form @submit.prevent="save" class="mo-body">
            <div v-if="formError" class="form-err">{{ formError }}</div>
            <div class="field-row">
              <div class="field">
                <label>Nom *</label>
                <input v-model="form.nom" required placeholder="DUPONT" />
              </div>
              <div class="field">
                <label>Prénom *</label>
                <input v-model="form.prenom" required placeholder="Jean" />
              </div>
            </div>
            <div class="field">
              <label>Fonction *</label>
              <input v-model="form.fonction" required placeholder="ex: Président, Secrétaire général..." />
            </div>
            <div class="field">
              <label>Photo</label>
              <label class="file-pick">
                <i class="fas fa-image"></i>
                <span>{{ form.imageFile ? form.imageFile.name : 'Choisir une photo...' }}</span>
                <input type="file" accept="image/*" @change="form.imageFile = $event.target.files[0]" />
              </label>
              <div v-if="form.imagePreview || editingMembre?.image" style="margin-top:8px;">
                <img :src="form.imageFile ? form.imagePreview : editingMembre?.image"
                     style="width:80px;height:80px;object-fit:cover;border-radius:8px;border:1px solid #e2e8f0;" />
              </div>
            </div>
            <div class="field">
              <label>Ordre d'affichage</label>
              <input v-model.number="form.ordre" type="number" min="0" placeholder="0" />
            </div>
            <div class="mo-foot">
              <button type="button" class="btn btn-ghost" @click="showForm = false">Annuler</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">
                <i v-if="saving" class="fas fa-spinner fa-spin"></i>
                <span v-else>{{ editing ? 'Enregistrer' : 'Créer le membre' }}</span>
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

    <div v-else-if="!membres.length" class="empty-state">
      <i class="fas fa-users"></i>
      <p>Aucun membre pour l'instant. Cliquez sur « Nouveau membre » pour commencer.</p>
    </div>

    <div v-else class="membres-grid">
      <div class="membre-card" v-for="m in membres" :key="m.id">
        <div class="mc-photo">
          <img v-if="m.image" :src="m.image" :alt="m.prenom + ' ' + m.nom" />
          <div v-else class="mc-ph"><i class="fas fa-user"></i></div>
        </div>
        <div class="mc-body">
          <div class="mc-name">{{ m.prenom }} {{ m.nom }}</div>
          <div class="mc-fonction">{{ m.fonction }}</div>
        </div>
        <div class="mc-acts">
          <button class="act" title="Modifier" @click="openForm(m)"><i class="fas fa-pen"></i></button>
          <button class="act act-red" title="Supprimer" @click="remove(m.id)"><i class="fas fa-trash"></i></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '../../api'

const membres = ref([])
const loadingData = ref(true)
const showForm = ref(false)
const saving = ref(false)
const formError = ref('')
const editing = ref(null)
const editingMembre = ref(null)
const form = ref({ prenom: '', nom: '', fonction: '', ordre: 0, imageFile: null, imagePreview: null })

async function load() {
  loadingData.value = true
  try {
    const { data } = await api.get('/admin/equipe/')
    membres.value = data.results || data
  } finally {
    loadingData.value = false
  }
}

function openForm(m = null) {
  editing.value = m?.id || null
  editingMembre.value = m || null
  form.value = m
    ? { prenom: m.prenom, nom: m.nom, fonction: m.fonction, ordre: m.ordre || 0, imageFile: null, imagePreview: null }
    : { prenom: '', nom: '', fonction: '', ordre: 0, imageFile: null, imagePreview: null }
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
  if (!form.value.prenom || !form.value.nom || !form.value.fonction) {
    formError.value = 'Prénom, nom et fonction sont requis.'
    return
  }
  saving.value = true
  const fd = new FormData()
  fd.append('prenom', form.value.prenom)
  fd.append('nom', form.value.nom)
  fd.append('fonction', form.value.fonction)
  fd.append('ordre', form.value.ordre)
  fd.append('actif', 'true')
  if (form.value.imageFile) fd.append('image', form.value.imageFile)
  try {
    if (editing.value) {
      await api.patch(`/admin/equipe/${editing.value}/`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    } else {
      await api.post('/admin/equipe/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
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
  if (!confirm('Supprimer ce membre ?')) return
  await api.delete(`/admin/equipe/${id}/`)
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

/* Grid membres */
.membres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.membre-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: box-shadow 0.2s, transform 0.2s;
}
.membre-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.08); transform: translateY(-2px); }

.mc-photo {
  width: 100%;
  aspect-ratio: 1;
  background: #f1f5f9;
  overflow: hidden;
}
.mc-photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
.mc-ph {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  color: #cbd5e1; font-size: 3rem;
}

.mc-body { padding: 12px 14px 8px; }
.mc-name { font-weight: 700; color: #0f172a; font-size: 0.9rem; margin-bottom: 3px; }
.mc-fonction { font-size: 0.75rem; color: #059669; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }

.mc-acts {
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
.field > input {
  width: 100%; padding: 9px 12px; border: 1px solid #e2e8f0; border-radius: 8px;
  font-size: 0.88rem; color: #0f172a; background: #fff;
  transition: border-color 0.15s; box-sizing: border-box;
}
.field > input:focus { outline: none; border-color: #059669; box-shadow: 0 0 0 3px rgba(5,150,105,0.1); }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

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
