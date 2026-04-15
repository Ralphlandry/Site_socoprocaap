from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    icone = models.CharField(max_length=50, blank=True, help_text="Nom de l'icône (ex: fa-leaf)")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordre']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.titre


class BlogPost(models.Model):
    titre = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    contenu = models.TextField()
    extrait = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='blog/')
    publie = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Article de blog'
        verbose_name_plural = 'Articles de blog'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre


class GalerieCategorie(models.Model):
    nom = models.CharField(max_length=100)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = 'Catégorie galerie'
        verbose_name_plural = 'Catégories galerie'

    def __str__(self):
        return self.nom


class GalerieImage(models.Model):
    titre = models.CharField(max_length=200)
    image = models.ImageField(upload_to='galerie/')
    categorie = models.ForeignKey(
        GalerieCategorie, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='images'
    )
    description = models.TextField(blank=True)
    publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Image galerie'
        verbose_name_plural = 'Images galerie'

    def __str__(self):
        return self.titre


class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_envoi']
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'

    def __str__(self):
        return f"{self.nom} - {self.sujet}"


class Statistique(models.Model):
    """Statistiques de production de l'entreprise."""
    titre = models.CharField(max_length=200)
    icone = models.CharField(max_length=50, blank=True, help_text="Nom de l'icône FontAwesome (ex: fas fa-seedling)")
    valeur = models.CharField(max_length=100, help_text="Valeur affichée (ex: 500+, 1000 T)")
    unite = models.CharField(max_length=50, blank=True, help_text="Unité (ex: Tonnes, Hectares, Producteurs)")
    description = models.TextField(blank=True)
    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordre']
        verbose_name = 'Statistique'
        verbose_name_plural = 'Statistiques'

    def __str__(self):
        return f"{self.titre}: {self.valeur} {self.unite}"


class MembreEquipe(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    fonction = models.CharField(max_length=200)
    image = models.ImageField(upload_to='equipe/', blank=True, null=True)
    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = 'Membre de l\'équipe'
        verbose_name_plural = 'Membres de l\'équipe'

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.fonction}"


class InfoSite(models.Model):
    nom_cooperative = models.CharField(max_length=200, default='SOCOPROCAAP')
    slogan = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    adresse = models.TextField(blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True)
    a_propos = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Information du site'
        verbose_name_plural = 'Informations du site'

    def __str__(self):
        return self.nom_cooperative


class Campagne(models.Model):
    PRODUITS = [
        ('Cacao', 'Cacao'),
        ('Maïs', 'Maïs'),
        ('Gombo', 'Gombo'),
        ('Élevage Porcin', 'Élevage Porcin'),
    ]
    produit = models.CharField(max_length=100, choices=PRODUITS)
    nom_producteur = models.CharField(max_length=200)
    tonnage = models.DecimalField(max_digits=10, decimal_places=2, help_text="en tonnes")
    superficie = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="en hectares")
    session = models.CharField(max_length=20, help_text="ex: 2025")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-session', 'produit', 'nom_producteur']
        verbose_name = 'Campagne'
        verbose_name_plural = 'Campagnes'

    def __str__(self):
        return f"{self.produit} — {self.nom_producteur} ({self.session})"


class Partenaire(models.Model):
    """Partenaires de commercialisation."""
    nom = models.CharField(max_length=200)
    image = models.ImageField(upload_to='partenaires/')
    description = models.TextField()
    ordre = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = 'Partenaire'
        verbose_name_plural = 'Partenaires'

    def __str__(self):
        return self.nom
