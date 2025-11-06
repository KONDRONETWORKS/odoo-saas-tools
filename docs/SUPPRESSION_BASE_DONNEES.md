# 🗑️ Guide de Suppression de Bases de Données Odoo

## ⚠️ Problème : "Access Denied" lors de la suppression via l'interface web

Lorsque vous essayez de supprimer une base de données via l'interface web Odoo (`http://localhost:8069/web/database/drop`), vous pouvez rencontrer l'erreur :

```
Database deletion error: Access Denied
```

**Cause :** Cette erreur se produit généralement lorsque le Master Password saisi ne correspond pas à celui configuré dans `odoo.conf`.

---

## ✅ Solution : Utiliser le script de suppression

Un script Python est disponible pour supprimer directement les bases de données via PostgreSQL.

### Script disponible

**Fichier :** `scripts/drop_database.py`

### Utilisation

#### 1. Lister les bases de données disponibles

```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
python3 scripts/drop_database.py --list
```

**Exemple de sortie :**
```
📋 Bases de données disponibles:
  - odoo
  - postgres
  - saas-portal-18.local
  - server-1.saas-portal-18.local
```

#### 2. Supprimer une base de données

**Avec confirmation :**
```bash
python3 scripts/drop_database.py "server-1.saas-portal-18.local"
```

Le script demandera confirmation avant de supprimer.

**Sans confirmation (automatique) :**
```bash
python3 scripts/drop_database.py "server-1.saas-portal-18.local" --confirm
```

#### 3. Options avancées

**Spécifier les paramètres de connexion PostgreSQL :**
```bash
python3 scripts/drop_database.py "nom-base" \
  --host localhost \
  --port 5433 \
  --user odoo \
  --password odoo
```

---

## 🔧 Alternative : Suppression via PostgreSQL directement

### Via Docker

```bash
# Se connecter au conteneur PostgreSQL
docker exec -it saas-postgres psql -U odoo -d postgres

# Dans psql, exécuter :
DROP DATABASE "server-1.saas-portal-18.local";
\q
```

### Via ligne de commande

```bash
# Terminer les connexions actives
docker exec saas-postgres psql -U odoo -d postgres -c \
  "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'server-1.saas-portal-18.local' AND pid <> pg_backend_pid();"

# Supprimer la base
docker exec saas-postgres psql -U odoo -d postgres -c \
  'DROP DATABASE "server-1.saas-portal-18.local";'
```

---

## 🔐 Vérifier le Master Password

Si vous souhaitez utiliser l'interface web, vérifiez que le Master Password correspond à celui dans `odoo.conf` :

**Fichier :** `odoo.conf`

```ini
[options]
admin_passwd = admin
```

**Dans l'interface web :**
- Allez sur `http://localhost:8069/web/database/drop`
- Entrez le Master Password : `admin`
- Sélectionnez la base à supprimer
- Cliquez sur "Delete"

---

## ⚠️ Précautions

### Avant de supprimer une base

1. **Sauvegarder les données** (si importantes)
2. **Vérifier les dépendances** (autres bases qui référencent cette base)
3. **Fermer les connexions actives** (le script le fait automatiquement)

### Bases à ne pas supprimer

- `postgres` : Base système PostgreSQL
- `odoo` : Base par défaut Odoo
- `saas-portal-18.local` : Base du portail SaaS (si vous l'utilisez)

---

## 📋 Exemples d'utilisation

### Supprimer une base de test

```bash
python3 scripts/drop_database.py "test-db.saas-portal-18.local" --confirm
```

### Supprimer plusieurs bases

```bash
for db in "db1" "db2" "db3"; do
  python3 scripts/drop_database.py "$db.saas-portal-18.local" --confirm
done
```

### Nettoyer toutes les bases client (attention !)

```bash
# Lister d'abord
python3 scripts/drop_database.py --list

# Supprimer sélectivement
python3 scripts/drop_database.py "client-001.saas-portal-18.local" --confirm
python3 scripts/drop_database.py "client-002.saas-portal-18.local" --confirm
# etc.
```

---

## 🐛 Dépannage

### Erreur : "database is being accessed by other users"

**Solution :** Le script ferme automatiquement les connexions. Si l'erreur persiste :

```bash
# Forcer la fermeture
docker exec saas-postgres psql -U odoo -d postgres -c \
  "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'nom-base';"
```

### Erreur : "connection refused"

**Vérifier :**
1. PostgreSQL Docker est démarré : `docker ps | grep postgres`
2. Le port est correct (5433 pour Docker)
3. Les credentials sont corrects (odoo/odoo)

### Erreur : "permission denied"

**Vérifier :**
1. L'utilisateur PostgreSQL a les droits : `odoo`
2. Vous êtes connecté à la bonne base (`postgres`)

---

## 📝 Notes

- Le script ferme automatiquement toutes les connexions actives avant de supprimer
- La suppression est **irréversible** (sauf si vous avez une sauvegarde)
- Les filestores associés ne sont pas supprimés automatiquement (à faire manuellement si nécessaire)

---

## 🔄 Recréer une base après suppression

Si vous avez supprimé une base par erreur, vous pouvez la recréer :

```bash
python3 saas.py \
  --use-existed-odoo \
  --odoo-config odoo.conf \
  --master-password admin \
  --server-create
```

---

**Le script `drop_database.py` est la méthode recommandée pour supprimer des bases de données Odoo de manière sûre et fiable.**

