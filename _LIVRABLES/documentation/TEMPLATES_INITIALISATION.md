# 📦 Templates et Plans d'Initialisation

## 🎯 Objectif

Lors de l'installation du module `saas_portal`, des **templates** et **plans** de base sont automatiquement créés pour guider les utilisateurs dans leur configuration SaaS.

## 📋 Données Créées

### 🔧 Serveur SaaS par Défaut

Un serveur SaaS par défaut est créé automatiquement lors de l'installation :

- **Nom** : `server-default`
- **Configuration** :
  - Schéma : `http`
  - Port : `8069`
  - Host local : `localhost`
  - Actif : ✅

> **Note** : Si un serveur existe déjà, il sera utilisé à la place.

---

### 🗄️ Templates de Base de Données

Deux templates sont créés en état `draft` :

#### 1. **template-odoo-standard**
- **Nom** : `template-odoo-standard`
- **État** : `draft`
- **Usage** : Template standard sans données de démo
- **Utilisé par** : Plan Starter, Plan Business

#### 2. **template-odoo-demo**
- **Nom** : `template-odoo-demo`
- **État** : `draft`
- **Usage** : Template avec données de démonstration
- **Utilisé par** : Plan Demo

> **Note** : Les templates sont en état `draft` et doivent être activés manuellement en cliquant sur "Create template DB" dans le plan.

---

### 💰 Plans SaaS

Trois plans sont créés automatiquement :

#### 1. **Plan Starter** 🆓
- **Nom** : Plan Starter
- **Description** : Plan gratuit pour tester et découvrir Odoo
- **Template** : `template-odoo-standard`
- **Configuration** :
  - Max DBs par partenaire : 1
  - Max DBs essai par partenaire : 1
  - Max utilisateurs : 5
  - Stockage : 1 Go
  - Blocage à l'expiration : ✅
  - Période de grâce : 7 jours
- **Idéal pour** : Découvrir Odoo, tester les fonctionnalités

#### 2. **Plan Business** 💼
- **Nom** : Plan Business
- **Description** : Plan standard pour les petites et moyennes entreprises
- **Template** : `template-odoo-standard`
- **Configuration** :
  - Max DBs par partenaire : 5
  - Max DBs essai par partenaire : 2
  - Max utilisateurs : 50
  - Stockage : 10 Go
  - Blocage à l'expiration : ❌
  - Blocage si stockage dépassé : ✅
  - Période de grâce : 30 jours
- **Idéal pour** : PME, croissance d'entreprise

#### 3. **Plan Demo** 🎬
- **Nom** : Plan Demo
- **Description** : Plan de démonstration avec données d'exemple
- **Template** : `template-odoo-demo`
- **Configuration** :
  - Max DBs par partenaire : 1
  - Max DBs essai par partenaire : 1
  - Max utilisateurs : 10
  - Stockage : 5 Go
  - Données de démo : ✅
  - Expiration automatique : 48 heures
  - Période de grâce : 0 jours
- **Idéal pour** : Démonstrations clients, présentations

---

## 🚀 Utilisation

### 1. Après l'Installation

Une fois le module installé, vous trouverez :

1. **1 Serveur** : `server-default`
2. **2 Templates** : `template-odoo-standard` et `template-odoo-demo` (en draft)
3. **3 Plans** : Plan Starter, Plan Business, Plan Demo

### 2. Activer les Templates

Pour utiliser les plans, vous devez d'abord créer les bases de données des templates :

1. Aller dans **SaaS > Plans**
2. Ouvrir un plan (ex: **Plan Starter**)
3. Cliquer sur **"Create template DB"**
4. Attendre la création (quelques minutes)
5. Le template passera de `draft` à `template`
6. Le plan passera de `draft` à `confirmed`

### 3. Personnaliser

Une fois les templates créés, vous pouvez :

- **Configurer le template** : Cliquer sur "Log in to template DB"
- **Installer des modules** : Ajouter les modules nécessaires
- **Configurer les paramètres** : Ajuster selon vos besoins
- **Créer des clients** : Utiliser le plan pour créer des instances clients

---

## 🔧 Configuration

### Fichier de Données

Les données sont définies dans : `saas_portal/data/init_data.xml`

### Hook Post-Init

Le hook `post_init_hook` dans `saas_portal/hooks.py` :

1. ✅ Crée un serveur par défaut si aucun n'existe
2. ✅ Lie les templates au serveur par défaut
3. ✅ Lie les plans au serveur par défaut
4. ✅ Assure que les vues sont correctement créées

---

## 📝 Personnalisation

### Modifier les Plans

Pour modifier les plans d'initialisation :

1. Modifier `saas_portal/data/init_data.xml`
2. Mettre à jour le module : `-u saas_portal`
3. Ou modifier directement dans l'interface Odoo

### Ajouter des Plans

Pour ajouter des plans personnalisés :

1. Ajouter un record dans `init_data.xml`
2. Ou créer directement depuis l'interface Odoo

### Modifier le Serveur par Défaut

Le serveur par défaut est créé dans `hooks.py`. Pour modifier :

1. Éditer `saas_portal/hooks.py`
2. Modifier la fonction `_ensure_default_server()`
3. Mettre à jour le module

---

## ✅ Avantages

- 🎯 **Guide les utilisateurs** : Exemples prêts à l'emploi
- ⚡ **Gain de temps** : Pas besoin de créer tout depuis zéro
- 📚 **Documentation** : Exemples de configuration
- 🚀 **Démarrage rapide** : Prêt à l'emploi en quelques clics

---

## 🔄 Réinitialisation

Pour réinitialiser les données d'initialisation :

1. Désinstaller le module : `-u saas_portal`
2. Réinstaller : `-i saas_portal`

> **Attention** : Cela supprimera toutes les données du module, y compris les clients existants.

---

## 📞 Support

Pour toute question ou problème, consultez :
- La documentation du module
- Les logs Odoo : `odoo.log`
- L'interface Odoo : **SaaS > Configuration**
