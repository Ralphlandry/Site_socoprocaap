from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('services/', views.ServiceListView.as_view(), name='service-list'),
    path('equipe/', views.EquipeListView.as_view(), name='equipe-list'),
    path('blog/', views.BlogPostListView.as_view(), name='blog-list'),
    path('blog/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog-detail'),
    path('galerie/categories/', views.GalerieCategorieListView.as_view(), name='galerie-categories'),
    path('galerie/', views.GalerieImageListView.as_view(), name='galerie-list'),
    path('contact/', views.ContactCreateView.as_view(), name='contact-create'),
    path('info/', views.InfoSiteView.as_view(), name='info-site'),
    path('statistiques/', views.StatistiqueListView.as_view(), name='statistique-list'),
    path('campagnes/', views.CampagneListView.as_view(), name='campagne-list'),

    # Auth
    path('auth/csrf/', views.CSRFView.as_view(), name='csrf'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/me/', views.MeView.as_view(), name='me'),

    # Admin CRUD
    path('admin/stats/', views.AdminStatsView.as_view(), name='admin-stats'),
    path('admin/services/', views.AdminServiceListCreateView.as_view(), name='admin-service-list'),
    path('admin/services/<int:pk>/', views.AdminServiceDetailView.as_view(), name='admin-service-detail'),
    path('admin/blog/', views.AdminBlogListCreateView.as_view(), name='admin-blog-list'),
    path('admin/blog/<int:pk>/', views.AdminBlogDetailView.as_view(), name='admin-blog-detail'),
    path('admin/galerie/categories/', views.AdminCategorieListCreateView.as_view(), name='admin-categorie-list'),
    path('admin/galerie/categories/<int:pk>/', views.AdminCategorieDetailView.as_view(), name='admin-categorie-detail'),
    path('admin/galerie/', views.AdminGalerieListCreateView.as_view(), name='admin-galerie-list'),
    path('admin/galerie/<int:pk>/', views.AdminGalerieDetailView.as_view(), name='admin-galerie-detail'),
    path('admin/contacts/', views.AdminContactListView.as_view(), name='admin-contact-list'),
    path('admin/contacts/<int:pk>/', views.AdminContactDetailView.as_view(), name='admin-contact-detail'),
    path('admin/statistiques/', views.AdminStatistiqueListCreateView.as_view(), name='admin-statistique-list'),
    path('admin/statistiques/<int:pk>/', views.AdminStatistiqueDetailView.as_view(), name='admin-statistique-detail'),
    path('admin/info/', views.AdminInfoSiteView.as_view(), name='admin-info'),
    path('admin/equipe/', views.AdminEquipeListCreateView.as_view(), name='admin-equipe-list'),
    path('admin/equipe/<int:pk>/', views.AdminEquipeDetailView.as_view(), name='admin-equipe-detail'),
    path('admin/campagnes/', views.AdminCampagneListCreateView.as_view(), name='admin-campagne-list'),
    path('admin/campagnes/<int:pk>/', views.AdminCampagneDetailView.as_view(), name='admin-campagne-detail'),
    path('admin/users/', views.AdminUserListCreateView.as_view(), name='admin-user-list'),
    path('admin/users/<int:pk>/', views.AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/users/<int:pk>/change-password/', views.AdminUserChangePasswordView.as_view(), name='admin-user-change-password'),
]
