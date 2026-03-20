<template>
  <div class="ap">
    <div class="ap-hd">
      <div>
        <h1 class="ap-title">Services</h1>
        <p class="ap-desc">Gérez les services proposés par la coopérative</p>
      </div>
      <button class="btn btn-primary" @click="openForm()">
        <i class="fas fa-plus"></i> Nouveau service
      </button>
    </div>

    <Teleport to="body">
      <transition name="mo">
        <div v-if="showForm" class="mo-overlay" @click.self="showForm = false">
          <div class="mo-box">
            <div class="mo-head">
              <h2>{{ editing ? 'Modifier le service' : 'Nouveau service' }}</h2>
              <button class="mo-close" @click="showForm = false"><i class="fas fa-times"></i></button>
            </div>
            <form @submit.prevent="save" class="mo-body">
              <div class="field"><label>Titre *</label><input v-model="form.titre" required placeholder="Nom du service" /></div>
              <div class="field">
                <label>Icône FontAwesome</label>
                <input v-model="form.icone" placeholder="ex: fas fa-leaf" />
                <div v-if="form.icone" class="icon-preview">
                  <i :class="form.icone"></i> <span>Aperçu</span>
                </div>
              </div>
              <div class="field"><label>Description *</label><textarea v-model="form.description" rows="6" required placeholder="Description du service..."></textarea></div>
              <div class="field">
                <label>Image</label>
                <label class="file-pick">
                  <i class="fas fa-upload"></i>
                  <span>{{ form.imageFile ? form.imageFile.name : 'Choisir une image...' }}</span>
                  <input type="file" accept="image/*" @change="form.imageFile = $event.target.files[0]" />
                </label>
              </div>
              <div class="field"><label>Ordre d'affichage</label><input v-model.number="form.ordre" type="number" /></div>
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

    <div v-if="services.length" class="svc-grid">
      <div v-for="s in services" :key="s.id" class="svc-card">
        <div class="svc-img">
          <img v-if="s.image" :src="s.image" :alt="s.titre" />
          <div v-else class="svc-ph">
            <i :class="s.icone || 'fas fa-seedling'"></i>
          </div>
        </div>
        <div class="svc-body">
          <h3 class="svc-title">{{ s.titre }}</h3>
          <p class="svc-desc">{{ s.description?.slice(0, 100) }}{{ s.description?.length > 100 ? '...' : '' }}</p>
        </div>
        <div class="svc-foot">
          <button class="act" @click="openForm(s)" title="Modifier"><i class="fas fa-pen"></i> Modifier</button>
          <button class="act act-red" @click="remove(s.id)" title="Supprimer"><i class="fas fa-trash-alt"></i></button>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <i class="fas fa-seedling"></i><p>Aucun service enregistré</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const services = ref([])
const showForm = ref(false)
const editing = ref(null)
const saving = ref(false)
const form = ref({ titre: '', icone: '', description: '', ordre: 0, imageFile: null })

async function load() {
  const { data } = await api.get('/admin/services/')
  services.value = data.results || data
}

function openForm(s = null) {
  editing.value = s?.id || null
  form.value = s
    ? { titre: s.titre, icone: s.icone || '', description: s.description || '', ordre: s.ordre || 0, imageFile: null }
    : { titre: '', icone: '', description: '', ordre: 0, imageFile: null }
  showForm.value = true
}

