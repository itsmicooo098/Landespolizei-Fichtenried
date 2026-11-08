from pathlib import Path
v='login-permission-20261108d'
def sub(f,a,b,n=1):
 p=Path(f);s=p.read_text();assert s.count(a)==n,(f,a,s.count(a));p.write_text(s.replace(a,b))
sub('site/assets/spark.js',"async function protect(force=false){if(!appCheck)return null;return getToken(appCheck,force)}","async function protect(force=false,required=false){if(!appCheck){if(required)throw Error('CAPTCHA-Schutz fehlt');return null}try{return await getToken(appCheck,force)}catch(e){console.warn('App Check:',e?.code||e?.message);if(required)throw e;return null}}")
sub('site/assets/spark.js','await protect(true)}','await protect(true,true)}')
sub('site/leitung/assets/app.js','../../assets/spark.js?v=staff-sync-20261107a',f'../../assets/spark.js?v={v}',2)
sub('site/leitung/assets/app.js',"catch(e){showLogin('Anmeldung nicht möglich. Bitte Zugangsdaten und Berechtigung prüfen.');console.error('Login:',e.code||e.message)}","catch(e){const c=e?.code||'';showLogin(c?`Anmeldung fehlgeschlagen (${c}).`:'Anmeldung fehlgeschlagen. Bitte erneut versuchen.');console.error('Login:',c||e?.message)}")
for f,a,b,n in [
 ('site/leitung/login-guard.js','./assets/app.js?v=staff-sync-20261107a',f'./assets/app.js?v={v}',1),
 ('site/leitung/index.html','assets/app.css?v=staff-sync-20261107a',f'assets/app.css?v={v}',1),
 ('site/leitung/index.html','assets/features.css?v=staff-sync-20261107a',f'assets/features.css?v={v}',1),
 ('site/leitung/index.html','login-guard.js?v=staff-sync-20261107a',f'login-guard.js?v={v}',1),
 ('site/assets/firebase-client.js','./spark.js?v=staff-directory-20261108a',f'./spark.js?v={v}',1),
 ('site/index.html','assets/firebase-client.js?v=staff-directory-20261108a',f'assets/firebase-client.js?v={v}',1)]: sub(f,a,b,n)

# Keep non-critical public-directory synchronization from blocking staff sign-in.
sub('site/leitung/assets/app.js',
 "  if(access.personnel){try{await callFunction('syncPublicDirectory')}catch(syncError){console.warn('Personalverzeichnis konnte nicht abgeglichen werden:',syncError.code||syncError.message)}}\n  $('#password').value='';await log('login','','Dienstkonto angemeldet');showWorkspace(user.user.displayName||username);await loadData();$('#loginMessage').textContent='';}",
 "  $('#password').value='';showWorkspace(user.user.displayName||username);await loadData();try{await log('login','','Dienstkonto angemeldet')}catch(auditError){if(auditError?.code!=='permission-denied')throw auditError;console.warn('Login konnte nicht protokolliert werden:',auditError.code);toast('Anmeldung aktiv; Firebase blockiert derzeit den Protokolleintrag.')}$('#loginMessage').textContent='';}")
sub('site/leitung/assets/app.js',
 "   if(access.personnel){try{await callFunction('syncPublicDirectory')}catch(syncError){console.warn('Personalverzeichnis konnte nicht abgeglichen werden:',syncError.code||syncError.message)}}\n   await log('login','','Sitzung wiederhergestellt');showWorkspace(user.displayName||user.email?.split('@')[0]);await loadData();}",
 "   showWorkspace(user.displayName||user.email?.split('@')[0]);await loadData();try{await log('login','','Sitzung wiederhergestellt')}catch(auditError){if(auditError?.code!=='permission-denied')throw auditError;console.warn('Sitzung konnte nicht protokolliert werden:',auditError.code);toast('Sitzung aktiv; Firebase blockiert derzeit den Protokolleintrag.')}}")
sub('site/assets/spark.js',
 " if(name==='audit'){const b=f.writeBatch(db);audit(b,p.action,p.targetId||'',p.detail||'');await b.commit();return {success:true};}",
 " if(name==='audit'){const b=f.writeBatch(db);audit(b,p.action,p.targetId||'',p.detail||'');try{await b.commit();return {success:true};}catch(error){if(error?.code==='permission-denied'&&['login','view_requests'].includes(p.action)){console.warn('Nicht-kritischer Sitzungs-/Ansichtsprotokolleintrag wurde von Firestore abgewiesen:',p.action);return {success:false};}throw error;}}")
