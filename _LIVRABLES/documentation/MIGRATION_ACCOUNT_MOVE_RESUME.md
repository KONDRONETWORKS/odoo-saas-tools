# ✅ Migration account.invoice → account.move (Odoo 18)

## 📋 Résumé de la Migration

Toutes les références aux anciens modèles `account.invoice` et `account.invoice.line` ont été migrées vers les nouveaux modèles Odoo 18 : `account.move` et `account.move.line`.

---

## 🔧 Fichiers Modifiés

### **1. Fichiers XML**

#### `saas_portal_sale/data/mail_template_data.xml`
- ✅ `account.model_account_invoice` → `account.model_account_move`

#### `saas_portal_sale_subscription/views/account_invoice_view.xml`
- ✅ `model="account.invoice"` → `model="account.move"`
- ✅ `model="account.invoice.line"` → `model="account.move.line"`
- ✅ `inherit_id ref="account.invoice_form"` → `inherit_id ref="account.view_move_form"`
- ✅ `inherit_id ref="account.view_invoice_line_form"` → `inherit_id ref="account.view_move_line_form"`

#### `saas_portal_sale/views/saas_portal.xml`
- ✅ `form_view_ref': 'account.invoice_form'` → `form_view_ref': 'account.view_move_form'`

---

### **2. Fichiers Python**

#### `saas_portal_sale_subscription/models/account_invoice.py`
**Changements de classe :**
- ✅ `class AccountInvoice(_inherit='account.invoice')` → `class AccountMove(_inherit='account.move')`
- ✅ `class AccountInvoiceLine(_inherit='account.invoice.line')` → `class AccountMoveLine(_inherit='account.move.line')`

**Changements de méthodes :**
- ✅ `invoice_validate()` → `action_post()`
  - Ajout de filtrage pour ne traiter que les factures : `invoices = self.filtered(lambda m: m.is_invoice(include_receipts=True))`
- ✅ `action_invoice_paid()` → `_invoice_paid_hook()`
  - Ajout de `raise_if_not_found=False` pour le template
  - Correction : `compositon_mode` → `composition_mode`

**Changements de champs (AccountMoveLine) :**
- ✅ `date_invoice = fields.Date(related='invoice_id.date_invoice')` → `invoice_date = fields.Date(related='move_id.invoice_date')`
- ✅ `state = fields.Selection(related='invoice_id.state')` → `move_state = fields.Selection(related='move_id.state')`
- ✅ `invoice_id` → `move_id` (dans les relations)

#### `saas_portal_sale_subscription/models/saas_portal.py`
**Changements de relations :**
- ✅ `invoice_line_ids = fields.One2many('account.invoice.line', ...)` → `invoice_line_ids = fields.One2many('account.move.line', ...)`
- ✅ `@api.depends('invoice_line_ids.invoice_id.state')` → `@api.depends('invoice_line_ids.move_id.payment_state')`
- ✅ `line.invoice_id.state == 'paid'` → `line.move_id.payment_state == 'paid'`
- ✅ `record.env['account.invoice.line']` → `record.env['account.move.line']`
- ✅ `invoice_line.invoice_id` → `invoice_line.move_id`

#### `saas_portal_sale_subscription/wizard/subscription_wizard.py`
**Changements de modèles :**
- ✅ `invoice_line_ids = fields.Many2many('account.invoice.line', ...)` → `invoice_line_ids = fields.Many2many('account.move.line', ...)`
- ✅ `self.env['account.invoice.line'].search([('partner_id', '=', ...)])` → `self.env['account.move.line'].search([('move_id.partner_id', '=', ...)])`

---

## 📊 Mapping des Changements

| Ancien (Odoo 11) | Nouveau (Odoo 18) | Notes |
|------------------|-------------------|-------|
| `account.invoice` | `account.move` | Modèle unifié pour factures/bons |
| `account.invoice.line` | `account.move.line` | Lignes de mouvement |
| `account.model_account_invoice` | `account.model_account_move` | External ID XML |
| `account.invoice_form` | `account.view_move_form` | Vue formulaire |
| `invoice_validate()` | `action_post()` | Validation facture |
| `action_invoice_paid()` | `_invoice_paid_hook()` | Hook paiement |
| `invoice_id` | `move_id` | Relation vers mouvement |
| `date_invoice` | `invoice_date` | Date facture |
| `state == 'paid'` | `payment_state == 'paid'` | État paiement |
| `line.invoice_id.state` | `line.move_id.payment_state` | État via relation |

---

## ✅ Vérifications Effectuées

1. ✅ Tous les fichiers XML mis à jour
2. ✅ Tous les modèles Python migrés
3. ✅ Méthodes remplacées par leurs équivalents Odoo 18
4. ✅ Relations et dépendances corrigées
5. ✅ Filtrage ajouté pour ne traiter que les factures (pas les autres types de moves)

---

## 🎯 Tests Recommandés

### Test 1 : Création et Validation de Facture
- Créer une facture client
- Valider la facture (vérifier que `action_post()` fonctionne)
- Vérifier que les lignes de facture sont correctement liées

### Test 2 : Paiement de Facture
- Marquer une facture comme payée
- Vérifier que `_invoice_paid_hook()` est appelé
- Vérifier que les emails sont envoyés correctement

### Test 3 : Relations SaaS
- Vérifier que `invoice_line_ids` fonctionne correctement
- Vérifier que `saas_client_id` est correctement assigné
- Vérifier les calculs de `period_paid`

---

## ⚠️ Points d'Attention

1. **Filtrage des Factures** : Les méthodes `action_post()` et `_invoice_paid_hook()` filtrent maintenant avec `is_invoice(include_receipts=True)` pour ne traiter que les factures, pas les autres types de moves.

2. **Payment State** : Utiliser `payment_state == 'paid'` au lieu de `state == 'paid'`.

3. **Relations** : Toutes les relations passent maintenant par `move_id` au lieu de `invoice_id`.

4. **Templates Email** : Ajout de `raise_if_not_found=False` pour éviter les erreurs si le template n'existe pas.

---

## 📝 Statut

✅ **Migration complète** - Tous les fichiers ont été migrés avec succès.

Les modules ont été mis à jour et se chargent sans erreurs critiques.

