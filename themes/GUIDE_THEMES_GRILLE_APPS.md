# 🎨 Guide des Thèmes avec Grille d'Applications

## 📋 Thèmes Compatibles

Les thèmes suivants affichent vos modules Odoo dans une grille d'icônes avec fond personnalisable, similaire aux images fournies :

### 1. **theme_hue_backend** ⭐ (Recommandé)

**Fonctionnalités :**
- ✅ Grille d'applications avec icônes
- ✅ Fond personnalisable (image de fond)
- ✅ Configuration via Settings > Themes
- ✅ Support des images PNG/JPG pour le fond
- ✅ Interface moderne et élégante

**Installation :**
```bash
# Via l'interface Odoo
Apps > Rechercher "Hue Backend Theme" > Installer

# Via ligne de commande
docker compose -f config/docker-compose.simple.yml exec odoo odoo -u theme_hue_backend -d odoo
```

**Configuration du fond :**
1. Aller dans **Settings** > **Themes**
2. Section **Hue Backend Theme**
3. Télécharger une image de fond (montagnes, paysage, etc.)
4. Configurer les couleurs de l'app bar et navbar
5. Sauvegarder

**Fichiers clés :**
- `models/res_config_settings.py` : Configuration du fond
- `static/src/components/app_menu/side_menu.xml` : Grille d'applications
- `static/src/layout/style/layout_style.scss` : Styles avec fond personnalisé

---

### 2. **theme_diwy**

**Fonctionnalités :**
- ✅ Grille d'applications (6 colonnes)
- ✅ Fond personnalisable via CSS
- ✅ Icônes avec ombres
- ✅ Design moderne

**Installation :**
```bash
# Via l'interface Odoo
Apps > Rechercher "Theme Diwy" > Installer

# Via ligne de commande
docker compose -f config/docker-compose.simple.yml exec odoo odoo -u theme_diwy -d odoo
```

**Configuration :**
- Modifier `static/src/css/style.css` pour personnaliser le fond
- La grille est définie dans `static/src/xml/home_menus.xml`

---

### 3. **theme_modern**

**Fonctionnalités :**
- ✅ Menu d'applications amélioré
- ✅ Design responsive
- ✅ Support des icônes personnalisées

**Installation :**
```bash
docker compose -f config/docker-compose.simple.yml exec odoo odoo -u theme_modern -d odoo
```

---

## 🎯 Recommandation : theme_hue_backend

**Pourquoi choisir theme_hue_backend ?**

1. ✅ **Fond personnalisable** : Vous pouvez uploader votre propre image de fond (montagnes, paysage, etc.)
2. ✅ **Configuration facile** : Tout se configure depuis l'interface Odoo (Settings)
3. ✅ **Grille d'applications** : Affiche tous vos modules en grille avec icônes
4. ✅ **Couleurs personnalisables** : App bar, navbar, kanban, etc.
5. ✅ **Compatible Odoo 18** : Entièrement compatible avec la version 18

## 📸 Configuration pour obtenir l'affichage des images

### Étape 1 : Installer le thème

```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
docker compose -f config/docker-compose.simple.yml exec odoo odoo -u theme_hue_backend -d odoo
```

### Étape 2 : Configurer le fond

1. **Connectez-vous à Odoo** (http://localhost:8069)
2. Allez dans **Settings** > **Themes**
3. Section **Hue Backend Theme**
4. **Background Image** : Téléchargez votre image de fond
   - Format recommandé : JPG ou PNG
   - Résolution : 1920x1080 ou plus
   - Exemples : Montagnes, paysage, fond dégradé, etc.

### Étape 3 : Personnaliser les couleurs

- **App Bar Background Color** : Couleur de la barre d'applications
- **Navbar Background Color** : Couleur de la barre de navigation
- **Kanban Background Color** : Couleur de fond des vues kanban
- **Home Menu Text Color** : Couleur du texte dans le menu

### Étape 4 : Vérifier l'affichage

1. Cliquez sur le menu **Apps** (icône en haut à gauche)
2. Vous devriez voir tous vos modules en grille avec le fond personnalisé

## 🖼️ Exemples de fonds

Pour obtenir un affichage similaire aux images :

1. **Fond montagnes** : Utilisez une image de montagnes avec ciel bleu
2. **Fond dégradé** : Créez un dégradé orange/bleu diagonal
3. **Fond abstrait** : Utilisez des formes géométriques colorées

## 🔧 Personnalisation avancée

### Modifier le nombre de colonnes

Pour `theme_diwy`, modifiez dans `static/src/css/style.css` :
```css
.app_container .app_list {
  grid-template-columns: repeat(6, 1fr); /* 6 colonnes au lieu de 5 */
}
```

### Ajouter un fond CSS personnalisé

Pour `theme_hue_backend`, modifiez dans `static/src/layout/style/layout_colors.scss` :
```scss
--full-screen-bg: url(/theme_hue_backend/static/description/assets/votre-image.jpg);
```

## 📚 Documentation des thèmes

- `theme_hue_backend` : Voir `themes/theme_hue_backend/README.rst`
- `theme_diwy` : Voir `themes/theme_diwy/README.rst`
- `theme_modern` : Voir `themes/theme_modern/readme/`

## ⚠️ Notes importantes

1. **Performance** : Les images de fond grandes peuvent ralentir le chargement
2. **Contraste** : Assurez-vous que le texte reste lisible sur le fond
3. **Responsive** : Testez sur différentes tailles d'écran
4. **Cache** : Après modification, videz le cache du navigateur (Ctrl+F5)

## 🆘 Dépannage

### Le fond ne s'affiche pas
- Vérifiez que l'image est bien uploadée dans Settings
- Videz le cache du navigateur
- Vérifiez les permissions du fichier

### Les icônes ne s'affichent pas
- Vérifiez que les modules ont des icônes définies
- Regardez la console du navigateur pour les erreurs
- Vérifiez que le thème est bien installé

---

**Dernière mise à jour :** Novembre 2025

