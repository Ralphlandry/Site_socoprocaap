<template>
  <div class="ap">
    <div class="ap-hd">
      <div>
        <h1 class="ap-title">Messages reçus</h1>
        <p class="ap-desc">Consultez les messages envoyés via le formulaire de contact</p>
      </div>
      <span v-if="unread > 0" class="unread-info">
        <i class="fas fa-circle"></i> {{ unread }} non lu{{ unread > 1 ? 's' : '' }}
      </span>
    </div>

    <!-- Detail modal -->
    <Teleport to="body">
      <transition name="mo">
        <div v-if="selected" class="mo-overlay" @click.self="selected = null">
          <div class="mo-box">
            <div class="mo-head">
              <div class="mo-sender">
                <div class="mo-avatar">{{ selected.nom.charAt(0).toUpperCase() }}</div>
                <div>
                  <strong>{{ selected.nom }}</strong>
                  <span>{{ selected.email }}</span>
                </div>
              </div>
              <button class="mo-close" @click="selected = null"><i class="fas fa-times"></i></button>
            </div>
            <div class="mo-body">
              <div class="msg-meta">
                <span><i class="fas fa-phone"></i> {{ selected.telephone || '—' }}</span>
                <span><i class="fas fa-calendar-alt"></i> {{ fmtDate(selected.date_envoi) }}</span>
              </div>
              <h3 class="msg-subject">{{ selected.sujet }}</h3>
              <div class="msg-content">{{ selected.message }}</div>
            </div>
            <div class="mo-foot">
              <a :href="`mailto:${selected.email}`" class="btn btn-primary">
                <i class="fas fa-reply"></i> Répondre
              </a>
              <button class="btn btn-ghost" @click="selected = null">Fermer</button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>

    <div class="tbl-card">
      <div class="tbl-top">
        <span class="tbl-count">{{ contacts.length }} message{{ contacts.length > 1 ? 's' : '' }}</span>
      </div>
      <div class="tbl-wrap">
        <table>
          <thead>
            <tr>
              <th></th>
              <th>EXPÉDITEUR</th>
              <th>SUJET</th>
              <th>DATE</th>
              <th>STATUT</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in contacts" :key="c.id" @click="open(c)" class="clickable" :class="{ unread: !c.lu }">
              <td><span class="row-avatar">{{ c.nom.charAt(0).toUpperCase() }}</span></td>
              <td>
                <div class="sender-info">
                  <span class="cell-bold">{{ c.nom }}</span>
                  <span class="cell-email">{{ c.email }}</span>
                </div>
              </td>
              <td class="cell-subject">{{ c.sujet }}</td>
              <td class="cell-date">{{ fmtDate(c.date_envoi) }}</td>
              <td>
                <span class="badge" :class="c.lu ? 'badge-muted' : 'badge-new'">
                  {{ c.lu ? 'Lu' : 'Nouveau' }}
                </span>
              </td>
              <td @click.stop>
                <button class="act act-red" @click="remove(c.id)" title="Supprimer"><i class="fas fa-trash-alt"></i></button>
              </td>
            </tr>
            <tr v-if="!contacts.length">
              <td colspan="6" class="tbl-empty">
                <i class="fas fa-inbox"></i><span>Aucun message pour l'instant</span>
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

const contacts = ref([])
const selected = ref(null)
const unread = computed(() => contacts.value.filter(c => !c.lu).length)

