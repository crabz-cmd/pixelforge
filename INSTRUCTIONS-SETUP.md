# ═══════════════════════════════════════════════════════════════
# PIXELFORGE — FORMULAIRE DE CONTACT
# INSTRUCTIONS DE CONFIGURATION ET DÉPLOIEMENT
# ═══════════════════════════════════════════════════════════════

## ✅ Ce qui a été créé

### Fichiers backend (Node.js)

1. **`server.js`** (nouveau) : Backend Express complet avec :
   - Resend API pour l'envoi d'emails
   - Google reCAPTCHA v3 (anti-spam)
   - Honeypot field (détection bots)
   - Rate limiting (5 requêtes/15 minutes)
   - Validation serveur robuste

2. **`package.json`** (nouveau) : Dépendances Node.js

3. **`.env.example`** (nouveau) : Template de configuration

4. **`email-template.html`** (nouveau) : Template d'email HTML

5. **`.gitignore`** (nouveau) : Fichiers à ignorer dans git

6. **`test.js`** (nouveau) : Tests automatisés

7. **`README-CONTACT.md`** (nouveau) : Documentation complète

### Fichiers frontend modifiés

8. **`index.html`** (modifié) :
   - ✅ Email corrigé : `hello@pixelforge.fr` → `hello@pixelforgelab.fr`
   - ✅ Script reCAPTCHA v3 ajouté
   - ✅ Honeypot field ajouté
   - ✅ Champ "Entreprise" (optionnel) ajouté
   - ✅ Backend pointe vers `http://localhost:3001/api/contact`
   - ✅ JavaScript amélioré avec gestion d'erreurs détaillée
   - ✅ Message de confirmation : "Merci pour votre message. Nous vous répondrons sous 24h."
   - ✅ Loader visuel pendant l'envoi

---

## 🚀 Instructions de configuration

### ÉTAPE 1 : Installer les dépendances

```bash
cd C:\Users\crabz\PixelForge2
npm install
```

### ÉTAPE 2 : Configurer reCAPTCHA v3

1. Allez sur https://www.google.com/recaptcha/admin
2. Cliquez sur "+"
3. Remplissez le formulaire :
   - **Label** : PixelForge Contact Form
   - **Type** : reCAPTCHA v3
   - **Domains** :
     - `localhost` (pour le dev)
     - `www.pixelforgelab.fr` (pour la prod)
   - **Owners** : votre email
4. Cliquez sur "Submit"
5. **Copiez la "Site Key"** → déjà dans `index.html` (ligne 11)
   ```
   6LcXyZspAAAAAKxXj8J8H8J8H8J8H8J8H8J8
   ```
6. **Copiez la "Secret Key"** → à ajouter dans `.env`

### ÉTAPE 3 : Configurer Resend API

1. Créez un compte sur https://resend.com
2. Vérifiez votre domaine :
   - Ajoutez les enregistrements DNS indiqués
   - SPF (Sender Policy Framework)
   - DKIM (DomainKeys Identified Mail)
   - DMARC (Domain-based Message Authentication, Reporting, and Conformance)
3. Obtenez votre **API Key**
4. Ajoutez la clé dans `.env`

### ÉTAPE 4 : Créer le fichier `.env`

```bash
cp .env.example .env
```

Éditez `.env` et ajoutez vos clés :

```env
PORT=3001
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
RECAPTCHA_SECRET_KEY=6LcXyZspAAAAAKxXj8J8H8H8J8H8J8H8J8
EMAIL_FROM=hello@pixelforgelab.fr
EMAIL_TO=hello@pixelforgelab.fr
```

⚠️ **IMPORTANT** : Ne jamais commiter `.env` dans git !

### ÉTAPE 5 : Tester localement

```bash
# Démarrer le backend
npm run dev
```

Le serveur démarre sur `http://localhost:3001`

Dans un autre terminal, démarrez le serveur frontend :

```bash
npx serve -p 3333 .
```

Ouvrez `http://localhost:3333` dans le navigateur et testez le formulaire.

---

## 🧪 Tests

### Tests automatisés

```bash
npm test
```

Cela exécute les tests dans `test.js` :
- ✅ Health check
- ✅ Validation champs manquants
- ✅ Validation email invalide
- ✅ Validation téléphone invalide
- ✅ Honeypot (détection bots)
- ✅ reCAPTCHA manquant

### Test manuel

