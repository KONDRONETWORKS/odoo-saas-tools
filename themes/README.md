# 🎨 Thèmes Odoo - Dossier Themes

Ce dossier contient tous les modules de thèmes personnalisés pour Odoo 18.

## 📋 Structure

```
themes/
├── README.md                    ← Ce fichier
├── theme_backend_odoo12/        ← Thème backend Odoo 12 (Blueberry)
├── theme_crest/                 ← Thème Crest (complet)
├── theme_diwy/                  ← Thème Diwy
├── theme_hue_backend/           ← Thème backend Hue
├── theme_magic3brothers/        ← Thème Magic 3 Brothers (Carousel)
├── theme_modern/                ← Thème moderne
├── theme_slife_backend/         ← Thème backend SLife
└── theme_ylhc_base/             ← Base de thème YLHC
```

## 🎯 Versions

Tous les thèmes sont configurés pour **Odoo 18.0.1.0.0**.

## 📦 Installation

### Méthode 1 : Via l'interface Odoo

1. Aller dans **Apps** > **Update Apps List**
2. Rechercher le thème souhaité
3. Cliquer sur **Install**

### Méthode 2 : Via la ligne de commande

```bash
# Installer un thème spécifique
docker compose -f config/docker-compose.simple.yml exec odoo odoo -u theme_name -d odoo

# Installer tous les thèmes
docker compose -f config/docker-compose.simple.yml exec odoo odoo -u modern_theme,hue_backend_theme -d odoo
```

## 🔧 Configuration

### Ajouter un nouveau thème

1. Créer un nouveau dossier dans `themes/`
2. Ajouter le fichier `__manifest__.py` avec la version `18.0.1.0.0`
3. Suivre la structure standard Odoo pour les modules

### Structure minimale d'un thème

```
mon_theme/
├── __init__.py
├── __manifest__.py
├── static/
│   └── description/
│       └── icon.png
└── views/
```

## 📝 Liste des Thèmes

| Thème | Version | Catégorie | Description | Statut |
|-------|---------|-----------|-------------|--------|
| `theme_backend_odoo12` | 18.0.1.0.1 | `Themes/Backend` | Thème backend style Odoo 12 (Blueberry) | ✅ |
| `theme_crest` | 18.0.1.0.2 | `Themes/eCommerce` | Thème Crest complet (e-commerce) | ✅ |
| `theme_diwy` | 18.0.1.0.0 | `Themes/Backend` | Thème Diwy | ✅ |
| `theme_hue_backend` | 18.0.1.0.0 | `Themes/Backend` | Thème backend Hue | ✅ |
| `theme_magic3brothers` | 18.0.1.0.0 | `Themes/Website` | Thème Magic 3 Brothers (Carousel) | ✅ |
| `theme_modern` | 18.0.1.0.0 | `Themes/Backend` | Thème moderne responsive | ✅ |
| `theme_slife_backend` | 18.0.1.0.0 | `Themes/Backend` | Thème backend SLife | ✅ |
| `theme_ylhc_base` | 18.0.1.0.0 | `Themes/Backend` | Base de thème YLHC | ✅ |

## 📂 Catégories

Tous les thèmes sont organisés en catégories standardisées :

- **`Themes/Backend`** : Thèmes pour l'interface backend (administration)
- **`Themes/Website`** : Thèmes pour l'interface frontend (site public)
- **`Themes/eCommerce`** : Thèmes complets pour sites e-commerce

Voir [CATEGORIES.md](CATEGORIES.md) pour plus de détails.

## 🚀 Utilisation

### Activer un thème

1. Aller dans **Settings** > **Themes**
2. Sélectionner le thème souhaité
3. Cliquer sur **Apply**

### Personnaliser un thème

Les thèmes peuvent être personnalisés via :
- **Settings** > **Themes** > **Customize**
- Fichiers CSS/SCSS dans `static/src/css/`
- Templates XML dans `views/`

## 🔄 Mise à jour

Pour mettre à jour tous les thèmes vers la version 18.0.1.0.0 :

```bash
# Exécuter le script de mise à jour
./scripts/update_theme_versions.sh
```

## 📚 Documentation

- [Guide de création de thèmes Odoo](https://www.odoo.com/documentation/18.0/developer/reference/backend/themes.html)
- [Assets et CSS dans Odoo 18](https://www.odoo.com/documentation/18.0/developer/reference/backend/assets.html)

## ⚠️ Notes Importantes

1. **Compatibilité** : Tous les thèmes sont testés pour Odoo 18.0
2. **Dépendances** : Certains thèmes nécessitent des modules spécifiques
3. **Performance** : Les thèmes peuvent affecter les performances, tester avant production
4. **Backup** : Toujours faire un backup avant d'installer un nouveau thème

## 🆘 Support

Pour toute question ou problème :
- Vérifier les logs : `docker compose logs odoo`
- Vérifier la compatibilité avec Odoo 18
- Consulter la documentation du thème spécifique

---

**Dernière mise à jour :** Novembre 2025

