<template>
  <div class="ap">
    <!-- Page header — uses "ap-hd" NOT "page-header" to avoid global CSS conflict -->
    <div class="ap-hd">
      <div>
        <h1 class="ap-title">Articles de blog</h1>
        <p class="ap-desc">Gérez vos publications</p>
      </div>
      <button class="btn btn-primary" @click="openForm()">
        <i class="fas fa-plus"></i> Nouvel article
      </button>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <transition name="mo">
        <div v-if="showForm" class="mo-overlay" @click.self="showForm = false">
          <div class="mo-box">
            <div class="mo-head">
              <h2>{{ editing ? 'Modifier l\'article' : 'Nouvel article' }}</h2>
              <button class="mo-close" @click="showForm = false"><i class="fas fa-times"></i></button>
            </div>
            <form @submit.prevent="save" class="mo-body">
              <div class="field">
                <label>Titre *</label>
                <input v-model="form.titre" required placeholder="Titre de l'article" />
              </div>
              <div class="field">
                <label>Extrait</label>
                <textarea v-model="form.extrait" rows="2" placeholder="Court résumé..."></textarea>
              </div>
              <div class="field">
                <label>Contenu *</label>
                <textarea v-model="form.contenu" rows="8" required placeholder="Contenu de l'article..."></textarea>
              </div>
              <div class="field-row">
                <div class="field">
                  <label>Image de couverture</label>
                  <label class="file-pick">
                    <i class="fas fa-upload"></i>
                    <span>{{ form.imageFile ? form.imageFile.name : 'Choisir un fichier' }}</span>
                    <input type="file" accept="image/*" @change="form.imageFile = $event.target.files[0]" />
                  </label>
                </div>
                <div class="field">
                  <label>Statut de publication</label>
                  <label class="tgl">
                    <input type="checkbox" v-model="form.publie" />
                    <span class="tgl-track"></span>
                    <span class="tgl-lbl">{{ form.publie ? 'Publié' : 'Brouillon' }}</span>
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
        <span class="tbl-count">{{ posts.length }} article{{ posts.length > 1 ? 's' : '' }}</span>
      </div>
      <div class="tbl-wrap">
        <table>
          <thead>
            <tr>
              <th>IMAGE</th>
              <th>TITRE</th>
              <th>STATUT</th>
              <th>DATE</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in posts" :key="p.id">
              <td>
                <img v-if="p.image" :src="p.image" class="thumb" :alt="p.titre" />
                <div v-else class="thumb-ph"><i class="fas fa-image"></i></div>
              </td>
              <td><span class="cell-bold">{{ p.titre }}</span></td>
              <td>
                <span class="badge" :class="p.publie ? 'badge-ok' : 'badge-muted'">
                  {{ p.publie ? 'Publié' : 'Brouillon' }}
                </span>
              </td>
              <td class="cell-date">{{ fmtDate(p.date_creation) }}</td>
              <td>
                <div class="cell-acts">
                  <button class="act" @click="openForm(p)" title="Modifier"><i class="fas fa-pen"></i></button>
                  <button class="act act-red" @click="remove(p.id)" title="Supprimer"><i class="fas fa-trash-alt"></i></button>
                </div>
              </td>
            </tr>
            <tr v-if="!posts.length">
              <td colspan="5" class="tbl-empty">
                <i class="fas fa-newspaper"></i><span>Aucun article pour l'instant</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const posts = ref([])
const showForm = ref(false)
const editing = ref(null)
const saving = ref(false)
const form = ref({ titre: '', extrait: '', contenu: '', publie: false, imageFile: null })

