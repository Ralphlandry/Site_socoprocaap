from django.contrib import admin
from .models import Service, BlogPost, GalerieCategorie, GalerieImage, Contact, InfoSite, Statistique


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['titre', 'ordre', 'actif', 'date_creation']
    list_filter = ['actif']
    list_editable = ['ordre', 'actif']
    search_fields = ['titre', 'description']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['titre', 'publie', 'date_creation', 'date_modification']
    list_filter = ['publie', 'date_creation']
    list_editable = ['publie']
    search_fields = ['titre', 'contenu']
    prepopulated_fields = {'slug': ('titre',)}
    readonly_fields = ['date_creation', 'date_modification']


@admin.register(GalerieCategorie)
class GalerieCategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ordre']
    list_editable = ['ordre']


@admin.register(GalerieImage)
class GalerieImageAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'publie', 'date_creation']
    list_filter = ['publie', 'categorie']
    list_editable = ['publie']
    search_fields = ['titre', 'description']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'sujet', 'lu', 'date_envoi']
    list_filter = ['lu', 'date_envoi']
    list_editable = ['lu']
    search_fields = ['nom', 'email', 'sujet', 'message']
    readonly_fields = ['nom', 'email', 'sujet', 'message', 'date_envoi']

    def has_add_permission(self, request):
        return False


@admin.register(InfoSite)
class InfoSiteAdmin(admin.ModelAdmin):
    list_display = ['nom_cooperative', 'telephone', 'email']

    def has_add_permission(self, request):
        # Singleton: only one instance allowed
        return not InfoSite.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Statistique)
class StatistiqueAdmin(admin.ModelAdmin):
    list_display = ['titre', 'valeur', 'unite', 'ordre', 'actif']
    list_filter = ['actif']
    list_editable = ['ordre', 'actif']
    search_fields = ['titre']


# Customize admin site
admin.site.site_header = 'SOCOPROCAAP - Administration'
admin.site.site_title = 'SOCOPROCAAP Admin'
admin.site.index_title = 'Gestion du site'
