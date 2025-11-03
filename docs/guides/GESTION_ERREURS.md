# 🛡️ Système de Gestion d'Erreurs Amélioré

## Vue d'Ensemble

Système complet de gestion d'erreurs avec messages utilisateur-friendly et boundaries pour les API.

## 📦 Composants

### 1. Exceptions Personnalisées (`saas_base/exceptions.py`)

**Exceptions avec messages traduits**:
- `MaximumDBException` - Limite de bases atteinte
- `MaximumTrialDBException` - Limite d'essais atteinte
- `SuspendedDBException` - Base suspendue
- `DatabaseCreationException` - Erreur création DB
- `ServerConnectionException` - Erreur connexion serveur

### 2. Gestionnaire d'Erreurs (`saas_base/user_error_handler.py`)

**Fonctionnalités**:
- `AuthenticationError` - Erreur d'authentification
- `PermissionError` - Erreur de permissions
- `DatabaseNotFoundError` - Base non trouvée
- `QuotaExceededError` - Quota dépassé
- `DatabaseLimitExceededError` - Limite DB atteinte

**Decorators**:
- `@handle_api_error` - Pour les API JSON
- `@handle_http_error` - Pour les contrôleurs HTTP

**Fonctions utilitaires**:
- `format_error_response()` - Format standardisé
- `log_error_with_context()` - Logging avec contexte

### 3. Templates d'Erreur (`saas_base/views/error_templates.xml`)

- Page d'erreur user-friendly
- Messages traduits
- Codes d'erreur clairs
- Liens vers support

### 4. Décorateur Webservice Amélioré

Le décorateur `@webservice` dans `saas_server/controllers/main.py` :
- Capture toutes les exceptions
- Retourne des messages JSON user-friendly
- Log les erreurs avec contexte
- Gère les codes HTTP appropriés

## 🚀 Utilisation

### Dans les Contrôleurs API

```python
from odoo.addons.saas_base.user_error_handler import handle_api_error

class MyController(http.Controller):
    
    @http.route('/api/endpoint', type='json', auth='user')
    @handle_api_error
    def my_endpoint(self, **kw):
        # Votre code
        # Les erreurs seront automatiquement gérées
        ...
```

### Lever des Exceptions User-Friendly

```python
from odoo.addons.saas_base.exceptions import DatabaseCreationException
from odoo.addons.saas_base.user_error_handler import AuthenticationError

# Exception avec message utilisateur
raise AuthenticationError("Invalid token")

# Exception avec détails
raise DatabaseCreationException(
    message="Technical error",
    details={'step': 'database_creation', 'error': '...'}
)
```

### Format de Réponse Standardisé

```python
from odoo.addons.saas_base.user_error_handler import format_error_response

# Retourner une erreur formatée
return format_error_response(
    error_code='QUOTA_EXCEEDED',
    message=_("Vous avez atteint votre limite"),
    details={'limit': 10, 'current': 11},
    status_code=400
)
```

## 📊 Codes d'Erreur

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `MAX_DB_REACHED` | Limite DB atteinte | 400 |
| `MAX_TRIAL_DB_REACHED` | Limite essais atteinte | 400 |
| `DB_CREATION_ERROR` | Erreur création | 500 |
| `SERVER_CONNECTION_ERROR` | Serveur indisponible | 503 |
| `AUTH_ERROR` | Erreur authentification | 401 |
| `PERMISSION_ERROR` | Permissions insuffisantes | 403 |
| `DB_NOT_FOUND` | Base non trouvée | 404 |
| `QUOTA_EXCEEDED` | Quota dépassé | 400 |
| `INTERNAL_ERROR` | Erreur interne | 500 |

## 🎨 Messages Utilisateur

Tous les messages sont :
- ✅ Traduits en français (et autres langues)
- ✅ Clairs et compréhensibles
- ✅ Sans jargon technique
- ✅ Avec actions suggérées

## 🔍 Logging Amélioré

Toutes les erreurs sont loggées avec :
- Contexte complet (user, operation, params)
- Traceback complet
- Timestamp
- Enregistrement dans `saas.error.log`

## 📝 Exemples

### Avant (Message technique)
```python
raise Exception('auth error')
# → "auth error" (incompréhensible pour l'utilisateur)
```

### Après (Message user-friendly)
```python
raise AuthenticationError("Invalid OAuth authentication")
# → "Erreur d'authentification. Veuillez vérifier vos identifiants et réessayer."
```

## ✅ Avantages

1. **Expérience Utilisateur** : Messages clairs et compréhensibles
2. **Support** : Codes d'erreur pour faciliter le debugging
3. **Traduction** : Messages traduits automatiquement
4. **Consistance** : Format standardisé pour toutes les erreurs
5. **Debugging** : Logging complet avec contexte

## 🚀 Déploiement

Les améliorations sont automatiquement actives après :
1. Mise à jour du module `saas_base`
2. Mise à jour du module `saas_server`

Les messages d'erreur existants seront améliorés progressivement.