sub('site/leitung/assets/app.js',
 "  try{const token={claims:await spark.role()};\n   access=capabilities(token.claims);if(!(access.personnel||access.cases)){showLogin();return}\n   showWorkspace(user.displayName||user.email?.split('@')[0]);await loadData();try{await log('login','','Sitzung wiederhergestellt')}catch(auditError){if(auditError?.code!=='permission-denied')throw auditError;console.warn('Sitzung konnte nicht protokolliert werden:',auditError.code);toast('Sitzung aktiv; Firebase blockiert derzeit den Protokolleintrag.')}}\n  catch(err){console.error('Session:',err.code||err.message);showLogin('Verbindung fehlgeschlagen. Bitte neu anmelden.')}",
 "  let stage='Dienstkonto laden';try{const token={claims:await spark.role()};\n   stage='Berechtigungen prüfen';access=capabilities(token.claims);if(!(access.personnel||access.cases)){showLogin();return}\n   stage='Vorgänge laden';showWorkspace(user.displayName||user.email?.split('@')[0]);await loadData();stage='Anmeldung protokollieren';try{await log('login','','Sitzung wiederhergestellt')}catch(auditError){if(auditError?.code!=='permission-denied')throw auditError;console.warn('Sitzung konnte nicht protokolliert werden:',auditError.code);toast('Sitzung aktiv; Firebase blockiert derzeit den Protokolleintrag.')}}\n  catch(err){console.error('Session ('+stage+'):',err.code||err.message);showLogin('Verbindung bei „'+stage+'“ fehlgeschlagen ('+(err?.code||'Fehler')+').')}" )
sub('site/assets/spark.js',
 "if(!(a.personnel&&a.cases))c.push(a.personnel?f.where('serviceId','==','bewerbung'):f.where('serviceId','in',CASE_SERVICES));c.push(f.orderBy('submittedAt','desc'),f.limit(300));const s=await f.getDocs(f.query(f.collection(db,'requests'),...c));let internal=[];if(a.cases){const q=await f.getDocs(f.query(f.collection(db,'internalCases'),f.orderBy('submittedAt','desc'),f.limit(200)));internal=q.docs.map(x=>({...dto(x),internal:true}));}const records=[...s.docs.map(dto),...internal].sort((x,y)=>new Date(y.submittedAt||0)-new Date(x.submittedAt||0));await call('audit',{action:'view_requests',detail:`Vorgangsübersicht geladen · ${records.length} sichtbare Vorgänge, davon ${internal.length} interne · Anzeigegrenze 300 reguläre / 200 interne`});return {records,limit:500};}",
 "c.push(f.where('serviceId','in',a.personnel&&a.cases?[...CASE_SERVICES,'bewerbung']:a.personnel?['bewerbung']:CASE_SERVICES));c.push(f.orderBy('submittedAt','desc'),f.limit(300));const s=await f.getDocs(f.query(f.collection(db,'requests'),...c));let internal=[],internalUnavailable=false;if(a.cases){try{const q=await f.getDocs(f.query(f.collection(db,'internalCases'),f.orderBy('submittedAt','desc'),f.limit(200)));internal=q.docs.map(x=>({...dto(x),internal:true}));}catch(e){if(e?.code!=='permission-denied')throw e;internalUnavailable=true;console.warn('Interne Vorgänge konnten nicht geladen werden:',e.code)}}const records=[...s.docs.map(dto),...internal].sort((x,y)=>new Date(y.submittedAt||0)-new Date(x.submittedAt||0));await call('audit',{action:'view_requests',detail:`Vorgangsübersicht geladen · ${records.length} sichtbare Vorgänge, davon ${internal.length} interne · Anzeigegrenze 300 reguläre / 200 interne`});return {records,limit:500,internalUnavailable};}")
sub('site/leitung/assets/app.js',
 "const result=await callFunction('listRequests');records=result.records||[];updateMetrics();renderRows()}",
 "const result=await callFunction('listRequests');records=result.records||[];updateMetrics();renderRows();if(result.internalUnavailable)toast('Interne Vorgänge wurden von Firebase nicht freigegeben.')}")

# Remove public personnel profiles and every client-side sync/write path.
import re
v='no-public-personnel-20261108e'
for f in ['site/leitung/assets/app.js','site/leitung/login-guard.js','site/leitung/index.html','site/assets/firebase-client.js','site/index.html']:
 p=Path(f);s=p.read_text();s=s.replace('login-permission-20261108d',v).replace('login-permission-20261108b',v);p.write_text(s)