1. Ouvrez le formulaire sur `http://localhost:3333`
2. Remplissez tous les champs obligatoires
3. Cliquez sur "Envoyer ma demande"
4. Vérifiez que :
   - Le bouton affiche "Envoi en cours…"
   - Le message de succès apparaît
   - L'email est reçu sur `hello@pixelforgelab.fr`

---

## 🌐 Déploiement en production

### Option A : Vercel (recommandé)

1. Installer Vercel CLI :
   ```bash
   npm install -g vercel
   ```

2. Déployer :
   ```bash
   vercel
   ```

3. Ajouter les variables d'environnement dans Vercel Dashboard :
   - `RESEND_API_KEY`
   - `RECAPTCHA_SECRET_KEY`
   - `EMAIL_FROM`
   - `EMAIL_TO`

4. Mettre à jour l'URL du backend dans `index.html` :
   ```
   http://localhost:3001/api/contact → https://votre-backend.vercel.app/api/contact
   ```

### Option B : Railway / Render / Heroku

Déployez le backend et mettez à jour l'URL dans `index.html`.

---

## 📧 Configuration DNS (Resend)

Pour que les emails ne soient pas marqués comme spam, configurez :

### SPF (Sender Policy Framework)

Ajoutez un enregistrement TXT à votre DNS :

```
v=spf1 include:resend.com ~all
```

### DKIM (DomainKeys Identified Mail)

Resend vous fournira un enregistrement DKIM à ajouter :

```
resend._domainkey IN TXT "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
```

### DMARC (Domain-based Message Authentication)

Ajoutez un enregistrement TXT :

```
v=DMARC1; p=none; rua=mailto:dmarc@pixelforgelab.fr
```

---

## 🔒 Sécurité

### Ce qui est en place :

- ✅ **Google reCAPTCHA v3** : Anti-bot invisible
- ✅ **Honeypot field** : Détection bots avancée
- ✅ **Rate limiting** : 5 requêtes/15 minutes par IP
- ✅ **Validation serveur** : Email, téléphone, champs obligatoires
- ✅ **Sanitization** : Échappement HTML/XSS
- ✅ **SPF/DKIM/DMARC** : Configuration email sécurisée

### Score reCAPTCHA

Le score actuel est **0.5** (entre 0 et 1) :
- 0.0 = Certainement un bot
- 0.5 = Ambigu
- 1.0 = Certainement humain

Pour plus de sécurité, augmentez à 0.7. Pour plus de facilité, diminuez à 0.3.

---

## 📊 Monitoring

### Logs du backend

Les soumissions sont loguées en console :

```
✅ Contact form submitted successfully in 1234ms
📧 Email sent to: jean.dupont@email.com (Jean Dupont)
```

### Surveillance (optionnel)

Ajoutez une solution de monitoring :
- Sentry (erreurs)
- Datadog (logs)
- Vercel Analytics (métriques)

---

## 🐛 Résolution de problèmes

### Problème : reCAPTCHA ne se charge pas

**Solution** :
1. Vérifiez que le script est bien dans le `<head>` de `index.html`
2. Vérifiez votre connexion internet
3. Essayez en mode incognito

### Problème : Email n'est pas reçu

**Solution** :
1. Vérifiez le dossier spam
2. Vérifiez que Resend API Key est correcte
3. Vérifiez que le domaine est vérifié sur Resend
4. Vérifiez les logs du backend

### Problème : Rate limiting trop strict

**Solution** :
Dans `server.js`, modifiez les valeurs :

```javascript
const contactFormLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // Augmenter à 30 minutes
  max: 10, // Augmenter à 10 requêtes
  // ...
});
```

---

## 📞 Support

En cas de problème :

- Email : `hello@pixelforgelab.fr`
- Docs : `README-CONTACT.md`
- Tests : `test.js`

---

## ✅ Checklist de mise en production

- [ ] Installer les dépendances (`npm install`)
- [ ] Configurer `.env` avec les vraies clés API
- [ ] Configurer reCAPTCHA v3 sur Google
- [ ] Configurer Resend API et vérifier le domaine
- [ ] Configurer DNS (SPF, DKIM, DMARC)
- [ ] Tester le formulaire localement
- [ ] Mettre à jour l'URL du backend dans `index.html`
- [ ] Déployer le backend sur Vercel/Railway/Render
- [ ] Tester le formulaire en production
- [ ] Vérifier que les emails sont bien reçus
- [ ] Surveiller les logs pendant les premiers jours

---

**Version** : 1.0.0
**Date** : 2026-03-26
**Auteur** : PixelForge