async function save() {
  saving.value = true
  const fd = new FormData()
  fd.append('titre', form.value.titre)
  fd.append('description', form.value.description)
  fd.append('icone', form.value.icone)
  fd.append('ordre', form.value.ordre)
  if (form.value.imageFile) fd.append('image', form.value.imageFile)
  try {
    if (editing.value) {
      await api.put(`/admin/services/${editing.value}/`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    } else {
      await api.post('/admin/services/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    }
    showForm.value = false
    await load()
  } finally { saving.value = false }
}

async function remove(id) {
  if (!confirm('Supprimer ce service ?')) return
  await api.delete(`/admin/services/${id}/`)
  await load()
}

onMounted(load)
</script>

<style scoped>
.ap { width: 100%; }
.ap-hd {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 24px; flex-wrap: wrap; gap: 12px;
}
.ap-title { font-size: 1.4rem; font-weight: 700; color: #0f172a; margin-bottom: 2px; letter-spacing: -0.02em; }
.ap-desc { color: #94a3b8; font-size: 0.82rem; font-weight: 500; }

.btn { display: inline-flex; align-items: center; gap: 7px; padding: 9px 18px; border-radius: 9px; font-size: 0.85rem; font-weight: 600; border: none; cursor: pointer; transition: all 0.15s; }
.btn-primary { background: #059669; color: #fff; }
.btn-primary:hover { background: #047857; }
.btn-primary:disabled { opacity: 0.55; cursor: not-allowed; }
.btn-ghost { background: #f8fafc; color: #374151; border: 1px solid #e2e8f0; }
.btn-ghost:hover { background: #f1f5f9; }

.mo-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(3px); display: flex; align-items: center; justify-content: center; z-index: 3000; padding: 20px; }
.mo-box { background: #fff; border-radius: 14px; width: 100%; max-width: 560px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.mo-head { display: flex; justify-content: space-between; align-items: center; padding: 18px 24px; border-bottom: 1px solid #e2e8f0; }
.mo-head h2 { color: #0f172a; font-size: 1rem; font-weight: 700; }
.mo-close { background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 1.1rem; border-radius: 6px; transition: background 0.15s; padding: 4px 8px; }
.mo-close:hover { background: #f1f5f9; color: #dc2626; }
.mo-body { padding: 22px; }
.mo-foot { display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px; padding-top: 16px; border-top: 1px solid #e2e8f0; }
.mo-enter-active, .mo-leave-active { transition: opacity 0.2s; }
.mo-enter-from, .mo-leave-to { opacity: 0; }
.mo-enter-active .mo-box { transition: transform 0.2s; }
.mo-enter-from .mo-box { transform: scale(0.96) translateY(10px); }

.field { margin-bottom: 15px; }
.field label { display: block; font-size: 0.72rem; font-weight: 700; color: #475569; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.05em; }
.field input, .field textarea, .field select { width: 100%; padding: 9px 12px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.88rem; color: #0f172a; background: #fff; transition: border-color 0.15s; box-sizing: border-box; }
.field input:focus, .field textarea:focus { outline: none; border-color: #059669; box-shadow: 0 0 0 3px rgba(5,150,105,0.1); }

.icon-preview { margin-top: 6px; padding: 8px 12px; background: #ecfdf5; border-radius: 8px; color: #059669; font-size: 0.9rem; display: flex; align-items: center; gap: 8px; }
.file-pick { display: flex; align-items: center; gap: 8px; padding: 9px 12px; border: 1px dashed #cbd5e1; border-radius: 8px; color: #64748b; font-size: 0.84rem; cursor: pointer; background: #f8fafc; transition: border-color 0.15s; }
.file-pick:hover { border-color: #059669; color: #059669; }
.file-pick input { display: none; }

.svc-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 18px; }
.svc-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: box-shadow 0.2s, transform 0.2s; }
.svc-card:hover { box-shadow: 0 6px 24px rgba(0,0,0,0.08); transform: translateY(-2px); }
.svc-img { aspect-ratio: 16/9; background: #f1f5f9; overflow: hidden; }
.svc-img img { width: 100%; height: 100%; object-fit: cover; display: block; }
.svc-ph { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: #cbd5e1; }
.svc-body { padding: 16px; flex: 1; }
.svc-title { font-size: 0.95rem; font-weight: 700; color: #0f172a; margin-bottom: 6px; }
.svc-desc { font-size: 0.82rem; color: #64748b; line-height: 1.55; }
.svc-foot { padding: 10px 16px; border-top: 1px solid #f1f5f9; display: flex; gap: 8px; align-items: center; }

.act { display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; border: 1px solid #e2e8f0; background: #f8fafc; color: #64748b; border-radius: 8px; cursor: pointer; font-size: 0.76rem; font-weight: 600; transition: all 0.15s; }
.act:hover { background: #ecfdf5; color: #059669; border-color: #a7f3d0; }
.act-red:hover { background: #fef2f2; color: #dc2626; border-color: #fecaca; }

.empty-state { text-align: center; padding: 60px 20px; color: #cbd5e1; background: #fff; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.empty-state i { font-size: 3rem; display: block; margin-bottom: 12px; opacity: 0.4; }
.empty-state p { font-size: 0.88rem; color: #94a3b8; }

@media (max-width: 600px) {
  .svc-grid { grid-template-columns: 1fr; }
  .ap-hd { flex-direction: column; align-items: flex-start; }
}
</style>
