#!/usr/bin/env python3
"""Générateur de maquettes EventLyx, à partir du gabarit validé (rocamadour/index.html).

Usage (depuis la racine du dépôt) : python3 _gabarit/gen.py <dossier>
Pour un nouveau club : copie un des dicts d'exemple (chierry, randon) en bas du fichier,
adapte-le (couleurs du club, textes, distances, timeline, réponses du chatbot R/Q/fallback/hello),
ajoute-le au tuple de la boucle finale, mets les photos (hero.jpg, etc.) dans <dossier>/, puis lance.
Voir CLAUDE.md à la racine pour la procédure complète."""
import re, json, html, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

T = open(os.path.join(ROOT, 'rocamadour', 'index.html'), encoding='utf-8').read()
CSS = T[T.index('<style>') + 7:T.index('</style>')]
CHAT_JS_TAIL = T[T.index(" const $=id=>document.getElementById(id),box=$('chat')"):T.rindex('</script>')]

EXTRA_CSS = '''
.logo.txt{background:var(--safran);color:var(--encre);padding:16px 18px 14px;text-decoration:none;font-stretch:62%;font-weight:900;text-transform:uppercase;font-size:clamp(22px,2.4vw,32px);line-height:.9;max-width:9.5em}
.dist .nm{font-weight:800;font-size:18px;margin:0 0 8px}
.dist .num.w{font-size:clamp(64px,7.6vw,128px)}
.tl time small{font-size:.5em;font-weight:800;margin-left:.2em}
.av{width:46px;height:46px;border-radius:50%;border:2px solid #fff;flex:none;display:grid;place-items:center;background:var(--safran);color:var(--encre);font-weight:900;font-size:15px}
.msg.a::before{background:var(--safran);content:var(--ini);color:var(--encre);font:900 10px/26px var(--f);text-align:center}
.cw .note a{color:inherit}
.facts b{white-space:normal}
img{height:auto}
.date{font-size:clamp(52px,11.2vw,168px)}
'''


def build(c):
    css = CSS
    css = re.sub(r':root\{color-scheme:light;.*?--f:', ':root{color-scheme:light;--vin:%(vin)s;--vind:%(vind)s;--encre:%(encre)s;--creme:%(creme)s;--safran:%(safran)s;--sable:%(sable)s;--ini:"%(ini)s";--f:' % c, css, count=1, flags=re.S)
    css = re.sub(r'/\* VOICE.*?\*/', c['notes'], css, count=1, flags=re.S)
    css = css.replace('rgba(23,19,46,', 'rgba(%s,' % c['encre_rgb']).replace('rgba(250,248,253,', 'rgba(%s,' % c['creme_rgb'])
    css = css.replace('rgba(88,77,160,', 'rgba(%s,' % c['vin_rgb']).replace('rgba(52,40,120,.45)', 'rgba(%s,.45)' % c['vin_rgb'])
    css = css.replace('linear-gradient(135deg,#6A5BB8,var(--vin) 55%,#453B86)', 'linear-gradient(135deg,%s,var(--vin) 55%%,%s)' % (c['g1'], c['g2']))
    css = css.replace('#F7F5FB', c['chatbg']).replace('color:#EFEBFA', 'color:%s' % c['clubtxt'])
    css = css.replace('.msg.a::before{content:"";position:absolute;left:-34px;bottom:0;width:26px;height:26px;border-radius:50%;background:url(clublogo.jpg) center/cover}',
                      '.msg.a::before{position:absolute;left:-34px;bottom:0;width:26px;height:26px;border-radius:50%}')
    css = css.replace('center 30%/cover no-repeat;isolation:isolate', '%s/cover no-repeat;isolation:isolate' % c['heropos'])
    css = re.sub(r'\.hero::before\{[^}]*\}', '.hero::before{content:"";position:absolute;inset:0;z-index:-1;background:%s}' % c['overlay'], css, count=1)
    css += EXTRA_CSS + c.get('css', '')
    e = html.escape
    dists = ''
    for i, d in enumerate(c['dists']):
        rows = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % r for r in d['rows'])
        dists += ' <a class="dist c%d" href="%s"><p class="nm">%s</p><span class="d num%s">%s<small>%s</small></span>\n  <dl>%s</dl>\n  <p>%s</p><span class="go">%s</span></a>\n' % (
            i + 1, d['href'], d['nm'], ' w' if d.get('wide') else '', d['num'], d.get('unit', ''), rows, d['txt'], d['go'])
    tl = ''.join('   <li><time>%s</time><span>%s</span></li>\n' % t for t in c['tl'])
    facts = ''.join('  <div><b>%s</b><p>%s</p></div>\n' % f for f in c['facts'])
    clubli = ''.join('   <li>%s</li>\n' % x for x in c['club']['li'])
    nav = ''.join('<li><a href="%s">%s</a></li>' % n for n in c['nav'])
    R = json.dumps(c['R'], ensure_ascii=False)
    Q = json.dumps(c['Q'], ensure_ascii=False)
    js_tail = CHAT_JS_TAIL
    js_tail = re.sub(r'return r\?r\[1\]:".*?"\};', 'return r?r[1]:%s};' % json.dumps(c['fallback'], ensure_ascii=False), js_tail, count=1, flags=re.S)
    js_tail = re.sub(r'm\.innerHTML=".*?";', 'm.innerHTML=%s;' % json.dumps(c['hello'], ensure_ascii=False), js_tail, count=1, flags=re.S)
    mid = c.get('mid', '')
    page = f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{e(c['title'])}</title>
