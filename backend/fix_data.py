# -*- coding: utf-8 -*-
"""
Script de correction de l'encodage des données.
Corrige les caractères français corrompus (fèves → f??ves, etc.)

Usage (depuis le dossier backend/) :
    python -X utf8 fix_data.py
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socopro.settings')

import django
django.setup()

from api.models import Service, InfoSite

print("=== Correction des données (encodage UTF-8) ===\n")

# --- Réactiver tous les services désactivés ---
reactives = Service.objects.filter(actif=False).update(actif=True)
print(f'  ✓ {reactives} service(s) réactivé(s) (actif=True)')

# --- Correction des descriptions ---
services_corriges = [
    (
        'Production de Cacao',
        'Nous produisons des fèves de cacao de qualité supérieure grâce à des techniques agricoles durables et respectueuses de l\'environnement. Nos plantations sont certifiées et suivent les meilleures pratiques agronomiques.',
    ),
    (
        'Culture du Maïs',
        'Notre coopérative développe la culture du maïs à grande échelle, fournissant une céréale de premier choix aux marchés locaux. Nous utilisons des semences sélectionnées et des méthodes de culture optimisées pour garantir des rendements élevés.',
    ),
    (
        'Production de Gombo',
        'Le gombo fait partie de nos cultures maraîchères phares. Nous cultivons du gombo frais et de qualité, très demandé sur les marchés locaux et régionaux, en respectant les cycles naturels de production.',
    ),
    (
        'Élevage Porcin',
        'Notre filière d\'élevage porcin s\'appuie sur des pratiques modernes et respectueuses du bien-être animal. Nous assurons un suivi vétérinaire régulier et une alimentation de qualité pour produire une viande saine.',
    ),
    (
        'Formation des Producteurs',
        'Nous formons nos membres aux meilleures pratiques agricoles et d\'élevage, incluant les techniques de culture, la gestion des récoltes, la santé animale et la commercialisation. Des sessions régulières sont organisées tout au long de l\'année.',
    ),
    (
        'Commercialisation',
        'Nous assurons la commercialisation de l\'ensemble des produits de nos membres sur les marchés nationaux et internationaux, garantissant des prix justes et compétitifs pour chaque producteur de la coopérative.',
    ),
]

for titre, description in services_corriges:
    n = Service.objects.filter(titre=titre).update(description=description)
    status = '✓' if n else '✗ (non trouvé)'
    print(f'  {status} Service : {titre}')

# --- Correction InfoSite ---
info = InfoSite.objects.first()
if info:
    info.slogan = "L'excellence agropastorale camerounaise"
    info.description = "Coopérative agropastorale spécialisée dans le cacao, le maïs, le gombo et l'élevage porcin."
    info.a_propos = "SOCOPROCAAP est une coopérative agropastorale basée à Obala, village Nkolndobo, dédiée à la production de cacao, maïs, gombo et à l'élevage porcin."
    info.save()
    print('  ✓ InfoSite mise à jour')
else:
    print('  ✗ InfoSite non trouvée')

print('\n=== Correction terminée ===')
print(f'  {Service.objects.count()} services en base.')
