# 🚀 Guide Complet : Création d'un Nouveau Client SaaS

## Vue d'Ensemble

Ce guide vous accompagne dans la création complète d'un nouveau client SaaS, incluant :
1. ✅ Création d'un Serveur SaaS
2. ✅ Création d'un Plan
3. ✅ Création d'un Client
4. ✅ Configuration et Déploiement

---

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :

- ✅ Odoo 18 installé et fonctionnel
- ✅ Module `saas_portal` installé dans le portail
- ✅ Module `saas_server` installé sur le serveur
- ✅ PostgreSQL configuré et accessible
- ✅ Domaine de base SaaS configuré (`base_saas_domain`)

---

## ÉTAPE 1 : Créer un Serveur SaaS 🖥️

### Via l'Interface Odoo

1. **Accéder au Portail Principal**
   ```
   http://localhost:8069/web?db=saas-portal-18.local
   ```

2. **Aller dans SaaS > Servers**
   - Menu : `SaaS` > `Servers`
   - Ou recherche : `Servers`

3. **Créer un nouveau Serveur**
   - Cliquer sur `Create`
   - Remplir les champs :
     ```
     Name: server-1
     Host: localhost (ou IP du serveur)
     Database UUID: (auto-généré ou manuel)
     Max Clients: 100
     Active: ✓
     ```

4. **Configurer OAuth**
   - Dans le serveur, aller dans `Settings > OAuth Providers`
   - Créer/Configurer le provider "SaaS"
   - Noter le `Client ID` (UUID du serveur)

5. **Synchroniser le Serveur**
   - Retourner au Portail
   - Ouvrir le serveur créé
   - Cliquer sur `Sync Server`

### Via Script Python

```python
# scripts/create_server.py
from odoo import api, SUPERUSER_ID
from odoo.tools import config

# Connexion au portail
registry = api.Environment(
    cr=db_connect('saas-portal-18.local'),
    uid=SUPERUSER_ID
)

# Créer le serveur
server = registry['saas_portal.server'].create({
    'name': 'server-1',
    'host': 'localhost',
    'max_clients': 100,
    'state': 'open',
})

print(f"✅ Serveur créé: {server.name} (UUID: {server.client_id})")
```

---

## ÉTAPE 2 : Créer un Plan 💰

### Via l'Interface Odoo

1. **Aller dans SaaS > Plans**
   - Menu : `SaaS` > `Plans`

2. **Créer un nouveau Plan**
   - Cliquer sur `Create`
   - Remplir les champs :
     ```
     Name: Plan Starter
     Description: Plan de base pour nouveaux clients
     Server: server-1 (sélectionner)
     Price: 99.00 €/mois
     Trial Period: 14 jours
     ```

3. **Configurer le Template DB**
   - Template DB: `template-starter.odoo.local`
   - Cliquer sur `Create Template DB`
   - Attendre la création (quelques minutes)

4. **Configurer le Template**
   - Cliquer sur `Log in to template DB`
   - Installer les modules nécessaires
   - Configurer les paramètres par défaut
   - Configurer les droits utilisateur

5. **Synchroniser**
   - Cliquer sur `Sync Server`

### Via Script Python

```python
# scripts/create_plan.py
registry = api.Environment(
    cr=db_connect('saas-portal-18.local'),
    uid=SUPERUSER_ID
)

# Récupérer le serveur
server = registry['saas_portal.server'].search([
    ('name', '=', 'server-1')
], limit=1)

# Créer le plan
plan = registry['saas_portal.plan'].create({
    'name': 'Plan Starter',
    'server_id': server.id,
    'trial': 14,  # 14 jours d'essai
    'price': 99.00,
    'description': 'Plan de base pour nouveaux clients',
})

print(f"✅ Plan créé: {plan.name} (ID: {plan.id})")
```

---

## ÉTAPE 3 : Créer un Client 👤

### Via l'Interface Odoo (Wizard)

1. **Depuis un Plan**
   - Aller dans `SaaS > Plans`
   - Sélectionner un plan
   - Cliquer sur `Create Client`

