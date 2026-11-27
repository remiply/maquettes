"""Maquette COHM (Club Olympique de la Haute Moselotte) : un seul site pour les 6 rendez-vous.
Mise en page propre : calendrier de saison en tête, une couleur par rendez-vous (les 6 pastilles du logo),
bleu ciel / blanc / bande noire du maillot. Usage : python3 _gabarit/sites/cohm.py"""
import os, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from chatbot import block

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'cohm', 'index.html')
SITE = 'https://www.couriraveclecohm.com/'
THM_SIGN = 'https://in.sporkrono-inscriptions.fr/trail-hivernal-de-la-moselotte-2027'

# Les 6 rendez-vous, dans l'ordre de la saison. col = pastille du logo ; txt = couleur du texte posé dessus.
EV = [
    dict(id='cross', nm='Cross du COHM', sub='Cross Super U', col='#ED8A20', txt='#1B181A', d='6', m='déc.', y='2026', mo=0,
         jour='Dimanche 6 décembre 2026', lieu='Base de loisirs, Saulxures-sur-Moselotte', court='500 m à 9 km, de l\'éveil athlé à la course des as',
         st='Engagements par les clubs', stc='clubs', go='#cross'),
    dict(id='thm', nm='THM', sub='Trail Hivernal de la Moselotte', col='#167991', txt='#fff', d='21', m='févr.', y='2027', mo=2,
         jour='Dimanche 21 février 2027', lieu='Gymnase de Cornimont', court='14, 28 et 38 km, dans la neige des hauteurs',
         st='Inscriptions ouvertes', stc='ok', go='#thm'),
    dict(id='chamois', nm='Trail des Chamois', sub='Trophée Philippe Bragard', col='#994A1A', txt='#fff', d='13', m='juin', y='2027', mo=6,
         jour='Dimanche 13 juin 2027', lieu='Saulxures-sur-Moselotte', court='23 km et 12 km, plus deux courses jeunes',
         st='Inscriptions bientôt', stc='wait', go='#chamois'),
    dict(id='foulees', nm='Foulées Bressaudes', sub='En nocturne à La Bresse', col='#7B1B61', txt='#fff', d='17', m='juil.', y='2027', mo=7,
         jour='Samedi 17 juillet 2027', lieu='Place du Champtel, La Bresse', court='Course des as, course populaire et courses jeunes, le soir',
         st='Inscriptions bientôt', stc='wait', go='#foulees'),
    dict(id='rainkopf', nm='Rainkopf Trail', sub='Au pied des pistes du Hohneck', col='#545420', txt='#fff', d='5', m='sept.', y='2027', mo=9,
         jour='Dimanche 5 septembre 2027', lieu='Station La Bresse Hohneck', court='40 km, 25 km et 11 km sur les crêtes',
         st='Inscriptions bientôt', stc='wait', go='#rainkopf'),
    dict(id='marche', nm='Marche populaire de Vagney', sub='Marche internationale des Chamois', col='#9F0729', txt='#fff', d='?', m='', y='2027', mo=None,
         jour='Date 2027 pas encore annoncée', lieu='Salle polyvalente, Vagney', court='5, 10 et 20 km, à son rythme',
         st='Date à venir', stc='wait', go='#marche'),
]
MOIS = ['Déc.', 'Janv.', 'Févr.', 'Mars', 'Avril', 'Mai', 'Juin', 'Juil.', 'Août', 'Sept.']