function fmtDate(d) {
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function load() {
  const { data } = await api.get('/admin/blog/')
  posts.value = data.results || data
}

function openForm(post = null) {
  editing.value = post?.id || null
  form.value = post
    ? { titre: post.titre, extrait: post.extrait || '', contenu: post.contenu || '', publie: post.publie, imageFile: null }
    : { titre: '', extrait: '', contenu: '', publie: false, imageFile: null }
  showForm.value = true
}

async function save() {
  saving.value = true
  const fd = new FormData()
  fd.append('titre', form.value.titre)
  fd.append('extrait', form.value.extrait)
  fd.append('contenu', form.value.contenu)
  fd.append('publie', form.value.publie)
  if (form.value.imageFile) fd.append('image', form.value.imageFile)
  try {
    if (editing.value) {
      await api.patch(`/admin/blog/${editing.value}/`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    } else {
      await api.post('/admin/blog/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    }
    showForm.value = false
    await load()
  } finally { saving.value = false }
}

async function remove(id) {
  if (!confirm('Supprimer cet article ?')) return
  await api.delete(`/admin/blog/${id}/`)
  await load()
}

onMounted(load)
</script>

<style scoped>
.ap { width: 100%; }

/* ── Page header ── */
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

/* ── Buttons ── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 9px 18px;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.15s;
  text-decoration: none;
}
.btn-primary { background: #059669; color: #fff; }
.btn-primary:hover { background: #047857; }
.btn-primary:disabled { opacity: 0.55; cursor: not-allowed; }
.btn-ghost {
  background: #f8fafc;
  color: #374151;
  border: 1px solid #e2e8f0;
}
.btn-ghost:hover { background: #f1f5f9; }

/* ── Modal ── */
.mo-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.35);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
  padding: 20px;
}
.mo-box {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 640px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.mo-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 24px;
  border-bottom: 1px solid #e2e8f0;
}
.mo-head h2 { color: #0f172a; font-size: 1rem; font-weight: 700; }
.mo-close {
  background: none;
  border: none;
  color: #9ab5a4;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 4px;
  border-radius: 6px;
  transition: background 0.15s;
}
.mo-close:hover { background: #f1f5f9; color: #dc2626; }
.mo-body { padding: 24px; }
.mo-foot {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}
.mo-enter-active, .mo-leave-active { transition: opacity 0.2s; }
.mo-enter-from, .mo-leave-to { opacity: 0; }
.mo-enter-active .mo-box { transition: transform 0.2s ease; }
.mo-enter-from .mo-box { transform: scale(0.96) translateY(10px); }

/* ── Form fields ── */
.field { margin-bottom: 16px; }
.field > label {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  color: #475569;
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.field input, .field textarea, .field select {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.88rem;
  color: #0f172a;
  background: #fff;
  transition: border-color 0.15s, box-shadow 0.15s;
  box-sizing: border-box;
}
.field input:focus, .field textarea:focus, .field select:focus {
  outline: none;
  border-color: #059669;
  box-shadow: 0 0 0 3px rgba(5,150,105,0.1);
}
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

.file-pick {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 12px;
  border: 1px dashed #cbd5e1;
  border-radius: 8px;
  color: #64748b;
  font-size: 0.84rem;
  cursor: pointer;
  transition: border-color 0.15s;
  background: #f8fafc;
}
.file-pick:hover { border-color: #059669; color: #059669; }
.file-pick input { display: none; }

.tgl { display: flex !important; align-items: center; gap: 10px; cursor: pointer; margin-top: 8px; }
.tgl input { display: none; }
.tgl-track {
  width: 40px; height: 22px;
  background: #cbd5e1;
  border-radius: 11px;
  position: relative;
  transition: background 0.2s;
  flex-shrink: 0;
}
.tgl-track::after {
  content: '';
  position: absolute;
  top: 3px; left: 3px;
  width: 16px; height: 16px;
  background: #fff;
  border-radius: 50%;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.25);
}
.tgl input:checked + .tgl-track { background: #059669; }
.tgl input:checked + .tgl-track::after { transform: translateX(18px); }
.tgl-lbl { color: #64748b; font-size: 0.84rem; font-weight: 500; }

/* ── Table ── */
.tbl-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.tbl-top {
  padding: 12px 20px;
  border-bottom: 1px solid #e2e8f0;
}
.tbl-count { color: #94a3b8; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.02em; }
.tbl-wrap { overflow-x: auto; }

table { width: 100%; border-collapse: collapse; }
th {
  text-align: left;
  padding: 10px 18px;
  font-size: 0.65rem;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.08em;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
  text-transform: uppercase;
}
td {
  padding: 12px 18px;
  color: #334155;
  font-size: 0.84rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}
tr:last-child td { border-bottom: none; }
tr:hover td { background: #f8fafc; }

.thumb {
  width: 52px; height: 36px;
  object-fit: cover;
  border-radius: 7px;
  border: 1px solid #e0ebe5;
  display: block;
}
.thumb-ph {
  width: 52px; height: 36px;
  background: #f0f6f2;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c0d4c8;
}
.cell-bold { font-weight: 600; color: #0f172a; }
.cell-date { color: #94a3b8; font-size: 0.76rem; white-space: nowrap; }

.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.72rem;
  font-weight: 700;
}
.badge-ok { background: #d1fae5; color: #065f46; }
.badge-muted { background: #f1f5f9; color: #64748b; }

.cell-acts { display: flex; gap: 6px; }
.act {
  width: 32px; height: 32px;
  border: 1px solid #ddeae2;
  background: #f4f8f5;
  color: #5a7a68;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  transition: all 0.15s;
}
.act:hover { background: #ddf0e5; color: #2d7d46; border-color: #b8d4c4; }
.act-red { }
.act-red:hover { background: #fef2f2; color: #dc2626; border-color: #fca5a5; }

.tbl-empty {
  text-align: center;
  padding: 40px;
  color: #b8d4c4;
}
.tbl-empty i { font-size: 2rem; display: block; margin-bottom: 8px; }
.tbl-empty span { font-size: 0.88rem; display: block; }

@media (max-width: 600px) {
  .field-row { grid-template-columns: 1fr; }
  .ap-hd { flex-direction: column; align-items: flex-start; }
  th:nth-child(1), td:nth-child(1) { display: none; }
}
</style>
