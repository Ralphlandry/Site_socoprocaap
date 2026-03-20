#!/bin/sh
# Script d'initialisation - Crée un superutilisateur Django
# Usage: docker compose exec backend python manage.py shell < init_admin.py

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socopro.settings')

import django
django.setup()

from django.contrib.auth.models import User
from api.models import InfoSite, Service, GalerieCategorie

# Créer le superutilisateur admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@socopro.com', 'admin123')
    print('Superutilisateur créé: admin / admin123')
else:
    print('Superutilisateur admin existe déjà.')

# Créer les informations du site
if not InfoSite.objects.exists():
    InfoSite.objects.create(
        nom_cooperative='SOCOPROCAAP',
        slogan='L\'excellence agropastorale camerounaise',
        description='Coopérative agropastorale spécialisée dans le cacao, le maïs, le gombo et l\'élevage porcin.',
        adresse='Obala, Village Nkolndobo, Cameroun',
        telephone='+237 699 810 144 / +237 679 152 963',
        email='contact@socopro.com',
        a_propos='SOCOPROCAAP est une coopérative agropastorale basée à Obala, village Nkolndobo, dédiée à la production de cacao, maïs, gombo et à l\'élevage porcin.',
    )
    print('Informations du site créées.')

# Créer des services de démonstration
services_data = [
    {
        'titre': 'Production de Cacao',
        'description': 'Nous produisons des fèves de cacao de qualité supérieure grâce à des techniques agricoles durables et respectueuses de l\'environnement. Nos plantations sont certifiées et suivent les meilleures pratiques agronomiques.',
        'icone': 'fas fa-seedling',
        'ordre': 1,
    },
    {
        'titre': 'Culture du Maïs',
        'description': 'Notre coopérative développe la culture du maïs à grande échelle, fournissant une céréale de premier choix aux marchés locaux. Nous utilisons des semences sélectionnées et des méthodes de culture optimisées pour garantir des rendements élevés.',
        'icone': 'fas fa-wheat-awn',
        'ordre': 2,
    },
    {
        'titre': 'Production de Gombo',
        'description': 'Le gombo fait partie de nos cultures maraîchères phares. Nous cultivons du gombo frais et de qualité, très demandé sur les marchés locaux et régionaux, en respectant les cycles naturels de production.',
        'icone': 'fas fa-leaf',
        'ordre': 3,
    },
    {
        'titre': 'Élevage Porcin',
        'description': 'Notre filière d\'élevage porcin s\'appuie sur des pratiques modernes et respectueuses du bien-être animal. Nous assurons un suivi vétérinaire régulier et une alimentation de qualité pour produire une viande saine.',
        'icone': 'fas fa-piggy-bank',
        'ordre': 4,
    },
    {
        'titre': 'Formation des Producteurs',
        'description': 'Nous formons nos membres aux meilleures pratiques agricoles et d\'élevage, incluant les techniques de culture, la gestion des récoltes, la santé animale et la commercialisation. Des sessions régulières sont organisées tout au long de l\'année.',
        'icone': 'fas fa-graduation-cap',
        'ordre': 5,
    },
    {
        'titre': 'Commercialisation',
        'description': 'Nous assurons la commercialisation de l\'ensemble des produits de nos membres sur les marchés nationaux et internationaux, garantissant des prix justes et compétitifs pour chaque producteur de la coopérative.',
        'icone': 'fas fa-handshake',
        'ordre': 6,
    },
]

for s_data in services_data:
    Service.objects.get_or_create(titre=s_data['titre'], defaults=s_data)

print(f'{Service.objects.count()} services en base.')

# Créer des catégories de galerie
categories_data = ['Cacao', 'Maïs', 'Gombo', 'Élevage Porcin', 'Équipe', 'Événements']
for i, nom in enumerate(categories_data):
    GalerieCategorie.objects.get_or_create(nom=nom, defaults={'ordre': i})

print(f'{GalerieCategorie.objects.count()} catégories de galerie créées.')
print('Initialisation terminée !')