<link rel="preload" as="image" href="hero.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&display=swap">
<style>{css}</style></head><body>

<div class="maq"><span>Maquette de refonte réalisée par EventLyx pour {c['club_name']}. Ce n'est pas le site officiel.</span><a href="{c['official']}">Site officiel du club</a></div>

<header class="hero" id="haut">
 <div class="top">
  <a class="logo txt" href="#haut">{c['wordmark']}</a>
  <ul>{nav}</ul>
 </div>
 <div class="txt"><div class="in">
  <p class="d date" aria-hidden="true">{c['date_big']}</p>
  <h1 class="d">{c['h1']}</h1>
  <p class="sub">{c['sub']}</p>
  <div class="row">
   <a class="btn" href="{c['signup']}">Je m'inscris</a>
   <a class="btn line" href="#distances">{c['btn2']}</a>
   <div class="count" id="count" aria-label="Temps restant avant le départ"><div><b id="cj">–</b>jours</div><div><b id="ch">–</b>heures</div><div><b id="cm">–</b>minutes</div></div>
  </div>
 </div></div>
</header>

<section class="dists" id="distances" aria-label="Les formats">
{dists}</section>

<section class="prog" id="programme">
 <div class="pic" role="img" aria-label="{e(c['prog']['alt'])}"></div>
 <div class="pan">
  <h2 class="d">{c['prog']['h2']}</h2>
  <ol class="tl">
{tl}  </ol>
 </div>
</section>

<section class="sec" id="{c['facts_id']}"><div class="in">
 <h2 class="d">{c['facts_h2']}</h2>{c.get('facts_lead','')}
 <div class="facts">
{facts} </div>
</div></section>
{mid}
<section class="sec club" id="club">
 <div>
  <h2 class="d">{c['club']['h2']}</h2>
  <ul>
{clubli}  </ul>
  <a class="btn" href="{c['club']['href']}">{c['club']['btn']}</a>
 </div>
 <img src="{c['club']['img']}" alt="{e(c['club']['alt'])}" width="{c['club']['w']}" height="{c['club']['h']}">
</section>

<footer id="contact"><div class="in">
 <div><h3>Nous joindre</h3>{c['contact']}</div>
 <div><h3>{c['where_h']}</h3>{c['where']}</div>
 <div><h3>À propos de cette page</h3><p class="small">Maquette proposée par EventLyx. Informations relevées le {c.get('releve', '26 novembre 2026')} sur le site du club. {c['credits']}</p></div>
</div></footer>

<div class="bar"><span>{c['bar_t']}<small>{c['bar_s']}</small></span><a class="btn" href="{c['signup']}">Je m'inscris</a></div>

