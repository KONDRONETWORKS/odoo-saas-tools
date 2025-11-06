# 🎯 Scénario Utilisateur - Accès et Utilisation du SaaS

## Vue d'Ensemble

Ce document explique le parcours complet d'un utilisateur depuis l'inscription jusqu'à l'utilisation quotidienne de votre service SaaS Odoo.

---

## 📋 Architecture du Système

### Composants Principaux

```
┌─────────────────────────────────────────────────────────────┐
│                    PORTAL (saas-portal-18.local)            │
│  - Interface d'inscription et gestion                       │
│  - Gestion des plans et abonnements                         │
│  - Tableau de bord client                                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ OAuth2 + API REST
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  SERVER (server-1.saas-portal-18.local)     │
│  - Création des bases de données                            │
│  - Gestion des instances Odoo                              │
│  - API de création/suppression                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ PostgreSQL
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              INSTANCE CLIENT (client-XXX.saas-portal-18.local) │
│  - Odoo complet pour le client                             │
│  - Données isolées                                         │
│  - Modules configurés selon le plan                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Scénario Complet : De l'Inscription à l'Utilisation

### ÉTAPE 1 : Découverte et Inscription

#### 1.1 Accès au Portail Public

**URL :** `http://localhost:8069/page/start` (ou votre domaine public)

**Ce que voit l'utilisateur :**
- Page d'accueil du portail SaaS
- Liste des plans disponibles avec leurs fonctionnalités
- Prix et caractéristiques de chaque plan
- Bouton "Essai gratuit" ou "S'inscrire"

**Exemple de plans :**
- **Starter** : 10 utilisateurs, 5 GB stockage, 14 jours d'essai
- **Business** : 50 utilisateurs, 50 GB stockage, 30 jours d'essai
- **Enterprise** : Illimité, 500 GB stockage, 30 jours d'essai

#### 1.2 Inscription

