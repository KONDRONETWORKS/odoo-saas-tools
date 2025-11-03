# Guide : Créer des templates de bases de données manuellement

## 🎯 Objectif

Créer des templates de bases de données **sans serveur SaaS séparé** pour le développement.

## ✅ Pourquoi créer manuellement ?

Dans un environnement de développement, vous n'avez pas besoin d'un serveur SaaS séparé. Vous pouvez créer les templates directement depuis l'interface Odoo.

## 📝 Étapes détaillées

### Étape 1 : Accéder à l'interface Odoo

1. Ouvrez votre navigateur
2. Accédez à : **http://localhost:8069**
3. Connectez-vous avec :
   - **Email** : admin
   - **Mot de passe** : admin

### Étape 2 : Accéder au menu Bases de données

1. Dans le menu principal, cliquez sur **"SaaS"**
2. Dans le sous-menu, cliquez sur **"Bases de données"**
   - Si vous ne voyez pas ce menu, activez le mode développeur :
     - Paramètres > Activer le mode développeur

### Étape 3 : Créer le premier template (template-basic)

1. Cliquez sur le bouton **"Créer"**
2. Remplissez le formulaire :
   - **Nom de la base de données** : `template-basic`
   - **État** : Sélectionnez `Template` dans le menu déroulant
   - **Serveur** : Sélectionnez `saas-server-001` dans le menu déroulant
   - **Application OAuth** : Laisser vide (sera créée automatiquement)
3. Cliquez sur **"Enregistrer"**

### Étape 4 : Créer le deuxième template (template-standard)

1. Répétez les étapes de l'Étape 3
2. Utilisez ces valeurs :
   - **Nom de la base de données** : `template-standard`
   - **État** : `Template`
   - **Serveur** : `saas-server-001`
3. Cliquez sur **"Enregistrer"**

### Étape 5 : Créer le troisième template (template-premium)

1. Répétez les étapes de l'Étape 3
2. Utilisez ces valeurs :
   - **Nom de la base de données** : `template-premium`
   - **État** : `Template`
   - **Serveur** : `saas-server-001`
3. Cliquez sur **"Enregistrer"**

### Étape 6 : Vérifier les templates créés

1. Dans la liste des bases de données, vous devriez voir vos 3 templates
2. Vérifiez que :
   - Le nom est correct
   - L'état est bien `Template`
   - Le serveur est bien `saas-server-001`

### Étape 7 : Utiliser les templates dans un plan

1. Allez dans **SaaS > Plans**
2. Créez ou modifiez un plan
3. Sélectionnez un template dans le champ **"Template"**
4. Enregistrez

## ⚠️ Notes importantes

- **Les templates créés manuellement sont pour le développement uniquement**
- Pour créer de vraies bases de données clients, vous aurez besoin d'un serveur SaaS séparé
- Les templates avec l'état `Template` peuvent être utilisés dans les plans
- Assurez-vous que le serveur `saas-server-001` existe avant de créer les templates

## 🔍 Dépannage

### Le menu "Bases de données" n'apparaît pas

1. Activez le mode développeur : Paramètres > Activer le mode développeur
2. Rafraîchissez la page
3. Vérifiez que le module `saas_portal` est bien installé

### Erreur lors de la création d'un template

1. Vérifiez que le serveur `saas-server-001` existe
2. Vérifiez que vous avez les permissions d'administration
3. Consultez les logs Odoo pour plus de détails

### Le bouton "Create template DB" ne fonctionne pas

C'est normal ! Ce bouton nécessite un serveur SaaS séparé. Utilisez la méthode manuelle décrite ci-dessus pour créer les templates.

## ✅ Checklist de vérification

Avant d'utiliser les templates :

- [ ] Au moins un template existe avec l'état `Template`
- [ ] Le template est lié au serveur `saas-server-001`
- [ ] Le serveur `saas-server-001` existe et est actif
- [ ] Les templates sont visibles dans SaaS > Plans > Template

## 🎉 Prochaines étapes

Une fois les templates créés :

1. Créez un plan SaaS
2. Sélectionnez un template dans le plan
3. Le plan sera prêt à créer des clients

**Note** : Pour créer de vraies instances client, vous aurez besoin d'un serveur SaaS séparé avec le module `saas_server` installé.
