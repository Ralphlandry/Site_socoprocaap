from rest_framework import serializers
from .models import Service, BlogPost, GalerieCategorie, GalerieImage, Contact, InfoSite, Statistique, MembreEquipe, Campagne, Partenaire


class CampagneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campagne
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class MembreEquipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembreEquipe
        fields = '__all__'


class BlogPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'titre', 'slug', 'extrait', 'image', 'date_creation']


class BlogPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'


class BlogPostAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
        read_only_fields = ['slug', 'date_creation', 'date_modification']


class GalerieCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalerieCategorie
        fields = '__all__'


class GalerieImageSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True, default=None)

    class Meta:
        model = GalerieImage
        fields = ['id', 'titre', 'image', 'categorie', 'categorie_nom', 'description', 'publie', 'date_creation']


class GalerieImageAdminSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True, default=None)

    class Meta:
        model = GalerieImage
        fields = ['id', 'titre', 'image', 'categorie', 'categorie_nom', 'description', 'publie', 'date_creation']
        read_only_fields = ['date_creation']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'nom', 'email', 'sujet', 'message', 'date_envoi']
        read_only_fields = ['date_envoi']


class ContactAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class StatistiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistique
        fields = '__all__'


class InfoSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoSite
        fields = '__all__'


class PartenaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partenaire
        fields = '__all__'


class PartenaireAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partenaire
        fields = '__all__'
        read_only_fields = ['date_creation']
