# 🔐 INFORMATIONS DE CONNEXION SAAS

## ✅ ACCÈS AU SYSTÈME

### **MASTER PASSWORD**
```
admin
```
*Utilisé pour créer/supprimer des bases de données*

---

### **BASES DE DONNÉES DISPONIBLES**

1. **saas-portal-18.local** (Portal - Administration SaaS)
2. **server-1.saas-portal-18.local** (Server - Serveur Technique)

---

### **URLS D'ACCÈS DIRECT**

#### Portal (Interface Admin)
```
http://localhost:8069/?db=saas-portal-18.local
```

#### Server (Serveur Technique)
```
http://localhost:8069/?db=server-1.saas-portal-18.local
```

---

### **CREDENTIALS UTILISATEUR**

```
Email/Login: admin
Password: admin
```

---

### **CONFIGURATION HÔTES LOCAUX**

Ajoutez ces lignes à `/etc/hosts` pour accéder via les domaines :

```bash
127.0.0.1 saas-portal-18.local
127.0.0.1 server-1.saas-portal-18.local
127.0.0.1 template-1.saas-portal-18.local
127.0.0.1 client-001.saas-portal-18.local
127.0.0.1 client-002.saas-portal-18.local
127.0.0.1 client-003.saas-portal-18.local
```

---

### **VÉRIFICATION POSTGRESQL**

```bash
psql -U odoo -d postgres -c "\l" | grep portal
```

Bases attendues :
- ✅ `saas-portal-18.local`
- ✅ `server-1.saas-portal-18.local`

---

### **ÉTAPES SUIVANTES**

1. ✅ Connectez-vous au Portal : http://localhost:8069/?db=saas-portal-18.local
2. ✅ Créez un Plan dans SaaS > Plans
3. ✅ Créez un Serveur dans SaaS > Serveurs (déjà créé)
4. ✅ Testez la création d'un client/test via l'interface

---

**Date** : 2025-11-03  
**Statut** : ✅ OPÉRATIONNEL

