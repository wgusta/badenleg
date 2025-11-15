# SendGrid Setup für BadenLEG

## Warum SendGrid?

- **Kostenlos**: 100 E-Mails pro Tag im Free Plan
- **Zuverlässig**: Professioneller E-Mail-Service mit hoher Zustellrate
- **Einfach**: API-Integration in wenigen Minuten

---

## Schritt 1: SendGrid Account erstellen

1. Gehe zu https://signup.sendgrid.com/
2. Klicke auf "Start for Free"
3. Fülle das Formular aus:
   - **Email**: Deine echte E-Mail
   - **Password**: Sicheres Passwort
   - **Company**: z.B. "BadenLEG" oder "Sihl Icon Valley"
   - **Website**: https://www.badenleg.ch

4. Bestätige deine E-Mail-Adresse

---

## Schritt 2: Sender Authentication (Domain Verification)

**Option A: Single Sender Verification (Schnell, empfohlen für Start)**

1. SendGrid Dashboard → **Settings** → **Sender Authentication**
2. Klicke auf **"Verify a Single Sender"**
3. Fülle das Formular aus:
   - **From Name**: BadenLEG
   - **From Email Address**: `noreply@badenleg.ch` (oder deine bevorzugte)
   - **Reply To**: `hallo@badenleg.ch`
   - **Company Address**: Deine Firmenadresse
4. Klicke "Create"
5. **Wichtig**: Du erhältst eine Bestätigungs-E-Mail → **Klicke den Link!**
6. Nach Bestätigung ist `noreply@badenleg.ch` verifiziert

**Option B: Domain Authentication (Professionell, optional)**

Für bessere Zustellraten, aber benötigt DNS-Zugriff:
1. SendGrid Dashboard → Settings → Sender Authentication
2. "Authenticate Your Domain"
3. Wähle DNS-Host: "Other Host (Not Listed)"
4. Domain: `badenleg.ch`
5. SendGrid zeigt DNS-Records → Trage sie in Infomaniak DNS ein
6. Warte auf Verification (kann 24-48h dauern)

---

## Schritt 3: API Key erstellen

1. SendGrid Dashboard → **Settings** → **API Keys**
2. Klicke **"Create API Key"**
3. Einstellungen:
   - **API Key Name**: `badenleg-production`
   - **API Key Permissions**: **Full Access** (oder "Restricted Access" mit Mail Send aktiviert)
4. Klicke "Create & View"
5. **WICHTIG**: Kopiere den API Key sofort – er wird nur einmal angezeigt!
   ```
   Beispiel: SG.xxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyy
   ```

---

## Schritt 4: API Key in Railway hinzufügen

1. Railway Dashboard → dein Projekt → **Variables**
2. Füge hinzu:
   ```
   SENDGRID_API_KEY=SG.xxxxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyy
   FROM_EMAIL=noreply@badenleg.ch
   ```
3. Klicke "Add" für jede Variable

**⚠️ Wichtig**: `FROM_EMAIL` muss die gleiche Adresse sein, die du in Schritt 2 verifiziert hast!

---

## Schritt 5: Deployment testen

1. Push zu `main`:
   ```bash
   git commit --allow-empty -m "Trigger deployment with SendGrid"
   git push origin main
   ```

2. Warte 1-2 Minuten auf Deployment

3. Teste E-Mail-Versand:
   - Gehe zu https://www.badenleg.ch/
   - Trage eine Adresse ein
   - Registriere dich mit deiner E-Mail
   - **Du solltest innerhalb von 1-2 Minuten eine E-Mail erhalten!**

4. Prüfe SendGrid Activity:
   - SendGrid Dashboard → **Activity**
   - Hier siehst du alle gesendeten E-Mails mit Status

---

## Troubleshooting

### E-Mails kommen nicht an

**1. Prüfe Railway Logs:**
```
Railway Dashboard → Deployments → Deploy Logs
```

Suche nach:
- `[EMAIL] Verifizierung gesendet an xxx (Status: 202)` ✅ = E-Mail versendet
- `[EMAIL] Fehler beim Senden` ❌ = Fehler

**2. Prüfe SendGrid Activity:**
```
SendGrid Dashboard → Activity
```
- **Processed**: E-Mail wurde angenommen
- **Delivered**: E-Mail wurde zugestellt
- **Bounce**: E-Mail konnte nicht zugestellt werden
- **Dropped**: E-Mail wurde abgelehnt (z.B. ungültige From-Adresse)

**3. Häufige Fehler:**

| Fehler | Lösung |
|--------|--------|
| `401 Unauthorized` | API Key falsch → Prüfe Railway Variables |
| `403 Forbidden` | Sender nicht verifiziert → Schritt 2 wiederholen |
| E-Mail im Spam | Domain Authentication aktivieren (Option B) |
| `The from address does not match a verified Sender Identity` | FROM_EMAIL muss in SendGrid verifiziert sein |

### E-Mails landen im Spam

1. **Domain Authentication aktivieren** (Schritt 2, Option B)
2. Prüfe SPF/DKIM Records in Infomaniak DNS
3. Verwende professionelle E-Mail-Texte (kein "Test", keine Großbuchstaben)

### SendGrid Free Limit erreicht

- Free Plan: **100 E-Mails pro Tag**
- Pro Plan: **40.000 E-Mails pro Monat** für $19.95
- Upgrade: SendGrid Dashboard → Billing

---

## Wichtige SendGrid Links

- **Dashboard**: https://app.sendgrid.com/
- **API Keys**: https://app.sendgrid.com/settings/api_keys
- **Sender Authentication**: https://app.sendgrid.com/settings/sender_auth
- **Activity Feed**: https://app.sendgrid.com/email_activity
- **Documentation**: https://docs.sendgrid.com/

---

## Überwachung

**Täglich prüfen:**
1. SendGrid Activity → Bounce/Drop Rate unter 5%
2. Railway Logs → Keine E-Mail-Fehler

**Wöchentlich prüfen:**
1. SendGrid Statistics → Open Rate, Click Rate
2. E-Mail-Limit: Wie viele der 100 Daily Emails wurden genutzt?

---

## Nächste Schritte nach Setup

✅ SendGrid Account erstellt  
✅ Sender verifiziert  
✅ API Key erstellt  
✅ Railway Variables gesetzt  
✅ Deployment getestet  

**Jetzt bist du bereit!** 🚀

Registrierungen auf BadenLEG senden jetzt echte E-Mails.

