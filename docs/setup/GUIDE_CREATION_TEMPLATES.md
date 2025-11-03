# Guide de création des templates SaaS

## 📋 Vue d'ensemble

Ce guide vous explique comment créer les templates de bases de données nécessaires pour votre système SaaS.

## 🎯 Objectif

Créer 3 templates de bases de données :
1. `template-basic`
2. `template-standard`
3. `template-premium`

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

### Étape 7 : Relancer le script de création

Une fois les templates créés, relancez le script pour créer le plan et le client :

```powershell
docker compose -f config/docker-compose.windows.yml exec -T odoo python3 /mnt/extra-addons/saas_portal/scripts/create_saas_data.py
```

## ⚠️ Notes importantes

- Les templates doivent avoir l'état `Template` pour être utilisables dans les plans
- Assurez-vous que le serveur `saas-server-001` existe avant de créer les templates
- Si vous rencontrez des erreurs de permissions, vérifiez que vous êtes connecté en tant qu'administrateur

## 🔍 Dépannage

### Le menu "Bases de données" n'apparaît pas

1. Activez le mode développeur : Paramètres > Activer le mode développeur
2. Rafraîchissez la page
3. Vérifiez que le module `saas_portal` est bien installé

### Erreur lors de la création d'un template

1. Vérifiez que le serveur `saas-server-001` existe
2. Vérifiez que vous avez les permissions d'administration
3. Consultez les logs Odoo pour plus de détails

### Le script ne trouve pas les templates

1. Vérifiez que les templates ont bien l'état `Template`
2. Vérifiez que les templates sont liés au serveur `saas-server-001`
3. Relancez le script après vérification

## ✅ Checklist de vérification

Avant de relancer le script, vérifiez que :

- [ ] Au moins un template existe avec l'état `Template`
- [ ] Le template est lié au serveur `saas-server-001`
- [ ] Le serveur `saas-server-001` existe et est actif
- [ ] Vous êtes connecté en tant qu'administrateur

## 🎉 Prochaines étapes

Une fois les templates créés et le script relancé, vous aurez :

- ✅ 1 Serveur SaaS configuré
- ✅ 3 Templates de bases de données
- ✅ 1 Plan SaaS "Plan Standard"
- ✅ 1 Client de test "client-test-001"

Vous pourrez alors :
- Accéder aux plans : SaaS > Plans
- Accéder aux clients : SaaS > Clients
- Créer de nouveaux clients depuis les plans

