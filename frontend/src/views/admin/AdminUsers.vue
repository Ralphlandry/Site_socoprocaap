<template>
  <div class="ap">
    <!-- Header -->
    <div class="ap-hd">
      <div>
        <div class="ap-title">Utilisateurs</div>
        <div class="ap-desc">Gérer les comptes d'accès à l'administration</div>
      </div>
      <button class="btn btn-primary" @click="openCreate">
        <i class="fas fa-plus"></i> Nouvel utilisateur
      </button>
    </div>

    <!-- User list -->
    <div class="table-wrap">
      <div v-if="loading" class="state-loading">
        <i class="fas fa-spinner fa-spin"></i> Chargement…
      </div>
      <div v-else-if="!users.length" class="empty-state">
        <i class="fas fa-users"></i>
        <p>Aucun utilisateur trouvé.</p>
      </div>
      <table v-else class="user-table">
        <thead>
          <tr>
            <th>Utilisateur</th>
            <th>Email</th>
            <th>Rôle</th>
            <th>Statut</th>
            <th>Mot de passe</th>
            <th>Inscrit le</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id" :class="{ 'row-me': u.id === myId }">
            <td>
              <div class="u-name-wrap">
                <div class="u-avatar">{{ u.username.charAt(0).toUpperCase() }}</div>
                <span class="u-name">{{ u.username }}</span>
                <span v-if="u.id === myId" class="badge-me">Vous</span>
              </div>
            </td>
            <td class="u-email">{{ u.email || '—' }}</td>
            <td>
              <span v-if="u.is_superuser" class="badge badge-super">Super-admin</span>
              <span v-else-if="u.is_staff" class="badge badge-staff">Admin</span>
              <span v-else class="badge badge-user">Utilisateur</span>
            </td>
            <td>
              <span class="badge" :class="u.is_active ? 'badge-active' : 'badge-inactive'">
                {{ u.is_active ? 'Actif' : 'Inactif' }}
              </span>
            </td>
            <td class="u-pass">
              <span class="pass-mask"><i class="fas fa-lock"></i> ••••••••</span>
            </td>
            <td class="u-date">{{ formatDate(u.date_joined) }}</td>
            <td>
              <div class="acts">
                <button class="act" title="Modifier" @click="openEdit(u)">
                  <i class="fas fa-pen"></i>
                </button>
                <button class="act" title="Changer le mot de passe" @click="openPassword(u)">
                  <i class="fas fa-key"></i>
                </button>
                <button
                  class="act act-red"
                  title="Supprimer"
                  :disabled="u.id === myId"
                  @click="deleteUser(u)"
                >
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ── Create modal ── -->
    <transition name="mo">
      <div v-if="showCreate" class="mo-overlay" @click.self="showCreate = false">
        <div class="mo-box">
          <div class="mo-head">
            <h2><i class="fas fa-user-plus"></i> Nouvel utilisateur</h2>
            <button class="mo-close" @click="showCreate = false"><i class="fas fa-times"></i></button>
          </div>
          <div class="mo-body">
            <div v-if="createError" class="form-err">{{ createError }}</div>
            <div class="field-row">
              <div class="field">
                <label>Identifiant *</label>
                <input v-model="form.username" type="text" placeholder="nomutilisateur" required />
              </div>
              <div class="field">
                <label>Email</label>
                <input v-model="form.email" type="email" placeholder="utilisateur@exemple.com" />
              </div>
            </div>
            <div class="field">
              <label>Mot de passe * <small>(8 caractères min.)</small></label>
              <input v-model="form.password" type="password" placeholder="••••••••" required />
            </div>
            <div class="field">
              <label class="tgl">
                <input type="checkbox" v-model="form.is_staff" />
                <span class="tgl-track"></span>
                <span class="tgl-lbl">Accès administrateur</span>
              </label>
            </div>
            <div class="mo-foot">
              <button class="btn btn-ghost" @click="showCreate = false">Annuler</button>
              <button class="btn btn-primary" :disabled="creating" @click="createUser">
                <i v-if="creating" class="fas fa-spinner fa-spin"></i>
                <span v-else>Créer l'utilisateur</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- ── Edit modal ── -->
    <transition name="mo">
      <div v-if="showEdit" class="mo-overlay" @click.self="showEdit = false">
        <div class="mo-box">
          <div class="mo-head">
            <h2><i class="fas fa-user-edit"></i> Modifier « {{ editTarget?.username }} »</h2>
            <button class="mo-close" @click="showEdit = false"><i class="fas fa-times"></i></button>
          </div>
          <div class="mo-body">
            <div v-if="editError" class="form-err">{{ editError }}</div>
            <div class="field-row">
              <div class="field">
                <label>Identifiant *</label>
                <input v-model="editForm.username" type="text" />
              </div>
              <div class="field">
                <label>Email</label>
                <input v-model="editForm.email" type="email" />
              </div>
            </div>
            <div class="field">
              <label class="tgl">
                <input type="checkbox" v-model="editForm.is_staff" />
                <span class="tgl-track"></span>
                <span class="tgl-lbl">Accès administrateur</span>
              </label>
            </div>
            <div class="field" style="margin-top:8px;">
              <label class="tgl">
                <input type="checkbox" v-model="editForm.is_active" />
                <span class="tgl-track"></span>
                <span class="tgl-lbl">Compte actif</span>
              </label>
            </div>
            <div class="mo-foot">
              <button class="btn btn-ghost" @click="showEdit = false">Annuler</button>
              <button class="btn btn-primary" :disabled="editing" @click="saveEdit">
                <i v-if="editing" class="fas fa-spinner fa-spin"></i>
                <span v-else>Enregistrer</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- ── Change password modal ── -->
    <transition name="mo">
      <div v-if="showPassword" class="mo-overlay" @click.self="showPassword = false">
        <div class="mo-box mo-sm">
          <div class="mo-head">
            <h2><i class="fas fa-key"></i> Mot de passe — {{ passwordTarget?.username }}</h2>
            <button class="mo-close" @click="showPassword = false"><i class="fas fa-times"></i></button>
          </div>
          <div class="mo-body">
            <div v-if="pwdError" class="form-err">{{ pwdError }}</div>
            <div v-if="pwdSuccess" class="form-ok">{{ pwdSuccess }}</div>
            <div class="field">
              <label>Nouveau mot de passe <small>(8 caractères min.)</small></label>
              <input v-model="pwdForm.password" type="password" placeholder="••••••••" />
            </div>
            <div class="field">
              <label>Confirmer</label>
              <input v-model="pwdForm.confirm" type="password" placeholder="••••••••" />
            </div>
            <div class="mo-foot">
              <button class="btn btn-ghost" @click="showPassword = false">Annuler</button>
              <button class="btn btn-primary" :disabled="changingPwd" @click="changePassword">
                <i v-if="changingPwd" class="fas fa-spinner fa-spin"></i>
                <span v-else>Changer le mot de passe</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import api from '../../api'

