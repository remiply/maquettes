"""Maquette Ceven'Trail (PVEN, Le Vigan) : 5 courses le samedi 6 mars 2027.
Mise en page propre : orange et rouge du logo sur anthracite et sable, courses comparées en barres
(distance et dénivelé), fiches dépliables, samedi heure par heure de la nuit à la nuit.
Usage : python3 _gabarit/sites/ceventrail.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from chatbot import block

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'ceventrail', 'index.html')
SITE = 'https://www.ceventrail.org/'
NJ = 'https://in.njuko.com/ceventrail-2027'
REG = 'https://www.ceventrail.org/s/REGLEMENT-2027-9fzr.pdf'
RB = 'https://www.ceventrail.org/s/roadbook_V1_2027_compressed.pdf'
BOURSE = 'https://docs.google.com/forms/d/e/1FAIpQLSetuS3XiCO7oaMlsDb2ODfeEyYYUNcjeBlw9hqLf3JbJGb2UQ/viewform'
BENEV = 'https://widget.weezevent.com/crew/organization/719/event/10457/form/22209'
LOGER = 'https://www.ceventrail.org/se-loger'
LIVE = 'https://live.l-chrono.com/resultats/ceventrail-2027'
MAIL = 'info.ceventrail@gmail.com'

# Chiffres du roadbook 2027 (distance, D+, départ) ; places, tarifs et âges du règlement 2027 ; statut lu sur Njuko le 27/11/2026.
C = [
    dict(id='ultra', nm='Ultra du Bout du Cirque', surnom="L'ultra", km=101, dp=4500, h='4 h 00', lieu='Halle aux Sports', brief='3 h 50',
         places='380 dossards, dont 80 réservés aux femmes', prix='87 €', repas='repas d\'après course compris', age='Nés en 2007 et avant',
         st='Inscriptions ouvertes', stc='ok', gpx='https://www.ceventrail.org/s/Ultra_du_Bout_du_Cirque_2027.gpx',
         bh=[('L\'Arboux', '10,5', '5 h 50'), ('Saint-André-de-Majencoules', '14,5', '7 h 00'), ('Mandagout', '31', '10 h 25'), ('Arrigas', '55', '15 h 00'),
             ('Rocher du Loup', '71', '18 h 15'), ('Relais du Cirque, Blandas', '80', '20 h 05'), ('Bez', '90', '22 h 00')],
         rav='Saint-André (km 14,5), Cap de Coste (km 25, liquide), Mandagout (km 31), Serres (km 44, liquide), Le Travers (km 49, eau), Arrigas (km 55), Le Quintanel (km 62), Blandas (km 80), Bez (km 90), puis la soupe à l\'oignon à l\'arrivée.',
         plus='Un sac est déposé au ravitaillement de mi-course. Itinéraire de délestage possible depuis Calo Rouge, environ 5 km plus court.'),
    dict(id='etoiles', nm='Trail aux Étoiles', surnom='La Doyenne', km=63, dp=2400, h='11 h 00', lieu='Place du Quai', brief='10 h 50',
         places='380 dossards, dont 125 réservés aux femmes', prix='62 €', repas='repas d\'après course compris', age='Nés en 2007 et avant',
         st='Complet · liste d\'attente', stc='full', gpx='https://www.ceventrail.org/s/Trail_aux_Etoiles_2027.gpx',
         bh=[('Arrigas', '17', '15 h 00'), ('Rocher du Loup', '34', '18 h 15'), ('Blandas', '44', '20 h 05'), ('Bez', '54,5', '22 h 00')],
         rav='Serres (km 6, liquide), Le Travers (km 12, eau), Arrigas (km 17), Le Quintanel (km 26,5), Blandas (km 44), Bez (km 54,5), puis l\'arrivée.',
         plus=''),
    dict(id='toureille', nm='Marathon de la Toureille', surnom='La Cadette', km=42, dp=2200, h='10 h 00', lieu='Place du Quai', brief='9 h 50',
         places='380 dossards, dont 125 réservés aux femmes', prix='41 €', repas='sans repas', age='Nés en 2007 et avant',
         st='Complet · liste d\'attente', stc='full', gpx='https://www.ceventrail.org/s/marathon_de_la_toureille_2026.gpx',
         bh=[('L\'Arboux', '10,5', '12 h 00'), ('Saint-André-de-Majencoules', '16', '13 h 15'), ('Mandagout', '32', '17 h 00')],
         rav='Saint-André (km 16), Cap de Coste (km 25) et Mandagout (km 32), puis l\'arrivée.',
         plus='Créé en 2020.'),
    dict(id='oignon', nm='Trail de l\'Oignon Doux', surnom='Le Terroir Cévenol', km=23, dp=1000, h='14 h 00', lieu='Halle aux Sports', brief='13 h 50',
         places='380 dossards', prix='23 €', repas='', age='Nés en 2007 et avant',
         st='Complet · liste d\'attente', stc='full', gpx='https://www.ceventrail.org/s/SityTrail-2328005-sitytrail-x-oignon-doux-2025-x2x.gpx',
         bh=[('Mandagout', '13,5', '16 h 45')],
         rav='Mandagout (km 13,5), puis l\'arrivée.', plus=''),
    dict(id='locale', nm='Trail du Pays Viganais', surnom='La Locale', km=12, dp=450, h='14 h 30', lieu='Halle aux Sports', brief='14 h 15',
         places='190 dossards', prix='12 €', repas='', age='Nés en 2011 et avant',
         st='Liste d\'attente', stc='full', gpx='https://www.ceventrail.org/s/SityTrail-2328117-trail-du-pays-viganais-2025.gpx',
         bh=[], rav='Ravitaillement à l\'arrivée uniquement.', plus='Pas de barrière horaire.'),
]

chat_css, chat_html, chat_js = block(dict(
    acc='#D8432A', acc1='#F06A2A', acc2='#A8231F', ink='#282D30', bg='#FBF6EF', rgb='216,67,42',
    ini='CT', font="'Work Sans',system-ui,sans-serif", bottom=24,
    tz="Une question sur le Ceven'Trail ?", small='Le Vigan · 6 mars 2027', title="Ceven'Trail",
    ph='Posez votre question…',
    hello="<p>Bonjour ! 👋 Je suis l'assistant du <strong>Ceven'Trail</strong>.</p><p>Les 5 courses, les barrières horaires, le retrait des dossards, les parkings… posez-moi votre question !</p>",
    fallback="Je n'ai pas cette information. Sur le site en ligne, je transmets la question aux bénévoles de l'organisation. En attendant, vous pouvez écrire à info.ceventrail@gmail.com.",
    Q=[["🏔️ Les courses", "Quelles sont les 5 courses ?"], ["⏱️ Barrières", "Quelles sont les barrières horaires de l'ultra ?"], ["🎽 Dossards", "Quand retirer mon dossard ?"],
       ["🅿️ Parking", "Où se garer ?"], ["🍝 Pasta party", "Y a-t-il une pasta party ?"], ["🔁 Bourse", "Je ne peux plus courir, que faire ?"]],
    R=[
        [['barriere'], "Ultra : L'Arboux 5 h 50, Saint-André 7 h 00, Mandagout 10 h 25, Arrigas 15 h 00, Rocher du Loup 18 h 15, Blandas 20 h 05, Bez 22 h 00. Trail aux Étoiles : Arrigas 15 h 00, Rocher du Loup 18 h 15, Blandas 20 h 05, Bez 22 h 00. Marathon : L'Arboux 12 h 00, Saint-André 13 h 15, Mandagout 17 h 00. 23 km : Mandagout 16 h 45."],
        [['bourse', 'revendre', 'revente', 'plus courir', 'annul', 'rembours', 'echange', 'report', 'blesse'], "Il n'y a pas de remboursement, mais un report ou un échange est possible jusqu'à 15 jours avant la course. Vous pouvez aussi passer par la bourse aux dossards : le formulaire est dans la partie « Pratique » de la page."],
        [['pasta', 'vendredi', 'veille'], "Oui : la pasta party a lieu le vendredi 5 mars de 18 h 30 à 21 h 00 à la Halle aux Sports, sur réservation (8 €). Le retrait des dossards est ouvert le même soir, de 17 h 30 à 21 h 00."],
        [['retrait', 'dossard'], "Retrait des dossards à la Halle aux Sports : le vendredi 5 mars de 17 h 30 à 21 h 00 pour tout le monde. Le samedi, dès 7 h 30 pour le 42 et le 63 km, dès 11 h 30 pour le 23 et le 12 km. Fermeture 15 min avant chaque départ."],
        [['parking', 'garer', 'stationn', 'voiture'], "Le stationnement est interdit aux abords de la Halle. Parkings : Maison de la Petite Enfance et stade annexe (800 m, 250 à 300 places), parking des écoles rue Pierre Gorlier (200 m, 60 places), rond-point Charles de Gaulle (500 m, 100 places)."],
        [['bus', 'train', 'venir', 'acces', 'covoit'], "En bus : ligne liO 608 depuis Montpellier, ligne 140 depuis Nîmes. Pour le covoiturage, le site renvoie vers un forum et vers Blablacar."],
        [['loger', 'hebergement', 'dormir', 'hotel', 'gite'], "La page « Se loger » du site donne une sélection d'hébergements (PDF mis à jour), avec des liens vers Sud Cévennes, Gîtes de France et Airbnb."],
        [['douche'], "Les douches sont à la Halle aux Sports."],
        [['enfant', 'jeune', 'kid', 'minime', 'poussin'], "Les courses enfants sont gratuites, le samedi à partir de 11 h 15, aux abords de la Halle aux Sports. Il faut une attestation de santé (ou un certificat) et une autorisation parentale."],
        [['benevole', 'aider'], "Plus de 150 bénévoles font le Ceven'Trail. Le formulaire d'inscription bénévole est dans la partie « Pratique » de la page."],
        [['ultra', '100', '101', 'cirque', 'navacelles'], "L'Ultra du Bout du Cirque : 101 km et 4 500 m de dénivelé selon le roadbook 2027. Départ le samedi 6 mars à 4 h 00 de la Halle aux Sports, briefing à 3 h 50. 87 €, repas compris. 380 dossards, dont 80 réservés aux femmes. Inscriptions ouvertes."],
        [['63', 'etoile', 'doyenne'], "Le Trail aux Étoiles (« La Doyenne ») : 63 km et 2 400 m de dénivelé. Départ à 11 h 00, place du Quai. 62 €, repas compris. Il est complet, avec une liste d'attente sur Njuko."],
        [['42', 'marathon', 'toureille', 'cadette'], "Le Marathon de la Toureille (« La Cadette ») : 42 km et 2 200 m de dénivelé. Départ à 10 h 00, place du Quai. 41 €. Il est complet, avec une liste d'attente sur Njuko."],
        [['23', 'oignon', 'terroir'], "Le Trail de l'Oignon Doux : 23 km et 1 000 m de dénivelé. Départ à 14 h 00 de la Halle aux Sports. 23 €. Il est complet, avec une liste d'attente sur Njuko."],
        [['12', 'pays viganais', 'locale'], "Le Trail du Pays Viganais (« La Locale ») : 12 km et 450 m de dénivelé. Départ à 14 h 30 de la Halle aux Sports. 12 €, ouvert dès les cadets (nés en 2011 et avant). Liste d'attente sur Njuko."],
        [['tarif', 'prix', 'cout', 'combien', '€'], "Ultra 87 €, Trail aux Étoiles 62 € (repas compris pour ces deux-là), Marathon 41 €, 23 km 23 €, 12 km 12 €. Pasta party du vendredi : 8 €. Repas accompagnateur : 12 €."],
        [['pps', 'certificat', 'licence', 'medical'], "Il faut une licence FFA valide ou un PPS. Le dossier doit être complet au 20 février 2027 : rien n'est collecté au retrait des dossards."],
        [['inscri', 'complet', 'attente', 'njuko'], "Les inscriptions se font sur Njuko. Au 27 novembre, l'ultra est ouvert ; le 63, le 42 et le 23 km sont complets avec liste d'attente, et le 12 km est en liste d'attente. Aucune inscription le jour de la course."],
        [['materiel', 'obligatoire', 'frontale', 'sac'], "Pour l'ultra et le Trail aux Étoiles : téléphone, frontale et piles, couverture de survie, sifflet, réserve d'eau, veste imperméable et écotasse. Pour les autres courses, le détail est dans le règlement 2027. Pas de gobelet aux ravitaillements."],
        [['resultat', 'classement', 'live', 'direct', 'suivre'], "Le classement est en direct sur live.l-chrono.com, avec une vidéo en direct sur écran géant, sur le site et sur Facebook."],
        [['heure', 'horaire', 'depart', 'quand', 'date', 'programme'], "Samedi 6 mars 2027 : ultra à 4 h 00, marathon à 10 h 00, Trail aux Étoiles à 11 h 00, courses enfants dès 11 h 15, 23 km à 14 h 00 et 12 km à 14 h 30."],
        [['contact', 'mail', 'telephone', 'joindre', 'appeler'], "Vous pouvez écrire à info.ceventrail@gmail.com ou appeler le 07 86 99 20 00 ou le 06 52 31 83 32."],
        [['bonjour', 'salut', 'hello', 'coucou'], "Bonjour ! Posez-moi votre question sur le Ceven'Trail."],
    ]))

CSS = r'''
:root{color-scheme:light;--or:#F06A2A;--rouge:#D8282F;--brique:#B8321F;--anth:#282D30;--anth2:#1E2225;--sable:#E9CEB0;--creme:#FBF6EF;--gris:#6B6560;--ligne:rgba(40,45,48,.14);--f:'Work Sans',system-ui,sans-serif;--ft:'Anton','Impact',sans-serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--creme);color:var(--anth);font:17px/1.6 var(--f)}
img{max-width:100%;height:auto;display:block}
a{color:inherit}
.w{max-width:1200px;margin:0 auto;padding:0 32px}
h1,h2,h3{font-family:var(--ft);font-weight:400;text-transform:uppercase;letter-spacing:.01em;line-height:.98;margin:0}
.maq{background:#000;color:#fff;font-size:13px;padding:7px 16px;display:flex;gap:14px;justify-content:space-between;flex-wrap:wrap}
.maq a{color:var(--sable)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:50px;padding:0 24px;background:var(--or);color:#fff;text-decoration:none;font:600 16px/1 var(--f);letter-spacing:.02em;border-radius:4px;transition:background .15s}
.btn:hover{background:var(--brique)}
.btn.clair{background:transparent;color:#fff;box-shadow:inset 0 0 0 2px rgba(255,255,255,.75)}
.btn.clair:hover{background:rgba(255,255,255,.12)}
.btn.sombre{background:var(--anth)}
/* hero */
.hero{position:relative;color:#fff;background:#1E2225 url(hero.jpg) 30% center/cover no-repeat;min-height:min(820px,100vh);display:flex;flex-direction:column;isolation:isolate}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(20,22,24,.86) 0,rgba(20,22,24,.55) 42%,rgba(20,22,24,.05) 75%),linear-gradient(0deg,rgba(20,22,24,.7) 0,transparent 35%)}
.nav{display:flex;align-items:center;gap:28px;padding:22px 0}
.wm{font:400 30px/1 var(--ft);text-transform:uppercase;text-decoration:none;letter-spacing:.02em}
.wm .c{color:var(--or)}.wm .t{color:#FF5A4F}
.wm small{display:block;font:600 11.5px/1 var(--f);letter-spacing:.24em;color:var(--sable);margin-top:6px}
.nav ul{list-style:none;margin:0 0 0 auto;padding:0;display:flex;gap:26px}
.nav ul a{text-decoration:none;font-weight:600;font-size:15.5px}
.nav ul a:hover{color:var(--or)}
.hero .in{margin:auto 0;padding:40px 0 64px;max-width:640px}
.ed{display:inline-block;font:600 13px/1 var(--f);letter-spacing:.18em;text-transform:uppercase;color:var(--sable);border:1px solid rgba(233,206,176,.5);padding:8px 12px;margin-bottom:22px}
.hero h1{font-size:clamp(64px,10vw,150px)}
.hero h1 span{color:var(--or)}
.hero .date{font:400 clamp(28px,3.4vw,46px)/1.05 var(--ft);text-transform:uppercase;margin:14px 0 0;color:var(--sable)}
.hero .lead{font-size:19px;margin:18px 0 30px;opacity:.94;max-width:34em}
.hero .row{display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.count{display:flex;gap:20px;margin-top:34px}
.count div{font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;opacity:.85}
.count b{display:block;font:400 40px/1 var(--ft);color:#fff;opacity:1}
/* bandeau chiffres */
.chif{background:var(--anth);color:#fff}
.chif .w{display:grid;grid-template-columns:repeat(4,minmax(0,1fr))}
.chif .w>div{padding:24px 20px 22px;border-left:1px solid rgba(255,255,255,.12)}
.chif .w>div:first-child{border-left:0;padding-left:0}
.chif b{display:block;font:400 44px/1 var(--ft);color:var(--or)}
.chif span{font-size:15px;opacity:.85}
/* courses */
.sec{padding:96px 0}
.sec h2{font-size:clamp(46px,5.6vw,84px)}
.sec .lead{max-width:42em;font-size:18.5px;color:var(--gris);margin:16px 0 40px}
.races{border-top:2px solid var(--anth)}
.race{border-bottom:1px solid var(--ligne)}
.race summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1.6fr) 110px 150px 28px;gap:24px;align-items:center;padding:22px 0}
.race summary::-webkit-details-marker{display:none}
.race .nm{font:400 30px/1 var(--ft);text-transform:uppercase}
.race .nm small{display:block;font:600 13px/1.2 var(--f);letter-spacing:.14em;color:var(--brique);margin-bottom:6px}
.bars{display:grid;gap:7px}
.bar{display:grid;grid-template-columns:minmax(0,1fr) 92px;align-items:center;gap:10px;font:600 14px/1 var(--f);white-space:nowrap}
.bar .tr{display:block;min-width:0}
.bar i{display:block;height:12px;border-radius:2px}
.bar.km i{background:var(--or)}
.bar.dp i{background:var(--anth);opacity:.82}
.race .h{font:400 32px/1 var(--ft)}
.race .h small{display:block;font:600 12px/1.2 var(--f);letter-spacing:.1em;text-transform:uppercase;color:var(--gris);margin-top:4px}
.st{font:600 13px/1.2 var(--f);padding:7px 10px;border-radius:4px;text-align:center}
.st.ok{background:#2F7D4F;color:#fff}
.st.full{background:var(--sable);color:var(--anth)}
.pl{width:28px;height:28px;border-radius:50%;border:2px solid var(--anth);display:grid;place-items:center;font:700 18px/1 var(--f);transition:transform .2s}
.race[open] .pl{transform:rotate(45deg);background:var(--anth);color:#fff}
.race .det{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:36px;padding:4px 0 34px}
.race .det h3{font-size:22px;margin:0 0 12px;color:var(--brique)}
.race .det p{margin:0 0 10px;font-size:16px}
.kv{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;font-size:16px;margin:0 0 16px}
.kv dt{color:var(--gris)}
.kv dd{margin:0;font-weight:600}
.bh{width:100%;border-collapse:collapse;font-size:15.5px;background:#fff;box-shadow:0 0 0 1px var(--ligne);border-radius:6px;overflow:hidden}
.bh td{padding:9px 12px;border-bottom:1px solid var(--ligne)}
.bh tr:last-child td{border-bottom:0}
.bh td:nth-child(2){color:var(--gris);white-space:nowrap}
.bh td:last-child{font-weight:700;text-align:right;white-space:nowrap}
.det .act{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:16px}
.det .act a.s{font-weight:600;font-size:15px}
.races-note{font-size:14.5px;color:var(--gris);margin:18px 0 0}
/* photo pleine largeur */
.band{position:relative;height:clamp(300px,42vw,560px);background:#1E2225 center/cover no-repeat;display:flex;align-items:flex-end}
.band p{margin:0;padding:28px 32px;color:#fff;font:400 clamp(30px,4vw,56px)/1 var(--ft);text-transform:uppercase;max-width:1200px;width:100%;margin:0 auto;text-shadow:0 2px 16px rgba(0,0,0,.4)}
/* samedi heure par heure */
.jour{color:#fff;background:linear-gradient(180deg,#14161A 0,#1F2A3A 14%,#3A4C63 26%,#C9826A 40%,#E9CEB0 52%,#E9CEB0 62%,#D98A5B 74%,#3A2C3A 86%,#14161A 100%)}
.jour .w{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:56px}
.jour .stick{position:sticky;top:40px;align-self:start}
.jour h2{color:#fff}
.jour .lead{color:rgba(255,255,255,.8)}
.vend{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);padding:20px 22px;border-radius:6px;margin-top:10px}
.vend h3{font-size:24px;color:var(--or);margin-bottom:10px}
.vend p{margin:0 0 6px;font-size:15.5px}
.tl{list-style:none;margin:0;padding:0}
.tl li{display:grid;grid-template-columns:96px minmax(0,1fr);gap:18px;padding:14px 18px;margin-bottom:8px;border-radius:6px;background:rgba(255,255,255,.9);color:var(--anth);align-items:baseline}
.tl li.dep{background:#fff;box-shadow:inset 4px 0 0 var(--or)}
.tl time{font:400 26px/1 var(--ft)}
.tl span{font-size:16px}
.tl span b{font-weight:700}
/* pratique */
.prat{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.box{background:#fff;border-radius:6px;padding:24px 24px 22px;box-shadow:0 0 0 1px var(--ligne)}
.box h3{font-size:26px;margin:0 0 12px}
.box p{margin:0 0 8px;font-size:16px}
.box ul{margin:0;padding-left:18px;font-size:16px}
.box li{margin-bottom:6px}
.box a.s{font-weight:600}
.vigan{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:center;margin-top:64px}
.vigan img{border-radius:6px;aspect-ratio:4/3;object-fit:cover;width:100%}
.vigan h3{font-size:clamp(36px,3.6vw,52px);margin-bottom:14px}
.vigan p{margin:0 0 12px}
/* partenaires */
.parts{display:flex;flex-wrap:wrap;gap:10px}
.parts span{background:#fff;box-shadow:0 0 0 1px var(--ligne);border-radius:4px;padding:10px 14px;font-weight:600;font-size:15px}
.parts span.inst{background:var(--anth);color:#fff;box-shadow:none}
/* pied */
footer{background:var(--anth2);color:#fff;padding:64px 0 110px;font-size:16px}
footer .w{display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:40px}
footer h3{font-size:26px;color:var(--or);margin:0 0 14px}
footer p{margin:0 0 8px}
footer .small{font-size:13.5px;opacity:.7}
@media(max-width:1020px){
 .nav ul{display:none}
 .race summary{grid-template-columns:minmax(0,1fr) 90px 28px;gap:14px 18px}
 .race .bars{grid-column:1/-1;grid-row:2}
 .race .st{grid-column:1/-1;grid-row:3;justify-self:start}
 .race .det,.jour .w,.vigan{grid-template-columns:minmax(0,1fr);gap:28px}
 .jour .stick{position:static}
 .prat{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:760px){
 body{font-size:16px}
 .w{padding:0 18px}
 .hero{min-height:0;background-position:28% center}
 .hero::before{background:linear-gradient(180deg,rgba(20,22,24,.55) 0,rgba(20,22,24,.35) 30%,rgba(20,22,24,.85) 75%,rgba(20,22,24,.95) 100%)}
 .hero .in{padding:110px 0 40px}
 .count{gap:16px}.count b{font-size:34px}
 .chif .w{grid-template-columns:repeat(2,minmax(0,1fr))}
 .chif .w>div{padding:18px 10px 16px;border-left:0;border-top:1px solid rgba(255,255,255,.12)}
 .chif .w>div:nth-child(-n+2){border-top:0}
 .chif .w>div:nth-child(odd){padding-left:0}
 .sec{padding:64px 0}
 .race .nm{font-size:26px}
 .race .h{font-size:28px}
 .band p{padding:20px 18px}
 .tl li{grid-template-columns:74px minmax(0,1fr);gap:12px;padding:12px 14px}
 .tl time{font-size:22px}
 .prat{grid-template-columns:minmax(0,1fr)}
 footer .w{grid-template-columns:minmax(0,1fr)}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
'''

KMAX, DMAX = 101, 4500
races = ''
for c in C:
    kw = max(4, round(c['km'] / KMAX * 100))
    dw = max(4, round(c['dp'] / DMAX * 100))
    bh = ''
    if c['bh']:
        bh = '<h3>Barrières horaires</h3><table class="bh">' + ''.join('<tr><td>%s</td><td>km %s</td><td>%s</td></tr>' % b for b in c['bh']) + '</table>'
    else:
        bh = '<h3>Barrières horaires</h3><p>Aucune barrière horaire.</p>'
    repas = (' · ' + c['repas']) if c['repas'] else ''
    plus = ('<p>%s</p>' % c['plus']) if c['plus'] else ''
    lab = "S'inscrire" if c['stc'] == 'ok' else "Liste d'attente"
    races += f'''<details class="race" id="{c['id']}">
 <summary>
  <span class="nm"><small>{c['surnom']}</small>{c['nm']}</span>
  <span class="bars"><span class="bar km"><span class="tr"><i style="width:{kw}%"></i></span>{c['km']} km</span><span class="bar dp"><span class="tr"><i style="width:{dw}%"></i></span>{c['dp']:,} m D+</span></span>
  <span class="h">{c['h']}<small>{c['lieu']}</small></span>
  <span class="st {c['stc']}">{c['st']}</span>
  <span class="pl" aria-hidden="true">+</span>
 </summary>
 <div class="det">
  <div>
   <h3>La fiche</h3>
   <dl class="kv"><dt>Départ</dt><dd>Samedi 6 mars, {c['h']}, {c['lieu']}</dd><dt>Briefing</dt><dd>{c['brief']}</dd><dt>Places</dt><dd>{c['places']}</dd><dt>Tarif</dt><dd>{c['prix']}{repas}</dd><dt>Âge</dt><dd>{c['age']}</dd></dl>
   <p><b>Ravitaillements.</b> {c['rav']}</p>
   {plus}
   <div class="act"><a class="btn" href="{NJ}">{lab}</a><a class="s" href="{c['gpx']}">Trace GPX</a><a class="s" href="{REG}">Règlement 2027</a></div>
  </div>
  <div>{bh}</div>
 </div>
</details>
'''.replace('4,500', '4 500').replace('2,400', '2 400').replace('2,200', '2 200').replace('1,000', '1 000')

TL = [
    ('3 h 00', 'Ouverture de la Halle aux Sports', False),
    ('4 h 00', '<b>Départ de l\'Ultra du Bout du Cirque</b>, briefing à 3 h 50', True),
    ('7 h 30', 'Retrait des dossards du 42 et du 63 km', False),
    ('8 h 00', 'Ouverture du salon', False),
    ('10 h 00', '<b>Départ du Marathon de la Toureille</b>, place du Quai', True),
    ('10 h 45', 'Déambulation avec la batucada, place du Quai', False),
    ('11 h 00', '<b>Départ du Trail aux Étoiles</b>, place du Quai', True),
    ('11 h 15', 'Début des courses enfants', False),
    ('11 h 30', 'Retrait des dossards du 23 et du 12 km', False),
    ('13 h 45', 'Premières arrivées du 100 et du 42 km', False),
    ('14 h 00', '<b>Départ du Trail de l\'Oignon Doux</b>', True),
    ('14 h 30', '<b>Départ du Trail du Pays Viganais</b>', True),
    ('15 h 20', 'Premières arrivées du 23 et du 12 km', False),
    ('16 h 30', 'Premières arrivées du 63 km', False),
    ('17 h 00', 'Podiums du 23 et du 12 km', False),
    ('18 h 30', 'Repas', False),
    ('19 h 00', 'Podiums du 100 km, puis du 63 km à 19 h 30', False),
    ('23 h 45', 'Les derniers coureurs rentrent à la Halle', False),
]
tl = ''.join('<li class="%s"><time>%s</time><span>%s</span></li>' % ('dep' if d else '', t, s) for t, s, d in TL)

PARTS_INST = ['Région Occitanie', 'Département du Gard', 'Ville du Vigan', 'Communauté de communes du Pays Viganais', 'Office de tourisme Sud Cévennes',
              'Grand Site Cirque de Navacelles', 'Tourisme Occitanie', 'Tourisme Gard', 'CCI Gard', 'Challenge Gardois des Trails']
PARTS = ['Magasins U', 'Biocoop', 'AXA', 'Groupama', 'Café des Cévennes', 'Sud Bois', 'Monts et Merveilles', 'Lieure Immobilier', 'Immo3D', 'Well',
         'M&TM Cavaillac', "L'Échappée Belledonne", 'Cinéma Le Palace', 'Bbass', 'Oignon doux des Cévennes', 'ABV Films', 'Spiruline Arc-en-ciel']
parts = ''.join('<span class="inst">%s</span>' % p for p in PARTS_INST) + ''.join('<span>%s</span>' % p.replace('&', '&amp;') for p in PARTS)

PAGE = f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Ceven'Trail 2027 : maquette de site par EventLyx</title>
<link rel="preload" as="image" href="hero.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Work+Sans:wght@400;600;700&display=swap">
<style>{CSS}{chat_css}</style></head><body>

<div class="maq"><span>Maquette de refonte réalisée par EventLyx pour le Ceven'Trail. Ce n'est pas le site officiel.</span><a href="{SITE}">Site officiel</a></div>

<header class="hero" id="haut"><div class="w" style="width:100%">
 <nav class="nav" aria-label="Navigation principale">
  <a class="wm" href="#haut"><span class="c">Ceven'</span><span class="t">Trail</span><small>LE VIGAN · 30</small></a>
  <ul><li><a href="#courses">Les courses</a></li><li><a href="#samedi">Le programme</a></li><li><a href="#pratique">Pratique</a></li><li><a href="#partenaires">Partenaires</a></li><li><a href="#contact">Contact</a></li></ul>
 </nav>
 <div class="in">
  <span class="ed">21e édition</span>
  <h1>Ceven'<span>Trail</span></h1>
  <p class="date">Samedi 6 mars 2027 · Le Vigan</p>
  <p class="lead">Cinq courses de 12 à 101 km entre le Pays Viganais et le cirque de Navacelles. Une même journée, de la nuit à la nuit, et l'arrivée à la Halle aux Sports.</p>
  <div class="row"><a class="btn" href="{NJ}">S'inscrire sur Njuko</a><a class="btn clair" href="#courses">Comparer les courses</a></div>
  <div class="count" aria-label="Temps restant avant le départ de l'ultra"><div><b id="cj">–</b>jours</div><div><b id="ch">–</b>heures</div><div><b id="cm">–</b>minutes</div></div>
 </div>
</div></header>

<section class="chif" aria-label="En chiffres"><div class="w">
 <div><b>5</b><span>courses, de 12 à 101 km</span></div>
 <div><b>4 h 00</b><span>départ de l'ultra, à la frontale</span></div>
 <div><b>+1 200</b><span>coureurs au départ</span></div>
 <div><b>+150</b><span>bénévoles</span></div>
</div></section>

<section class="sec" id="courses"><div class="w">
 <h2>Les 5 courses</h2>
 <p class="lead">Distance en orange, dénivelé en gris : les barres sont à la même échelle, de quoi choisir d'un coup d'œil. Ouvrez une course pour voir sa fiche, ses ravitaillements et ses barrières horaires.</p>
 <div class="races">
{races} </div>
 <p class="races-note">Distances, dénivelés et horaires du roadbook 2027 ; places, tarifs et âges du règlement 2027. Statut des inscriptions relevé sur Njuko le 27 novembre 2026. Licence FFA ou PPS obligatoire, dossier complet au 20 février 2027.</p>
</div></section>

<div class="band" style="background-image:url(aube.jpg);background-position:center 30%" role="img" aria-label="Un traileur avec ses bâtons au lever du soleil"><p>Départ de l'ultra à 4 h 00, le jour se lève en course.</p></div>

<section class="sec jour" id="samedi"><div class="w">
 <div class="stick">
  <h2>Samedi 6 mars, heure par heure</h2>
  <p class="lead">De l'ouverture de la Halle à 3 h du matin jusqu'aux derniers coureurs, peu avant minuit.</p>
  <div class="vend"><h3>La veille, vendredi 5 mars</h3><p>Halle aux Sports, accueil dès 17 h 30.</p><p>Retrait des dossards de 17 h 30 à 21 h 00.</p><p>Pasta party de 18 h 30 à 21 h 00, sur réservation (8 €).</p></div>
 </div>
 <ol class="tl">{tl}</ol>
</div></section>

<section class="sec" id="pratique"><div class="w">
 <h2>Pratique</h2>
 <p class="lead">Tout se passe autour de la Halle aux Sports Pierre Durand, au Vigan : retrait des dossards, salon, arrivées, douches et podiums.</p>
 <div class="prat">
  <div class="box"><h3>Se garer</h3><p>Stationnement interdit aux abords de la Halle.</p><ul><li>Maison de la Petite Enfance et stade annexe : 800 m, 250 à 300 places</li><li>Parking des écoles, rue Pierre Gorlier : 200 m, 60 places</li><li>Rond-point Charles de Gaulle : 500 m, 100 places</li></ul></div>
  <div class="box"><h3>Venir</h3><p>En bus : ligne liO 608 depuis Montpellier, ligne 140 depuis Nîmes.</p><p>Hébergements : sélection mise à jour sur la <a class="s" href="{LOGER}">page Se loger</a>.</p></div>
  <div class="box"><h3>Sur place</h3><p>Douches à la Halle aux Sports. Salon du Ceven'Trail le vendredi soir et le samedi.</p><p>Repas accompagnateur : 12 €. Pas de gobelet aux ravitaillements : écotasse.</p></div>
  <div class="box"><h3>Bourse aux dossards</h3><p>Pas de remboursement, mais report ou échange possible jusqu'à 15 jours avant la course.</p><p><a class="s" href="{BOURSE}">Revendre ou racheter un dossard</a></p></div>
  <div class="box"><h3>Courses enfants</h3><p>Gratuites, le samedi à partir de 11 h 15, aux abords de la Halle. Attestation de santé et autorisation parentale.</p></div>
  <div class="box"><h3>En direct</h3><p>Classement en direct sur <a class="s" href="{LIVE}">live.l-chrono.com</a>, vidéo sur écran géant, sur le site et sur Facebook.</p><p><a class="s" href="{RB}">Roadbook 2027 (PDF)</a></p></div>
 </div>
 <div class="vigan">
  <img src="crete.jpg" alt="Un groupe de traileurs dans la montée, au lever du jour" width="1500" height="1000" loading="lazy">
  <div><h3>Rejoindre les bénévoles</h3><p>Plus de 150 bénévoles font le Ceven'Trail. L'association Pays Viganais Endurance Nature organise la course depuis 2004.</p><p><a class="btn sombre" href="{BENEV}">Devenir bénévole</a></p></div>
 </div>
</div></section>

<div class="band" style="background-image:url(soir.jpg);background-position:center 60%" role="img" aria-label="Un coureur en silhouette sur une crête au coucher du soleil"><p>Les derniers rentrent peu avant minuit.</p></div>

<section class="sec" id="partenaires"><div class="w">
 <h2>Partenaires</h2>
 <p class="lead">Les institutions et les entreprises qui soutiennent la course.</p>
 <div class="parts">{parts}</div>
</div></section>

<footer id="contact"><div class="w">
 <div><h3>Nous joindre</h3><p><a href="mailto:{MAIL}">{MAIL}</a></p><p><a href="tel:+33786992000">07 86 99 20 00</a> · <a href="tel:+33652318332">06 52 31 83 32</a></p><p><a href="https://www.facebook.com/profile.php?id=100057467958256">Facebook</a> · <a href="https://www.instagram.com/ceventrail_levigan30/">Instagram</a> · <a href="https://www.youtube.com/channel/UCyKGWLKxDTW9SP7OY9wUR-g/videos">YouTube</a></p></div>
 <div><h3>L'organisateur</h3><p>Association Pays Viganais Endurance Nature (PVEN)<br>Hôtel de ville, 30120 Le Vigan</p></div>
 <div><h3>À propos de cette page</h3><p class="small">Maquette proposée par EventLyx. Informations relevées le 27 novembre 2026 sur ceventrail.org, dans le règlement et le roadbook 2027 et sur Njuko. Photos : Ceven'Trail, tirées du site de la course.</p></div>
</div></footer>
{chat_html}
<script>
{{
 const T=Date.parse('2027-03-06T04:00:00+01:00');
 const tick=()=>{{let s=Math.max(0,Math.floor((T-Date.now())/1000));
  document.getElementById('cj').textContent=Math.floor(s/86400);
  document.getElementById('ch').textContent=Math.floor(s%86400/3600);
  document.getElementById('cm').textContent=Math.floor(s%3600/60)}};
 tick();setInterval(tick,30000);
}}
</script>
{chat_js}
</body></html>
'''

open(OUT, 'w', encoding='utf-8').write(PAGE)
print(OUT, len(PAGE))
