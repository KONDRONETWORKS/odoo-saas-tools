# 📝 Guide : Comment les futurs clients s'enregistrent

## 🔄 Processus d'enregistrement automatique

### Vue d'ensemble

Les futurs clients s'enregistrent automatiquement via le portail web public. Le processus est entièrement automatisé grâce au module `saas_portal_signup`.

---

## 🌐 Processus étape par étape

### 1️⃣ **Inscription sur le portail web**

Le client accède à la page d'inscription :
- **URL publique** : `/web/signup`
- **Avec paramètres** : `/web/signup?dbname=mon-client&plan_id=1`

**Champs requis :**
- Nom complet
- Email (qui devient le login)
- Mot de passe
- Confirmation du mot de passe
- Nom de la base de données (`dbname`)
- Plan SaaS sélectionné (`plan_id`)

### 2️⃣ **Création du compte utilisateur**

Le module `auth_signup` d'Odoo crée :
- Un enregistrement `res.users`
- Un enregistrement `res.partner` associé
- Attribution du groupe **Portal** automatiquement

### 3️⃣ **Redirection vers la création du client**

Après l'inscription réussie, le client est automatiquement redirigé vers :
```
/saas_portal/add_new_client?dbname=mon-client&plan_id=1
```

### 4️⃣ **Création automatique du client**

La route `/saas_portal/add_new_client` appelle :
```python
plan.create_new_database(
    dbname='mon-client',
    user_id=<ID_utilisateur>,
    partner_id=<ID_partenaire>,
    trial=False
)
```

**Ce qui est créé automatiquement :**
- ✅ Enregistrement `saas_portal.client`
- ✅ Base de données client sur le serveur SaaS
- ✅ Application OAuth pour l'authentification
- ✅ Configuration initiale selon le plan

### 5️⃣ **Redirection vers la base de données client**

Le client est automatiquement redirigé vers sa nouvelle base de données avec un token d'authentification.

---

## 🔧 Configuration requise

### Modules nécessaires

1. **`saas_portal`** : Module principal
2. **`saas_portal_signup`** : Gestion de l'inscription automatique
3. **`auth_signup`** : Système d'inscription Odoo (core)

### Vérification de l'installation

```bash
# Vérifier que les modules sont installés
docker compose -f config/docker-compose.windows.yml exec -T odoo odoo-bin shell -d saas-portal-18.local
```

Dans le shell Odoo :
```python
env['ir.module.module'].search([
    ('name', 'in', ['saas_portal', 'saas_portal_signup', 'auth_signup']),
    ('state', '=', 'installed')
])
```

---

## 🔍 Pourquoi la liste des clients est vide ?

### Raison principale : Filtre par défaut

La vue des clients a un **filtre par défaut** qui affiche uniquement les clients avec `state='open'` :

```xml
<field name="context">{'search_default_current': 1}</field>
```

Ce filtre masque :
- ❌ Clients en brouillon (`state='draft'`)
- ❌ Clients en attente (`state='pending'`)
- ❌ Clients supprimés (`state='deleted'`)

### Solutions

#### Option 1 : Désactiver le filtre

Dans l'interface Odoo :
1. Allez dans **SaaS > Clients**
2. Cliquez sur le filtre **"In Progress"** pour le désactiver
3. Tous les clients seront visibles

#### Option 2 : Vérifier tous les états

Dans l'interface Odoo :
1. Allez dans **SaaS > Clients**
2. Utilisez la barre de recherche
3. Effacez tous les filtres actifs
4. Tous les clients seront visibles, quelle que soit leur état

#### Option 3 : Créer un client manuellement pour tester

Depuis **SaaS > Plans** :
1. Sélectionnez un plan
2. Cliquez sur **"Create Client"**
3. Remplissez le formulaire
4. Le client sera créé avec `state='open'` et visible dans la liste

---

## 📊 États des clients

| État | Description | Visible avec filtre "In Progress" ? |
|------|-------------|-------------------------------------|
| `draft` | Nouveau client, pas encore actif | ❌ Non |
| `open` | Client actif et opérationnel | ✅ Oui |
| `pending` | Client en attente de traitement | ❌ Non |
| `template` | Template de base de données | ❌ Non |
| `deleted` | Client supprimé | ❌ Non |

---

## 🧪 Test du processus d'enregistrement

### 1. Accéder à la page d'inscription

```
http://localhost:8069/web/signup?dbname=test-client&plan_id=1
```

Remplacez :
- `test-client` : Nom de votre base de données
- `1` : ID de votre plan SaaS

### 2. Remplir le formulaire

