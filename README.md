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

## Ajouter ou modifier une villa

Dans `index.html`, section `4. DONNÉES DES VILLAS`, chaque villa est un objet :

```js
{ slug:"dar-zitoune",            // identifiant du lien, sans espace ni accent
  name:"Dar Zitoune",
  area:{fr:"Palmeraie",en:"…",nl:"…",es:"…"},        // affiché sur la carte
  location:{fr:"Palmeraie, à 15 min de la médina", …},
  bedrooms:3, bathrooms:3, capacity:6, surface:380,   // classement automatique 3/4/5/6/7/8+
  description:{fr:"…",en:"…",nl:"…",es:"…"},
  outdoor:{…}, living:{…}, kitchen:{…},               // extérieur/piscine, salon, cuisine
  amenities:["pool_heated","staff","wifi"],           // clés de la liste AMENITIES
  rates:[{season:{fr:"Basse saison",…},from:"2026-11-01",to:"2027-02-28",night:650,min:3}],
  currency:"EUR",
  photos:[{file:"piscine 1.jpg",src:"https://…/piscine-1.jpg"}, …]   // ou img:"clé" vers PHOTO_SRC
}
```

Un texte peut être donné dans une seule langue (`description:"…"`) : il sera affiché
tel quel dans les 4 versions. Pour ajouter un équipement, ajoutez une clé dans `AMENITIES`.

## Photos : le tri automatique

Le tri lit le **nom de fichier** (ou `caption`) en FR / EN / NL / ES et impose l'ordre :

1. Extérieur, piscine, jardin, terrasse, vue, drone
2. Entrée / hall
3. Salon (et cinéma, bibliothèque, bureau)
4. Salle à manger
5. Cuisine
6. Bien-être (spa, hammam, gym)
7. Autres espaces
8. Chambres, regroupées par numéro : toutes les « Chambre 1 » puis « Chambre 2 », etc.
9. Salles de bain, toujours en dernier, dans l'ordre des chambres

Nommage recommandé : `Piscine 1.jpg`, `Salon 2.jpg`, `Chambre 1 (a).jpg`,
`Chambre 1 (b).jpg`, `Chambre 2.jpg`, `SDB chambre 1.jpg`, `Bathroom 2.jpg`.
Les mots reconnus incluent : chambre, bedroom, slaapkamer, dormitorio, suite, master /
sdb, salle de bain, bathroom, badkamer, baño, douche / piscine, pool, zwembad, piscina…
Une photo sans mot-clé va dans « Autres espaces ». La première photo triée devient la
photo de couverture.

## Où mettre les photos

- **Sur votre propre hébergement** (Netlify, OVH, o2switch, GitHub Pages…) : déposez
  `index.html` et le dossier `photos/`, puis `src:"photos/dar-zitoune/piscine-1.jpg"`.
  C'est la solution recommandée pour un vrai catalogue avec des dizaines de photos.
- **Dans l'artifact Claude** : les images externes sont bloquées ; les photos doivent être
  intégrées dans le fichier (data URI), avec une limite de 16 Mo au total. Convenable pour
  quelques villas avec des photos compressées (~80 Ko chacune), pas pour tout le parc.

Les photos d'exemple sont des images Unsplash (licence libre) encodées dans le fichier, dans
`PHOTO_SRC`. Une photo sans `src` ni `img` affiche un cadre vide avec le nom de la pièce.
Pour alléger le fichier avant mise en ligne, supprimez `PHOTO_SRC` et utilisez des `src` en URL.

## Passer des données d'exemple aux vraies villas

Mettez `const DEMO = false;` pour retirer le bandeau « Données d'exemple ».
