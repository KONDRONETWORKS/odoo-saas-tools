# ✅ Correction : Permissions OAuth + Création Automatique

## Problème Initial

Erreur lors de la création d'un serveur avec "Generate Demo Plan" :
```
Vous n'êtes pas autorisé à créer des enregistrements 'OAuth Application' (oauth.application).
Aucun groupe n'autorise actuellement cette opération.
```

## Solutions Appliquées

### 1️⃣ Permissions OAuth (`saas_oauth_provider/security/ir.model.access.csv`)

**Fichier modifié**: `saas_oauth_provider/security/ir.model.access.csv`

```csv
# AVANT:
access_oauth_application,model_oauth_application,base.group_user,1,0,0,0
access_oauth_access_token,model_oauth_access_token,,1,0,0,0

# APRÈS:
access_oauth_application,model_oauth_application,base.group_user,1,1,1,0
access_oauth_access_token,model_oauth_access_token,,1,1,1,0
```

**Changements**: Lecture, écriture et création activées (pas de suppression).

### 2️⃣ Création Automatique OAuth Apps

**Pour `saas_portal.server`** (`saas_portal/models/saas_portal.py` ligne 66-78) :
```python
@api.model_create_multi
def create(self, vals_list):
    # Créer les OAuth applications manuellement pour chaque enregistrement
    for vals in vals_list:
        # Si oauth_application_id n'est pas fourni, créer une OAuth app
        if 'oauth_application_id' not in vals or not vals.get('oauth_application_id'):
            oauth_app = self.env['oauth.application'].sudo().create({})
            vals['oauth_application_id'] = oauth_app.id
    
    records = super(SaasPortalServer, self).create(vals_list)
    for record in records:                                                                                                            
        record.oauth _application_id._get_access_token(create=True)
    return records
```

**Pour `saas_portal.database`** (`saas_portal/models/saas_portal.py` ligne 569-578) :```python
@api.model_create_multi
def create(self, vals_list):
    # Créer les OAuth applications manuellement pour chaque enregistrement
    for vals in vals_list:
        # Si oauth_application_id n'est pas fourni, créer une OAuth app
        if 'oauth_application_id' not in vals or not vals.get('oauth_application_id'):
            oauth_app = self.env['oauth.application'].sudo().create({})
            vals['oauth_application_id'] = oauth_app.id
    
    return super(SaasPortalDatabase, self).create(vals_list)
```

## 🚀 Actions Requises

**1. Redémarrer Odoo** pour charger les nouvelles configurations :
```bash
# Arrêter Odoo
pkill -f odoo

# Redémarrer Odoo
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
./.venv/bin/python odoo/odoo-bin -c infrastructure/config/odoo.conf --dev=reload
```

**2. OU mettre à jour le module** `saas_oauth_provider` dans Odoo :
1. Ouvrir Odoo
2. Settings > Apps
3. Rechercher `saas_oauth_provider`
4. Cliquer sur "Upgrade"

**3. Vérifier que le module `saas_portal` est à jour**

## 🔍 Vérification

Après redémarrage/mise à jour, vous devriez pouvoir :
1. ✅ Créer un serveur sans erreur de permissions
2. ✅ Utiliser "Generate Demo Plan" sans problème
3. ✅ Créer des clients automatiquement
4. ✅ Les OAuth Applications sont créées automatiquement

## 📝 Notes Techniques

**Pourquoi cette correction ?**

- `saas_portal.server` et `saas_portal.database` utilisent `_inherits = {'oauth.application': 'oauth_application_id'}`
- `_inherits` crée automatiquement un enregistrement lié
- Sans les droits de création sur `oauth.application`, l’opération échouait
- Il faut créer l’OAuth app en amont

---

**Status**: ✅ **Corrections appliquées - Redémarrage requis**