const auth = useAuthStore()
const myId = ref(null)
const users = ref([])
const loading = ref(false)

// ── Create ──
const showCreate = ref(false)
const creating = ref(false)
const createError = ref('')
const form = ref({ username: '', email: '', password: '', is_staff: false })

// ── Edit ──
const showEdit = ref(false)
const editing = ref(false)
const editError = ref('')
const editTarget = ref(null)
const editForm = ref({ username: '', email: '', is_staff: false, is_active: true })

// ── Password ──
const showPassword = ref(false)
const changingPwd = ref(false)
const pwdError = ref('')
const pwdSuccess = ref('')
const passwordTarget = ref(null)
const pwdForm = ref({ password: '', confirm: '' })

onMounted(async () => {
  myId.value = auth.user?.id ?? null
  fetchUsers()
})

async function fetchUsers() {
  loading.value = true
  try {
    const res = await api.get('/api/admin/users/')
    users.value = res.data
  } finally {
    loading.value = false
  }
}

function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('fr-FR', { year: 'numeric', month: 'short', day: 'numeric' })
}

// ── Create ──
function openCreate() {
  form.value = { username: '', email: '', password: '', is_staff: false }
  createError.value = ''
  showCreate.value = true
}
async function createUser() {
  createError.value = ''
  if (!form.value.username) { createError.value = 'L\'identifiant est requis.'; return }
  if (form.value.password.length < 8) { createError.value = 'Le mot de passe doit contenir au moins 8 caractères.'; return }
  creating.value = true
  try {
    await api.post('/api/admin/users/', form.value)
    showCreate.value = false
    fetchUsers()
  } catch (e) {
    createError.value = e.response?.data?.error || e.response?.data?.detail || 'Erreur lors de la création.'
  } finally {
    creating.value = false
  }
}

