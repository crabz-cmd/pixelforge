# 📊 Guide d'installation Google Analytics 4 — PixelForge

## 🎯 Pourquoi Google Analytics 4 est critique ?

Sans GA4, vous êtes **aveugle** :
- ❌ Vous ne savez pas combien de visiteurs
- ❌ Vous ne savez pas d'où ils viennent (Google, Facebook, etc.)
- ❌ Vous ne savez pas ce qu'ils font sur le site
- ❌ Vous ne savez pas quels CTA fonctionnent
- ❌ Vous ne pouvez pas optimiser
- ❌ Vous ne pouvez pas mesurer le ROI

Avec GA4, vous pouvez :
- ✅ Mesurer le trafic en temps réel
- ✅ Identifier les pages les plus populaires
- ✅ Suivre les conversions (formulaires, clics CTA)
- ✅ Optimiser le marketing (ROI)
- ✅ Comprendre le comportement des visiteurs

---

## 📋 Étape par étape (15 minutes)

### Étape 1 : Créer un compte GA4 (5 minutes)

1. Allez sur https://analytics.google.com/
2. Cliquez sur "Commencer la mesure" (si nouveau compte) ou "Créer un compte"
3. Remplissez les informations :
   - **Nom du compte** : "PixelForge"
   - **Paramètres du compte** : Tous activés
   - Cliquez sur "Suivant"

4. Créez une propriété :
   - **Nom de la propriété** : "PixelForge - Site web"
   - **Fuseau horaire** : (GMT+01:00) Paris
   - **Devise** : Euro (€)
   - Cliquez sur "Suivant"

5. Informations sur l'entreprise :
   - **Catégorie** : Commerce / Internet / Technologie
   - **Taille** : Petit (1-10)
   - **Objectif** : Générer des prospects (leads)
   - Cliquez sur "Suivant"

6. Acceptez les conditions
7. **Notez votre ID de mesure** (format : G-XXXXXXXXXX)

---

### Étape 2 : Obtenir le code de tracking (2 minutes)

1. Sur la page "Configuration du flux de données web"
2. Choisissez "Site web"
3. Remplissez :
   - **URL du site web** : https://www.pixelforgelab.fr
   - **Nom du flux** : PixelForge Web
   - Cliquez sur "Créer un flux"

4. **Copiez le code de tracking GA4** (ça ressemble à ça) :

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

### Étape 3 : Installer le code dans index.html (3 minutes)

1. Ouvrez `index.html`
2. Trouvez la ligne 6 (`<meta name="viewport"...>`)
3. **Juste après cette ligne**, collez le code GA4

Le résultat final sera :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>

  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>

  <title>PixelForge — Forgez votre présence digitale</title>
  ...
```

4. **Remplacez `G-XXXXXXXXXX` par votre vrai ID** que vous avez noté à l'étape 1

---

### Étape 4 : Configurer les événements (5 minutes)

Ajoutez ce code après le code GA4 pour suivre les conversions :

```html
<!-- Google Analytics 4 - Event Tracking -->
<script>
  // Formulaire de contact soumis
  function trackFormSubmit() {
    gtag('event', 'generate_lead', {
      'event_category': 'form',
      'event_label': 'contact_form'
    });
  }

  // CTA cliqué
  function trackCTA(cta_name) {
    gtag('event', 'click', {
      'event_category': 'cta',
      'event_label': cta_name
    });
  }

  // Modal portfolio ouvert
  function trackModalOpen(project_name) {
    gtag('event', 'view_item', {
      'event_category': 'portfolio',
      'event_label': project_name
    });
  }
