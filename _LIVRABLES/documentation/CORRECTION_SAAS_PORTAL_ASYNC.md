# 🔧 Correction : saas_portal_async - Vue wizard.xml

## ❌ Problème

**Erreur lors de l'installation du module `saas_portal_async` :**

```
ParseError: L'élément '<xpath expr="//field[@name='support_team_id']">' 
ne peut être localisé dans la vue parente
```

**Fichier concerné :** `saas_portal_async/views/wizard.xml`

## 🔍 Analyse

### Cause du Problème

1. Le module `saas_portal` charge `config_wizard_minimal.xml` dans son manifest (ligne 10)
2. Cette vue minimale ne contient **pas** le champ `support_team_id`
3. Le module `saas_portal_async` essaie d'hériter de cette vue et cherche `support_team_id` avec un xpath
4. Le xpath échoue car le champ n'existe pas dans la vue parente

### Structure des Vues

**Vue minimale** (`config_wizard_minimal.xml`) :
```xml
<form string="Create client">
    <group>
        <field name="name" />
        <field name="plan_id" />
        <field name="trial" />
    </group>
</form>
```

**Vue complète** (`config_wizard.xml`) - **NON chargée** :
```xml
<form string="Create client">
    <group>
        <field name="name" />
        <field name="plan_id" />
        <field name="trial" />
        <field name="user_id" />
        <field name="partner_id" />
        <field name="notify_user" />
        <field name="support_team_id" />  <!-- ❌ N'existe pas dans la vue minimale -->
    </group>
</form>
```

## ✅ Solution Appliquée

**Changement du xpath** pour cibler un champ qui existe dans **les deux versions** :

**Avant :**
```xml
<xpath expr="//field[@name='support_team_id']" position="after">
    <field name="async_creation" />
</xpath>
```

**Après :**
```xml
<xpath expr="//field[@name='trial']" position="after">
    <field name="async_creation" />
</xpath>
```

Le champ `trial` existe dans les deux versions (minimale et complète), donc le xpath fonctionnera dans tous les cas.

## 📝 Fichier Modifié

**`saas_portal_async/views/wizard.xml`**

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record model="ir.ui.view" id="saas_portal_create_client_view_form_mod">
        <field name="name">saas_portal_create_client_view_form_inherit</field>
        <field name="model">saas_portal.create_client</field>
        <field name="inherit_id" ref="saas_portal.saas_portal_create_client_view_form" />
        <field name="arch" type="xml">
            <xpath expr="//field[@name='trial']" position="after">
                <field name="async_creation" />
            </xpath>
        </field>
    </record>
</odoo>
```

## ✅ Résultat

- ✅ Le xpath fonctionne avec la vue minimale (chargée par défaut)
- ✅ Le xpath fonctionne également avec la vue complète (si elle était chargée)
- ✅ Le champ `async_creation` sera ajouté après `trial` dans le formulaire

## 🔄 Alternative (Optionnelle)

Si vous souhaitez utiliser la vue complète avec tous les champs, vous pouvez modifier le manifest de `saas_portal` :

```python
'data': [
    # 'wizard/config_wizard_minimal.xml',  # ❌ Commenter
    'wizard/config_wizard.xml',  # ✅ Décommenter si nécessaire
    # ...
]
```

**Note :** Cette alternative n'est pas recommandée si le module utilise intentionnellement la vue minimale.

---

**Date de correction :** 1er Novembre 2025  
**Statut :** ✅ Corrigé

