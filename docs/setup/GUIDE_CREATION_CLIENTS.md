# Guide : Création de Clients SaaS - Processus Concret

## 🎯 Vue d'ensemble

La création d'un client SaaS se fait en plusieurs étapes et peut être déclenchée de différentes manières. Ce guide explique le processus concret.

## 📋 Prérequis

Avant de créer un client, vous devez avoir :

1. ✅ **Un serveur SaaS** (`saas-server-001`)
2. ✅ **Un plan SaaS** configuré avec un template
3. ✅ **Un partenaire** (client/entreprise) dans Odoo

## 🔄 Processus de création : 3 méthodes

### Méthode 1 : Création depuis l'interface Odoo (Manuelle)

#### Étape 1 : Accéder au menu Clients

1. Ouvrez Odoo : **http://localhost:8069**
2. Allez dans **SaaS > Clients**
3. Cliquez sur **"Créer"**

#### Étape 2 : Remplir le formulaire

**Champs obligatoires :**
- **Nom de la base de données** : `client-monentreprise-001` (sera utilisé comme nom de DB)
- **Plan** : Sélectionnez un plan (ex: `Plan Standard`)
- **Partenaire** : Sélectionnez ou créez un partenaire
- **Serveur** : Sélectionnez `saas-server-001`

**Champs optionnels :**
- **Date d'expiration** : Par défaut, calculée depuis le plan
- **Essai** : Cochez si c'est un essai gratuit
- **Équipe de support** : Sélectionnez une équipe si nécessaire

#### Étape 3 : Enregistrer

- Cliquez sur **"Enregistrer"**
- Le client est créé dans Odoo **MAIS** la base de données n'est pas encore créée

#### Étape 4 : Créer la base de données réelle

Pour créer la base de données réelle sur le serveur SaaS :

1. Ouvrez le client créé
2. Cliquez sur le bouton **"Create Database"** ou **"Créer la base de données"**
3. Le système va :
   - Appeler le serveur SaaS via OAuth
   - Créer une nouvelle base de données PostgreSQL
   - Installer Odoo sur cette base
   - Configurer l'accès OAuth

⚠️ **Note** : Cette étape nécessite un serveur SaaS séparé avec le module `saas_server` installé.

---

### Méthode 2 : Création automatique depuis un Plan

Cette méthode est utilisée quand un utilisateur final souscrit à un plan depuis le portail public.

#### Processus automatique :

```python
# Le code interne appelle :
plan.create_new_database(
    partner_id=partner_id,
    user_id=user_id,
    trial=True,  # ou False
    notify_user=True
)
```

**Ce qui se passe :**

1. **Validation** : Vérifie les limites du plan (max DBs, max trials)
2. **Génération du nom** : Génère un nom de DB unique selon le template
3. **Création du client** : Crée l'enregistrement `saas_portal.client`
4. **Préparation des données** : Prépare les données utilisateur propriétaire
5. **Appel au serveur SaaS** : 
   - OAuth authentication
   - Requête HTTP à `/saas_server/new_database`
   - Envoi de l'état (dbname, expiration, template, etc.)
6. **Création de la base** : Le serveur SaaS crée la base PostgreSQL
7. **Installation Odoo** : Installation d'Odoo sur la nouvelle base
8. **Configuration OAuth** : Configuration de l'accès OAuth
9. **Envoi d'email** : Notification à l'utilisateur (si configuré)
10. **Redirection** : Redirection vers la nouvelle instance Odoo

---

### Méthode 3 : Création via Script (Développement/Test)

#### Script Python via XML-RPC

```python
import xmlrpc.client

URL = 'http://localhost:8069'
DB = 'saas-portal-18.local'
USERNAME = 'admin'
PASSWORD = 'admin'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USERNAME, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

# 1. Créer ou trouver un partenaire
partner_id = models.execute_kw(
    DB, uid, PASSWORD,
    'res.partner', 'search',
    [[('email', '=', 'client@example.com')]],
    {'limit': 1}
)

if not partner_id:
    partner_id = models.execute_kw(
        DB, uid, PASSWORD,
        'res.partner', 'create',
        [{
            'name': 'Client Test',
            'email': 'client@example.com',
            'is_company': True,
        }]
    )[0]

# 2. Trouver un plan
plan_id = models.execute_kw(
    DB, uid, PASSWORD,
    'saas_portal.plan', 'search',
    [[]],
    {'limit': 1}
)[0]

# 3. Trouver un serveur
server_id = models.execute_kw(
    DB, uid, PASSWORD,
    'saas_portal.server', 'search',
    [[]],
    {'limit': 1}
)[0]

# 4. Créer le client
client_id = models.execute_kw(
    DB, uid, PASSWORD,
    'saas_portal.client', 'create',
    [{
        'name': 'client-test-001',
        'partner_id': partner_id,
        'plan_id': plan_id,
        'server_id': server_id,
        'state': 'open',
    }]
)

print(f"Client créé avec l'ID: {client_id}")
```

