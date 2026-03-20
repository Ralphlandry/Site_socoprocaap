import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'Accueil',
    component: () => import('../views/AccueilView.vue'),
  },
  {
    path: '/services',
    name: 'Services',
    component: () => import('../views/ServicesView.vue'),
  },
  {
    path: '/blog',
    name: 'Blog',
    component: () => import('../views/BlogView.vue'),
  },
  {
    path: '/blog/:slug',
    name: 'BlogDetail',
    component: () => import('../views/BlogDetailView.vue'),
  },
  {
    path: '/galerie',
    name: 'Galerie',
    component: () => import('../views/GalerieView.vue'),
  },
  {
    path: '/statistiques',
    name: 'Statistiques',
    component: () => import('../views/StatistiquesView.vue'),
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/ContactView.vue'),
  },
  // Admin
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/AdminLogin.vue'),
  },
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'AdminDashboard', component: () => import('../views/admin/AdminDashboard.vue') },
      { path: 'blog', name: 'AdminBlog', component: () => import('../views/admin/AdminBlog.vue') },
      { path: 'galerie', name: 'AdminGalerie', component: () => import('../views/admin/AdminGalerie.vue') },
      { path: 'services', name: 'AdminServices', component: () => import('../views/admin/AdminServices.vue') },
      { path: 'contacts', name: 'AdminContacts', component: () => import('../views/admin/AdminContacts.vue') },
      { path: 'statistiques', name: 'AdminStatistiques', component: () => import('../views/admin/AdminStatistiques.vue') },
      { path: 'users', name: 'AdminUsers', component: () => import('../views/admin/AdminUsers.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach(async (to) => {
  if (to.matched.some(r => r.meta.requiresAuth)) {
    const auth = useAuthStore()
    if (!auth.isAuthenticated) {
      await auth.checkAuth()
      if (!auth.isAuthenticated) {
        return { name: 'AdminLogin' }
      }
    }
  }
})

export default router
