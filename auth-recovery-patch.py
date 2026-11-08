from pathlib import Path
v='auth-recovery-20261108a'
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