</script>
```

---

### Étape 5 : Intégrer le tracking dans le code (5 minutes)

**Formulaire de contact** : Modifiez la fonction `submitForm`

```javascript
// Dans submitForm(), après le succès :
function submitForm(e) {
  e.preventDefault();
  // ... code existant ...

  // Ajoutez ceci après le succès :
  if (status === 200) {
    trackFormSubmit(); // ← Nouvelle ligne
    // ... reste du code ...
  }
}
```

**CTA buttons** : Ajoutez le tracking sur tous les CTA

```javascript
// Dans les onclick ou event listeners :
trackCTA('hero_voir_realisations');
trackCTA('hero_demander_devis');
trackCTA('contact_demander_devis');
// etc.
```

---

## 📊 Vérifier que GA4 fonctionne (2 minutes)

1. **Méthode 1 : Rapport en temps réel**
   - Allez sur https://analytics.google.com/
   - Cliquez sur "Rapports" → "Rapport en temps réel"
   - Ouvrez votre site dans un autre onglet
   - Vous devriez voir "1 utilisateur actif" apparaître

2. **Méthode 2 : Google Tag Assistant**
   - Installez l'extension Google Tag Assistant
   - Ouvrez votre site
   - Cliquez sur l'extension
   - Vous devriez voir "GA4 Configuration" en vert

---

## 🎯 Configurer les objectifs (conversions)

### Étape 1 : Créer des événements de conversion

1. Allez sur GA4 → "Administration" → "Événements"
2. Cliquez sur "Créer un événement"
3. Configurez 3 événements de conversion :

**Conversion 1 : Formulaire de contact**
- Nom de l'événement personnalisé : `contact_form_submit`
- Condition : `event_name` = `generate_lead` ET `event_label` = `contact_form`

**Conversion 2 : Modal projet ouvert**
- Nom de l'événement personnalisé : `project_modal_view`
- Condition : `event_name` = `view_item` ET `event_category` = `portfolio`

**Conversion 3 : CTA principal cliqué**
- Nom de l'événement personnalisé : `hero_cta_click`
- Condition : `event_name` = `click` ET `event_label` = `hero_demander_devis`

### Étape 2 : Marquer comme conversion

1. Allez sur GA4 → "Administration" → "Conversions"
2. Cliquez sur "Créer un événement de conversion"
3. Sélectionnez les événements créés ci-dessus
4. Cochez "Marquer comme conversion"

---

## 📈 Que regarder dans GA4 ?

### Jour 1 : Vérifier l'installation
- ✅ Rapport en temps réel → 1+ utilisateur actif
- ✅ Rapport Événements → événements générés
- ✅ Rapport Acquisition → sources de trafic

### Semaine 1 : Analyser le trafic
- **Rapport Rapports** → **Acquisition**
  - De où viennent les visiteurs ?
  - Quels canaux performent le mieux ?
- **Rapport Rapports** → **Engagement**
  - Temps passé sur le site
  - Pages les plus populaires
  - Taux de rebond

### Semaine 2 : Optimiser
- **Rapport Rapports** → **Événements**
  - Quels CTA sont les plus cliqués ?
  - Quels projets sont les plus vus ?
  - Combien de formulaires sont soumis ?

### Semaine 4 : Mesurer le ROI
- **Rapport Rapports** → **Monétisation**
  - Coût par acquisition (si pub)
  - Valeur des conversions
  - ROI par canal

---

## ⚠️ Erreurs fréquentes à éviter

### Erreur 1 : Mauvais placement du code
- ❌ Dans le `<body>` ou en bas du `<head>`
- ✅ Juste après `<meta name="viewport"...>`

### Erreur 2 : ID de mesure incorrect
- ❌ Copié depuis un autre site
- ✅ Utilisez votre propre ID `G-XXXXXXXXXX`

### Erreur 3 : Pas de test
- ❌ Ajouté sans vérifier
- ✅ Toujours tester avec "Rapport en temps réel"

### Erreur 4 : Pas de conversions configurées
- ❌ Seulement le code de tracking
- ✅ Configurer au moins 1 événement de conversion

---

## 🔗 Ressources utiles

- **Guide officiel GA4** : https://support.google.com/analytics/answer/9304153
- **Assistant Tag Google** : https://tagassistant.google.com/
- **Débogueur GA4** : https://analytics.google.com/analytics/web/#/a000000000p000000000/reports/realtime

---

## ✅ Checklist de validation

- [ ] Compte GA4 créé
- [ ] ID de mesure noté
- [ ] Code de tracking copié
- [ ] Code ajouté dans index.html (ligne 7)
- [ ] ID remplacé par le vrai ID
- [ ] Code de tracking événements ajouté
- [ ] Fonction submitForm modifiée
- [ ] CTA modifiés avec tracking
- [ ] Rapport en temps réel fonctionne
- [ ] Événements de conversion configurés
- [ ] Marqués comme conversions

---

## 📞 Besoin d'aide ?

Si vous rencontrez des problèmes :
1. Vérifiez que le code est bien dans le `<head>`
2. Vérifiez que l'ID est correct
3. Utilisez Google Tag Assistant
4. Consultez le rapport "Rapport de diagnostic" dans GA4

---

**Ce guide vous prend environ 15-30 minutes.**
**Une fois installé, vous aurez une visibilité totale sur votre site !**
