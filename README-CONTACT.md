# ═══════════════════════════════════════════════════════════════
# PIXELFORGE — FORMULAIRE DE CONTACT
# ═══════════════════════════════════════════════════════════════

## 📋 Vue d'ensemble

Ce dossier contient le système complet de formulaire de contact pour PixelForge :

- **Backend Node.js** (`server.js`) : API Express avec Resend + anti-spam
- **Frontend** (`index.html`) : Formulaire modifié avec reCAPTCHA v3
- **Email Template** (`email-template.html`) : Design HTML pour les notifications
- **Configuration** (`.env.example`) : Variables d'environnement à configurer

---

## 🚀 Installation rapide

### 1. Installer les dépendances

```bash
npm install
```

### 2. Configurer les variables d'environnement

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et ajouter vos clés API
nano .env
```

Variables requises dans `.env` :

| Variable | Description | Exemple |
|----------|-------------|----------|
| `RESEND_API_KEY` | Clé API Resend pour l'envoi d'emails | `re_xxxxxxxxxxxxx` |
| `RECAPTCHA_SECRET_KEY` | Clé secrète reCAPTCHA v3 | `6LcXyZspAAAAAKxXj8J8H8J8H8J8H8J8H8J8` |
| `PORT` | Port du serveur backend (optionnel) | `3001` |

### 3. Configurer reCAPTCHA v3 (Google)

1. Allez sur [Google reCAPTCHA Admin](https://www.google.com/recaptcha/admin)
2. Créez un nouveau site reCAPTCHA **v3**
3. Configurez les domaines :
   - `www.pixelforgelab.fr` (production)
   - `localhost` (développement)
4. Copiez la **Site Key** → déjà dans `index.html`
5. Copiez la **Secret Key** → ajoutez dans `.env`

### 4. Configurer Resend API

1. Créez un compte sur [Resend.com](https://resend.com)
2. Vérifiez votre domaine `pixelforgelab.fr` (DNS SPF/DKIM)
3. Obtenez votre **API Key** → ajoutez dans `.env`

---

## 🎯 Démarrage

### Mode développement

```bash
npm run dev
```

Serveur lancé sur `http://localhost:3001`

### Mode production

```bash
npm start
```

---

## 📧 Endpoints API

### POST `/api/contact`

Envoie le formulaire de contact.

**Corps de la requête (JSON)** :

```json
{
  "prenom": "Jean",
  "nom": "Dupont",
  "email": "jean.dupont@email.com",
  "telephone": "+33 6 00 00 00 00",
  "entreprise": "Mon Entreprise",
  "type_projet": "Création de site vitrine",
  "message": "Je souhaite créer un site web...",
  "honeypot": "",
  "recaptchaToken": "03AHJ_Vu5...token..."
}
```

**Réponses** :

- **200 OK** : Email envoyé avec succès
  ```json
  {
    "success": true,
    "message": "Merci pour votre message. Nous vous répondrons sous 24h."
  }
  ```

- **400 Bad Request** : Erreur de validation
  ```json
  {
    "success": false,
    "error": "invalid_email",
    "message": "Veuillez entrer une adresse email valide."
  }
  ```

- **429 Too Many Requests** : Rate limiting dépassé
  ```json
  {
    "success": false,
    "error": "too_many_requests",
    "message": "Trop de tentatives. Réessayez dans 15 minutes."
  }
  ```

- **500 Internal Server Error** : Erreur serveur
  ```json
  {
    "success": false,
    "error": "server_error",
    "message": "Une erreur est survenue. Réessayez ou contactez-nous sur WhatsApp."
  }
  ```

### GET `/api/health`

Health check pour monitoring.

**Réponse** :

```json
{
  "status": "ok",
  "service": "pixelforge-contact-api",
  "timestamp": "2026-03-26T23:45:00.000Z"
}
```

---

## 🔒 Sécurité

### Anti-spam multi-couches

1. **Google reCAPTCHA v3** : Vérification invisible sans friction
2. **Honeypot field** : Champ invisible pour détecter les bots
3. **Rate limiting** : Maximum 5 formulaires par IP toutes les 15 minutes
4. **Validation serveur** : Validation stricte de tous les champs

