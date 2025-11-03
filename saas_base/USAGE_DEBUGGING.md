# 🔍 Guide d'utilisation du système de debugging amélioré

## Vue d'ensemble

Le système de debugging amélioré permet de :
- ✅ Capturer automatiquement toutes les erreurs avec contexte complet
- ✅ Logger les opérations avec détails (requêtes, réponses, durée)
- ✅ Créer des tickets automatiquement depuis les erreurs
- ✅ Suivre les erreurs récurrentes
- ✅ Visualiser les erreurs dans une interface Odoo

## 📦 Composants

### 1. DebugContext
Contexte de debugging pour capturer les informations d'erreur

### 2. @debug_log decorator
Décorateur pour logger automatiquement les opérations

### 3. safe_redirect()
Helper pour les redirections avec gestion d'erreur

### 4. handle_exception()
Gestion centralisée des exceptions

### 5. SaasErrorLog model
Modèle pour stocker et visualiser les erreurs

---

## 🚀 Utilisation

### Décorateur @debug_log

```python
from odoo.addons.saas_base.debugging import debug_log

class SaasPortalPlan(models.Model):
    _name = 'saas_portal.plan'
    
    @debug_log(operation_name="create_database", log_request=True, log_response=True)
    def create_new_database(self, **kwargs):
        # Votre code ici
        # Toutes les erreurs seront automatiquement loggées avec contexte
        ...
```

### Gestion des exceptions améliorée

```python
from odoo.addons.saas_base.debugging import handle_exception, DebugContext

@http.route(['/saas_portal/add_new_client'], type='http', auth='public')
def add_new_client(self, **post):
    debug_ctx = DebugContext(
        operation='add_new_client',
        user_id=request.session.uid,
        plan_id=post.get('plan_id')
    )
    
    try:
        # Votre code
        res = plan.create_new_database(...)
        return werkzeug.utils.redirect(res.get('url'))
    except Exception as e:
        # Gestion centralisée des exceptions
        return handle_exception(e, context=debug_ctx)
```

### Redirections avec erreur

```python
from odoo.addons.saas_base.debugging import safe_redirect

# Au lieu de:
return werkzeug.utils.redirect('/error')

# Utiliser:
return safe_redirect(
    '/error',
    error_message='Database limit reached',
    error_code='MAX_DB',
    debug_info={'plan_id': plan_id, 'user_id': user_id}
)
```

---

## 📊 Visualisation des erreurs

### Accès au menu
1. Aller dans **Paramètres > Technique > Error Logs**
2. Ou **SaaS > Error Logs**

### Fonctionnalités
- ✅ Filtrer par état (New, Investigating, Resolved, Ignored)
- ✅ Filtrer par sévérité (Low, Medium, High, Critical)
- ✅ Filtrer par type d'erreur
- ✅ Filtrer par date
- ✅ Grouper par différents critères
- ✅ Créer des tickets automatiquement
- ✅ Marquer comme résolu/ignoré

### Actions disponibles
- **Create Ticket** : Créer un ticket de support depuis l'erreur
- **Resolve** : Marquer l'erreur comme résolue
- **Ignore** : Ignorer cette erreur

---

## 🔧 Migration des contrôleurs existants

### Avant:
```python
@http.route(['/saas_portal/add_new_client'], type='http', auth='public')
def add_new_client(self, **post):
    try:
        res = plan.create_new_database(...)
    except MaximumDBException:
        _logger.info("MaximumDBException")
        url = request.env['ir.config_parameter'].sudo().get_param(...)
        return werkzeug.utils.redirect(url)
```

### Après:
```python
from odoo.addons.saas_base.debugging import debug_log, handle_exception, DebugContext

@http.route(['/saas_portal/add_new_client'], type='http', auth='public')
@debug_log(operation_name="add_new_client")
def add_new_client(self, **post):
    debug_ctx = DebugContext(
        operation='add_new_client',
        user_id=request.session.uid,
        plan_id=post.get('plan_id')
    )
    
    try:
        res = plan.create_new_database(...)
        return werkzeug.utils.redirect(res.get('url'))
    except Exception as e:
        return handle_exception(e, context=debug_ctx)
```

---

## 🎯 Exemple complet

```python
from odoo import http
from odoo.http import request
from odoo.addons.saas_base.debugging import (
    debug_log, 
    handle_exception, 
    DebugContext,
    safe_redirect
)

class SaasPortal(http.Controller):
    
    @http.route(['/saas_portal/create_instance'], type='http', auth='user')
    @debug_log(operation_name="create_instance", log_request=True, log_response=True)
    def create_instance(self, **post):
        """Créer une nouvelle instance SaaS"""
        debug_ctx = DebugContext(
            operation='create_instance',
            user_id=request.session.uid,
            partner_id=request.env.user.partner_id.id,
            plan_id=post.get('plan_id'),
            database=post.get('dbname')
        )
        
        try:
            plan = request.env['saas_portal.plan'].browse(int(post.get('plan_id')))
            client = plan.create_new_database(
                dbname=post.get('dbname'),
                user_id=request.session.uid
            )
            
            return safe_redirect(client.public_url)
            
        except Exception as e:
            # Gestion automatique avec logging complet
            return handle_exception(e, context=debug_ctx, redirect_url='/my/home')
```

---

## 🔍 Recherche et filtrage

Les erreurs peuvent être filtrées par :
- **État** : New, Investigating, Resolved, Ignored
- **Sévérité** : Low, Medium, High, Critical
- **Type d'erreur** : MaximumDBException, AuthenticationError, etc.
- **Opération** : create_database, add_new_client, etc.
- **Date** : Today, This Week, etc.
- **Utilisateur** : Filtrer par user_id
- **Base de données** : Filtrer par database

---

## 📈 Statistiques

Le modèle `saas.error.log` enregistre automatiquement :
- Nombre d'occurrences de la même erreur
- Date de première occurrence
- Date de dernière occurrence
- Contexte complet (JSON)
- Traceback complet

---

## ✅ Avantages

1. **Debugging facilité** : Toutes les erreurs sont capturées avec contexte
2. **Traçabilité** : Historique complet des erreurs
3. **Automatisation** : Création de tickets automatique
4. **Performance** : Monitoring des durées d'exécution
5. **Support** : Informations complètes pour le support client

---

## 🚨 Configuration

Pour activer le logging complet, vérifier que le niveau de log dans `odoo.conf` est configuré :

```ini
[options]
log_level = info
log_handler = :INFO
```

Pour le debugging approfondi :
```ini
log_level = debug
log_handler = :DEBUG
```