chat_css, chat_html, chat_js = block(dict(
    acc='#0E6F9E', acc1='#3FA3D1', acc2='#0B4F72', ink='#1B181A', bg='#F2F9FD', rgb='14,111,158',
    ini='COHM', font="'Source Sans 3',system-ui,sans-serif", bottom=24,
    tz='Une question sur nos courses ?', small='Club Olympique de la Haute Moselotte', title='Les courses du COHM',
    ph='Posez votre question…',
    hello="<p>Bonjour ! 👋 Je suis l'assistant du <strong>COHM</strong>.</p><p>Cross, THM, Trail des Chamois, Foulées Bressaudes, Rainkopf, Marche de Vagney : dates, distances, inscriptions… posez-moi votre question !</p>",
    fallback="Je n'ai pas cette information. Sur le site en ligne, je transmets la question aux bénévoles du club. En attendant, vous pouvez écrire à cohm@laposte.net.",
    Q=[["📅 Prochaine course", "Quelle est la prochaine course ?"], ["❄️ THM", "C'est quoi le THM ?"], ["🐐 Chamois", "Quand a lieu le Trail des Chamois ?"],
       ["🌙 Foulées", "C'est quand les Foulées Bressaudes ?"], ["⛰️ Rainkopf", "Quelles distances au Rainkopf ?"], ["🥾 Marche", "Et la marche de Vagney ?"]],
    R=[
        [['prochain', 'bientot', 'calendrier', 'saison'], "Le prochain rendez-vous est le Cross du COHM (Cross Super U), le dimanche 6 décembre 2026 à la base de loisirs de Saulxures-sur-Moselotte. Ensuite : THM le 21 février 2027, Trail des Chamois le 13 juin, Foulées Bressaudes le 17 juillet et Rainkopf Trail le 5 septembre 2027."],
        [['tarif', 'prix', 'cout', 'combien', '€'], "THM : 35 € (38 km), 25 € (28 km), 14 € (14 km) en ligne, un peu plus sur place. Trail des Chamois : 23 € (23 km) et 12 € (12 km) en ligne. Les tarifs des autres courses 2027 ne sont pas encore publiés."],
        [['ligue', 'cancer'], "Une partie de la recette du THM est reversée à la Ligue contre le cancer."],
        [['repas'], "Au THM, un repas chaud à 15 € est servi dès 11 h 30, sur réservation jusqu'au 17 février. Au Rainkopf (édition 2026), le repas était à 15 €, de 12 h à 15 h 30."],
        [['douche', 'vestiaire'], "Au THM, vestiaires et douches sont au gymnase de Cornimont."],
        [['utmb', 'index', 'itra'], "Le Grand THM et le THM comptent pour les UTMB World Series (règlement 2027). Au Rainkopf, en 2026, le 40 km avait l'index UTMB 50K et le 25 km l'index 20K."],
        [['grand thm', '38'], "Le Grand THM : 38 km et 1 800 m de dénivelé, départ à 8 h 00 du gymnase de Cornimont, le dimanche 21 février 2027. 35 € en ligne, 39 € sur place."],
        [['mini thm', 'thm 14', '14 km'], "Le Mini THM : 14 km et 700 m de dénivelé, départ à 10 h 00. Ouvert aux juniors et plus. 14 € en ligne, 17 € sur place."],
        [['thm', 'hivernal', 'cornimont', 'neige', 'fevrier'], "Le THM (Trail Hivernal de la Moselotte) a lieu le dimanche 21 février 2027 au gymnase de Cornimont : 38 km (8 h 00), 28 km (9 h 00) et 14 km (10 h 00). Inscriptions ouvertes sur Sporkrono, 1 500 places au total."],
        [['cross', 'super u', 'decembre', 'lac'], "Le Cross du COHM (Cross Super U) a lieu le dimanche 6 décembre 2026 à la base de loisirs de Saulxures-sur-Moselotte. Il sert de support aux Championnats des Vosges de cross. Il est réservé aux licenciés FFA, engagés par leur club sur cva.athle.fr avant le 3 décembre à 23 h 59."],
        [['chamois', 'bragard', 'juin', 'mini trail'], "Le Trail des Chamois (Trophée Philippe Bragard) a lieu le dimanche 13 juin 2027 à Saulxures-sur-Moselotte : trail de 23 km (840 m D+) à 9 h 00, mini trail de 12 km (420 m D+) à 10 h 00, et deux courses jeunes. Les inscriptions ne sont pas encore ouvertes."],
        [['foulee', 'bressaude', 'champtel', 'nocturne', 'juillet'], "Les Foulées Bressaudes se courent le soir, place du Champtel à La Bresse. Prochaine édition le samedi 17 juillet 2027. En 2026, la course des as partait à 21 h 00 et la course populaire à 20 h 30."],
        [['rainkopf', 'hohneck', 'champis', 'septembre', '40 km'], "Le Rainkopf Trail aura lieu le dimanche 5 septembre 2027 à la station La Bresse Hohneck. En 2026 : Rainkopf Trail 40 km (1 800 m D+), Trail Nature 25 km (925 m D+) et Tour des Champis 11 km (358 m D+)."],
        [['marche', 'vagney', 'randonn', 'marcher'], "La Marche populaire de Vagney propose des parcours de 5, 10 et 20 km, sans difficulté particulière. L'édition 2026 a été annulée, et la date 2027 n'est pas encore annoncée. Contact : D. Vernier, 07 86 87 98 38."],
        [['enfant', 'jeune', 'poussin', 'eveil', 'kid'], "Il y a des courses jeunes au Cross (de 500 m à 4 500 m selon l'âge), au Trail des Chamois (500 m à 11 h 30, 1 km à 11 h 45, gratuites) et aux Foulées Bressaudes."],
        [['pps', 'certificat', 'licence', 'medical'], "Pour le THM, la licence FFA ou le PPS est obligatoire. Le Cross est réservé aux licenciés FFA. Pour le Rainkopf 2026, il fallait la licence FFA 2026/27 ou un PPS."],
        [['inscri', 'dossard'], "THM : inscriptions ouvertes sur Sporkrono, jusqu'au samedi 20 février à 12 h. Cross : engagements par les clubs sur cva.athle.fr. Trail des Chamois, Foulées et Rainkopf : inscriptions pas encore ouvertes pour 2027."],
        [['contact', 'mail', 'telephone', 'joindre', 'appeler'], "Vous pouvez écrire à cohm@laposte.net. Pour le THM : Hervé Claudel, 06 75 46 63 20. Pour le Cross : 03 29 24 11 61."],
        [['club', 'cohm', 'licen', 'adherer'], "Le COHM, c'est le Club Olympique de la Haute Moselotte. Les recettes de ses courses aident les déplacements des athlètes, surtout des plus jeunes, et le matériel d'entraînement."],
        [['bonjour', 'salut', 'hello', 'coucou'], "Bonjour ! Posez-moi votre question sur l'une des courses du COHM."],
    ]))

