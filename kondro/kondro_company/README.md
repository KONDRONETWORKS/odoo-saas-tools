# Module KONDRONETWORKS - Configuration Entreprise

## Description

Module de configuration spécifique pour l'entreprise **KONDRONETWORKS** en **Côte d'Ivoire**.

Ce module configure automatiquement :
- Les informations de l'entreprise KONDRONETWORKS
- La localisation Côte d'Ivoire (devise XOF, langue française)
- Les paramètres fiscaux et légaux ivoiriens
- Les paramètres par défaut pour tous les modules KONDRO

## Installation

1. Installer le module depuis l'interface Odoo : **Apps > Rechercher "KONDRONETWORKS"**
2. Le module configurera automatiquement l'entreprise

## Configuration

### Informations Entreprise

- **Nom:** KONDRONETWORKS
- **Pays:** Côte d'Ivoire (CI)
- **Devise:** XOF (Franc CFA Ouest-Africain)
- **Langue:** Français (fr_FR)
- **Fuseau horaire:** Africa/Abidjan
- **Email:** contact@kondronetworks.com
- **Site web:** https://www.kondronetworks.com

### Paramètres Configurés

- Devise principale: XOF
- Pays par défaut: Côte d'Ivoire
- Langue par défaut: Français
- Fuseau horaire: Africa/Abidjan

## Dépendances

- `base`
- `base_setup`
- `account`
- `l10n_ci` (si disponible)

## Structure

```
kondro_company/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── res_company.py
├── data/
│   ├── res_company_data.xml
│   ├── res_currency_data.xml
│   ├── res_country_data.xml
│   ├── res_lang_data.xml
│   ├── ir_config_parameter_data.xml
│   └── res_users_data.xml
├── views/
│   └── res_company_views.xml
└── security/
    └── ir.model.access.csv
```

## Auteur

**KONDRONETWORKS**
- Website: https://www.kondronetworks.com
- Email: contact@kondronetworks.com

## Licence

LGPL-3