**Processus :**
1. L'utilisateur clique sur "S'inscrire" ou "Essai gratuit"
2. Redirection vers le formulaire d'inscription
3. Remplissage des informations :
   - Nom et prénom
   - Email
   - Mot de passe
   - Sélection du plan (optionnel pour l'essai)
   - Nom de l'entreprise

**Ce qui se passe en arrière-plan :**
- Création d'un compte utilisateur dans le Portal
- Création automatique d'un enregistrement `saas_portal.client`
- Association utilisateur-client
- Génération d'un nom de domaine unique (ex: `client-001.saas-portal-18.local`)

#### 1.3 Confirmation et Création de l'Instance

**Email de confirmation :**
```
Objet : Bienvenue sur [Votre SaaS] - Votre instance est en cours de création

Bonjour [Nom],

Votre compte a été créé avec succès !

Votre instance Odoo sera disponible dans quelques minutes à l'adresse :
https://client-001.saas-portal-18.local

Vous recevrez un email avec vos identifiants de connexion une fois l'instance prête.

Cordialement,
L'équipe SaaS
```

**Processus automatique :**
1. Le Portal envoie une requête au Server via API REST
2. Le Server crée une nouvelle base de données PostgreSQL
3. Le Server initialise une instance Odoo avec les modules du plan
4. Le Server configure le domaine et les paramètres
5. Le Server retourne les informations au Portal
6. Le Portal enregistre l'URL et les credentials

**Durée :** 2-5 minutes selon la complexité du plan

---

### ÉTAPE 2 : Première Connexion

#### 2.1 Email de Bienvenue

**Email reçu :**
```
Objet : Votre instance Odoo est prête !

Bonjour [Nom],

Votre instance Odoo est maintenant disponible !

🔗 Accès : https://client-001.saas-portal-18.local
👤 Login : admin
🔑 Mot de passe : [mot de passe généré]

⚠️ Important : Changez votre mot de passe lors de la première connexion.

Bonne utilisation !
```

#### 2.2 Connexion à l'Instance

**URL d'accès :** `https://client-001.saas-portal-18.local` (ou `http://localhost:8069/web?db=client-001.saas-portal-18.local`)

**Première connexion :**
1. L'utilisateur saisit `admin` / `[mot de passe]`
2. Odoo demande de changer le mot de passe
3. Configuration du profil utilisateur
4. Accès au tableau de bord Odoo

**Ce que voit l'utilisateur :**
- Interface Odoo standard
- Modules installés selon le plan choisi
- Données de démonstration (si activées)
- Applications disponibles (CRM, Ventes, Comptabilité, etc.)

---

### ÉTAPE 3 : Utilisation Quotidienne

#### 3.1 Tableau de Bord Client

**Accès au portail client :**
- URL : `http://localhost:8069/web?db=saas-portal-18.local`
- Menu : "Mon Compte" ou "Mes Instances"

**Informations disponibles :**
- Statut de l'abonnement (Actif, Essai, Expiré)
- Date d'expiration
- Nombre d'utilisateurs utilisés / maximum
- Stockage utilisé / maximum
- Historique des factures
- Support et tickets

#### 3.2 Utilisation de l'Instance Odoo

**Accès quotidien :**
- URL : `https://client-001.saas-portal-18.local`
- Connexion avec les identifiants configurés
- Utilisation normale d'Odoo

**Fonctionnalités disponibles :**
- Toutes les fonctionnalités Odoo standard
- Modules installés selon le plan
- Personnalisation limitée selon le plan
- Sauvegarde automatique (selon configuration)

#### 3.3 Gestion des Utilisateurs

**Depuis l'instance Odoo :**
- Création d'utilisateurs internes
- Attribution de droits et permissions
- Gestion des équipes

**Limites :**
- Nombre maximum d'utilisateurs selon le plan
- Alertes si limite approchée
- Blocage si limite dépassée (selon configuration)

---

### ÉTAPE 4 : Gestion de l'Abonnement

#### 4.1 Renouvellement

**Avant expiration :**
- Email de rappel 7 jours avant
- Email de rappel 3 jours avant
- Email de rappel 1 jour avant

**Processus de renouvellement :**
1. L'utilisateur reçoit un email avec lien de paiement
2. Redirection vers le portail de paiement
3. Paiement effectué
4. Extension automatique de l'abonnement
5. Confirmation par email

#### 4.2 Upgrade/Downgrade

**Changement de plan :**
1. L'utilisateur accède au portail client
2. Sélectionne "Changer de plan"
3. Choix du nouveau plan
4. Calcul de la différence de prix
5. Paiement (si upgrade) ou crédit (si downgrade)
6. Application immédiate des nouvelles limites
7. Notification des changements

**Effets :**
- Modification des limites (utilisateurs, stockage)
- Ajout/suppression de modules (selon plan)
- Ajustement des fonctionnalités disponibles

#### 4.3 Expiration et Suspension

**Si non renouvelé :**
1. Date d'expiration atteinte
2. Période de grâce (si configurée) : 7 jours
3. Suspension de l'instance :
   - Accès en lecture seule
   - Pas de modifications possibles
   - Message d'avertissement affiché
4. Après période de grâce :
   - Suppression automatique (si configurée)
   - Ou conservation avec accès bloqué

---

## 🔐 Flux d'Authentification

### Connexion au Portal

```
Utilisateur → Portal (saas-portal-18.local)
  ↓
Formulaire de connexion
  ↓
Vérification credentials
  ↓
Session créée
  ↓
Accès au tableau de bord client
```

### Connexion à l'Instance Client

```
Utilisateur → Instance Client (client-001.saas-portal-18.local)
  ↓
Formulaire de connexion Odoo standard
  ↓
Vérification dans la base de données client
  ↓
Session Odoo créée
  ↓
Accès à l'instance Odoo
```

### Communication Portal ↔ Server

```
Portal → API REST → Server
  ↓
Authentification OAuth2
  ↓
Validation du token
  ↓
Exécution de la requête (création DB, etc.)
  ↓
Retour des résultats au Portal
```

---

## 📊 Exemples de Scénarios Concrets

### Scénario 1 : Nouvelle Entreprise (Essai Gratuit)

**Jour 1 - Inscription :**
- Marie, directrice d'une petite entreprise, découvre votre SaaS
- Elle s'inscrit pour un essai gratuit du plan "Starter"
- Elle reçoit un email de confirmation

**Jour 1 - 5 minutes après :**
- Email : "Votre instance est prête"
- Marie se connecte à `client-001.saas-portal-18.local`
- Elle configure son profil et explore Odoo

**Jour 1-14 :**
- Marie utilise Odoo quotidiennement
- Elle crée des contacts, des devis, des factures
- Elle ajoute 3 utilisateurs de son équipe

**Jour 14 :**
- Email : "Votre essai expire dans 24h"
- Marie décide de s'abonner au plan "Business"
- Paiement effectué
- Abonnement activé pour 1 an

**Résultat :** Client payant avec abonnement annuel

---

### Scénario 2 : Entreprise Existante (Migration)

**Semaine 1 :**
- Jean, responsable IT, cherche une solution SaaS pour remplacer leur Odoo on-premise
- Il s'inscrit et teste le plan "Enterprise"
- Il importe les données de test

**Semaine 2 :**
- Jean valide la solution avec son équipe
- Il contacte le support pour migration
- Planification de la migration

**Semaine 3 :**
- Migration des données effectuée par l'équipe SaaS
- Formation des utilisateurs
- Go-live

**Résultat :** Client Enterprise avec migration complète

---

### Scénario 3 : Freemium → Payant

**Mois 1-3 :**
- Sophie utilise le plan gratuit (limité)
- Elle crée quelques contacts et factures
- Elle atteint les limites du plan gratuit

**Mois 3 :**
- Notification : "Limite atteinte"
- Sophie décide de passer au plan "Starter"
- Paiement mensuel activé

**Résultat :** Conversion freemium → payant

---

## 🎨 Interface Utilisateur

### Portail Public (Inscription)

**Page d'accueil :**
- Header avec logo et navigation
- Section hero : "Gérez votre entreprise avec Odoo"
- Liste des plans avec comparaison
- Témoignages clients
- FAQ
- Footer avec contact

**Page d'inscription :**
- Formulaire simple
- Sélection du plan
- Conditions générales
- Bouton "Créer mon compte"

### Portail Client (Tableau de Bord)

**Menu principal :**
- Tableau de bord
- Mes instances
- Mon abonnement
- Factures
- Support
- Paramètres

**Tableau de bord :**
- Statut de l'abonnement
- Utilisation des ressources (graphiques)
- Dernières activités
- Notifications importantes
- Accès rapide à l'instance

### Instance Odoo Client

**Interface standard Odoo :**
- Applications installées selon le plan
- Personnalisation limitée
- Branding possible (selon plan)
- Modules additionnels (selon plan)

---

## 🔄 Workflow Technique Détaillé

### Création d'une Instance Client

```
1. Utilisateur s'inscrit sur le Portal
   ↓
2. Portal crée l'enregistrement saas_portal.client
   ↓
3. Portal génère un nom de domaine unique
   ↓
4. Portal appelle l'API Server : POST /saas_server/new_database
   ↓
5. Server valide le token OAuth2
   ↓
6. Server crée la base PostgreSQL : client-001.saas-portal-18.local
   ↓
7. Server initialise Odoo avec modules du plan
   ↓
8. Server configure le domaine et paramètres
   ↓
9. Server retourne URL et credentials au Portal
   ↓
10. Portal enregistre les informations
   ↓
11. Portal envoie email de bienvenue à l'utilisateur
   ↓
12. Instance prête et accessible
```

### Synchronisation Portal ↔ Server

```
Toutes les heures (cron) :
  ↓
Portal → API Server : GET /saas_server/client_status
  ↓
Server retourne :
  - Nombre d'utilisateurs actifs
  - Stockage utilisé
  - Modules installés
  - État de l'instance
  ↓
Portal met à jour saas_portal.client
  ↓
Vérification des limites et quotas
  ↓
Alertes si nécessaire
```

---

## 📱 Accès Multi-Plateformes

### Depuis un Navigateur Web

**Desktop :**
- Chrome, Firefox, Safari, Edge
- Interface complète
- Toutes les fonctionnalités

**Mobile :**
- Interface responsive
- Applications principales accessibles
- Optimisé pour écrans tactiles

### Application Mobile Odoo (si activée)

- Application native iOS/Android
- Synchronisation avec l'instance
- Notifications push
- Accès hors ligne limité

---

## 🛡️ Sécurité et Isolation

### Isolation des Données

**Chaque client a :**
- Base de données PostgreSQL dédiée
- Fichiers stockés dans un répertoire isolé
- Aucun accès aux données d'autres clients
- Domaine unique

### Authentification

**Portal :**
- Authentification Odoo standard
- Sessions sécurisées
- MFA possible (selon configuration)

**Instance Client :**
- Authentification Odoo standard
- Gestion des utilisateurs par le client
- Permissions configurables

**Communication Portal ↔ Server :**
- OAuth2 avec tokens sécurisés
- Validation par Client ID
- Chiffrement HTTPS

---

## 💰 Modèles de Facturation

### Abonnement Mensuel

- Facturation le même jour chaque mois
- Paiement automatique (si configuré)
- Renouvellement automatique
- Résiliation possible à tout moment

### Abonnement Annuel

- Facturation une fois par an
- Réduction généralement appliquée
- Renouvellement automatique
- Résiliation possible avec remboursement pro-rata

### Pay-as-you-Go

- Facturation selon l'utilisation
- Surcoût si limites dépassées
- Facturation mensuelle
- Flexible selon les besoins

---

## 📞 Support et Assistance

### Niveaux de Support

**Plan Starter :**
- Support par email
- Documentation en ligne
- Forum communautaire
- Temps de réponse : 48h

**Plan Business :**
- Support prioritaire
- Chat en direct
- Support téléphonique
- Temps de réponse : 24h

**Plan Enterprise :**
- Support dédié
- Gestionnaire de compte
- Support 24/7
- Temps de réponse : 4h

### Canaux de Support

- Email : support@votresaaS.com
- Chat en direct (si disponible)
- Tickets dans le portail client
- Documentation en ligne
- Vidéos tutoriels

---

## 📈 Évolutivité

### Croissance de l'Entreprise

**Scénario :**
- Client démarre avec plan "Starter" (10 utilisateurs)
- L'entreprise grandit et a besoin de 30 utilisateurs
- Upgrade vers plan "Business" (50 utilisateurs)
- Processus transparent, pas de perte de données

### Ajout de Modules

**Processus :**
1. Client demande un module supplémentaire
2. Vérification de la compatibilité avec le plan
3. Installation sur l'instance
4. Facturation si module payant
5. Module disponible immédiatement

---

## 🎯 Points Clés pour l'Utilisateur

### Avantages

✅ **Simplicité :** Pas besoin d'infrastructure
✅ **Rapidité :** Instance disponible en quelques minutes
✅ **Sécurité :** Données isolées et sécurisées
✅ **Maintenance :** Gérée automatiquement
✅ **Mises à jour :** Automatiques et transparentes
✅ **Scalabilité :** Changement de plan facile
✅ **Support :** Disponible selon le plan

### Responsabilités de l'Utilisateur

- Gestion des utilisateurs de son instance
- Configuration des modules et workflows
- Sauvegarde des données importantes (sauvegardes automatiques incluses)
- Respect des limites du plan
- Paiement des abonnements

---

## 🔍 Monitoring et Métriques

### Métriques Visibles par le Client

**Dans le portail client :**
- Nombre d'utilisateurs actifs
- Stockage utilisé
- Nombre de transactions
- Modules installés
- Historique des factures

### Métriques Internes (Admin SaaS)

- Performance des instances
- Utilisation des ressources
- Taux de conversion
- Taux de rétention
- Satisfaction client

---

## 📝 Checklist Utilisateur Final

### Avant de Commencer

- [ ] Comprendre les différents plans disponibles
- [ ] Choisir le plan adapté à ses besoins
- [ ] Préparer les informations d'inscription
- [ ] Vérifier les prérequis techniques (navigateur, etc.)

### Après Inscription

- [ ] Vérifier l'email de confirmation
- [ ] Attendre l'email "Instance prête"
- [ ] Se connecter et changer le mot de passe
- [ ] Explorer l'interface Odoo
- [ ] Configurer le profil utilisateur

### Utilisation Quotidienne

- [ ] Se connecter à l'instance
- [ ] Utiliser les modules selon les besoins
- [ ] Gérer les utilisateurs de l'équipe
- [ ] Surveiller l'utilisation des ressources
- [ ] Contacter le support si nécessaire

### Gestion de l'Abonnement

- [ ] Surveiller les dates d'expiration
- [ ] Renouveler avant expiration
- [ ] Upgrader si besoin de plus de ressources
- [ ] Consulter les factures régulièrement
- [ ] Contacter le support pour questions

---

## 🎓 Ressources pour l'Utilisateur

### Documentation

- Guide de démarrage rapide
- Tutoriels vidéo
- FAQ complète
- Documentation des modules
- Bonnes pratiques

### Formation

- Webinaires réguliers
- Sessions de formation en ligne
- Documentation pas-à-pas
- Exemples de cas d'usage
- Support communautaire

---

**Ce scénario décrit le parcours complet d'un utilisateur dans votre système SaaS Odoo, de l'inscription à l'utilisation quotidienne.**

