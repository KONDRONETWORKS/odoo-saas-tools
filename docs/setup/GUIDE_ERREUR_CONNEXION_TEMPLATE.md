# Guide : Erreur de connexion lors de la création de template

## ✅ Bonne nouvelle

L'erreur JavaScript sur les vues est **résolue** ! La page des Plans fonctionne maintenant correctement.

## ❌ Nouvelle erreur

L'erreur actuelle concerne la **création d'un template de base de données** :

```
ConnectionRefusedError: [Errno 111] Connection refused
HTTPConnectionPool(host='localhost', port=8072)
```

## 🔍 Cause

Le système essaie de créer un template en se connectant à un serveur SaaS qui n'existe pas encore ou qui n'est pas configuré correctement.

Le port `8072` est le port de longpolling d'Odoo, pas le port XML-RPC (8069). Cela suggère que la configuration du serveur SaaS n'est pas correcte.

## ✅ Solutions

### Option 1 : Configuration pour développement local

Pour le développement local, vous pouvez configurer le serveur SaaS pour pointer vers le même Odoo :

1. **Accédez à SaaS > Serveurs**
2. **Modifiez le serveur `saas-server-001`** :
   - **Local Host** : `localhost`
   - **Local Port** : `8069` (pas 8072)
   - **Local Request Scheme** : `http`
   - **Request Port** : `8069`

### Option 2 : Créer les templates manuellement

Pour le développement, vous pouvez créer les templates manuellement sans passer par le serveur SaaS :

1. **Accédez à SaaS > Bases de données**
2. **Créez un template** :
   - Nom : `template-basic`
   - État : `Template`
   - Serveur : `saas-server-001`
3. **Répétez pour** `template-standard` et `template-premium`

### Option 3 : Installer un serveur SaaS séparé

Pour un environnement de production, vous devez installer et configurer un serveur SaaS séparé qui écoute sur le port configuré.

## 📝 Note

Les templates peuvent être créés manuellement depuis l'interface Odoo sans avoir besoin d'un serveur SaaS séparé pour le développement/test.