<div class="tz" id="tz"><b>{c['tz']}</b><span>Réponse en quelques secondes</span><button type="button" id="tzX" aria-label="Masquer ce message">×</button></div>
<button class="cb" id="chatB" type="button" aria-expanded="false" aria-controls="chat" aria-label="Ouvrir l'assistant de la course">
 <svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3C6.5 3 2 6.8 2 11.5c0 2.6 1.4 4.9 3.6 6.5-.2 1.2-.8 2.4-1.7 3.4 2 0 3.8-.7 5.2-1.8.9.2 1.9.4 2.9.4 5.5 0 10-3.8 10-8.5S17.5 3 12 3zM7.5 13a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm4.5 0a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm4.5 0a1.5 1.5 0 110-3 1.5 1.5 0 010 3z"/></svg>
 <svg class="ix" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
</button>
<section class="cw" id="chat" role="dialog" aria-label="Assistant de la course">
 <header>
  <div class="av" aria-hidden="true">{c['ini']}</div>
  <div><small>{c['chat_small']}</small><b>{c['chat_b']}</b><em>Assistant de démonstration</em></div>
  <button type="button" id="chatR" aria-label="Recommencer la conversation"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12a8 8 0 108-8 8 8 0 00-6 2.7"/><path d="M4 4v4h4"/></svg></button>
  <button type="button" id="chatX" aria-label="Réduire l'assistant"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
 </header>
 <div class="msgs" id="msgs" aria-live="polite"></div>
 <div class="chips" id="chips"></div>
 <form id="chatF"><input id="chatI" type="text" autocomplete="off" placeholder="{c['ph']}" aria-label="Votre question"><button type="submit" aria-label="Envoyer"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 20.5l19-8.5L3 3.5v6.5l12 2-12 2z"/></svg></button></form>
 <p class="note">Démonstration EventLyx : réponses tirées des informations de cette page.</p>
</section>
<script>
{{
 const T=Date.parse('{c['t0']}');
 const tick=()=>{{let s=Math.max(0,Math.floor((T-Date.now())/1000));
  document.getElementById('cj').textContent=Math.floor(s/86400);
  document.getElementById('ch').textContent=Math.floor(s%86400/3600);
  document.getElementById('cm').textContent=Math.floor(s%3600/60)}};
 tick();setInterval(tick,30000);
}}
</script>