function fmtDate(d) {
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function load() {
  const { data } = await api.get('/admin/contacts/')
  contacts.value = data.results || data
}

async function open(c) {
  selected.value = c
  if (!c.lu) {
    try {
      await api.patch(`/admin/contacts/${c.id}/`, { lu: true })
      c.lu = true
    } catch { /* */ }
  }
}

async function remove(id) {
  if (!confirm('Supprimer ce message ?')) return
  await api.delete(`/admin/contacts/${id}/`)
  await load()
}

onMounted(load)
</script>

<style scoped>
.ap { width: 100%; }
.ap-hd { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }
.ap-title { font-size: 1.4rem; font-weight: 700; color: #0f172a; margin-bottom: 2px; letter-spacing: -0.02em; }
.ap-desc { color: #94a3b8; font-size: 0.82rem; font-weight: 500; }
.unread-info { background: #fef2f2; color: #dc2626; padding: 5px 12px; border-radius: 20px; font-size: 0.76rem; font-weight: 700; border: 1px solid #fecaca; display: flex; align-items: center; gap: 6px; }
.unread-info i { font-size: 0.5rem; }

.btn { display: inline-flex; align-items: center; gap: 7px; padding: 9px 18px; border-radius: 9px; font-size: 0.85rem; font-weight: 600; border: none; cursor: pointer; transition: all 0.15s; text-decoration: none; }
.btn-primary { background: #059669; color: #fff; }
.btn-primary:hover { background: #047857; }
.btn-ghost { background: #f8fafc; color: #374151; border: 1px solid #e2e8f0; }
.btn-ghost:hover { background: #f1f5f9; }

/* Modal */
.mo-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); backdrop-filter: blur(3px); display: flex; align-items: center; justify-content: center; z-index: 3000; padding: 20px; }
.mo-box { background: #fff; border-radius: 14px; width: 100%; max-width: 560px; max-height: 90vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.mo-head { display: flex; justify-content: space-between; align-items: center; padding: 18px 24px; border-bottom: 1px solid #e2e8f0; }
.mo-sender { display: flex; align-items: center; gap: 12px; }
.mo-sender strong { display: block; color: #0f172a; font-size: 0.92rem; font-weight: 600; }
.mo-sender span { color: #94a3b8; font-size: 0.76rem; }
.mo-avatar { width: 40px; height: 40px; background: #059669; color: #fff; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1rem; flex-shrink: 0; }
.mo-close { background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 1.1rem; border-radius: 6px; padding: 4px 8px; transition: background 0.15s; }
.mo-close:hover { background: #f1f5f9; color: #dc2626; }
.mo-body { padding: 22px; }
.mo-foot { display: flex; gap: 10px; padding: 16px 22px; border-top: 1px solid #e2e8f0; }
.mo-enter-active, .mo-leave-active { transition: opacity 0.2s; }
.mo-enter-from, .mo-leave-to { opacity: 0; }
.mo-enter-active .mo-box { transition: transform 0.2s; }
.mo-enter-from .mo-box { transform: scale(0.96) translateY(10px); }

.msg-meta { display: flex; gap: 20px; margin-bottom: 14px; }
.msg-meta span { color: #94a3b8; font-size: 0.78rem; display: flex; align-items: center; gap: 6px; }
.msg-subject { color: #0f172a; font-size: 1rem; font-weight: 700; margin-bottom: 12px; }
.msg-content { color: #334155; font-size: 0.88rem; line-height: 1.7; white-space: pre-wrap; background: #f8fafc; border-radius: 8px; padding: 14px; }

/* Table */
.tbl-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.tbl-top { padding: 12px 20px; border-bottom: 1px solid #e2e8f0; }
.tbl-count { color: #94a3b8; font-size: 0.78rem; font-weight: 600; }
.tbl-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 10px 16px; font-size: 0.65rem; font-weight: 700; color: #94a3b8; letter-spacing: 0.08em; border-bottom: 1px solid #e2e8f0; background: #f8fafc; text-transform: uppercase; }
td { padding: 12px 16px; color: #334155; font-size: 0.84rem; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
tr:last-child td { border-bottom: none; }

.clickable { cursor: pointer; }
.clickable:hover td { background: #f8fafc; }
.unread td { background: #f0fdf9; }
.unread:hover td { background: #e6faf4; }

.row-avatar {
  width: 32px; height: 32px; background: #059669;
  color: #fff; border-radius: 8px; display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 0.82rem;
}
.sender-info { display: flex; flex-direction: column; }
.cell-bold { font-weight: 600; color: #0f172a; font-size: 0.84rem; }
.cell-email { color: #94a3b8; font-size: 0.73rem; }
.cell-subject { color: #334155; max-width: 220px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cell-date { color: #94a3b8; font-size: 0.76rem; white-space: nowrap; }

.badge { display: inline-flex; align-items: center; padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }
.badge-new { background: #d1fae5; color: #065f46; }
.badge-muted { background: #f1f5f9; color: #64748b; }

.act { width: 30px; height: 30px; border: 1px solid #e2e8f0; background: #f8fafc; color: #64748b; border-radius: 7px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; transition: all 0.15s; }
.act-red:hover { background: #fef2f2; color: #dc2626; border-color: #fecaca; }

.tbl-empty { text-align: center; padding: 40px; color: #b8d4c4; }
.tbl-empty i { font-size: 2rem; display: block; margin-bottom: 8px; }
.tbl-empty span { font-size: 0.88rem; display: block; }

@media (max-width: 700px) {
  th:nth-child(4), td:nth-child(4) { display: none; }
  .cell-subject { max-width: 120px; }
}
@media (max-width: 500px) {
  th:nth-child(3), td:nth-child(3) { display: none; }
  .ap-hd { flex-direction: column; align-items: flex-start; }
}
</style>