// ── Edit ──
function openEdit(u) {
  editTarget.value = u
  editForm.value = { username: u.username, email: u.email || '', is_staff: u.is_staff, is_active: u.is_active }
  editError.value = ''
  showEdit.value = true
}
async function saveEdit() {
  editError.value = ''
  if (!editForm.value.username) { editError.value = 'L\'identifiant est requis.'; return }
  editing.value = true
  try {
    await api.patch(`/api/admin/users/${editTarget.value.id}/`, editForm.value)
    showEdit.value = false
    fetchUsers()
  } catch (e) {
    editError.value = e.response?.data?.error || e.response?.data?.detail || 'Erreur lors de la modification.'
  } finally {
    editing.value = false
  }
}

// ── Password ──
function openPassword(u) {
  passwordTarget.value = u
  pwdForm.value = { password: '', confirm: '' }
  pwdError.value = ''
  pwdSuccess.value = ''
  showPassword.value = true
}
async function changePassword() {
  pwdError.value = ''
  pwdSuccess.value = ''
  if (pwdForm.value.password.length < 8) { pwdError.value = 'Le mot de passe doit contenir au moins 8 caractères.'; return }
  if (pwdForm.value.password !== pwdForm.value.confirm) { pwdError.value = 'Les mots de passe ne correspondent pas.'; return }
  changingPwd.value = true
  try {
    await api.post(`/api/admin/users/${passwordTarget.value.id}/change-password/`, { password: pwdForm.value.password })
    pwdSuccess.value = 'Mot de passe modifié avec succès.'
    pwdForm.value = { password: '', confirm: '' }
  } catch (e) {
    pwdError.value = e.response?.data?.error || e.response?.data?.detail || 'Erreur lors du changement.'
  } finally {
    changingPwd.value = false
  }
}

// ── Delete ──
async function deleteUser(u) {
  if (u.id === myId.value) return
  if (!confirm(`Supprimer l'utilisateur « ${u.username} » ? Cette action est irréversible.`)) return
  try {
    await api.delete(`/api/admin/users/${u.id}/`)
    fetchUsers()
  } catch (e) {
    alert(e.response?.data?.error || 'Erreur lors de la suppression.')
  }
}
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

/* Table */
.table-wrap {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  overflow: auto;
}
.user-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}
.user-table thead tr {
  border-bottom: 1px solid #e2e8f0;
}
.user-table thead th {
  padding: 12px 16px;
  text-align: left;
  font-size: 0.72rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}