<script>
{{
 const R={R};
 const Q={Q};
{js_tail}</script>
</body></html>
'''
    open(os.path.join(ROOT, c['dir'], 'index.html'), 'w', encoding='utf-8').write(page)
    print(c['dir'], len(page))


CH_SITE = 'https://chierryjycours.e-monsite.com/'
CH_TROLLS = 'https://chierryjycours.e-monsite.com/pages/la-nuit-des-trolls.html'
CH_INF = 'https://chierryjycours.e-monsite.com/pages/off-l-infernal-du-bois.html'
chierry = dict(
    dir='chierry', title="Tamp'Trolls et Infernal du Bois : maquette de site par EventLyx", club_name="Chierry J'y Cours", official=CH_SITE,
    notes="/* VOICE  le club parle en « tu », sans chrono : on garde ce ton dans l'assistant\n   PICTURE le village de la course, Nesles-la-Montagne, assombri comme à la tombée de la nuit\n   COLOUR l'orange des vestes du club, un noir chaud, deux tons clairs ; l'orange vif seulement pour s'inscrire\n   TYPE   Archivo, très condensée et noire pour les titres */",
    vin='#C2410C', vind='#1F1611', encre='#16100C', creme='#FFF8F2', safran='#FF7A1A', sable='#FFE3CC', ini='CJC',
    encre_rgb='22,16,12', creme_rgb='255,248,242', vin_rgb='194,65,12', g1='#DD5A1C', g2='#8F2F08', chatbg='#FBF6F1', clubtxt='#FFEFE3',
    heropos='center 62%',
    overlay='linear-gradient(180deg,rgba(22,16,12,.74) 0,rgba(22,16,12,.46) 30%,rgba(22,16,12,.5) 52%,rgba(22,16,12,.94) 100%)',
    css='.prog .pic{background-position:42% 40%}',
    wordmark="Chierry J'y Cours",
    nav=[('#distances', 'Les formats'), ('#programme', "Tamp'Trolls"), ('#infernal', 'Infernal du Bois'), ('#club', 'Le club'), ('#contact', 'Contact')],
    date_big='23 janv. 2027', h1="Tamp'Trolls",
    sub="Samedi 23 janvier 2027, à Nesles-la-Montagne. Un trail de nuit de 13,8 km, à la frontale. Départ à 18 h.",
    signup=CH_TROLLS, btn2='Voir les formats', t0='2027-01-23T18:00:00+01:00',
    dists=[
        dict(nm="Tamp'Trolls", num='13,8', unit='km', href=CH_TROLLS, rows=[('Dénivelé', 'environ 470 m D+'), ('Départ', 'sam. 23 janv., 18 h')],
             txt="Le trail nocturne du club, en autonomie complète. 200 dossards, pas un de plus.", go='Prendre ce dossard'),
        dict(nm="L'Infernal", num='6', unit='heures', href=CH_INF, rows=[('La boucle', '6 km, 314 m D+'), ('Départ', 'dim. 4 avril, 8 h 00')],
             txt="Six heures de boucles dans le bois Pierre, à Chierry. Autant de tours que les jambes le permettent.", go="Voir l'Infernal"),
        dict(nm='La Pénible', num='3', unit='heures', href=CH_INF, rows=[('La boucle', '6 km, 314 m D+'), ('Départ', 'dim. 4 avril, 9 h 30')],
             txt="Le même bois et la même boucle, pendant trois heures.", go='Voir la Pénible'),
        dict(nm='La Cerisiènne', num='12', unit='km', href=CH_INF, rows=[('Le format', '2 tours de boucle'), ('Départ', 'dim. 4 avril, 10 h 30')],
             txt="Deux tours et c'est plié : le format trail de la journée.", go='Voir la Cerisiènne'),
    ],
    prog=dict(alt='Nesles-la-Montagne, entre les vignes et la vallée de la Marne', h2="Avant de t'inscrire"),
    tl=[('18 h', 'Départ de Nesles-la-Montagne, frontale allumée'), ('200', 'dossards, inscriptions en ligne'),
        ('0', 'ravitaillement sur le parcours : chacun part avec ce qu\'il lui faut'), ('13,8<small>km</small>', 'et environ 470 m de dénivelé, que la météo peut faire bouger un peu')],
    facts_id='infernal', facts_h2="L'Infernal du Bois",
    facts_lead='\n <p class="lead">Dimanche 4 avril 2027, à Chierry. Une boucle de 6 km et 314 m de dénivelé dans le bois Pierre, à refaire encore et encore.</p>',
    facts=[('3 formats', "L'Infernal pendant 6 heures, la Pénible pendant 3 heures, la Cerisiènne sur 2 tours."),
           ('150 dossards', 'Pour les trois formats réunis.'),
           ('PPS', 'À jour avant le 25 mars 2027, sinon pas de dossard.')],
    club=dict(h2="Chierry J'y Cours", li=[
        '<b>« Ne viens pas pour un chrono ou une place. »</b> La seule consigne du club.',
        "<b>255 dossards en 2026</b>, tous partis trois semaines avant le jour J.",
        "<b>255 € remis aux urgences</b> de l'hôpital de Château-Thierry après l'édition 2026.",
        "<b>Des BénéTrolls partout</b> : à l'accueil, au chrono et aux traversées de route."],
        href=CH_SITE, btn='Découvrir le club', img='trolls.jpg', alt="Des coureurs déguisés au départ d'une édition des Trolls, de nuit", w=1050, h=680),
    contact='<p>Par le formulaire du <a href="%s">site du club</a>.</p><p>Sur Facebook : « Chierry j\'y cours » et « Trolls ».</p>' % CH_SITE,
    where_h='Où ça se passe', where="<p>Tamp'Trolls : Nesles-la-Montagne (02400)</p><p>Infernal du Bois : Chierry (02400)</p>",
    credits="Photo de Nesles-la-Montagne : Pascal3012, Wikimedia Commons, licence CC BY-SA 4.0, assombrie. Photo des coureurs : Chierry J'y Cours.",
    bar_t='Inscriptions ouvertes', bar_s="Tamp'Trolls, samedi 23 janvier 2027",
    tz="Une question sur les Trolls ?", chat_small="Chierry J'y Cours", chat_b="Tamp'Trolls", ph='Pose ta question…',
    hello="<p>Salut ! 👋 Je suis l'assistant de <strong>Chierry J'y Cours</strong>.</p><p>Tamp'Trolls, Infernal du Bois, dossards, horaires… pose-moi ta question !</p>",
    fallback="Je n'ai pas cette information. Sur le site en ligne, je transmets la question aux bénévoles du club. En attendant, passe par le formulaire du site du club.",
    Q=[["🕕 Départ", "À quelle heure est le départ ?"], ["🔦 Parcours", "Quelle distance et quel dénivelé ?"], ["🥤 Ravitos", "Y a-t-il des ravitaillements ?"],
       ["🌲 Infernal du Bois", "C'est quoi l'Infernal du Bois ?"], ["🎟️ Places", "Combien de dossards ?"]],
    R=[
        [['penible'], "La Pénible, c'est 3 heures de boucles dans le bois Pierre (6 km et 314 m de dénivelé par tour). Départ le dimanche 4 avril 2027 à 9 h 30, à Chierry."],
        [['cerisi'], "La Cerisiènne fait 2 tours de la boucle, soit 12 km. Départ le dimanche 4 avril 2027 à 10 h 30, à Chierry."],
        [['pps', 'certificat', 'licence'], "Pour l'Infernal du Bois, ton PPS doit être à jour avant le 25 mars 2027, sinon pas de dossard."],
        [['infernal', 'bois pierre', 'boucle', 'avril'], "L'Infernal du Bois a lieu le dimanche 4 avril 2027 à Chierry. Une boucle de 6 km et 314 m de dénivelé, et trois formats : l'Infernal pendant 6 heures (départ 8 h 00), la Pénible pendant 3 heures (9 h 30) et la Cerisiènne sur 2 tours (10 h 30). 150 dossards en tout."],
        [['ravito', 'ravitaillement', 'manger', 'boire', 'eau', 'autonomie'], "Tamp'Trolls se court en autonomie complète : pas de ravitaillement sur le parcours, tu pars avec ce qu'il te faut."],
        [['combien de dossard', 'places', 'limite', 'complet', 'dossard'], "Tamp'Trolls est limité à 200 dossards. En 2026, tous les dossards étaient partis trois semaines avant le jour J : n'attends pas."],
        [['inscri'], "Les inscriptions de Tamp'Trolls sont ouvertes depuis le 15 septembre 2026. Le bouton « Je m'inscris », en bas de la page, t'y emmène."],
        [['distance', 'denivele', 'parcours', 'km', 'd+'], "Tamp'Trolls fait 13,8 km pour environ 470 m de dénivelé positif. Selon la météo du jour, le parcours peut être légèrement modifié."],
        [['heure', 'horaire', 'depart', 'quand part'], "Le départ de Tamp'Trolls est donné à 18 h 00, le samedi 23 janvier 2027, à Nesles-la-Montagne."],
        [['date', 'quel jour', 'quand'], "Tamp'Trolls a lieu le samedi 23 janvier 2027 à Nesles-la-Montagne. L'Infernal du Bois, le dimanche 4 avril 2027 à Chierry."],
        [['ou se', 'ou est', 'ou a lieu', 'lieu', 'adresse', 'nesles'], "Tamp'Trolls part de Nesles-la-Montagne (02400). L'Infernal du Bois se court à Chierry, dans le bois Pierre."],
        [['frontale', 'materiel', 'lampe', 'nuit'], "Tamp'Trolls est un trail nocturne : la frontale est de sortie. Pour la liste complète du matériel, regarde le règlement 2027 sur le site du club."],
        [['reglement'], "Le règlement 2027 est en téléchargement sur le site du club."],
        [['contact', 'mail', 'joindre', 'facebook'], "Tu peux écrire au club par le formulaire de son site, ou passer par les pages Facebook « Chierry j'y cours » et « Trolls »."],
        [['bonjour', 'salut', 'hello', 'coucou'], "Salut ! Pose-moi ta question sur Tamp'Trolls ou l'Infernal du Bois."]
    ],
)

RA_SITE = 'https://lerandontrail.sportsregions.fr/'
RA_SIGN = 'https://chronohb.fr/inscriptions-randon-nuit-2027-nouveaux-parcours/'
randon = dict(
    dir='randon', title="Randon'Nuit et Randon Trail : maquette de site par EventLyx", club_name='Les Traileurs du Randon', official=RA_SITE,
    notes="/* PICTURE la Margeride sous la neige, comme un 2 janvier : granit, pins et ciel bleu\n   COLOUR le bleu du ciel d'hiver, un bleu nuit, deux bleus très clairs ; le jaune seulement pour s'inscrire\n   TYPE   Archivo, très condensée et noire pour les titres */",
    vin='#1257C4', vind='#0B1F4B', encre='#0A1530', creme='#F7FAFF', safran='#F2B90F', sable='#DCE8FB', ini='TR',
    encre_rgb='10,21,48', creme_rgb='247,250,255', vin_rgb='18,87,196', g1='#2D74E0', g2='#0C3F96', chatbg='#F4F7FC', clubtxt='#E6EFFF',
    heropos='center 45%',
    overlay='linear-gradient(180deg,rgba(10,21,48,.5) 0,rgba(10,21,48,.08) 26%,rgba(10,21,48,.34) 50%,rgba(10,21,48,.93) 100%)',
    css='.prog .pic{background-image:url(signal.jpg);background-position:70% center}.ben img{aspect-ratio:4/3;object-fit:cover}',
    wordmark='Les Traileurs du Randon',
    nav=[('#distances', 'Les parcours'), ('#programme', 'Programme'), ('#trail', 'Randon Trail'), ('#club', 'Le club'), ('#contact', 'Contact')],
    date_big='2 janv. 2027', h1="Randon'Nuit",
    sub="Samedi 2 janvier 2027, à Rieutort-de-Randon. Deux trails à la frontale et une randonnée, pour commencer l'année en Margeride.",
    signup=RA_SIGN, btn2='Choisir mon parcours', t0='2027-01-02T18:00:00+01:00',
    dists=[
        dict(nm='Trail', num='15', unit='km', href=RA_SIGN, rows=[('Dénivelé', '493 m D+'), ('Départ', '18 h 00')],
             txt="Le grand parcours de la soirée, à la frontale. Repas compris à l'arrivée.", go='Prendre ce dossard'),
        dict(nm='Trail', num='9', unit='km', href=RA_SIGN, rows=[('Dénivelé', '265 m D+'), ('Départ', '18 h 00')],
             txt="Le format court, de nuit lui aussi. Repas compris à l'arrivée.", go='Prendre ce dossard'),
        dict(nm='Randonnée', num='9', unit='km', href=RA_SIGN, rows=[('Dénivelé', '265 m D+'), ('Départ', '16 h 00')],
             txt="Neuf kilomètres à la marche. Départ deux heures avant les trails.", go="M'inscrire à la rando"),
        dict(nm='Randon Trail', num='Mai', unit='2027', wide=True, href='#trail', rows=[('En 2026', '15 km, 595 m D+'), ('et', '10 km, 415 m D+')],
             txt="Le rendez-vous de printemps, de jour. La date sera annoncée par le club.", go='Voir le Randon Trail'),
    ],
    prog=dict(alt='Le signal de Randon vu depuis le truc de Fortunio', h2='Le samedi, heure par heure'),
    tl=[('16 h 00', 'Départ de la randonnée de 9 km'), ('18 h 00', 'Départ des trails de 15 km et de 9 km'), ('Après', "Le repas, compris dans l'inscription des traileurs")],
    facts_id='pratique', facts_h2='Avant de venir',
    facts=[('Tracés 2027', 'De nouveaux parcours pour cette édition.'),
           ('Challenge', "La Randon'Nuit compte pour le Challenge des Trails Nocturnes."),
           ('Inscriptions', 'En ligne, sur <a href="%s">la page ChronoHB de la course</a>.' % RA_SIGN)],
    mid='''
<section class="sec ben" id="trail">
 <img src="runner.jpg" alt="Un coureur et son chien sur les blocs de granit, près du truc de Fortunio" width="720" height="540">
 <div>
  <h2 class="d">Randon Trail, en mai 2027</h2>
  <p class="lead">Le même village, de jour. La date sera annoncée par le club. En 2026, il y avait un 15 km (595 m de dénivelé) et un 10 km (415 m).</p>
  <a class="btn" href="%s">Suivre les annonces du club</a>
 </div>
</section>
''' % RA_SITE,
    club=dict(h2='Les Traileurs du Randon', li=[
        "<b>Deux courses par an</b> : la Randon'Nuit en janvier, le Randon Trail en mai.",
        '<b>Un village</b> : Rieutort-de-Randon, en Lozère, au pied du truc de Fortunio.',
        '<b>Des classements faciles à lire</b> : de vrais tableaux, où chacun retrouve son temps sur son téléphone.'],
        href=RA_SITE, btn='Découvrir le club', img='tower.jpg', alt='Le relais du truc de Fortunio entre les pins', w=720, h=540),
    contact='<p>Par le <a href="https://lerandontrail.sportsregions.fr/contactez-nous">formulaire du site du club</a>.</p><p>Sur Facebook : lestraileursdurandon</p>',
    where_h='Où ça se passe', where='<p>Rieutort-de-Randon</p><p>Lozère (48), Margeride</p>',
    credits="Photos de la Margeride, Wikimedia Commons : truc de Chapelat par Charpalprod (CC BY-SA 4.0), signal de Randon par Anthospace (CC BY-SA 3.0). Autres photos : Les Traileurs du Randon.",
    bar_t='Inscriptions ouvertes', bar_s="Randon'Nuit, samedi 2 janvier 2027",
    tz="Une question sur la Randon'Nuit ?", chat_small='Les Traileurs du Randon', chat_b="Randon'Nuit", ph='Posez votre question…',
    hello="<p>Bonjour ! 👋 Je suis l'assistant de la <strong>Randon'Nuit</strong>.</p><p>Parcours, horaires, repas, inscriptions… posez-moi votre question !</p>",
    fallback="Je n'ai pas cette information. Sur le site en ligne, je transmets la question aux bénévoles du club. En attendant, vous pouvez leur écrire par le formulaire du site du club.",
    Q=[["🕕 Horaires", "À quelle heure sont les départs ?"], ["🔦 Parcours", "Quels sont les parcours ?"], ["🍲 Repas", "Le repas est-il compris ?"],
       ["🥾 Randonnée", "Y a-t-il une randonnée ?"], ["🌱 Randon Trail", "C'est quand le Randon Trail ?"]],
    R=[
        [['randon trail', 'en mai', 'printemps'], "Le Randon Trail aura lieu en mai 2027. La date sera annoncée par le club. En 2026, il proposait un 15 km (595 m de dénivelé) et un 10 km (415 m)."],
        [['randonnee', 'marche', 'marcher'], "Oui, une randonnée de 9 km (265 m de dénivelé) part à 16 h 00, deux heures avant les trails."],
        [['repas', 'manger'], "Le repas est compris dans l'inscription des traileurs."],
        [['15'], "Le trail de 15 km compte 493 m de dénivelé positif. Départ à 18 h 00."],
        [['9 km', '9km'], "Le trail de 9 km compte 265 m de dénivelé positif, départ à 18 h 00. La randonnée de 9 km part à 16 h 00."],
        [['inscri', 'dossard'], "Les inscriptions se font en ligne sur ChronoHB. Le bouton « Je m'inscris », en bas de la page, vous y emmène directement."],
        [['challenge'], "Oui, la Randon'Nuit compte pour le Challenge des Trails Nocturnes."],
        [['heure', 'horaire', 'depart', 'quand part'], "Le samedi 2 janvier 2027 : la randonnée part à 16 h 00, les trails de 15 km et de 9 km à 18 h 00."],
        [['parcours', 'distance', 'denivele', 'format', 'km'], "Deux trails : 15 km (493 m de dénivelé) et 9 km (265 m), départ à 18 h 00. Et une randonnée de 9 km, départ à 16 h 00."],
        [['date', 'quel jour', 'quand'], "La Randon'Nuit a lieu le samedi 2 janvier 2027, à Rieutort-de-Randon, en Lozère."],
        [['ou se', 'ou est', 'ou a lieu', 'lieu', 'adresse', 'rieutort'], "La course se déroule à Rieutort-de-Randon, en Lozère, dans la Margeride."],
        [['frontale', 'lampe', 'nuit', 'materiel'], "Les deux trails se courent de nuit, à la frontale. Pour le matériel demandé, consultez le règlement sur la page d'inscription."],
        [['contact', 'mail', 'joindre', 'facebook'], "Vous pouvez écrire au club par le formulaire de son site, ou passer par sa page Facebook : lestraileursdurandon."],
        [['bonjour', 'salut', 'hello'], "Bonjour ! Posez-moi votre question sur la Randon'Nuit."]
    ],
)

for c in (chierry, randon):
    if len(sys.argv) < 2 or sys.argv[1] in c['dir']:
        build(c)
