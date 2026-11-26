# Maquettes de sites web — EventLyx

Dépôt public des maquettes de refonte que Rémi Pauly (EventLyx) envoie aux clubs et organisateurs.
Publié sur GitHub Pages : https://remiply.github.io/maquettes/<dossier>/ (branche main, racine).
Chaque dossier = un club. ⚠️ Ce dépôt est PUBLIC (et servi en ligne) : aucune info commerciale interne ici (prix, CRM, notes sur les prospects). Les pages sont en `noindex,nofollow` et `robots.txt` bloque l'indexation.

## Avant de commencer : 3 contrôles bloquants
1. **Contact vérifié** : un mail ou un téléphone du club, trouvé sur son site, ses mentions légales ou sa page Facebook. Sans contact, on s'arrête là : pas de maquette.
2. **Pas déjà contacté** : vérifier dans Gmail (boîte EventLyx, `in:sent` sur 12 mois) et dans le CRM que le club n'a pas déjà reçu une offre de site.
3. **Hors exclusions** : voir le skill « maquette-site-web ».

## Fabriquer la maquette
1. Crée le dossier `<slug>/` (ex. `rocamadour`, `chierry`).
2. **Couleurs** : celles du club (logo, maillots), palette sobre, 6 variables (`vin`, `vind`, `encre`, `creme`, `safran`, `sable`).
3. **Photos** : uniquement des images de qualité. Photos du club si elles sont nettes, sinon photos HD libres de droits du lieu (Wikimedia Commons, crédits dans le pied de page). Cadrage soigné : le sujet visible sur ordinateur ET sur mobile (`heropos`). Fichiers : `hero.jpg` + 2-3 photos de section, compressées.
4. **Contenu** : uniquement des infos vraies, tirées du site du club (dates, distances, horaires, lien d'inscription). Rien d'inventé.
5. **Chatbot** : toujours le chatbot façon Challenge du Montcalm (bulle, teaser, fenêtre avec en-tête, suggestions, points de saisie). Réponses `R` (mots-clés → réponse), suggestions `Q`, `fallback` et `hello` écrits à partir des vraies infos du club.
6. Ajoute le dict du club dans `_gabarit/gen.py` (modèles : `chierry`, `randon`), puis :
   ```
   python3 _gabarit/gen.py <slug>
   python3 _gabarit/shoot.py <slug>
   ```
7. **Contrôle visuel obligatoire** : ouvre les captures de `_gabarit/shots/` (ordinateur + mobile). Vérifie : pas de débordement horizontal (`scrollWidth` = largeur), pas d'erreur JS, photos bien cadrées, compte à rebours non masqué par la bulle du chatbot, chatbot qui répond. Corrige et recommence jusqu'à ce que ce soit propre. Le site ne doit jamais avoir l'air « fait par une IA ».
8. Ajoute le club à `index.html` si besoin, puis commit (auteur « Rémi Pauly <contact.eventlyx@gmail.com> ») et push sur main. Attends 1-2 min et vérifie que l'URL publique répond.

## Le mail de proposition (brouillon seulement, Rémi envoie)
- Boîte EventLyx (contact.eventlyx@gmail.com), signature incluse, vouvoiement, court, à la première personne, ton de Rémi (jamais « mail d'IA »).
- Le lien exact de la maquette, en clair, à la ligne. Un appel à l'action simple.
- **Prix** : selon la règle de prix du skill « maquette-site-web » (privé, jamais dans ce dépôt public).
- Toujours préciser que **de petites modifications sont possibles à l'achat**.
- Aucun chiffre de preuve chatbot, pas de jargon technique.

## Après
- Suivi commercial : voir le skill « maquette-site-web ».

## Ne jamais
- Envoyer un mail (brouillon seulement).
- Inventer une info sur le club.
- Toucher aux dossiers des autres clubs sans demande.