def rx(f, pattern, replacement, n=1):
 p=Path(f);s=p.read_text();s2,count=re.subn(pattern,replacement,s,count=n,flags=re.S)
 assert count==n,(f,pattern,count)
 p.write_text(s2)

# No public staff cards, details, or profile modal remain in the citizen site.
rx('site/index.html',r'<section class="section people" id="leitung">.*?</section>','')
rx('site/index.html',r'<div class="profile-backdrop" id="profileModal".*?</div></div>','')
s=Path('site/index.html').read_text().replace('<a href="#leitung">Personal</a>','').replace('<a href="#leitung">Personal</a>','')
Path('site/index.html').write_text(s)
rx('site/assets/app.js',r'const people=\[.*?\];\nconst \$=', 'const $=')
sub('site/assets/app.js','let currentService=null,previousFocus=null,personFocus=null,activePeople=\'alle\',activeReceipt=null,activeSubmission=null,toastTimer,draftTimer,formOpenedAt=0,publicProfiles=[],stopPublicProfiles=null;','let currentService=null,previousFocus=null,activeReceipt=null,activeSubmission=null,toastTimer,draftTimer,formOpenedAt=0;')
rx('site/assets/app.js',r'const nameInitials=.*?function rankBadge', 'function rankBadge')
rx('site/assets/app.js',r'function renderPeople\(\).*?function fieldControl', 'function fieldControl')
sub('site/assets/app.js','renderRanks(\'hoeher\');renderPeople();renderRecent();','renderRanks(\'hoeher\');renderRecent();')
rx('site/assets/app.js',r'waitCloud\(\)\.then\(async cloud=>\{stopPublicProfiles\?\.\(\);.*?\}\)\.catch\(\(\)=>\{\}\);','')
rx('site/assets/app.js',r'document\.querySelectorAll\(\'\[data-person-filter\]\'\).*?\}\);document\.addEventListener\(\'click\'', 'document.addEventListener(\'click\'')
sub('site/assets/app.js',"$('#profileClose').onclick=closeProfile;",'')
sub('site/assets/app.js',"$('#profileModal').onclick=e=>{if(e.target===$('#profileModal'))closeProfile()};",'')
sub('site/assets/app.js',"if(!$('#profileModal').hidden)closeProfile();else if(!$('#serviceModal').hidden)closeService()","if(!$('#serviceModal').hidden)closeService()")
sub('site/assets/app.js',"const modal=!$('#profileModal').hidden?$('#profileModal'):!$('#serviceModal').hidden?$('#serviceModal'):null","const modal=!$('#serviceModal').hidden?$('#serviceModal'):null")
sub('site/assets/firebase-client.js',',publicProfiles:spark.publicProfiles,watchPublicProfiles:spark.watchPublicProfiles','')
sub('site/assets/spark.js',"export async function publicProfiles(){await protect();const s=await f.getDocs(f.query(f.collection(db,'publicProfiles'),f.limit(100)));return s.docs.map(dto);}\nexport function watchPublicProfiles(onRows,onError){let active=true,stop=()=>{};protect().then(()=>{if(active)stop=f.onSnapshot(f.query(f.collection(db,'publicProfiles'),f.limit(100)),s=>onRows(s.docs.map(dto)),onError)}).catch(onError);return()=>{active=false;stop()};}\n",'')
rx('site/assets/spark.js',r'async function syncPublicProfiles\(staffRows\).*?\n(?=export async function call)', '')
rx('site/assets/spark.js',r" if\(name==='syncPublicDirectory'\).*?\n",'')
sub('site/assets/spark.js',"await syncPublicProfiles(rows);",'')
# Staff account management must only update private staff records.
rx('site/assets/spark.js',r"const profileRef=ref\('publicProfiles',p\.uid\),oldProfile=await f\.getDoc\(profileRef\),d=oldProfile\.exists\(\)\?oldProfile\.data\(\):\{\};b\.set\(profileRef,\{.*?\}\);",'')
rx('site/assets/spark.js',r"const profileRef=ref\('publicProfiles',p\.uid\),oldProfile=await f\.getDoc\(profileRef\),d=oldProfile\.exists\(\)\?oldProfile\.data\(\):\{\};b\.set\(profileRef,\{.*?\}\);",'')
sub('site/assets/spark.js',"b.set(ref('publicProfiles',user.uid),{displayName,profileKey:username,badge,rank,phone:'',motto:'',description:'',active:true,updatedAt:now(),auditId:aid});",'')
rx('site/assets/spark.js',r" if\(name==='getPublicProfile'\).*?\n",'')
rx('site/assets/spark.js',r" if\(name==='savePublicProfile'\).*?\n",'')
# Remove the public-profile editor while retaining password settings.
rx('site/leitung/index.html',r'<div id="accountOverlay".*?<hr><form id="passwordSettingsForm">','<div id="accountOverlay" class="drawer-backdrop" hidden><section class="drawer account-drawer" role="dialog" aria-modal="true" aria-labelledby="accountTitle"><div class="drawer-head"><div><div class="overline">PERSÖNLICHE EINSTELLUNGEN</div><h2 id="accountTitle">Eigenes Dienstkonto</h2></div><button id="accountClose" class="circle-button" type="button" aria-label="Kontoeinstellungen schließen">×</button></div><div class="drawer-scroll"><p>Hier kannst du das Passwort deines Dienstkontos ändern.</p><form id="passwordSettingsForm">')
rx('site/leitung/assets/app.js',r'async function openAccountSettings\(\).*?\nfunction closeAccountSettings',"function openAccountSettings(){const overlay=$('#accountOverlay');overlay.hidden=false;document.body.style.overflow='';$('#currentPassword').focus()}\nfunction closeAccountSettings")
rx('site/leitung/assets/app.js',r'async function saveProfileSettings\(e\).*?\n(?=async function changeAccountPassword)', '')
sub('site/leitung/assets/app.js',"$('#profileSettingsForm').addEventListener('submit',saveProfileSettings);",'')

