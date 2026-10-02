# Concierge Service by Medina First Marrakech

Site de villas de luxe à Marrakech (de 3 à plus de 20 chambres) et de services de
conciergerie, en français, anglais, néerlandais et espagnol, avec un lien WhatsApp par
villa et par service.

Onglets : Villas · Spa & Beauté à la villa · Location de véhicules · Activités &
Excursions · Événements privés · Tables & Adresses exclusives · Conciergerie 24/7.

Chaque fiche villa suit la même structure : 1. Nom · 2. Localisation · 3. Description ·
4. Services & équipements · 5. Autres informations importantes.

Numéro WhatsApp des demandes : à renseigner dans `BRAND.whatsapp` en haut du script.

**Site en ligne :** https://akhimysah.github.io/villas-marrakech/

Tout tient dans `index.html` (design, textes, tri des photos, données) et le dossier
`photos/`. Les villas actuelles sont des **exemples** en attendant les vraies données.

## Liens à partager sur WhatsApp

| Quoi | Lien |
|---|---|
| Catalogue complet (FR) | `https://akhimysah.github.io/villas-marrakech/#/fr` |
| Catalogue, une catégorie | `https://akhimysah.github.io/villas-marrakech/#/fr/chambres/5` (ou `8%2B` pour 8+) |
| Une villa (FR) | `https://akhimysah.github.io/villas-marrakech/#/fr/villa/dar-zitoune` |
| Même villa en anglais | `https://akhimysah.github.io/villas-marrakech/#/en/villa/dar-zitoune` |

Langues : `fr`, `en`, `nl`, `es`. Chaque fiche a un bouton WhatsApp et un bouton
« Copier le lien » qui génèrent ces liens automatiquement.

## Les villas

Les 97 villas viennent de la base Notion « Propriétés » (bloc « ✨ VILLA … » de chaque fiche).
La transcription française est dans `data/villas_fr.txt`, les traductions EN / NL / ES dans
`data/tr.json`. Prix, disponibilités et conditions discriminatoires en ont été retirés.

Format d'une villa dans `data/villas_fr.txt` :

```
== Villa Alya | 5 | 10 | - | -        (nom | chambres | capacité | salles de bain | surface)
L Route d'Amizmiz • Face à l'hôtel Eden Andalou      (localisation)
D 5 suites • Double séjour • Piscine privée 15 m     (description)
S+ Femme de ménage • Jardinier 2×/semaine            (services inclus)
S? Cuisinière (petit-déjeuner & déjeuner)            (services sur demande)
X Espace bien-être | Hammam • Sauna                  (bloc complémentaire)
I Accès exclusif à toute la villa                    (autres informations)
```

## Photos

Les photos des villas ne sont pas encore en ligne : Notion bloque leur copie et l'export est
désactivé pour les invités de l'espace « Argan 90 ». Dès qu'un export Notion (Markdown & CSV,
sous-pages incluses) est disponible, les photos seront triées (extérieur, salon, cuisine,
chambres, salles de bain en dernier) et ajoutées dans `photos/`.

