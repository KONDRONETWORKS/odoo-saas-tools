# 🚀 Démarrage Rapide - Odoo SaaS

## ⚡ Commande Simple

**Pour démarrer le service :**
```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
docker compose -f config/docker-compose.simple.yml up -d
```

**Pour arrêter le service :**
```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
docker compose -f config/docker-compose.simple.yml down
```

**Pour redémarrer :**
```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
docker compose -f config/docker-compose.simple.yml restart
```

---

## 📋 Fichier à Utiliser

**Utilisez TOUJOURS :** `config/docker-compose.simple.yml`

C'est le fichier principal pour le développement local.

---

## 🔍 Vérifier l'État

**Voir si les conteneurs sont actifs :**
```bash
docker ps | grep saas
```

**Voir les logs :**
```bash
docker logs saas-odoo-dev --tail 50
```

**Voir l'état détaillé :**
```bash
docker compose -f config/docker-compose.simple.yml ps
```

---

## 🌐 Accès

Une fois démarré, accédez à :
- **Interface Odoo** : http://localhost:8069
- **Portail SaaS** : http://localhost:8069/web?db=saas-portal-18.local

---

## ⚠️ Si le Service est Arrêté

**1. Vérifier l'état :**
```bash
docker ps -a | grep saas
```

**2. Démarrer :**
```bash
docker compose -f config/docker-compose.simple.yml up -d
```

**3. Attendre 30 secondes** puis vérifier :
```bash
docker logs saas-odoo-dev --tail 20
```

---

## 🛑 Arrêter Complètement

**Arrêter et supprimer les conteneurs (données conservées) :**
```bash
docker compose -f config/docker-compose.simple.yml down
```

**Arrêter et supprimer TOUT (y compris les données) :**
```bash
docker compose -f config/docker-compose.simple.yml down -v
```

---

## 📝 Noms des Conteneurs

- **Odoo** : `saas-odoo-dev`
- **PostgreSQL** : `saas-postgres-dev`

---

**C'est tout ! Utilisez toujours `config/docker-compose.simple.yml`**