# Keep the repository rules aligned with the live change: old public profiles are inaccessible.
rx('backend/firestore.rules',r'  match /publicProfiles/\{uid\} \{[\s\S]*?\n  \}', '  match /publicProfiles/{uid} {\n   allow read, write: if false;\n  }')
rx('tests/rules.test.mjs',r"test\('Inactive staff accounts remain in the public people directory'.*?(?=function addAudit)", """test('Public personnel profile collection is closed',async()=>{
 await env.withSecurityRulesDisabled(async c=>{await setDoc(doc(c.firestore(),'publicProfiles','stored'),{displayName:'Stored profile',profileKey:'stored',phone:'',motto:'',description:'',active:true,updatedAt:new Date()});});
 await assertFails(getDoc(doc(db('citizen'),'publicProfiles','stored')));
 await assertFails(getDocs(collection(db('citizen'),'publicProfiles')));
 const d=db('boss'),b=writeBatch(d),aid=addAudit(b,'boss','update_public_profile','','Profile collection is closed');
 b.set(doc(d,'publicProfiles','new-profile'),{displayName:'Hidden profile',profileKey:'hidden',badge:'',rank:'',phone:'',motto:'',description:'',active:true,updatedAt:serverTimestamp(),auditId:aid});
 await assertFails(b.commit());
});
""")

