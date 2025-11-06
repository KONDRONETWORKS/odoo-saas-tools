# 📄 Comportement du Module SaaS Portal Start

## 🎯 Vue d'Ensemble

Le module `saas_portal_start` crée la page d'accueil publique (`/page/start`) permettant aux utilisateurs de découvrir et s'inscrire à votre service SaaS.

---

## 🔄 Comportement d'Installation

### Installation Automatique (Recommandé)

**Comportement actuel :** Le module `saas_portal_start` est maintenant installé **automatiquement** lors de l'installation de `saas_portal` grâce au hook `post_init_hook`.

**Processus :**
1. Installation de `saas_portal`
2. Exécution du hook `post_init_hook`
3. Recherche du module `saas_portal_start`
4. Installation automatique si trouvé et non installé
5. Page `/page/start` disponible immédiatement

**Avantages :**
- ✅ Installation transparente
- ✅ Pas d'intervention manuelle nécessaire
- ✅ Page d'accueil disponible dès le démarrage
- ✅ Expérience utilisateur optimale

### Installation Manuelle (Alternative)

Si l'installation automatique échoue ou si vous préférez un contrôle manuel :

**Étapes :**
1. Accéder à Apps : `http://localhost:8069/web?db=saas-portal-18.local`
2. Rechercher "SaaS Portal - /page/start"
3. Cliquer sur "Activer"
4. Attendre la fin de l'installation
5. La page `/page/start` est maintenant accessible

---

## 📍 Route Créée

### URL d'Accès

**Route principale :**
```
/page/start
```

**Route alternative :**
```
/page/website.start
```

**Accès complet :**
```
http://localhost:8069/page/start
```

### Caractéristiques

- **Type :** HTTP
- **Authentification :** Public (pas de connexion requise)
- **Website :** Oui (utilise le système de templates Odoo)
- **Méthode :** GET

---

## 🎨 Fonctionnalités de la Page

### Ce que voit l'utilisateur

**Page d'accueil :**
- Titre : "Get your own Database!"
- Formulaire de création d'instance :
  - Champ texte : nom de l'entreprise (ex: `mon-entreprise`)
  - Domaine affiché : `.saas-portal-18.local`
  - Bouton "Create!" pour créer l'instance

**Exemple visuel :**
```
┌─────────────────────────────────────┐
│  Get your own Database!             │
│                                       │
│  [mon-entreprise].saas-portal-18.local │
│                    [Create!]          │
└─────────────────────────────────────┘
```

### Processus de Création

**Quand l'utilisateur clique sur "Create!" :**

1. **Vérification de l'authentification**
   - Si non connecté → Redirection vers `/web/login` ou `/web/signup`
   - Si connecté → Continue

2. **Génération du nom de base**
   - Format : `{nom-saisi}.{base_saas_domain}`
   - Exemple : `mon-entreprise.saas-portal-18.local`

3. **Vérification de disponibilité**
   - Vérifie si la base existe déjà
   - Si oui → Message d'erreur
   - Si non → Continue

4. **Création de l'instance**
   - Appel à `plan.create_new_database()`
   - Création via le Server
   - Redirection vers l'instance créée

---

## ⚙️ Configuration Requise

### Dépendances

Le module `saas_portal_start` nécessite :
- ✅ `website` : Pour les templates web
- ✅ `saas_portal` : Pour les fonctionnalités SaaS

### Paramètres de Configuration

**Paramètre requis :**
- `base_saas_domain` : Domaine de base pour les instances
  - Exemple : `saas-portal-18.local`
  - Configuré dans : Paramètres → Technique → Paramètres → `saas_portal.base_saas_domain`

**Vérification :**
```python
# Dans le contrôleur
base_saas_domain = self.get_config_parameter('base_saas_domain')
```

---

## 🔧 Intégration avec le Système

### Relation avec saas_portal

**Dépendance :**
- `saas_portal_start` dépend de `saas_portal`
- Utilise les méthodes de `SaasPortal` controller
- Accède aux plans via `saas_portal.plan`

**Workflow :**
```
Utilisateur → /page/start
  ↓
Saisit nom entreprise
  ↓
Clique "Create!"
  ↓
Redirection si non connecté
  ↓
Appel saas_portal.plan.create_new_database()
  ↓
Création instance via Server
  ↓
Redirection vers instance créée
```

### Relation avec saas_portal_signup

**Complémentarité :**
- `saas_portal_start` : Page d'accueil publique
- `saas_portal_signup` : Processus d'inscription automatique
- Les deux travaillent ensemble pour l'expérience utilisateur complète

---

## 🚀 Scénarios d'Utilisation

### Scénario 1 : Utilisateur Non Connecté

**Étape 1 :** Visite `/page/start`
- Voit le formulaire de création
- Saisit un nom d'entreprise
- Clique sur "Create!"

**Étape 2 :** Redirection
- Redirigé vers `/web/signup` (inscription)
- Ou `/web/login` (connexion)

**Étape 3 :** Après connexion/inscription
- Retour automatique vers le processus de création
- Instance créée avec le nom saisi

### Scénario 2 : Utilisateur Connecté

**Étape 1 :** Visite `/page/start`
- Voit le formulaire de création
- Saisit un nom d'entreprise
- Clique sur "Create!"

**Étape 2 :** Création immédiate
- Vérification de disponibilité
- Création de l'instance
- Redirection vers l'instance créée

