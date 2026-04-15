<template>
  <div class="al-root">
    <!-- Mobile overlay -->
    <div v-if="mobileOpen" class="al-overlay" @click="mobileOpen = false"></div>

    <!-- Sidebar -->
    <aside class="al-sidebar" :class="{ 'al-sidebar--open': mobileOpen, 'al-sidebar--collapsed': collapsed }">
      <div class="al-brand">
        <img src="/LOGO (1).png" alt="SOCOPROCAAP" class="al-brand-logo" />
        <div v-show="!collapsed" class="al-brand-text">
          <span class="al-brand-name">SOCOPROCAAP</span>
          <span class="al-brand-sub">Administration</span>
        </div>
      </div>

      <nav class="al-nav">
        <span v-show="!collapsed" class="al-nav-section">TABLEAU DE BORD</span>
        <router-link to="/admin" class="al-nav-item" exact-active-class="al-nav-item--active" @click="mobileOpen = false">
          <i class="fas fa-th-large al-nav-icon"></i>
          <span v-show="!collapsed">Tableau de bord</span>
        </router-link>

        <span v-show="!collapsed" class="al-nav-section">CONTENU</span>
        <router-link to="/admin/blog" class="al-nav-item" active-class="al-nav-item--active" @click="mobileOpen = false">
          <i class="fas fa-file-alt al-nav-icon"></i>
          <span v-show="!collapsed">Articles</span>
        </router-link>
        <router-link to="/admin/galerie" class="al-nav-item" active-class="al-nav-item--active" @click="mobileOpen = false">
          <i class="fas fa-images al-nav-icon"></i>
          <span v-show="!collapsed">Galerie</span>
        </router-link>
        <router-link to="/admin/services" class="al-nav-item" active-class="al-nav-item--active" @click="mobileOpen = false">
          <i class="fas fa-cogs al-nav-icon"></i>
          <span v-show="!collapsed">Productions</span>
        </router-link>
        <router-link to="/admin/equipe" class="al-nav-item" active-class="al-nav-item--active" @click="mobileOpen = false">
          <i class="fas fa-id-badge al-nav-icon"></i>
          <span v-show="!collapsed">Équipe</span>
        </router-link>
        <router-link to="/admin/campagne" class="al-nav-item" active-class="al-nav-item--active" @click="mobileOpen = false">
          <i class="fas fa-seedling al-nav-icon"></i>
          <span v-show="!collapsed">Campagne</span>
        </router-link>
        <router-link to="/admin/partenaires" class="al-nav-item" active-class="al-nav-item--active" @click="mobileOpen = false">
          <i class="fas fa-link al-nav-icon"></i>
          <span v-show="!collapsed">Partenaires</span>
        </router-link>
        <router-link to="/admin/statistiques" class="al-nav-item" active-class="al-nav-item--active" @click="mobileOpen = false">
          <i class="fas fa-chart-bar al-nav-icon"></i>
          <span v-show="!collapsed">Statistiques</span>
        </router-link>

        <span v-show="!collapsed" class="al-nav-section">COMMUNICATION</span>
        <router-link to="/admin/contacts" class="al-nav-item" active-class="al-nav-item--active" @click="mobileOpen = false">
          <i class="fas fa-envelope al-nav-icon"></i>
          <span v-show="!collapsed">Messages</span>
          <span v-if="!collapsed && unread > 0" class="al-badge">{{ unread }}</span>
          <span v-if="collapsed && unread > 0" class="al-dot"></span>
        </router-link>

        <span v-show="!collapsed" class="al-nav-section">ADMINISTRATION</span>
        <router-link to="/admin/users" class="al-nav-item" active-class="al-nav-item--active" @click="mobileOpen = false">
          <i class="fas fa-users al-nav-icon"></i>
          <span v-show="!collapsed">Utilisateurs</span>
        </router-link>
      </nav>

      <div class="al-sidebar-footer">
        <router-link to="/" class="al-nav-item" @click="mobileOpen = false">
          <i class="fas fa-external-link-alt al-nav-icon"></i>
          <span v-show="!collapsed">Voir le site</span>
        </router-link>
        <button class="al-nav-item al-logout" @click="logout">
          <i class="fas fa-sign-out-alt al-nav-icon"></i>
          <span v-show="!collapsed">Déconnexion</span>
        </button>
      </div>
    </aside>

    <!-- Main area -->
    <div class="al-main" :class="{ 'al-main--collapsed': collapsed }">
      <!-- Topbar -->
      <header class="al-topbar">
        <div class="al-topbar-left">
          <button class="al-hamburger" @click="toggleSidebar" aria-label="Menu">
            <i class="fas fa-bars"></i>
          </button>
          <nav class="al-breadcrumb" aria-label="Fil d'Ariane">
            <span class="al-breadcrumb-root">Admin</span>
            <i class="fas fa-chevron-right al-breadcrumb-sep"></i>
            <span class="al-breadcrumb-current">{{ pageTitle }}</span>
          </nav>
        </div>
        <div class="al-topbar-right">
          <button v-if="unread > 0" class="al-notif" @click="$router.push('/admin/contacts')" :title="`${unread} message(s) non lu(s)`">
            <i class="fas fa-bell"></i>
            <span class="al-notif-badge">{{ unread }}</span>
          </button>
          <div class="al-user">
            <div class="al-user-avatar">{{ auth.user?.username?.charAt(0)?.toUpperCase() || 'A' }}</div>
            <div class="al-user-info">
              <span class="al-user-name">{{ auth.user?.username }}</span>
              <span class="al-user-role">Administrateur</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="al-content">
        <router-view v-slot="{ Component }">
          <transition name="al-fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import api from '../../api'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const collapsed = ref(false)
