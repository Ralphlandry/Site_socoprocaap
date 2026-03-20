<template>
  <div class="ap">
    <div class="ap-hd">
      <div>
        <h1 class="ap-title">Galerie photo</h1>
        <p class="ap-desc">Gérez vos images et catégories</p>
      </div>
      <div class="ap-actions">
        <button class="btn btn-ghost" @click="showCatForm = true">
          <i class="fas fa-folder-plus"></i> Catégorie
        </button>
        <button class="btn btn-primary" @click="openForm()">
          <i class="fas fa-plus"></i> Nouvelle image
        </button>
      </div>
    </div>

    <!-- Cat modal -->
    <Teleport to="body">
      <transition name="mo">
        <div v-if="showCatForm" class="mo-overlay" @click.self="showCatForm = false">
          <div class="mo-box mo-sm">
            <div class="mo-head">
              <h2>Nouvelle catégorie</h2>
              <button class="mo-close" @click="showCatForm = false"><i class="fas fa-times"></i></button>
            </div>
            <form @submit.prevent="saveCat" class="mo-body">
              <div class="field"><label>Nom *</label><input v-model="catForm.nom" required placeholder="ex: Élevage" /></div>
              <div class="field"><label>Ordre d'affichage</label><input v-model.number="catForm.ordre" type="number" placeholder="0" /></div>
              <div class="mo-foot">
                <button type="button" class="btn btn-ghost" @click="showCatForm = false">Annuler</button>
                <button type="submit" class="btn btn-primary">Enregistrer</button>
              </div>
            </form>
          </div>
        </div>
      </transition>
    </Teleport>

    <!-- Image modal -->
    <Teleport to="body">
      <transition name="mo">
        <div v-if="showForm" class="mo-overlay" @click.self="showForm = false">
          <div class="mo-box">
            <div class="mo-head">
              <h2>{{ editing ? 'Modifier l\'image' : 'Nouvelle image' }}</h2>
              <button class="mo-close" @click="showForm = false"><i class="fas fa-times"></i></button>
            </div>
            <form @submit.prevent="save" class="mo-body">
              <div class="field"><label>Titre *</label><input v-model="form.titre" required placeholder="Titre de l'image" /></div>
              <div class="field-row">
                <div class="field">
                  <label>Catégorie</label>
                  <select v-model="form.categorie">
                    <option :value="null">-- Aucune --</option>
                    <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.nom }}</option>
                  </select>
                </div>
                <div class="field">
                  <label>Visibilité</label>
                  <label class="tgl">
                    <input type="checkbox" v-model="form.publie" />
                    <span class="tgl-track"></span>
                    <span class="tgl-lbl">{{ form.publie ? 'Publié' : 'Masqué' }}</span>
                  </label>
                </div>
              </div>
              <div class="field"><label>Description</label><textarea v-model="form.description" rows="3" placeholder="Description optionnelle..."></textarea></div>
              <div class="field">
                <label>Fichier image</label>
                <label class="file-pick">
                  <i class="fas fa-upload"></i>
                  <span>{{ form.imageFile ? form.imageFile.name : 'Choisir un fichier...' }}</span>
                  <input type="file" accept="image/*" @change="form.imageFile = $event.target.files[0]" />
                </label>
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

    <!-- Image grid -->
    <div v-if="images.length" class="img-grid">
      <div v-for="img in images" :key="img.id" class="img-card">
        <div class="img-thumb">
          <img v-if="img.image" :src="img.image" :alt="img.titre" />
          <div v-else class="img-ph"><i class="fas fa-image"></i></div>
          <span class="img-badge" :class="img.publie ? 'badge-ok' : 'badge-muted'">
            {{ img.publie ? 'Publié' : 'Masqué' }}
          </span>
        </div>
        <div class="img-info">
          <span class="img-name">{{ img.titre }}</span>
          <span class="img-cat">{{ img.categorie_nom || 'Sans catégorie' }}</span>
          <div class="img-acts">
            <button class="act" @click="openForm(img)" title="Modifier"><i class="fas fa-pen"></i></button>
            <button class="act act-red" @click="remove(img.id)" title="Supprimer"><i class="fas fa-trash-alt"></i></button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="empty-state">
      <i class="fas fa-images"></i><p>Aucune image dans la galerie</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const images = ref([])
const categories = ref([])
const showForm = ref(false)
const showCatForm = ref(false)
const editing = ref(null)
const saving = ref(false)
const form = ref({ titre: '', categorie: null, description: '', publie: true, imageFile: null })
const catForm = ref({ nom: '', ordre: 0 })

async function load() {
  const [imgRes, catRes] = await Promise.all([api.get('/admin/galerie/'), api.get('/admin/galerie/categories/')])
  images.value = imgRes.data.results || imgRes.data
  categories.value = catRes.data.results || catRes.data
}

function openForm(img = null) {
  editing.value = img?.id || null
  form.value = img
    ? { titre: img.titre, categorie: img.categorie, description: img.description || '', publie: img.publie, imageFile: null }
    : { titre: '', categorie: null, description: '', publie: true, imageFile: null }
  showForm.value = true
}