#### Utiliser le script fourni

```bash
python3 saas_portal/scripts/create_saas_data.py
```

Ce script crée automatiquement :
- ✅ Un serveur SaaS
- ✅ Un plan SaaS
- ✅ Un partenaire de test
- ✅ Un client de test

---

## 📊 Structure des données créées

### Enregistrement `saas_portal.client`

```python
{
    'name': 'client-test-001',              # Nom de la base de données
    'partner_id': 123,                      # ID du partenaire
    'plan_id': 45,                          # ID du plan
    'server_id': 1,                         # ID du serveur SaaS
    'state': 'open',                        # État: open, template, deleted
    'expiration_datetime': '2024-12-31',    # Date d'expiration
    'trial': True,                          # Est-ce un essai ?
    'expired': False,                       # Est expiré ?
    'active': True,                         # Actif ?
    'user_id': 2,                          # Commercial responsable
    'support_team_id': False,              # Équipe de support
}
```

### Héritage

Le modèle `saas_portal.client` hérite de :
- `saas_portal.database` : Gestion de la base de données
- `saas_base.client` : Fonctionnalités client de base
- `mail.thread` : Suivi des messages

---

## 🔍 Ce qui se passe techniquement

### 1. Création de l'enregistrement

```python
client = self.env['saas_portal.client'].create({
    'name': 'client-test-001',
    'partner_id': partner_id,
    'plan_id': plan_id,
    'server_id': server_id,
})
```

### 2. Génération automatique

Lors de la création, plusieurs choses sont générées automatiquement :

- **OAuth Application** : Application OAuth pour l'authentification
- **Client ID** : Identifiant unique pour OAuth
- **Public URL** : URL publique calculée depuis le template
- **Host** : Nom d'hôte calculé

### 3. Appel au serveur SaaS

```python
state = {
    'd': client.name,                        # Nom de la DB
    'public_url': client.public_url,         # URL publique
    'e': client.expiration_datetime,        # Expiration
    'r': client.public_url + 'web',          # URL de redirection
    'h': client.host,                        # Host
    'owner_user': owner_user_data,           # Données utilisateur
    't': client.trial,                       # Essai ?
    'db_template': template.name,            # Template à utiliser
}

req, req_kwargs = server._request_server(
    path='/saas_server/new_database',
    state=state,
    client_id=client.client_id,
    scope=['userinfo', 'force_login', 'trial', 'skiptheuse'],
)
res = requests.Session().send(req, **req_kwargs)
```

### 4. Réponse du serveur SaaS

Le serveur SaaS retourne :

```json
{
    "state": "installing",
    "url": "http://client-test-001.saas.local/web",
    "superuser_password": "admin_password",
    "database_token": "token_for_access"
}
```

### 5. Mise à jour du client

Le client est mis à jour avec les informations retournées :

```python
client.write({
    'state': data.get('state'),
    'password': data.get('superuser_password'),
})
```

---

## ⚠️ Limitations et notes importantes

### Pour le développement local

**Sans serveur SaaS séparé :**
- ✅ Vous pouvez créer des clients dans Odoo
- ✅ Les enregistrements sont créés
- ❌ Les bases de données réelles ne sont **pas** créées
- ❌ L'appel au serveur SaaS échouera

**Solution :**
- Créez les clients pour tester l'interface
- Pour créer de vraies bases, installez un serveur SaaS séparé

### Pour la production

**Avec serveur SaaS séparé :**
- ✅ Toutes les fonctionnalités sont disponibles
- ✅ Les bases sont créées automatiquement
- ✅ Les utilisateurs sont redirigés vers leur instance

---

## 📝 Exemple concret : Créer un client de test

### Depuis l'interface Odoo :

1. **SaaS > Clients > Créer**
2. **Nom** : `client-demo-001`
3. **Plan** : `Plan Standard`
4. **Partenaire** : Créez ou sélectionnez un partenaire
5. **Serveur** : `saas-server-001`
6. **Essai** : Cochez si essai gratuit
7. **Enregistrer**

### Vérifier la création :

```python
# Depuis Odoo Python shell ou script
client = env['saas_portal.client'].search([('name', '=', 'client-demo-001')])
print(f"Client: {client.name}")
print(f"Plan: {client.plan_id.name}")
print(f"État: {client.state}")
print(f"Partenaire: {client.partner_id.name}")
```

---

## 🎯 Prochaines étapes après création

1. **Créer la base de données** : Utilisez le bouton "Create Database"
2. **Configurer l'accès** : Configurez les permissions OAuth
3. **Tester l'accès** : Accédez à l'URL publique du client
4. **Configurer les modules** : Installez les modules nécessaires sur la nouvelle instance

---

## 📚 Ressources

- Script de création : `saas_portal/scripts/create_saas_data.py`
- Modèle : `saas_portal/models/saas_portal.py` (classe `SaasPortalClient`)
- Plan : `saas_portal/models/saas_portal.py` (méthode `create_new_database`)