# Match the citizen chat to the leadership chat layout and improve the small-screen controls.
rx('site/assets/app.js',r'function citizenChat\(container,id,accessCode\)\{.*?\nfunction renderStatusTimeline', """function citizenChat(container,id,accessCode){const shell=el('section','citizen-chat'),toggle=el('button','btn btn-outline','Mit der Dienststelle schreiben');toggle.type='button';const panel=el('div','citizen-chat-panel');panel.hidden=true;const heading=el('h3','citizen-chat-title','Vorgangschat'),intro=el('p','citizen-chat-intro','Nachrichten zwischen Ihnen und der zuständigen Dienststelle.');const toolbar=el('div','citizen-chat-toolbar'),refresh=el('button','btn btn-outline citizen-chat-refresh','Nachrichten aktualisieren');refresh.type='button';toolbar.append(refresh);const list=el('div','chat-feed');list.setAttribute('aria-live','polite');const form=el('form','citizen-chat-form'),label=el('label','citizen-chat-label','NACHRICHT AN DIE DIENSTSTELLE'),input=el('textarea');input.required=true;input.maxLength=1200;input.rows=4;input.placeholder='Nachricht an die Dienststelle …';const send=el('button','btn btn-outline','Nachricht senden');send.type='submit';const state=el('p','chat-state');form.append(label,input,send,state);panel.append(heading,intro,toolbar,list,form);shell.append(toggle,panel);let cloud=null;const render=rows=>{list.replaceChildren();for(const m of rows){const item=el('article','chat-message '+(m.sender==='Bürger'?'chat-own':'chat-staff'));item.append(el('strong','',m.sender==='Bürger'?'Sie':(m.senderName||'Landespolizei Fichtenried')),el('p','',m.body),el('small','',m.createdAt?new Date(m.createdAt).toLocaleString('de-DE'):'Gerade eben'));list.append(item)}if(!rows.length)list.append(el('p','chat-empty','Noch keine Nachrichten.'))};const reload=async()=>{try{cloud=cloud||await waitCloud();const rows=await cloud.citizenMessages({id,accessCode});render(rows);state.textContent='Nachrichten aktuell.'}catch(e){state.textContent=e.message||'Nachrichten konnten nicht geladen werden.'}};refresh.onclick=()=>reload();toggle.onclick=async()=>{panel.hidden=!panel.hidden;toggle.textContent=panel.hidden?'Mit der Dienststelle schreiben':'Vorgangschat schließen';if(panel.hidden){stopCitizenChat?.();stopCitizenChat=null;return}cloud=cloud||await waitCloud();await reload();stopCitizenChat?.();stopCitizenChat=cloud.watchCaseChat({id,accessCode},render,e=>{state.textContent=(e.message||'Live-Aktualisierung unterbrochen.')+' Bitte „Nachrichten aktualisieren“ wählen.'});input.focus()};form.onsubmit=async e=>{e.preventDefault();send.disabled=true;state.textContent='Nachricht wird gesendet …';try{cloud=cloud||await waitCloud();await cloud.sendCitizenMessage({id,accessCode,body:input.value});input.value='';await reload();state.textContent='Nachricht gesendet. Neue Antworten erscheinen hier automatisch.'}catch(err){state.textContent=err.message||'Nachricht konnte nicht gesendet werden.'}finally{send.disabled=false}};container.append(shell)}
function renderStatusTimeline""")
css='''\n/* Citizen case chat: polished, readable cards matching the leadership portal. */\n.citizen-chat{margin-top:18px}.citizen-chat>button{width:100%}.citizen-chat-panel{margin-top:12px;padding:18px;background:var(--bg);border:1px solid var(--line);border-radius:7px}.citizen-chat-title{margin:0;color:var(--heading);font:800 17px/1.35 Manrope,system-ui,sans-serif}.citizen-chat-intro{margin:7px 0 13px;color:var(--muted);font-size:11px;line-height:1.65}.citizen-chat-toolbar{display:flex;justify-content:flex-end}.citizen-chat-refresh{min-height:38px;padding:9px 13px;font-size:11px}.citizen-chat .chat-feed{max-height:340px;margin:12px 0 18px;padding:2px}.citizen-chat .chat-message{padding:12px 14px;border-radius:5px;background:var(--surface)}.citizen-chat .chat-message strong{font:800 11px Manrope,system-ui,sans-serif;color:var(--heading)}.citizen-chat .chat-message p{margin:7px 0;font-size:12px;line-height:1.65;white-space:pre-wrap}.citizen-chat .chat-message small{font-size:9px;color:var(--muted)}.citizen-chat-label{display:block;margin:0 0 8px;color:var(--muted);font:800 9px Manrope,system-ui,sans-serif;letter-spacing:.1em}.citizen-chat textarea{display:block;width:100%;min-height:112px;padding:12px 13px;background:var(--surface);border:1px solid var(--line);border-radius:5px;color:var(--text);font:400 13px/1.6 'DM Sans',system-ui,sans-serif;resize:vertical}.citizen-chat textarea:focus{outline:0;border-color:var(--gold);box-shadow:0 0 0 2px #dbba6626}.citizen-chat-form{display:grid;gap:9px}.citizen-chat-form .btn{justify-self:start;min-height:42px;padding:10px 15px;font-size:11px}.citizen-chat .chat-state{min-height:18px;margin:0;font-size:10px;line-height:1.5}.citizen-chat .chat-empty{margin:8px 0;color:var(--muted);font-size:11px}\n@media(max-width:620px){.citizen-chat-panel{padding:14px}.citizen-chat-toolbar{justify-content:stretch}.citizen-chat-refresh{width:100%}.citizen-chat .chat-feed{max-height:300px}.citizen-chat textarea{min-height:100px}.citizen-chat-form .btn{width:100%;justify-self:stretch}}\n'''
p=Path('site/assets/styles.css');s=p.read_text();p.write_text(s+'\n'+css)
# Bust browser caches for the citizen chat code and stylesheet.
p=Path('site/index.html');s=p.read_text()
for old in ['assets/styles.css?v=ux-polish-20261104a','assets/app.js?v=staff-directory-20261108a','assets/app.js?v=abholbereit-20261107']:
 s=s.replace(old,'assets/styles.css?v=chat-ui-20261108f' if old.startswith('assets/styles.css') else 'assets/app.js?v=chat-ui-20261108f')
p.write_text(s)