### Protection des données

- Sanitization des entrées (échappement des balises HTML)
- Validation email et téléphone côté serveur
- Pas de stockage de données sensibles

---

## 📧 Email Template

Le template `email-template.html` utilise des placeholders qui sont remplis dynamiquement :

| Placeholder | Description |
|-------------|-------------|
| `{{NOM}}` | Nom du client |
| `{{PRENOM}}` | Prénom du client |
| `{{EMAIL}}` | Email du client |
| `{{TELEPHONE}}` | Numéro de téléphone |
| `{{ENTREPRISE}}` | Nom de l'entreprise |
| `{{TYPE_PROJET}}` | Type de projet demandé |
| `{{MESSAGE}}` | Message du client |
| `{{DATE}}` | Date et heure d'envoi |
| `{{IP}}` | Adresse IP du client |

---

## 🧪 Tests

### Test manuel du formulaire

1. Démarrer le backend : `npm run dev`
2. Ouvrir `index.html` dans le navigateur
3. Remplir le formulaire
4. Envoyer
5. Vérifier que l'email est reçu sur `hello@pixelforgelab.fr`

### Test des scénarios d'erreur

- Envoyer sans remplir les champs obligatoires → Doit afficher une erreur
- Entrer un email invalide → Doit afficher une erreur
- Entrer un téléphone invalide → Doit afficher une erreur
- Envoyer plusieurs fois rapidement (rate limit) → Doit afficher une erreur après 5 tentatives

---

## 📊 Monitoring

### Logs du serveur

Le serveur affiche des logs en console :

```
╔══════════════════════════════════════════════════════════════╗
║  PIXELFORGE — CONTACT FORM BACKEND                             ║
╠══════════════════════════════════════════════════════════════╣
║  Server running on port 3001                                        ║
║  API endpoint: http://localhost:3001/api/contact                  ║
║  Health check: http://localhost:3001/api/health                   ║
╠══════════════════════════════════════════════════════════════╣
║  Environment: development                                            ║
║  Ready to receive contact form submissions!                          ║
╚══════════════════════════════════════════════════════════════╝
```

### Logs des soumissions

Chaque soumission réussie est loguée :

```
✅ Contact form submitted successfully in 1234ms
📧 Email sent to: jean.dupont@email.com (Jean Dupont)
```

---

## 🌐 Déploiement

### Déploiement sur Vercel (recommandé)

Le backend Node.js peut être déployé sur Vercel, Railway, Render, ou tout hébergeur Node.js.

**Exemple Vercel** :

1. Créer un fichier `vercel.json` :

```json
{
  "version": 2,
  "builds": [
    {
      "src": "server.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/server.js"
    }
  ]
}
```

2. Déployer :

```bash
vercel --prod
```

---

## 🔧 Personnalisation

### Modifier le design de l'email

Éditez `email-template.html` pour changer :
- Couleurs
- Layout
- Contenu du message
- Style du footer

### Ajuster le rate limiting

Dans `server.js`, modifiez les valeurs :

```javascript
const contactFormLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // Durée en ms
  max: 5, // Nombre maximum de requêtes
  // ...
});
```

### Ajuster le score reCAPTCHA

Dans `server.js`, modifiez le score minimum requis :

```javascript
if (data.score < 0.5) { // Score entre 0 et 1
  return false;
}
```

---

## 📞 Support

Pour toute question ou problème avec le formulaire de contact :

- Email : `hello@pixelforgelab.fr`
- GitHub Issues : [créer une issue](https://github.com/votre-repo/pixelforge/issues)

---

## 📝 Notes importantes

1. **Vérification de domaine** : Le domaine `pixelforgelab.fr` doit être vérifié sur Resend (DNS SPF/DKIM)
2. **Production** : Ne pas utiliser localhost en production
3. **Secrets** : JAMAIS commiter `.env` dans git
4. **HTTPS** : Utiliser HTTPS en production pour reCAPTCHA
5. **Rate limiting** : Ajuster selon vos besoins

---

**Version** : 1.0.0
**Dernière mise à jour** : 2026-03-26
**Auteur** : PixelForge
