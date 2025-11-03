# 📋 Checklist Rapide : Création d'un Nouveau Client SaaS

## 🚀 Processus en 4 Étapes

### ✅ Étape 1 : Serveur (5 minutes)

```
SaaS > Servers > Create
├── Name: server-1
├── Host: localhost
├── Max Clients: 100
└── Sync Server
```

### ✅ Étape 2 : Plan (10-15 minutes)

```
SaaS > Plans > Create
├── Name: Plan Starter
├── Server: server-1
├── Price: 99€/mois
├── Trial: 14 jours
├── Create Template DB
├── Configurer Template (installer modules)
└── Sync Server
```

### ✅ Étape 3 : Partner (1 minute)

```
Contacts > Create
├── Name: Client Name
└── Email: client@example.com
```

### ✅ Étape 4 : Client (5 minutes)

```
SaaS > Plans > [Sélectionner Plan] > Create Client
├── Database name: client-1
├── Partner: [Sélectionner]
├── User: [Sélectionner]
└── Create
```

---

## 🎯 Commande Rapide (Script)

```bash
python3 scripts/create_complete_setup.py \
    --server-name server-1 \
    --plan-name "Plan Starter" \
    --client-name client-1 \
    --partner-email client@example.com \
    --partner-name "Client Name"
```

---

## 🔍 Vérification

- [ ] Serveur créé et synchronisé
- [ ] Plan créé avec template DB
- [ ] Partner créé
- [ ] Client créé et accessible
- [ ] URL fonctionne : `http://client-1.saas-portal-18.local:8069/web`

---

## 📚 Documentation Complète

Voir `GUIDE_CREATION_CLIENT.md` pour les détails complets.