2. **Remplir le Formulaire**
   ```
   Database name: client-1 (ou auto-généré)
   Plan: Plan Starter (déjà sélectionné)
   Partner: (sélectionner ou créer)
   User: (sélectionner ou créer)
   Notify user: ✓
   Trial: (cocher si essai)
   ```

3. **Créer**
   - Cliquer sur `Create`
   - Attendre la création (quelques minutes)
   - Redirection automatique vers le client

### Via l'Interface Directe

1. **Aller dans SaaS > Clients**
   - Menu : `SaaS` > `Clients`

2. **Créer un nouveau Client**
   - Cliquer sur `Create`
   - Remplir :
     ```
     Name: client-1
     Plan: Plan Starter
     Server: server-1
     Partner: (sélectionner)
     Trial: ✓ (si essai)
     ```

3. **Déployer**
   - Cliquer sur `Create & Deploy`
   - Ou utiliser le bouton `Create Database`

### Via Script Python

```python
# scripts/create_client.py
registry = api.Environment(
    cr=db_connect('saas-portal-18.local'),
    uid=SUPERUSER_ID
)

# Récupérer le plan
plan = registry['saas_portal.plan'].search([
    ('name', '=', 'Plan Starter')
], limit=1)

# Récupérer ou créer le partner
partner = registry['res.partner'].search([
    ('email', '=', 'client@example.com')
], limit=1)

if not partner:
    partner = registry['res.partner'].create({
        'name': 'Client Example',
        'email': 'client@example.com',
    })

# Créer le client
result = plan.create_new_database(
    dbname='client-1',
    partner_id=partner.id,
    user_id=SUPERUSER_ID,
    trial=False,
    notify_user=True,
)

client = registry['saas_portal.client'].browse(result['id'])
print(f"✅ Client créé: {client.name}")
print(f"   URL: {client.public_url}")
print(f"   State: {client.state}")
```

---

## ÉTAPE 4 : Processus Automatisé Complet 🔄

### Script Python Complet

```python
#!/usr/bin/env python3
"""
Script complet pour créer un nouveau client SaaS
Création: Serveur → Plan → Client
"""
import sys
import os

# Ajouter le chemin Odoo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from odoo import api, SUPERUSER_ID
from odoo.tools import config
from odoo.service.db import db_connect

def create_complete_saas_setup(
    portal_db='saas-portal-18.local',
    server_name='server-1',
    server_host='localhost',
    plan_name='Plan Starter',
    plan_price=99.00,
    plan_trial_days=14,
    client_name='client-1',
    partner_email='client@example.com',
    partner_name='Client Example',
    trial=False,
):
    """
    Créer un setup SaaS complet : Serveur → Plan → Client
    """
    print("🚀 Création du setup SaaS complet...\n")
    
    # Connexion au portail
    try:
        cr = db_connect(portal_db)
        registry = api.Environment(cr, SUPERUSER_ID, {})
    except Exception as e:
        print(f"❌ Erreur connexion portail: {e}")
        return False
    
    # 1. Créer ou récupérer le serveur
    print(f"📦 Étape 1: Création du serveur '{server_name}'...")
    server = registry['saas_portal.server'].search([
        ('name', '=', server_name)
    ], limit=1)
    
    if not server:
        server = registry['saas_portal.server'].create({
            'name': server_name,
            'host': server_host,
            'max_clients': 100,
            'state': 'open',
        })
        print(f"   ✅ Serveur créé: {server.name}")
    else:
        print(f"   ℹ️  Serveur existant: {server.name}")
    
    # Synchroniser le serveur
    try:
        server.action_sync_server()
        print(f"   ✅ Serveur synchronisé")
    except Exception as e:
        print(f"   ⚠️  Erreur synchronisation: {e}")
    
    # 2. Créer ou récupérer le plan
    print(f"\n💰 Étape 2: Création du plan '{plan_name}'...")
    plan = registry['saas_portal.plan'].search([
        ('name', '=', plan_name)
    ], limit=1)
    
    if not plan:
        plan = registry['saas_portal.plan'].create({
            'name': plan_name,
            'server_id': server.id,
            'trial': plan_trial_days,
            'price': plan_price,
            'description': f'Plan {plan_name}',
        })
        print(f"   ✅ Plan créé: {plan.name}")
    else:
        print(f"   ℹ️  Plan existant: {plan.name}")
    
    # 3. Créer ou récupérer le partner
    print(f"\n👤 Étape 3: Création du partner...")
    partner = registry['res.partner'].search([
        ('email', '=', partner_email)
    ], limit=1)
    
    if not partner:
        partner = registry['res.partner'].create({
            'name': partner_name,
            'email': partner_email,
        })
        print(f"   ✅ Partner créé: {partner.name}")
    else:
        print(f"   ℹ️  Partner existant: {partner.name}")
    
    # 4. Créer le client
    print(f"\n🚀 Étape 4: Création du client '{client_name}'...")
    client = registry['saas_portal.client'].search([
        ('name', '=', client_name)
    ], limit=1)
    
    if client:
        print(f"   ⚠️  Client existant: {client.name}")
        print(f"   ℹ️  URL: {client.public_url}")
        return client
    
    try:
        result = plan.create_new_database(
            dbname=client_name,
            partner_id=partner.id,
            user_id=SUPERUSER_ID,
            trial=trial,
            notify_user=False,  # Pas d'email pour les tests
        )
        
        client = registry['saas_portal.client'].browse(result['id'])
        
        # Synchroniser le serveur après création
        client.server_id.action_sync_server()
        
        print(f"   ✅ Client créé: {client.name}")
        print(f"   ✅ URL: {client.public_url}")
        print(f"   ✅ State: {client.state}")
        
        return client
        
    except Exception as e:
        print(f"   ❌ Erreur création client: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    finally:
        cr.close()


if __name__ == '__main__':
    # Exemple d'utilisation
    client = create_complete_saas_setup(
        portal_db='saas-portal-18.local',
        server_name='server-1',
        plan_name='Plan Starter',
        client_name='client-test-1',
        partner_email='test@example.com',
        partner_name='Test Client',
        trial=True,
    )
    
    if client:
        print(f"\n✅ Setup complet créé avec succès!")
        print(f"   Accéder à: {client.public_url}")
    else:
        print(f"\n❌ Échec de la création")
```

