from pathlib import Path
v='login-permission-20261108b'
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