async function save() {
  saving.value = true
  const fd = new FormData()
  fd.append('titre', form.value.titre)
  if (form.value.categorie) fd.append('categorie', form.value.categorie)
  fd.append('description', form.value.description)
  fd.append('publie', form.value.publie)
  if (form.value.imageFile) fd.append('image', form.value.imageFile)
  try {
    if (editing.value) {
      await api.put(`/admin/galerie/${editing.value}/`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    } else {
      await api.post('/admin/galerie/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    }
    showForm.value = false
    await load()
  } finally { saving.value = false }
}

async function saveCat() {
  await api.post('/admin/galerie/categories/', catForm.value)
  catForm.value = { nom: '', ordre: 0 }
  showCatForm.value = false
  await load()
}

async function remove(id) {
  if (!confirm('Supprimer cette image ?')) return
  await api.delete(`/admin/galerie/${id}/`)
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
.ap-actions { display: flex; gap: 10px; flex-wrap: wrap; }

.btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 9px 18px;
  border-radius: 9px;
  font-size: 0.85rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.15s;
}
.btn-primary { background: #059669; color: #fff; }
.btn-primary:hover { background: #047857; }
.btn-primary:disabled { opacity: 0.55; cursor: not-allowed; }
.btn-ghost { background: #f8fafc; color: #374151; border: 1px solid #e2e8f0; }
.btn-ghost:hover { background: #f1f5f9; }

/* Modal */
.mo-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
  padding: 20px;
}
.mo-box {
  background: #fff;
  border-radius: 14px;
  width: 100%;
  max-width: 580px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.mo-sm { max-width: 380px; }
.mo-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 24px;
  border-bottom: 1px solid #e2e8f0;
}
.mo-head h2 { color: #0f172a; font-size: 1rem; font-weight: 700; }
.mo-close {
  background: none; border: none; color: #94a3b8;
  cursor: pointer; font-size: 1.1rem; border-radius: 6px;
  transition: background 0.15s; padding: 4px 8px;
}
.mo-close:hover { background: #f1f5f9; color: #dc2626; }
.mo-body { padding: 22px; }
.mo-foot {
  display: flex; gap: 10px; justify-content: flex-end;
  margin-top: 20px; padding-top: 16px; border-top: 1px solid #e2e8f0;
}
.mo-enter-active, .mo-leave-active { transition: opacity 0.2s; }
.mo-enter-from, .mo-leave-to { opacity: 0; }
.mo-enter-active .mo-box { transition: transform 0.2s; }
.mo-enter-from .mo-box { transform: scale(0.96) translateY(10px); }

/* Fields */
.field { margin-bottom: 15px; }
.field > label {
  display: block; font-size: 0.72rem; font-weight: 700; color: #475569;
  margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.05em;
}
.field input, .field textarea, .field select {
  width: 100%; padding: 9px 12px; border: 1px solid #e2e8f0; border-radius: 8px;
  font-size: 0.88rem; color: #0f172a; background: #fff; transition: border-color 0.15s; box-sizing: border-box;
}
.field input:focus, .field textarea:focus, .field select:focus {
  outline: none; border-color: #059669; box-shadow: 0 0 0 3px rgba(5,150,105,0.1);
}
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

.file-pick {
  display: flex; align-items: center; gap: 8px; padding: 9px 12px;
  border: 1px dashed #cbd5e1; border-radius: 8px; color: #64748b;
  font-size: 0.84rem; cursor: pointer; background: #f8fafc; transition: border-color 0.15s;
}
.file-pick:hover { border-color: #059669; color: #059669; }
.file-pick input { display: none; }

.tgl { display: flex !important; align-items: center; gap: 10px; cursor: pointer; margin-top: 8px; }
.tgl input { display: none; }
.tgl-track {
  width: 40px; height: 22px; background: #cbd5e1; border-radius: 11px;
  position: relative; transition: background 0.2s; flex-shrink: 0;
}
.tgl-track::after {
  content: ''; position: absolute; top: 3px; left: 3px; width: 16px; height: 16px;
  background: #fff; border-radius: 50%; transition: transform 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.25);
}
.tgl input:checked + .tgl-track { background: #059669; }
.tgl input:checked + .tgl-track::after { transform: translateX(18px); }
.tgl-lbl { color: #64748b; font-size: 0.84rem; font-weight: 500; }

/* Image grid */
.img-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}
.img-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: box-shadow 0.2s, transform 0.2s;
}
.img-card:hover { box-shadow: 0 6px 24px rgba(0,0,0,0.08); transform: translateY(-2px); }
.img-thumb {
  position: relative;
  aspect-ratio: 4/3;
  background: #f1f5f9;
}
.img-thumb img { width: 100%; height: 100%; object-fit: cover; display: block; }
.img-ph { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: #cbd5e1; font-size: 2.5rem; }

.img-badge {
  position: absolute;
  top: 8px; left: 8px;
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 0.64rem;
  font-weight: 700;
}
.badge-ok { background: #d1fae5; color: #065f46; }
.badge-muted { background: #f1f5f9; color: #64748b; }

.img-info {
  padding: 10px 12px;
}
.img-name { display: block; font-weight: 600; color: #0f172a; font-size: 0.84rem; margin-bottom: 2px; }
.img-cat { display: block; color: #94a3b8; font-size: 0.73rem; margin-bottom: 8px; }
.img-acts { display: flex; gap: 6px; }

.act {
  width: 30px; height: 30px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #64748b;
  border-radius: 7px;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem;
  transition: all 0.15s;
}
.act:hover { background: #ecfdf5; color: #059669; border-color: #a7f3d0; }
.act-red:hover { background: #fef2f2; color: #dc2626; border-color: #fecaca; }

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #cbd5e1;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.empty-state i { font-size: 3rem; display: block; margin-bottom: 12px; opacity: 0.4; }
.empty-state p { font-size: 0.88rem; color: #94a3b8; }

@media (max-width: 600px) {
  .img-grid { grid-template-columns: 1fr 1fr; }
  .field-row { grid-template-columns: 1fr; }
  .ap-hd { flex-direction: column; align-items: flex-start; }
}
@media (max-width: 400px) {
  .img-grid { grid-template-columns: 1fr; }
}
</style>
