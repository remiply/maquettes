"""Chatbot de démonstration façon Challenge du Montcalm, réutilisable dans n'importe quelle mise en page.

Usage dans un script de site :
    from chatbot import block
    css, html, js = block(dict(acc='#AB438E', acc1='#C45AA6', acc2='#6E2259', ink='#231F20', bg='#FBF6FA',
                               rgb='171,67,142', ini='AVPR', font='var(--f)', bottom=24,
                               tz='Une question ?', small='Club', title='Course', ph='Posez votre question…',
                               hello='<p>…</p>', fallback='…', Q=[[label, question]], R=[[[mots-clés], réponse]]))
Les mots-clés de R sont en minuscules et sans accents ; la première règle qui correspond gagne.
"""
import json


def block(c):
    b = c.get('bottom', 24)
    css = '''
/* assistant (démo) : même présentation que l'assistant EventLyx du Challenge du Montcalm */
.cb{position:fixed;right:max(2vw,16px);bottom:%(b)spx;z-index:28;width:64px;height:64px;border:0;border-radius:50%%;background:%(acc)s;color:#fff;cursor:pointer;display:grid;place-items:center;box-shadow:0 8px 24px rgba(%(rgb)s,.45);transition:transform .15s}
.cb:hover{transform:scale(1.06)}
.cb svg{width:30px;height:30px;grid-area:1/1}
.cb .ix{display:none}.cb.on .ic{display:none}.cb.on .ix{display:block}
.tz{position:fixed;right:max(2vw,16px);bottom:%(b76)spx;z-index:27;width:264px;background:#fff;color:%(ink)s;border-radius:14px 14px 4px 14px;box-shadow:0 8px 26px rgba(0,0,0,.18);padding:12px 34px 12px 14px;font:14.5px/1.35 %(font)s;cursor:pointer;display:none}
.tz.on{display:block}
.tz b{display:block;font-weight:800}
.tz span{opacity:.72;font-size:13.5px}
.tz button{position:absolute;top:2px;right:2px;width:32px;height:32px;border:0;background:none;font-size:18px;line-height:1;cursor:pointer;color:inherit;opacity:.6;border-radius:50%%}
.tz button:hover{opacity:1}
.cw{position:fixed;right:max(2vw,16px);bottom:%(b76)spx;z-index:28;width:min(390px,calc(100vw - 32px));height:min(640px,calc(100vh - %(b129)spx));background:%(bg)s;color:%(ink)s;border-radius:22px;box-shadow:0 18px 50px rgba(0,0,0,.3);display:none;flex-direction:column;overflow:hidden;font-family:%(font)s}
.cw.on{display:flex}
.cw header{position:relative;flex:none;background:linear-gradient(135deg,%(acc1)s,%(acc)s 55%%,%(acc2)s);color:#fff;padding:16px 16px 30px;display:flex;align-items:center;gap:12px;clip-path:polygon(0 0,100%% 0,100%% 82%%,95%% 92%%,90%% 84%%,84%% 96%%,78%% 86%%,71%% 95%%,64%% 83%%,57%% 94%%,50%% 85%%,43%% 97%%,36%% 86%%,29%% 94%%,22%% 84%%,15%% 96%%,8%% 87%%,0 95%%)}
.cw header div{flex:1}
.cw header small{display:block;font-size:11.5px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;opacity:.9}
.cw header b{display:block;font-size:20px;font-weight:800;font-style:italic;line-height:1.1}
.cw header em{font-style:normal;font-size:13px;display:flex;align-items:center;gap:6px;margin-top:3px}
.cw header em::before{content:"";width:9px;height:9px;border-radius:50%%;background:#3DDC84;box-shadow:0 0 0 2px rgba(255,255,255,.35)}
.cw header button{appearance:none;flex:none;width:36px;height:36px;border:0;border-radius:10px;background:rgba(255,255,255,.2);color:#fff;cursor:pointer;display:grid;place-items:center}
.cw header button:hover{background:rgba(255,255,255,.34)}
.cw header button svg{width:18px;height:18px}
.cw .av{width:46px;height:46px;border-radius:50%%;border:2px solid #fff;flex:none;display:grid;place-items:center;background:#fff;color:%(acc)s;font-weight:900;font-size:%(avfs)spx;letter-spacing:-.02em}
.msgs{flex:1;overflow-y:auto;padding:4px 14px 12px;display:flex;flex-direction:column;gap:10px}
.day{align-self:center;font-size:12.5px;opacity:.6;margin:4px 0 6px}
.msg{max-width:82%%;padding:11px 14px;border-radius:16px;font-size:15px;line-height:1.42}
.msg.a{background:#fff;align-self:flex-start;border-bottom-left-radius:4px;box-shadow:0 1px 0 rgba(0,0,0,.08),0 0 0 1px rgba(0,0,0,.06);margin-left:34px;position:relative}
.msg.a::before{content:%(inij)s;position:absolute;left:-34px;bottom:0;width:26px;height:26px;border-radius:50%%;background:%(acc)s;color:#fff;font:900 %(inifs)spx/26px %(font)s;text-align:center}
.msg.a strong{color:%(acc)s;font-weight:800}
.msg.a p{margin:0}.msg.a p+p{margin-top:.8em}
.msg.a a{color:%(acc)s}
.msg.u{background:%(acc)s;color:#fff;align-self:flex-end;border-bottom-right-radius:4px}
.typing{display:flex;gap:5px;align-items:center;min-height:42px}
.typing i{width:7px;height:7px;border-radius:50%%;background:%(acc)s;opacity:.35;animation:tp 1s infinite}
.typing i:nth-child(2){animation-delay:.15s}.typing i:nth-child(3){animation-delay:.3s}
@keyframes tp{30%%{opacity:1;transform:translateY(-3px)}}
.chips{flex:none;display:flex;gap:8px;padding:4px 14px 10px;overflow-x:auto;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chips button{appearance:none;flex:none;border:1px solid rgba(%(rgb)s,.35);background:#fff;color:%(acc)s;font:700 13.5px/1.2 %(font)s;padding:9px 14px;border-radius:999px;cursor:pointer;white-space:nowrap}
.chips button:hover{background:%(acc)s;color:#fff}
.cw form{flex:none;display:flex;align-items:center;gap:6px;margin:0 12px;padding:5px 5px 5px 16px;background:#fff;border:2px solid %(acc)s;border-radius:999px}
.cw input{flex:1;min-width:0;min-height:40px;border:0;outline:0;background:none;font:16px %(font)s;color:%(ink)s}
.cw form:focus-within{box-shadow:0 0 0 3px rgba(%(rgb)s,.25)}
.cw form button{flex:none;width:40px;height:40px;border:0;border-radius:50%%;background:%(acc)s;color:#fff;cursor:pointer;display:grid;place-items:center}
.cw form button svg{width:18px;height:18px}
.cw .note{flex:none;margin:0;padding:8px 16px 12px;text-align:center;font-size:11.5px;line-height:1.4;opacity:.7}
@media(max-width:760px){.cw{left:8px;right:8px;top:68px;bottom:%(b)spx;width:auto;height:auto}.cb.on{display:none}.tz{bottom:%(b72)spx}}
@media(prefers-reduced-motion:reduce){.typing i{animation:none}}
''' % dict(c, b=b, b76=b + 76, b72=b + 72, b129=b + 129, inij=json.dumps(c['ini']),
           avfs=15 if len(c['ini']) <= 3 else 12, inifs=10 if len(c['ini']) <= 3 else 8)
    html = '''
<div class="tz" id="tz"><b>%(tz)s</b><span>Réponse en quelques secondes</span><button type="button" id="tzX" aria-label="Masquer ce message">×</button></div>
<button class="cb" id="chatB" type="button" aria-expanded="false" aria-controls="chat" aria-label="Ouvrir l'assistant">
 <svg class="ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3C6.5 3 2 6.8 2 11.5c0 2.6 1.4 4.9 3.6 6.5-.2 1.2-.8 2.4-1.7 3.4 2 0 3.8-.7 5.2-1.8.9.2 1.9.4 2.9.4 5.5 0 10-3.8 10-8.5S17.5 3 12 3zM7.5 13a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm4.5 0a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm4.5 0a1.5 1.5 0 110-3 1.5 1.5 0 010 3z"/></svg>
 <svg class="ix" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>
</button>
<section class="cw" id="chat" role="dialog" aria-label="Assistant">
 <header>
  <div class="av" aria-hidden="true">%(ini)s</div>
  <div><small>%(small)s</small><b>%(title)s</b><em>Assistant de démonstration</em></div>
  <button type="button" id="chatR" aria-label="Recommencer la conversation"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12a8 8 0 108-8 8 8 0 00-6 2.7"/><path d="M4 4v4h4"/></svg></button>
  <button type="button" id="chatX" aria-label="Réduire l'assistant"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button>
 </header>
 <div class="msgs" id="msgs" aria-live="polite"></div>
 <div class="chips" id="chips"></div>
 <form id="chatF"><input id="chatI" type="text" autocomplete="off" placeholder="%(ph)s" aria-label="Votre question"><button type="submit" aria-label="Envoyer"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3 20.5l19-8.5L3 3.5v6.5l12 2-12 2z"/></svg></button></form>
 <p class="note">Démonstration EventLyx : réponses tirées des informations de cette page.</p>
</section>
''' % c
    js = '''<script>
{
 const R=%(R)s;
 const Q=%(Q)s;
 const $=id=>document.getElementById(id),box=$('chat'),msgs=$('msgs'),btn=$('chatB'),tz=$('tz');
 const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const norm=t=>t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
 const el=(c,t)=>{const d=document.createElement('div');d.className=c;if(t)d.textContent=t;msgs.appendChild(d);msgs.scrollTop=msgs.scrollHeight;return d};
 const add=(t,c)=>el('msg '+c,t.replace(/(\\d) (h|km|m|€)/g,'$1\\u00a0$2').replace(/h (\\d\\d)/g,'h\\u00a0$1'));
 const reply=q=>{const n=norm(q);const r=R.find(x=>x[0].some(k=>n.includes(k)));return r?r[1]:%(fallback)s};
 const ask=q=>{q=q.trim();if(!q)return;add(q,'u');
  if(still){add(reply(q),'a');return}
  const t=el('msg a typing');t.innerHTML='<i></i><i></i><i></i>';setTimeout(()=>{t.remove();add(reply(q),'a')},700)};
 const hello=()=>{msgs.innerHTML='';el('day',"Aujourd'hui");const m=el('msg a');
  m.innerHTML=%(hello)s;
  $('chips').innerHTML='';Q.forEach(q=>{const b=document.createElement('button');b.type='button';b.textContent=q[0];b.addEventListener('click',()=>ask(q[1]));$('chips').appendChild(b)})};
 let started=false;
 const open=on=>{box.classList.toggle('on',on);btn.classList.toggle('on',on);btn.setAttribute('aria-expanded',on);
  btn.setAttribute('aria-label',on?"Fermer l'assistant":"Ouvrir l'assistant");tz.classList.remove('on');
  if(on&&!started){started=true;hello()}
  if(on)$('chatI').focus()};
 btn.addEventListener('click',()=>open(!box.classList.contains('on')));
 $('chatX').addEventListener('click',()=>{open(false);btn.focus()});
 $('chatR').addEventListener('click',()=>{hello();$('chatI').focus()});
 tz.addEventListener('click',()=>open(true));
 $('tzX').addEventListener('click',e=>{e.stopPropagation();tz.classList.remove('on')});
 setTimeout(()=>{if(!started)tz.classList.add('on')},2500);
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&box.classList.contains('on')){open(false);btn.focus()}});
 $('chatF').addEventListener('submit',e=>{e.preventDefault();const i=$('chatI');ask(i.value);i.value=''});
}
</script>''' % dict(R=json.dumps(c['R'], ensure_ascii=False), Q=json.dumps(c['Q'], ensure_ascii=False),
                    fallback=json.dumps(c['fallback'], ensure_ascii=False), hello=json.dumps(c['hello'], ensure_ascii=False))
    return css, html, js