.user-table tbody tr {
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.12s;
}
.user-table tbody tr:last-child { border-bottom: none; }
.user-table tbody tr:hover { background: #f8fafc; }
.user-table tbody tr.row-me { background: #f0fdf4; }
.user-table td { padding: 12px 16px; vertical-align: middle; color: #334155; }

.u-name-wrap { display: flex; align-items: center; gap: 10px; }
.u-avatar {
  width: 32px; height: 32px; border-radius: 8px;
  background: #059669; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; font-weight: 700; flex-shrink: 0;
}
.u-name { font-weight: 600; color: #0f172a; }
.badge-me {
  font-size: 0.6rem; font-weight: 700; background: #d1fae5; color: #065f46;
  padding: 2px 6px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.04em;
}
.u-email { color: #64748b; font-size: 0.82rem; }
.u-pass { color: #94a3b8; }
.pass-mask { display: flex; align-items: center; gap: 6px; font-size: 0.82rem; }
.u-date { color: #94a3b8; font-size: 0.8rem; white-space: nowrap; }

.badge {
  display: inline-block; padding: 3px 9px; border-radius: 20px;
  font-size: 0.68rem; font-weight: 700; letter-spacing: 0.03em;
}
.badge-super { background: #ede9fe; color: #6d28d9; }
.badge-staff { background: #dbeafe; color: #1d4ed8; }
.badge-user  { background: #f1f5f9; color: #64748b; }
.badge-active   { background: #d1fae5; color: #065f46; }
.badge-inactive { background: #fee2e2; color: #b91c1c; }

.acts { display: flex; gap: 6px; }
.act {
  width: 30px; height: 30px;
  border: 1px solid #e2e8f0; background: #f8fafc; color: #64748b;
  border-radius: 7px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; transition: all 0.15s;
}
.act:hover { background: #ecfdf5; color: #059669; border-color: #a7f3d0; }
.act-red:hover { background: #fef2f2; color: #dc2626; border-color: #fecaca; }
.act:disabled { opacity: 0.35; cursor: not-allowed; }

/* Empty / loading */
.state-loading { padding: 60px; text-align: center; color: #94a3b8; font-size: 0.9rem; }
.empty-state {
  text-align: center; padding: 60px 20px; color: #cbd5e1;
}
.empty-state i { font-size: 2.5rem; display: block; margin-bottom: 12px; opacity: 0.5; }
.empty-state p { font-size: 0.88rem; color: #94a3b8; }

/* Modals */
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
.mo-sm { max-width: 400px; }
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

/* Form fields */
.field { margin-bottom: 15px; }
.field > label {
  display: block; font-size: 0.72rem; font-weight: 700; color: #475569;
  margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.05em;
}
.field small { font-size: 0.68rem; color: #94a3b8; font-weight: 400; text-transform: none; letter-spacing: 0; }
.field input {
  width: 100%; padding: 9px 12px; border: 1px solid #e2e8f0; border-radius: 8px;
  font-size: 0.88rem; color: #0f172a; background: #fff;
  transition: border-color 0.15s; box-sizing: border-box;
}
.field input:focus { outline: none; border-color: #059669; box-shadow: 0 0 0 3px rgba(5,150,105,0.1); }
.field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

/* Toggle */
.tgl { display: flex !important; align-items: center; gap: 10px; cursor: pointer; margin-top: 4px; }
.tgl input { display: none; }
.tgl-track {
  width: 40px; height: 22px; background: #cbd5e1; border-radius: 11px;
  position: relative; transition: background 0.2s; flex-shrink: 0;
}
.tgl-track::after {
  content: ''; position: absolute; top: 3px; left: 3px;
  width: 16px; height: 16px; background: #fff; border-radius: 50%;
  transition: transform 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.25);
}
.tgl input:checked + .tgl-track { background: #059669; }
.tgl input:checked + .tgl-track::after { transform: translateX(18px); }
.tgl-lbl { color: #64748b; font-size: 0.85rem; font-weight: 500; }

/* Alerts */
.form-err {
  background: #fef2f2; border: 1px solid #fca5a5; color: #dc2626;
  padding: 10px 14px; border-radius: 8px; margin-bottom: 16px; font-size: 0.84rem;
}
.form-ok {
  background: #f0fdf4; border: 1px solid #a7f3d0; color: #065f46;
  padding: 10px 14px; border-radius: 8px; margin-bottom: 16px; font-size: 0.84rem;
}

@media (max-width: 640px) {
  .field-row { grid-template-columns: 1fr; }
  .u-email, .u-date, .u-pass { display: none; }
}
</style>