### Scénario 3 : Plan Spécifique

**URL avec plan :**
```
/page/start?plan_id=1
```

**Comportement :**
- Le plan est pré-sélectionné
- L'instance sera créée avec ce plan
- Pas besoin de choisir le plan manuellement

---

## 🛠️ Personnalisation

### Modifier le Template

**Fichier :** `saas_portal_start/views/website.xml`

**Éléments personnalisables :**
- Titre de la page
- Texte du formulaire
- Style et design
- Messages d'aide

**Exemple de modification :**
```xml
<h2>Créez votre propre instance Odoo !</h2>
<!-- Au lieu de "Get your own Database!" -->
```

### Ajouter des Informations

**Possibilités :**
- Afficher les plans disponibles
- Afficher les prix
- Afficher les fonctionnalités
- Ajouter des témoignages
- Ajouter une FAQ

---

## ⚠️ Dépannage

### Erreur : Module non trouvé

**Symptôme :**
- Page `/page/start` retourne 404
- Erreur "Module not found"

**Solution :**
1. Vérifier que `saas_portal_start` est installé
2. Vérifier que `saas_portal` est installé
3. Vérifier que `website` est installé
4. Redémarrer Odoo si nécessaire

### Erreur : Paramètre manquant

**Symptôme :**
- Page s'affiche mais erreur lors de la création
- Message "base_saas_domain not configured"

**Solution :**
1. Aller dans Paramètres → Technique → Paramètres
2. Créer le paramètre : `saas_portal.base_saas_domain`
3. Valeur : `saas-portal-18.local` (ou votre domaine)
4. Recharger la page

### Erreur : Route non accessible

**Symptôme :**
- Erreur 404 sur `/page/start`
- Route non trouvée

**Solution :**
1. Vérifier l'installation du module
2. Mettre à jour la liste des modules
3. Vérifier les logs Odoo pour erreurs
4. Redémarrer Odoo

---

## 📋 Checklist d'Installation

### Installation Automatique (Recommandé)

- [ ] Installer `saas_portal`
- [ ] Vérifier que le hook `post_init_hook` s'exécute
- [ ] Vérifier dans les logs que `saas_portal_start` est installé
- [ ] Tester l'accès à `/page/start`
- [ ] Vérifier que le formulaire s'affiche correctement

### Installation Manuelle

- [ ] Installer `saas_portal` d'abord
- [ ] Aller dans Apps
- [ ] Rechercher "SaaS Portal - /page/start"
- [ ] Cliquer sur "Activer"
- [ ] Attendre la fin de l'installation
- [ ] Tester l'accès à `/page/start`

### Configuration

- [ ] Configurer `base_saas_domain` dans les paramètres
- [ ] Créer au moins un plan confirmé
- [ ] Créer au moins un serveur actif
- [ ] Tester la création d'une instance depuis `/page/start`

---

## 🎯 Recommandations

### Installation Automatique

**Recommandé pour :**
- ✅ Déploiements nouveaux
- ✅ Installations standard
- ✅ Expérience utilisateur optimale
- ✅ Moins de configuration manuelle

**Avantages :**
- Installation transparente
- Pas d'oubli possible
- Configuration cohérente

### Installation Manuelle

**Recommandé pour :**
- ⚠️ Personnalisations avancées
- ⚠️ Contrôle précis de l'ordre d'installation
- ⚠️ Débogage de problèmes

**Avantages :**
- Contrôle total
- Visibilité du processus
- Dépannage facilité

---

## 📊 État Actuel

### Comportement Implémenté

✅ **Installation automatique via hook**
- Le module `saas_portal_start` est installé automatiquement
- Hook `post_init_hook` dans `saas_portal/hooks.py`
- Fonction `_install_portal_start_module()` ajoutée

✅ **Gestion des erreurs**
- Logs informatifs si installation échoue
- Message clair pour installation manuelle
- Pas de blocage si module non trouvé

✅ **Compatibilité**
- Fonctionne avec installation manuelle aussi
- Vérifie si déjà installé avant d'essayer
- Gère les états "uninstalled" et "to install"

---

## 🔄 Mise à Jour

### Après Mise à Jour de saas_portal

**Comportement :**
- Le hook `post_upgrade_hook` vérifie aussi `saas_portal_start`
- Installation automatique si nécessaire
- Pas de réinstallation si déjà présent

### Après Mise à Jour de saas_portal_start

**Comportement :**
- Mise à jour normale via Apps
- Pas d'impact sur saas_portal
- Route `/page/start` reste disponible

---

## 📝 Résumé

### Installation

**Mode automatique (actuel) :**
- ✅ Installé automatiquement avec `saas_portal`
- ✅ Aucune action manuelle requise
- ✅ Page `/page/start` disponible immédiatement

**Mode manuel (alternative) :**
- ⚠️ Installation depuis Apps
- ⚠️ Contrôle total du processus
- ⚠️ Utile pour le débogage

### Utilisation

**Pour les utilisateurs :**
- Accès public à `/page/start`
- Formulaire simple de création d'instance
- Redirection automatique après création

**Pour les administrateurs :**
- Configuration via paramètres Odoo
- Personnalisation via templates XML
- Monitoring via logs Odoo

---

**Le module `saas_portal_start` est maintenant installé automatiquement pour une expérience utilisateur optimale !**