CSS = r'''
:root{color-scheme:light;--ciel:#A9E1FA;--cield:#0E6F9E;--glace:#F2F9FD;--noir:#1B181A;--gris:#5C6670;--ligne:rgba(27,24,26,.12);--f:'Source Sans 3',system-ui,sans-serif;--ft:'Montserrat',system-ui,sans-serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:#fff;color:var(--noir);font:18px/1.55 var(--f)}
img{max-width:100%;height:auto;display:block}
a{color:inherit}
.w{max-width:1200px;margin:0 auto;padding:0 32px}
h1,h2,h3{font-family:var(--ft);letter-spacing:-.02em;line-height:1.05;margin:0}
.maq{background:var(--noir);color:#fff;font-size:13px;padding:7px 16px;display:flex;gap:14px;justify-content:space-between;flex-wrap:wrap}
.maq a{color:var(--ciel)}
/* en-tête */
.top{background:#fff;border-bottom:1px solid var(--ligne);position:sticky;top:0;z-index:15}
.top .w{display:flex;align-items:center;gap:24px;min-height:72px}
.logo{display:flex;align-items:center;gap:12px;text-decoration:none}
.logo b{background:var(--noir);color:#fff;font:900 22px/1 var(--ft);padding:8px 12px 7px;letter-spacing:.02em}
.logo span{font:700 15px/1.15 var(--ft);color:var(--noir)}
.logo span small{display:block;font:400 13px/1.3 var(--f);color:var(--gris)}
.top ul{list-style:none;margin:0 0 0 auto;padding:0;display:flex;gap:26px}
.top ul a{text-decoration:none;font-weight:600;font-size:16px}
.top ul a:hover{color:var(--cield)}
.pts{display:flex;gap:6px;align-items:center}
.pts i{width:10px;height:10px;border-radius:50%;display:block}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;padding:0 22px;border-radius:999px;background:var(--cield);color:#fff;text-decoration:none;font:700 16px/1 var(--ft);border:0;transition:filter .15s,transform .15s}
.btn:hover{filter:brightness(1.1)}
.btn.noir{background:var(--noir)}
.btn.blanc{background:#fff;color:var(--noir)}
.btn.ligne{background:transparent;color:inherit;box-shadow:inset 0 0 0 2px currentColor}
/* hero */
.hero{background:var(--ciel);position:relative;overflow:hidden}
.hero .w{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0;min-height:560px;padding-right:0}
.hero .tx{padding:64px 48px 56px 0;display:flex;flex-direction:column;justify-content:center}
.hero .kicker{font:700 14px/1.3 var(--ft);letter-spacing:.12em;text-transform:uppercase;margin:0 0 16px;display:flex;gap:12px;align-items:center}
.hero h1{font-weight:900;font-size:clamp(42px,5.4vw,76px)}
.hero h1 .bande{display:inline-block;background:var(--noir);color:#fff;padding:0 .18em;margin-top:.08em}
.hero .lead{font-size:20px;margin:22px 0 28px;max-width:30em}
.next{background:#fff;border-radius:18px;padding:18px 20px;display:flex;gap:18px;align-items:center;flex-wrap:wrap;box-shadow:0 10px 30px rgba(14,111,158,.15);max-width:560px}
.next .cal{width:66px;flex:none;text-align:center;border-radius:12px;overflow:hidden;border:2px solid #ED8A20}
.next .cal b{display:block;font:900 30px/1.1 var(--ft);padding-top:6px}
.next .cal span{display:block;background:#ED8A20;color:var(--noir);font:800 12px/1.9 var(--ft);text-transform:uppercase}
.next .inf{flex:1;min-width:200px}
.next .inf small{display:block;font:700 12px/1.3 var(--ft);letter-spacing:.1em;text-transform:uppercase;color:var(--gris)}
.next .inf strong{display:block;font:800 19px/1.2 var(--ft);margin:3px 0 2px}
.next .inf span{font-size:15.5px;color:var(--gris)}
.count{display:flex;gap:14px}
.count div{text-align:center;font-size:12.5px;color:var(--gris)}
.count b{display:block;font:900 26px/1 var(--ft);color:var(--noir)}
.hero .ph{background:url(hero.jpg) 62% center/cover no-repeat;min-height:100%;clip-path:polygon(9% 0,100% 0,100% 100%,0 100%)}
/* calendrier */
.cal-sec{padding:88px 0 96px;background:#fff}
.sec-h{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;margin-bottom:36px}
.sec-h h2{font-weight:900;font-size:clamp(36px,4.2vw,58px)}
.sec-h p{margin:0;color:var(--gris);max-width:34em}
.frise{position:relative;display:grid;grid-template-columns:repeat(10,minmax(0,1fr));border-top:3px solid var(--noir);margin-bottom:44px}
.frise .m{grid-row:1;padding:10px 0 0;font:700 13px/1 var(--ft);text-transform:uppercase;letter-spacing:.06em;color:var(--gris);border-left:1px solid var(--ligne);padding-left:8px;min-height:132px}
.frise .m:first-child{border-left:0;padding-left:0}
.frise a{grid-row:1;align-self:start;margin:38px 0 0 6px;display:flex;align-items:center;gap:8px;text-decoration:none;font:800 14px/1.15 var(--ft);padding:8px 12px 8px 8px;border-radius:999px;justify-self:start;white-space:nowrap;position:relative;z-index:1}
.frise a.l2{margin-top:84px}
.frise a i{width:24px;height:24px;border-radius:50%;background:#fff;display:grid;place-items:center;font:900 12px/1 var(--ft);color:var(--noir);flex:none}
.frise .y{position:absolute;top:-30px;font:800 13px/1 var(--ft);color:var(--noir);background:#fff;padding-right:8px}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.card{position:relative;display:flex;flex-direction:column;border-radius:20px;overflow:hidden;background:var(--glace);text-decoration:none;color:var(--noir);transition:transform .15s,box-shadow .15s;min-height:300px}
.card:hover{transform:translateY(-3px);box-shadow:0 14px 34px rgba(27,24,26,.12)}
.card .hd{padding:20px 22px 18px;display:flex;gap:16px;align-items:center}
.card .dt{font:900 46px/.9 var(--ft);letter-spacing:-.03em}
.card .dt small{display:block;font:800 14px/1.2 var(--ft);letter-spacing:.04em;text-transform:uppercase;margin-top:6px}
.card .hd .nm{font:800 20px/1.15 var(--ft)}
.card .hd .nm small{display:block;font:600 14px/1.3 var(--f);opacity:.85;margin-top:4px}
.card .bd{padding:18px 22px 22px;display:flex;flex-direction:column;gap:10px;flex:1}
.card .bd p{margin:0;font-size:16.5px}
.card .bd .l{color:var(--gris);font-size:15.5px}
.card .ft{margin-top:auto;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;padding-top:8px}
.st{font:700 13px/1 var(--ft);padding:7px 10px;border-radius:999px;background:#fff;white-space:nowrap}
.st.ok::before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:#2DB36B;margin-right:6px}
.st.wait::before,.st.clubs::before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:#C9CED3;margin-right:6px}
.st.clubs::before{background:#ED8A20}
.card .go{font:800 14px/1 var(--ft)}
/* fiches */
.ev{padding:88px 0;border-top:1px solid var(--ligne)}
.ev:nth-of-type(even){background:var(--glace)}
.ev .w{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:56px;align-items:start}
.ev .tag{display:inline-flex;align-items:center;gap:10px;font:800 13px/1 var(--ft);letter-spacing:.1em;text-transform:uppercase;padding:8px 14px;border-radius:999px;margin-bottom:18px}
.ev h2{font-weight:900;font-size:clamp(36px,4vw,56px)}
.ev .sous{font:700 18px/1.3 var(--ft);color:var(--gris);margin:8px 0 18px}
.ev .quand{font:800 22px/1.3 var(--ft);margin:0 0 4px}
.ev .ou{margin:0 0 18px;color:var(--gris)}
.ev .txt p{margin:0 0 12px}
.ev .act{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}
.tb{width:100%;border-collapse:collapse;font-size:16px;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 0 0 1px var(--ligne)}
.cap{font:800 14px/1.3 var(--ft);letter-spacing:.08em;text-transform:uppercase;color:var(--gris);margin:6px 0 10px}
.tb th{text-align:left;font:700 13px/1.2 var(--ft);text-transform:uppercase;letter-spacing:.05em;color:var(--gris);padding:12px 14px;border-bottom:1px solid var(--ligne);background:#fff}
.tb td{padding:12px 14px;border-bottom:1px solid var(--ligne);vertical-align:top}
.tb tr:last-child td{border-bottom:0}
.tb td.h{font:800 16px/1.3 var(--ft);white-space:nowrap}
.tb td b{font-family:var(--ft);font-weight:800}
.tb td small{display:block;color:var(--gris);font-size:14px}
.info{list-style:none;margin:20px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.info li{background:#fff;border-radius:14px;padding:14px 16px;font-size:15.5px;box-shadow:0 0 0 1px var(--ligne)}
.info li b{display:block;font:800 14px/1.3 var(--ft);margin-bottom:3px}
.note{font-size:14.5px;color:var(--gris);margin:14px 0 0}
.bandeph{height:clamp(260px,38vw,520px);background:#000 center/cover no-repeat}
/* club */
.club{background:var(--noir);color:#fff}
.club .w{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:64px;align-items:center;padding-top:88px;padding-bottom:88px}
.club img{border-radius:20px;aspect-ratio:4/5;object-fit:cover;width:100%}
.club h2{font-weight:900;font-size:clamp(36px,4vw,56px);margin-bottom:18px}
.club h2 span{color:var(--ciel)}
.club p{margin:0 0 14px;font-size:19px;opacity:.92}
.club ul{list-style:none;padding:0;margin:22px 0 28px;display:grid;gap:10px}
.club li{display:flex;gap:12px;align-items:baseline}
.club li i{width:10px;height:10px;border-radius:50%;flex:none;transform:translateY(-1px)}
.parts{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px}
.parts span{border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:8px 14px;font-weight:600;font-size:15px}
/* pied */
footer{background:#111;color:#fff;padding:64px 0 110px;font-size:16px}
footer .w{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px}
footer h3{font:800 18px/1.2 var(--ft);margin:0 0 14px;color:var(--ciel)}
footer p{margin:0 0 8px}
footer .small{font-size:13.5px;opacity:.7}
@media(max-width:1020px){
 .top ul{display:none}
 .hero .w{grid-template-columns:minmax(0,1fr);padding-right:32px}
 .hero .ph{min-height:340px;clip-path:none;margin:0 -32px;order:-1}
 .hero .tx{padding:40px 0 48px}
 .frise{display:none}
 .cards{grid-template-columns:repeat(2,minmax(0,1fr))}
 .ev .w,.club .w{grid-template-columns:minmax(0,1fr);gap:36px}
}
@media(max-width:760px){
 body{font-size:17px}
 .w{padding:0 18px}
 .top .w{min-height:62px}
 .logo span{display:none}
 .hero .w{padding-right:18px}
 .hero .ph{margin:0 -18px;min-height:260px;background-position:70% center}
 .hero .tx{padding:30px 0 40px}
 .hero .lead{font-size:18px}
 .next{padding:16px}
 .cards{grid-template-columns:minmax(0,1fr);gap:14px}
 .card{min-height:0}
 .card .dt{font-size:40px}
 .cal-sec,.ev{padding:60px 0}
 .info{grid-template-columns:minmax(0,1fr)}
 .tb{font-size:15px}
 .tb th,.tb td{padding:10px 10px}
 .tb .hide{display:none}
 .club .w{padding-top:60px;padding-bottom:60px}
 footer .w{grid-template-columns:minmax(0,1fr)}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
'''