- **Nom** : Test Client
- **Email** : test@example.com
- **Mot de passe** : votre mot de passe
- **Confirmation** : même mot de passe
- **Nom de la base** : test-client (si pas pré-rempli)
- **Plan** : Sélectionnez un plan (si pas pré-sélectionné)

### 3. Soumettre le formulaire

Après soumission :
1. Le compte utilisateur est créé
2. Vous êtes redirigé vers `/saas_portal/add_new_client`
3. La base de données client est créée
4. Vous êtes redirigé vers votre nouvelle base de données

### 4. Vérifier dans Odoo

1. Connectez-vous à Odoo Portal (en tant qu'administrateur)
2. Allez dans **SaaS > Clients**
3. **Désactivez le filtre "In Progress"**
4. Vous devriez voir le nouveau client

---

## 🔐 Permissions et sécurité

### Groupes d'utilisateurs

Lors de l'inscription, les utilisateurs reçoivent automatiquement :
- **Portal** : Accès au portail client
- **View Online Payment Options** : Accès aux options de paiement

### Limitations

Les clients peuvent créer des bases de données selon les limites du plan :
- `maximum_allowed_dbs_per_partner` : Nombre maximum de bases de données
- `maximum_allowed_trial_dbs_per_partner` : Nombre maximum d'essais

---

## 🐛 Dépannage

### Problème : "Domain exists"

**Cause** : Le nom de base de données est déjà utilisé.

**Solution** : Utilisez un nom de base de données différent.

### Problème : "Limit of databases reached"

**Cause** : Le partenaire a atteint la limite de bases de données pour ce plan.

**Solution** : Vérifiez les paramètres du plan ou créez un nouveau plan.

### Problème : Aucun client visible dans la liste

**Cause** : Le filtre "In Progress" masque les clients avec d'autres états.

**Solution** : 
1. Désactivez le filtre "In Progress"
2. Ou vérifiez l'état des clients via le shell Odoo :
```python
env['saas_portal.client'].search([]).mapped('state')
```

### Problème : Erreur "Connection refused" lors de la création

**Cause** : Le serveur SaaS n'est pas accessible ou mal configuré.

**Solution** : 
1. Vérifiez que le serveur SaaS est actif
2. Vérifiez la configuration du serveur (host, port)
3. Consultez le guide `GUIDE_ERREUR_CONNEXION_TEMPLATE.md`

---

## 📝 Code de référence

### Route d'inscription

```python
# saas_portal_signup/controllers/main.py
@http.route()
def web_auth_signup(self, *args, **kw):
    if not kw.get('redirect', False) and kw.get('dbname', False):
        redirect = '/saas_portal/add_new_client'
        kw['redirect'] = '%s?dbname=%s&plan_id=%s' % (
            redirect, kw['dbname'], kw['plan_id']
        )
    return super(AuthSignupHome, self).web_auth_signup(*args, **kw)
```

### Création du client

```python
# saas_portal/controllers/main.py
@http.route(['/saas_portal/add_new_client'], type='http', auth='public', website=True)
def add_new_client(self, redirect_to_signup=False, **post):
    uid = request.session.uid
    # ... validation ...
    res = plan.create_new_database(
        dbname=dbname,
        user_id=user_id,
        partner_id=partner_id,
        trial=trial,
    )
    return werkzeug.utils.redirect(res.get('url'))
```

### Méthode de création

```python
# saas_portal/models/saas_portal.py
def _create_new_database(self, dbname=None, client_id=None, partner_id=None, ...):
    # Création de l'enregistrement client
    client = p_client.create(vals)
    # Création de la base de données sur le serveur
    # ...
    return {'url': url, 'id': client.id, 'client_id': client_id}
```

---

## ✅ Checklist de configuration

Avant que les clients puissent s'enregistrer, vérifiez :

- [ ] Module `saas_portal_signup` est installé
- [ ] Module `auth_signup` est activé
- [ ] Au moins un plan SaaS est créé et configuré
- [ ] Un serveur SaaS est configuré et accessible
- [ ] Le paramètre `saas_portal.base_saas_domain` est configuré
- [ ] Les templates de bases de données sont créés (si nécessaire)
- [ ] Les emails de notification sont configurés (optionnel)

---

## 🎯 Résumé

1. **Les clients s'enregistrent via** : `/web/signup?dbname=X&plan_id=Y`
2. **Le processus est automatique** : Création utilisateur → Création client → Création base de données
3. **Le problème de liste vide** : C'est dû au filtre "In Progress" qui masque les clients avec `state != 'open'`
4. **Solution immédiate** : Désactivez le filtre "In Progress" dans la vue des clients

---

**Dernière mise à jour** : 2025-01-03

