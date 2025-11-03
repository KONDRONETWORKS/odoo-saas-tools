# Guide Rapide : Créer un Client de Test

## 🎯 Méthode Rapide : Depuis l'Interface Odoo

### Étape 1 : Accéder à Odoo
1. Ouvrez votre navigateur : **http://localhost:8069**
2. Connectez-vous avec :
   - **Email** : admin
   - **Mot de passe** : admin

### Étape 2 : Vérifier les prérequis
Avant de créer un client, assurez-vous d'avoir :

1. **Un serveur SaaS** : 
   - Allez dans **SaaS > Serveurs**
   - Vérifiez que `saas-server-001` existe
   - Si non, créez-le avec les valeurs par défaut

2. **Un plan SaaS** :
   - Allez dans **SaaS > Plans**
   - Vérifiez qu'au moins un plan existe
   - Si non, créez-en un :
     - Nom : `Plan Standard`
     - Serveur : `saas-server-001`
     - Template : (optionnel pour le développement)

3. **Un partenaire** :
   - Allez dans **Contacts**
   - Vérifiez qu'au moins un partenaire existe
   - Si non, créez-en un :
     - Nom : `Client Test`
     - Email : `client-test@example.com`

### Étape 3 : Créer le client

1. **Allez dans SaaS > Clients**
2. **Cliquez sur "Créer"**
3. **Remplissez le formulaire** :
   ```
   Nom de la base de données : client-test-001
   Plan : [Sélectionnez votre plan]
   Partenaire : [Sélectionnez votre partenaire]
   Serveur : saas-server-001
   Essai : [Cochez si vous voulez un essai gratuit]
   ```
4. **Cliquez sur "Enregistrer"**

### Étape 4 : Vérifier la création

Vous devriez voir :
- ✅ Le client créé dans la liste
- ✅ L'état : `open`
- ✅ Les informations du plan et du partenaire

## 🔧 Méthode Alternative : Via Script Python

Si vous préférez utiliser le script :

```bash
# Depuis le conteneur Docker
docker compose -f config/docker-compose.windows.yml exec odoo python3 /mnt/extra-addons/saas_portal/scripts/create_saas_data.py
```

Le script créera automatiquement :
- ✅ Un serveur SaaS (si non existant)
- ✅ Un plan SaaS (si templates disponibles)
- ✅ Un partenaire de test
- ✅ Un client de test

## ⚠️ Notes Importantes

### Pour le développement local

**Sans serveur SaaS séparé :**
- ✅ Vous pouvez créer des clients dans Odoo
- ✅ Les enregistrements sont créés
- ❌ Les bases de données réelles ne sont **pas** créées
- ❌ Le bouton "Create Database" échouera (normal)

**C'est normal pour le développement !** Les clients créés servent à tester l'interface et le flux de données.

### Pour créer de vraies bases de données

Vous aurez besoin :
1. D'un serveur SaaS séparé avec le module `saas_server` installé
2. D'un serveur PostgreSQL accessible
3. De la configuration OAuth correcte

## 📝 Structure du Client Créé

Quand vous créez un client, le système crée automatiquement :

- **Enregistrement `saas_portal.client`** dans Odoo
- **Application OAuth** pour l'authentification
- **Client ID** unique
- **URL publique** calculée depuis le template
- **Host** calculé depuis le template

## 🔍 Vérifier le Client Créé

Après création, vous pouvez vérifier :

```python
# Depuis Odoo Python shell ou script
client = env['saas_portal.client'].search([('name', '=', 'client-test-001')])
print(f"Client: {client.name}")
print(f"Plan: {client.plan_id.name}")
print(f"État: {client.state}")
print(f"Partenaire: {client.partner_id.name}")
print(f"Serveur: {client.server_id.name}")
```

## 🎯 Prochaines Étapes

Une fois le client créé :

1. **Vérifier les données** : Ouvrez le client et vérifiez toutes les informations
2. **Tester l'interface** : Naviguez dans les différentes vues du client
3. **Créer d'autres clients** : Répétez pour créer plusieurs clients de test
4. **Tester les limites** : Testez les limites de DBs par partenaire si configurées