---

## 📊 Vérification

### Vérifier la Création

```bash
# Lister les bases de données
psql -l | grep -E "(client|server|template)"

# Vérifier via Odoo
# Portal > SaaS > Clients
# Vérifier que le client apparaît avec state = 'open'
```

### Accéder au Client

```
URL: http://client-1.saas-portal-18.local:8069/web
Login: admin / admin (par défaut)
```

---

## 🔄 Workflow Complet Simplifié

### Méthode Rapide (Script)

```bash
# 1. Créer le setup complet
python3 scripts/create_complete_setup.py

# 2. Vérifier
python3 check_modules.py
```

### Méthode Interface (Pas à Pas)

1. **SaaS > Servers** → Create → Remplir → Save → Sync
2. **SaaS > Plans** → Create → Remplir → Create Template DB → Configurer → Sync
3. **SaaS > Plans** → Sélectionner Plan → Create Client → Remplir → Create

---

## 📝 Checklist Complète

### Avant de Commencer
- [ ] Odoo 18 installé
- [ ] Modules SaaS installés
- [ ] PostgreSQL configuré
- [ ] Domaine de base configuré (`base_saas_domain`)

### Création Serveur
- [ ] Serveur créé dans Portal
- [ ] OAuth configuré sur le serveur
- [ ] UUID du serveur noté
- [ ] Serveur synchronisé

### Création Plan
- [ ] Plan créé
- [ ] Template DB créé
- [ ] Modules installés dans template
- [ ] Configuration template terminée
- [ ] Plan synchronisé

### Création Client
- [ ] Partner créé ou sélectionné
- [ ] Client créé
- [ ] Instance déployée
- [ ] Client accessible via URL
- [ ] Login fonctionne

---

## 🎯 Prochaines Étapes

Après création du client :

1. **Configurer le Client**
   - Accéder à l'instance
   - Installer modules additionnels
   - Configurer les paramètres

2. **Notifier le Client**
   - Envoyer email avec URL et credentials
   - Fournir documentation

3. **Monitoring**
   - Surveiller les logs
   - Vérifier les quotas
   - Gérer les backups

---

**Status**: ✅ **Guide complet créé**