e = html.escape
pts = ''.join('<i style="background:%s"></i>' % v['col'] for v in EV)

# frise (ordinateur) : années + mois + pastilles placées dans leur mois
frise = '<div class="frise" aria-hidden="true">'
frise += ''.join('<div class="m" style="grid-column:%d">%s</div>' % (k + 1, m) for k, m in enumerate(MOIS))
for k, v in enumerate(EV):
    if v['mo'] is None:
        continue
    frise += '<a class="l%d" href="#%s" style="grid-column:%d;background:%s;color:%s"><i>%s</i>%s</a>' % (k % 2 + 1, v['id'], v['mo'] + 1, v['col'], v['txt'], v['d'], e(v['nm']))
frise += '<span class="y" style="left:0">2026</span><span class="y" style="left:10%">2027</span></div>'

cards = ''
for v in EV:
    dt = '%s<small>%s %s</small>' % (v['d'], v['m'], v['y']) if v['mo'] is not None else '<span style="font-size:30px">%s</span><small>date à venir</small>' % v['y']
    cards += '''<a class="card" href="%(go)s"><div class="hd" style="background:%(col)s;color:%(txt)s"><span class="dt">%(dt)s</span><span class="nm">%(nm)s<small>%(sub)s</small></span></div>
 <div class="bd"><p>%(court)s</p><p class="l">%(jour)s · %(lieu)s</p><div class="ft"><span class="st %(stc)s">%(st)s</span><span class="go">Voir la fiche →</span></div></div></a>
''' % dict(v, dt=dt, nm=e(v['nm']))

