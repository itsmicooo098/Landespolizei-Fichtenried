# Landespolizei Fichtenried

Zwei RP-Websites unter einer kostenlosen GitHub-Pages-Veröffentlichung:
- Bürgerseite: `/`
- Leitungsportal: `/leitung/`

Firebase-Projekt: `landespolizei-fichtenried`, Tarif Spark. Keine Cloud Functions und kein Abrechnungskonto erforderlich.

## Sicherheit
Die Datenzugriffe werden durch `backend/firestore.rules` geprüft. Dienstrollen liegen in `staff/{Firebase-UID}` und können ausschließlich über administrative Projektzugriffe vergeben werden. Browsernutzer können sich keine Rollen selbst geben.

Antragsinhalte sind ausschließlich für die freigeschaltete Leitung lesbar. Die Statusabfrage verwendet einen zufälligen 128-Bit-Zugangscode und liefert nur Vorgangsnummer, Dienstleistung und Status. Keine Liste dieser Statusdokumente ist öffentlich lesbar. Jeder Inhaber der Vorgangsnummer samt Code kann den Status abfragen; Codes vertraulich behandeln.

Schreibvorgänge sind pro Firebase-UID auf einen pro Minute begrenzt. Anonyme Konten verhindern keinen gezielten Missbrauch durch neu angelegte Identitäten. Der kostenlose Spark-Tarif beendet Zugriffe beim Erreichen seiner Kontingente; es wird kein kostenpflichtiger Tarif aktiviert.

## Dienstkonten
Firebase Authentication: E-Mail/Passwort aktivieren, Konten mit individuellen Passwörtern anlegen. Für Benutzernamen verwendet das Portal `BENUTZERNAME@login.fichtenried.example.com`; alternativ ist eine echte E-Mail-Adresse möglich.

Für jede genehmigte Firebase-UID in der Firebase-Konsole ein Dokument `staff/{UID}` mit folgenden Feldern anlegen:

```json
{"admin": true, "role": "leitung", "level": "hoeher"}
```

Erwartete RP-Dienstkonten aus dem ursprünglichen Paket: ralf.schmitz, sven.schilling, felix.stahl, tom.schneider, mathis.lehmann, vincent.krobbe, matteo.ryker. Keine Passwörter oder privaten Schlüssel in dieses Repository eintragen.

## Discord, ausschließlich kostenlos
Der Workflow `.github/workflows/discord.yml` prüft ungefähr alle 15 Minuten neue Benachrichtigungen. GitHub kann die Läufe verzögern oder bei längerer Repository-Inaktivität deaktivieren. Nach einem Versandfehler sind doppelte Meldungen möglich. Dies ist kein Echtzeitdienst.

Ein separates Firebase-Auth-Konto erhält ausschließlich ein `staff/{UID}`-Dokument mit `role: notifier` und hat keinen Zugriff auf Bewerbungsinhalte. Hinterlege in GitHub Actions:
- Variable `FIREBASE_API_KEY` mit dem öffentlichen Firebase-Webschlüssel.
- Secrets `FIREBASE_NOTIFIER_EMAIL`, `FIREBASE_NOTIFIER_PASSWORD`, `DISCORD_WEBHOOK_URL`.

Im Leitungsportal Discord aktivieren und Kategorien wählen. Nur Vorgangsnummer und Kategorie werden übertragen. Der Workflow läuft ausschließlich in öffentlichen Repositories auf kostenlosen Standard-Runnern. Keine größeren kostenpflichtigen Runner einsetzen.

## Veröffentlichung und Tests
Pages-Quelle in GitHub auf GitHub Actions stellen. Der Pages-Workflow prüft die Firestore-Zugriffsregeln im Emulator und veröffentlicht ausschließlich `site/`, wenn die Tests erfolgreich sind. Binärdateien können im Repository als `.b64` gespeichert werden; der Build stellt sie vor der Veröffentlichung wieder her.

Lokal: Node 22, Java 21, `npm install` und `npm test`. Die Firebase-Konsole muss dieselben Regeln aus `backend/firestore.rules` verwenden. Nur die Regeln zu veröffentlichen erfordert kein Tarifupgrade.

## Grenzen
- Dashboard zeigt maximal 300 aktuelle Vorgänge.
- Kein echter Behördenbetrieb, keine realen Notrufe, Ausweisdokumente oder sensiblen Echtfälle.
- Technische Auth-Adressen haben kein Postfach; Passwortwechsel erfolgt administrativ. Für eigenständige Wiederherstellung echte E-Mail-Adressen verwenden.
- Dienstrollen und Discord-Secrets erst nach Eigentümerfreigabe einrichten.