const mobileOpen = ref(false)
const unread = ref(0)

const TITLES = {
  AdminDashboard: 'Tableau de bord',
  AdminBlog: 'Articles',
  AdminGalerie: 'Galerie',
  AdminServices: 'Productions',
  AdminEquipe: 'Équipe',
  AdminCampagne: 'Campagnes',
  AdminPartenaire: 'Partenaires',
  AdminContacts: 'Messages',
  AdminStatistiques: 'Statistiques',
  AdminUsers: 'Utilisateurs',
}
const pageTitle = computed(() => TITLES[route.name] || 'Admin')

function toggleSidebar() {
  if (window.innerWidth < 900) {
    mobileOpen.value = !mobileOpen.value
  } else {
    collapsed.value = !collapsed.value
  }
}

async function logout() {
  await auth.logout()
  router.push('/admin/login')
}

async function loadUnread() {
  try {
    const { data } = await api.get('/admin/stats/')
    unread.value = data.contacts_non_lus || 0
  } catch { /* */ }
}

onMounted(loadUnread)
</script>

<style scoped>
/* ─── Root ─── */
.al-root {
  display: flex;
  min-height: 100vh;
  background: #f1f5f9;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

/* ─── Sidebar ─── */
.al-sidebar {
  width: 248px;
  min-height: 100vh;
  background: #0f172a;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 200;
  transition: width 0.25s ease, transform 0.25s ease;
  overflow: hidden;
}
.al-sidebar--collapsed { width: 64px; }

/* Brand */
.al-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 14px;
  height: 64px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;
}
.al-brand-logo {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
  border: 2px solid rgba(5,150,105,0.4);
}
.al-brand-text { display: flex; flex-direction: column; overflow: hidden; }
.al-brand-name { color: #f8fafc; font-weight: 700; font-size: 0.85rem; white-space: nowrap; letter-spacing: -0.01em; }
.al-brand-sub { color: #059669; font-size: 0.6rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 1px; }

/* Nav */
.al-nav {
  flex: 1;
  padding: 8px 10px;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: thin;
  scrollbar-color: rgba(255,255,255,0.08) transparent;
}
.al-nav-section {
  display: block;
  padding: 16px 10px 5px;
  color: #475569;
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  white-space: nowrap;
}
.al-nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  margin: 1px 0;
  color: #94a3b8;
  font-size: 0.84rem;
  font-weight: 500;
  border-radius: 8px;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  width: 100%;
  text-align: left;
  transition: background 0.15s, color 0.15s;
  white-space: nowrap;
  position: relative;
}
.al-nav-item:hover {
  background: rgba(255,255,255,0.06);
  color: #f1f5f9;
}
.al-nav-item--active {
  background: rgba(5,150,105,0.15);
  color: #ffffff !important;
  font-weight: 600;
  border-left: 3px solid #059669;
  padding-left: 7px;
}
.al-nav-item--active .al-nav-icon { color: #059669; }
.al-nav-icon {
  width: 18px;
  text-align: center;
  font-size: 0.85rem;
  flex-shrink: 0;
  color: #64748b;
  transition: color 0.15s;
}
.al-nav-item:hover .al-nav-icon { color: #94a3b8; }
.al-badge {
  margin-left: auto;
  background: #ef4444;
  color: #fff;
  font-size: 0.62rem;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}
.al-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 7px;
  height: 7px;
  background: #ef4444;
  border-radius: 50%;
  border: 2px solid #0f172a;
}

/* Sidebar footer */
.al-sidebar-footer {
  padding: 8px 10px 12px;
  border-top: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;
}
.al-logout { color: #94a3b8; }
.al-logout:hover { background: rgba(239,68,68,0.12) !important; color: #fca5a5 !important; }

/* ─── Main ─── */
.al-main {
  flex: 1;
  margin-left: 248px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: margin-left 0.25s ease;
}
.al-main--collapsed { margin-left: 64px; }

/* Topbar */
.al-topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  height: 64px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.al-topbar-left { display: flex; align-items: center; gap: 16px; }
.al-hamburger {
  width: 34px;
  height: 34px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #64748b;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  transition: all 0.15s;
  flex-shrink: 0;
}
.al-hamburger:hover { background: #f1f5f9; color: #0f172a; border-color: #cbd5e1; }
.al-breadcrumb { display: flex; align-items: center; gap: 8px; }
.al-breadcrumb-root { color: #94a3b8; font-size: 0.82rem; font-weight: 500; }
.al-breadcrumb-sep { color: #cbd5e1; font-size: 0.5rem; }
.al-breadcrumb-current { color: #0f172a; font-size: 0.82rem; font-weight: 600; }

.al-topbar-right { display: flex; align-items: center; gap: 8px; }
.al-notif {
  position: relative;
  width: 34px;
  height: 34px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #64748b;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  transition: all 0.15s;
}
.al-notif:hover { background: #fef2f2; color: #ef4444; border-color: #fecaca; }
.al-notif-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  min-width: 16px;
  height: 16px;
  background: #ef4444;
  color: #fff;
  font-size: 0.58rem;
  font-weight: 700;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 3px;
  border: 2px solid #fff;
}
.al-user {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px 5px 5px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  cursor: default;
}
.al-user-avatar {
  width: 30px;
  height: 30px;
  background: #059669;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 0.78rem;
  font-weight: 700;
  flex-shrink: 0;
}
.al-user-info { display: flex; flex-direction: column; }
.al-user-name { color: #0f172a; font-size: 0.8rem; font-weight: 600; line-height: 1.2; }
.al-user-role { color: #94a3b8; font-size: 0.62rem; font-weight: 500; }

/* Content */
.al-content { flex: 1; padding: 28px; }

/* Transition */
.al-fade-enter-active, .al-fade-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.al-fade-enter-from { opacity: 0; transform: translateY(4px); }
.al-fade-leave-to { opacity: 0; }

/* Overlay (mobile) */
.al-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 199;
}

/* ─── Responsive ─── */
@media (max-width: 900px) {
  .al-sidebar { transform: translateX(-100%); width: 248px !important; }
  .al-sidebar--open { transform: translateX(0); }
  .al-main { margin-left: 0 !important; }
  .al-user-info { display: none; }
}
@media (max-width: 600px) {
  .al-topbar { padding: 0 16px; }
  .al-content { padding: 16px; }
  .al-breadcrumb { display: none; }
}
</style>