def tag(v, label):
    return '<span class="tag" style="background:%s;color:%s">%s</span>' % (v['col'], v['txt'], label)

C = {v['id']: v for v in EV}

FICHES = f'''
<section class="ev" id="cross"><div class="w">
 <div class="txt">
  {tag(C['cross'], 'Rendez-vous 1 · Cross')}
  <h2>Cross du COHM</h2>
  <p class="sous">Cross Super U · Championnats des Vosges de cross</p>
  <p class="quand">Dimanche 6 décembre 2026</p>
  <p class="ou">Base de loisirs de Saulxures-sur-Moselotte, le long du lac</p>
  <p>Des boucles de 500 m à 2 km autour du lac, de l'éveil athlé jusqu'à la course des as. Primes de la course des as : 100, 60 et 40 €, chez les hommes comme chez les femmes. Chaque enfant des courses éveil et poussins est récompensé.</p>
  <ul class="info">
   <li><b>Qui peut courir ?</b>Les licenciés FFA, engagés par leur club sur cva.athle.fr avant le 3 décembre à 23 h 59.</li>
   <li><b>Sur place</b>Engagement possible jusqu'à 1 h avant le départ. Dossards à partir de 10 h 00.</li>
  </ul>
  <p class="note">Partenaires : Super U, Groupama, Weldom, Comité des Vosges d'Athlétisme. Renseignements : 03 29 24 11 61.</p>
 </div>
 <div><p class="cap">Programme des départs</p><table class="tb">
  <tr><th>Départ</th><th>Course</th><th>Distance</th></tr>
  <tr><td class="h">11 h 00 · 11 h 10</td><td>Éveils athlétiques M / F<small>Nés de 2018 à 2020</small></td><td><b>500 m</b></td></tr>
  <tr><td class="h">11 h 20 · 11 h 30</td><td>Poussins / Poussines<small>Nés en 2016 et 2017</small></td><td><b>1 000 m</b></td></tr>
  <tr><td class="h">11 h 40 · 11 h 42</td><td>Benjamins / Benjamines<small>Nés en 2014 et 2015</small></td><td><b>2 500 m</b></td></tr>
  <tr><td class="h">12 h 00 · 12 h 02</td><td>Minimes H / F<small>Nés en 2012 et 2013</small></td><td><b>3 500 m</b></td></tr>
  <tr><td class="h">12 h 35 · 12 h 37</td><td>Cross court H / F, cadettes<small>Cadettes nées en 2010 et 2011</small></td><td><b>4 000 m</b></td></tr>
  <tr><td class="h">13 h 15 · 13 h 17</td><td>Cadets, juniores F<small>Nés de 2008 à 2011</small></td><td><b>4 500 m</b></td></tr>
  <tr><td class="h">13 h 45 · 13 h 47</td><td>Juniors H, course des as F<small>Juniors 2008-2009, as nées en 2007 et avant</small></td><td><b>6 000 m</b></td></tr>
  <tr><td class="h">14 h 30</td><td>Course des as H<small>Nés en 2007 et avant</small></td><td><b>9 000 m</b></td></tr>
 </table></div>
</div></section>

<section class="ev" id="thm"><div class="w">
 <div class="txt">
  {tag(C['thm'], 'Rendez-vous 2 · Trail d’hiver')}
  <h2>THM</h2>
  <p class="sous">Trail Hivernal de la Moselotte · 15e édition</p>
  <p class="quand">Dimanche 21 février 2027</p>
  <p class="ou">Départ et arrivée au gymnase de Cornimont</p>
  <p>Une boucle sur les hauteurs de Cornimont, Basse-sur-le-Rupt et Saulxures-sur-Moselotte, entre 500 et 1 000 m d'altitude. Le Grand THM et le THM comptent pour les UTMB World Series. Une partie de la recette est reversée à la Ligue contre le cancer.</p>
  <ul class="info">
   <li><b>Inscriptions</b>En ligne jusqu'au samedi 20 février à 12 h. Sur place le samedi de 16 h à 19 h et le dimanche dès 7 h. 1 500 places en tout.</li>
   <li><b>Licence ou PPS</b>Licence FFA ou PPS obligatoire.</li>
   <li><b>Ravitaillements</b>Au lac de Saulxures et au col des Hayes. Barrière horaire au lac à 12 h 30.</li>
   <li><b>Après la course</b>Repas chaud à 15 €, sur réservation jusqu'au 17 février. Vestiaires et douches au gymnase.</li>
  </ul>
  <div class="act"><a class="btn" style="background:#167991" href="{THM_SIGN}">S'inscrire au THM</a></div>
  <p class="note">Renseignements : Hervé Claudel, 06 75 46 63 20. Hébergement limité : à prévoir à l'avance.</p>
 </div>
 <div><p class="cap">Les trois formats</p><table class="tb">
  <tr><th>Course</th><th>Départ</th><th class="hide">Public</th><th>En ligne / sur place</th></tr>
  <tr><td><b>Grand THM</b><small>38 km · 1 800 m D+</small></td><td class="h">8 h 00</td><td class="hide">Espoirs et plus</td><td><b>35 €</b> / 39 €</td></tr>
  <tr><td><b>THM</b><small>28 km · 1 400 m D+</small></td><td class="h">9 h 00</td><td class="hide">Espoirs et plus</td><td><b>25 €</b> / 29 €</td></tr>
  <tr><td><b>Mini THM</b><small>14 km · 700 m D+</small></td><td class="h">10 h 00</td><td class="hide">Juniors et plus</td><td><b>14 €</b> / 17 €</td></tr>
 </table></div>
</div></section>

<div class="bandeph" style="background-image:url(depart.jpg);background-position:center 35%" role="img" aria-label="Le départ du Rainkopf Trail, au pied des pistes de La Bresse Hohneck"></div>

<section class="ev" id="chamois"><div class="w">
 <div class="txt">
  {tag(C['chamois'], 'Rendez-vous 3 · Trail')}
  <h2>Trail des Chamois</h2>
  <p class="sous">Trophée Philippe Bragard, président fondateur du COHM</p>
  <p class="quand">Dimanche 13 juin 2027</p>
  <p class="ou">Saulxures-sur-Moselotte</p>
  <p>Le trophée Philippe Bragard revient au premier homme et à la première femme du 23 km. Repas et ravitaillement à l'arrivée, et un ravitaillement à mi-course sur le 23 km. Remise des prix à partir de 12 h 30.</p>
  <ul class="info">
   <li><b>Inscriptions</b>Pas encore ouvertes. Elles se feront sur chronometrage.com.</li>
   <li><b>Tarifs affichés sur le site</b>23 km : 23 € en ligne. Mini trail : 12 € en ligne. Un peu plus sur place.</li>
  </ul>
  <p class="note">Partenaires : Crédit Agricole, Super U, Groupama.</p>
 </div>
 <div><p class="cap">Les formats 2027</p><table class="tb">
  <tr><th>Course</th><th>Départ</th><th>Public</th></tr>
  <tr><td><b>Trail des Chamois</b><small>23 km · 840 m D+</small></td><td class="h">9 h 00</td><td>Espoirs et plus</td></tr>
  <tr><td><b>Mini trail</b><small>12 km · 420 m D+</small></td><td class="h">10 h 00</td><td>Cadets et plus</td></tr>
  <tr><td><b>Animation éveil athlé</b><small>500 m · gratuit</small></td><td class="h">11 h 30</td><td>Nés de 2018 à 2020</td></tr>
  <tr><td><b>Course poussins</b><small>1 km · gratuit</small></td><td class="h">11 h 45</td><td>Nés en 2016 et 2017</td></tr>
 </table></div>
</div></section>

<section class="ev" id="foulees"><div class="w">
 <div class="txt">
  {tag(C['foulees'], 'Rendez-vous 4 · Course en ville, de nuit')}
  <h2>Foulées Bressaudes</h2>
  <p class="sous">Avec La Bressaude section athlétisme</p>
  <p class="quand">Samedi 17 juillet 2027</p>
  <p class="ou">Place du Champtel, La Bresse · secrétariat à la Halle des Congrès</p>
  <p>Une soirée de courses dans La Bresse, des plus petits jusqu'à la course des as. La 27e édition a eu lieu le samedi 18 juillet 2026. Croix-Rouge sur place, restauration et buvette sur le parcours et à la Halle des Congrès.</p>
  <ul class="info">
   <li><b>Inscriptions 2027</b>Pas encore ouvertes. En 2026, elles se faisaient sur chronometrage.com.</li>
   <li><b>Sur place</b>En 2026 : retrait des dossards de 16 h 30 à 19 h 30, supplément de 4 € sur place.</li>
  </ul>
 </div>
 <div><p class="cap">Le programme de l'édition 2026</p><table class="tb">
  <tr><th>Départ</th><th>Course</th><th>Tarif</th></tr>
  <tr><td class="h">19 h 45</td><td><b>Animation baby</b><small>730 m · nés en 2017 et après</small></td><td>gratuit</td></tr>
  <tr><td class="h">20 h 00</td><td><b>Course 1, poussins</b><small>1 300 m · nés en 2015 et 2016</small></td><td>3 €</td></tr>
  <tr><td class="h">20 h 15</td><td><b>Course 2, benjamins-minimes</b><small>2 500 m · nés de 2011 à 2014</small></td><td>3 €</td></tr>
  <tr><td class="h">20 h 30</td><td><b>Course 3, populaire</b><small>3 600 m · nés en 2010 et avant</small></td><td>6 €</td></tr>
  <tr><td class="h">21 h 00</td><td><b>Course 4, des as</b><small>7 740 m · nés en 2010 et avant</small></td><td>11 €</td></tr>
 </table></div>
</div></section>

<section class="ev" id="rainkopf"><div class="w">
 <div class="txt">
  {tag(C['rainkopf'], 'Rendez-vous 5 · Trail de montagne')}
  <h2>Rainkopf Trail</h2>
  <p class="sous">Avec La Bressaude athlétisme · au pied des pistes</p>
  <p class="quand">Dimanche 5 septembre 2027</p>
  <p class="ou">Station La Bresse Hohneck, 88 route de Vologne, La Bresse</p>
  <p>Les crêtes des Hautes-Vosges, au départ de la station. La 16e édition a eu lieu le dimanche 20 septembre 2026. Ravitaillements sans gobelet, repas à l'arrivée et un cadeau pour chaque participant.</p>
  <ul class="info">
   <li><b>Inscriptions 2027</b>Pas encore ouvertes. En 2026, elles se faisaient sur chronometrage.com.</li>
   <li><b>Licence ou PPS</b>En 2026 : licence FFA ou PPS.</li>
  </ul>
 </div>
 <div><p class="cap">Les formats de l'édition 2026</p><table class="tb">
  <tr><th>Course</th><th>Départ</th><th>Licencié / non licencié</th></tr>
  <tr><td><b>Rainkopf Trail</b><small>40 km · 1 800 m D+ · index UTMB 50K</small></td><td class="h">8 h 00</td><td><b>40 €</b> / 42 €</td></tr>
  <tr><td><b>Trail Nature</b><small>25 km · 925 m D+ · index UTMB 20K</small></td><td class="h">9 h 30</td><td><b>25 €</b> / 27 €</td></tr>
  <tr><td><b>Tour des Champis</b><small>11 km · 358 m D+ · cadets et plus</small></td><td class="h">matin</td><td><b>12 €</b></td></tr>
 </table></div>
</div></section>

<div class="bandeph" style="background-image:url(crete.jpg);background-position:center 40%" role="img" aria-label="Un traileur avec ses bâtons sur les crêtes du Rainkopf, une vache vosgienne derrière lui"></div>

<section class="ev" id="marche"><div class="w">
 <div class="txt">
  {tag(C['marche'], 'Rendez-vous 6 · Marche')}
  <h2>Marche populaire de Vagney</h2>
  <p class="sous">Marche populaire internationale des Chamois · avec l'association Les Courtes Gueules</p>
  <p class="quand">Date 2027 pas encore annoncée</p>
  <p class="ou">Salle polyvalente, place de la Libération, Vagney</p>
  <p>Trois parcours sans difficulté particulière, à faire à son rythme. Boisson et collation gratuites aux contrôles, petite restauration aux contrôles 2 et 3, et repas à l'arrivée. L'édition prévue le 23 août 2026 a été annulée.</p>
  <ul class="info">
   <li><b>Participation</b>3 € sans souvenir, ou licence famille à 6 € (enfants jusqu'à 16 ans). Membre FFSP, tampons IVV.</li>
   <li><b>Groupes</b>Préinscription auprès du club. Individuels : sur place.</li>
  </ul>
  <p class="note">Contact : D. Vernier, 07 86 87 98 38, cohm@laposte.net.</p>
 </div>
 <div><p class="cap">Les parcours</p><table class="tb">
  <tr><th>Parcours</th><th>Dénivelé</th><th>Départs</th></tr>
  <tr><td><b>5 km</b></td><td>+10 m</td><td>De 7 h à 14 h</td></tr>
  <tr><td><b>10 km</b></td><td>+218 m</td><td>De 7 h à 14 h</td></tr>
  <tr><td><b>20 km</b></td><td>+676 m</td><td>De 7 h à 13 h</td></tr>
 </table></div>
</div></section>
'''

PAGE = f'''<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Courir avec le COHM : maquette de site par EventLyx</title>
<link rel="preload" as="image" href="hero.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Source+Sans+3:wght@400;600;700&display=swap">
<style>{CSS}{chat_css}</style></head><body>

<div class="maq"><span>Maquette de refonte réalisée par EventLyx pour le COHM. Ce n'est pas le site officiel.</span><a href="{SITE}">Site officiel du club</a></div>

<header class="top"><div class="w">
 <a class="logo" href="#haut"><b>COHM</b><span>Courir avec le COHM<small>Club Olympique de la Haute Moselotte</small></span></a>
 <ul><li><a href="#calendrier">Calendrier</a></li><li><a href="#thm">THM</a></li><li><a href="#chamois">Chamois</a></li><li><a href="#rainkopf">Rainkopf</a></li><li><a href="#club">Le club</a></li><li><a href="#contact">Contact</a></li></ul>
</div></header>

<section class="hero" id="haut"><div class="w">
 <div class="tx">
  <p class="kicker"><span class="pts">{pts}</span>Saison 2026 – 2027</p>
  <h1>Six rendez-vous <span class="bande">dans la Haute Moselotte</span></h1>
  <p class="lead">Du cross de décembre au trail des crêtes en septembre, en passant par une marche : toutes les courses du COHM au même endroit, avec leurs dates, leurs distances et leurs inscriptions.</p>
  <div class="next">
   <div class="cal"><b>6</b><span>déc.</span></div>
   <div class="inf"><small>Prochain rendez-vous</small><strong>Cross du COHM</strong><span>Dimanche · base de loisirs de Saulxures</span></div>
   <div class="count" aria-label="Temps restant avant le premier départ du cross"><div><b id="cj">–</b>jours</div><div><b id="ch">–</b>heures</div><div><b id="cm">–</b>min</div></div>
  </div>
 </div>
 <div class="ph" role="img" aria-label="Un coureur du COHM sur les crêtes, pendant le Rainkopf Trail"></div>
</div></section>

<section class="cal-sec" id="calendrier"><div class="w">
 <div class="sec-h"><h2>Le calendrier de la saison</h2><p>Chaque rendez-vous a sa couleur, reprise des pastilles du logo. Cliquez sur une course pour voir sa fiche.</p></div>
 {frise}
 <div class="cards">
{cards} </div>
</div></section>
{FICHES}
<section class="club" id="club"><div class="w">
 <img src="club.jpg" alt="Un athlète du COHM, maillot bleu ciel, au passage de la rivière du steeple" width="1047" height="1300" loading="lazy">
 <div>
  <h2>Le <span>COHM</span></h2>
  <p>Le Club Olympique de la Haute Moselotte organise ou co-organise six rendez-vous par saison, de Saulxures-sur-Moselotte à Cornimont, Vagney et La Bresse.</p>
  <p>Les recettes de ces manifestations contribuent aux déplacements des athlètes, notamment des plus jeunes, et au matériel d'entraînement.</p>
  <ul>{''.join('<li><i style="background:%s"></i><span><b>%s</b> · %s</span></li>' % (v['col'], e(v['nm']), v['jour']) for v in EV)}</ul>
  <p style="font-size:16px;opacity:.75;margin-bottom:10px">Partenaires de la saison</p>
  <div class="parts"><span>Groupama</span><span>Super U</span><span>TS Informatique</span></div>
 </div>
</div></section>

<footer id="contact"><div class="w">
 <div><h3>Nous joindre</h3><p><a href="mailto:cohm@laposte.net">cohm@laposte.net</a></p><p>Ou par le formulaire du <a href="{SITE}contact/">site du club</a>.</p></div>
 <div><h3>Par course</h3><p>THM : Hervé Claudel, <a href="tel:+33675466320">06 75 46 63 20</a></p><p>Cross : <a href="tel:+33329241161">03 29 24 11 61</a></p><p>Marche : D. Vernier, <a href="tel:+33786879838">07 86 87 98 38</a></p></div>
 <div><h3>À propos de cette page</h3><p class="small">Maquette proposée par EventLyx. Informations relevées le 27 novembre 2026 sur couriraveclecohm.com, ses affiches et ses règlements. Photos : galeries du Rainkopf Trail et du club, sur le site du COHM.</p></div>
</div></footer>
{chat_html}
<script>
{{
 const T=Date.parse('2026-12-06T11:00:00+01:00');
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
