# 🐳 Noms des Conteneurs Docker

## 📋 Conteneurs Actifs

### Configuration : `docker-compose.simple.yml`

Les conteneurs créés par cette configuration ont les noms suivants :

| Service | Nom du Conteneur | Description |
|---------|------------------|-------------|
| `postgres` | `saas-postgres-dev` | Base de données PostgreSQL |
| `odoo` | `saas-odoo-dev` | Serveur Odoo |

---

## 🔍 Vérifier les Conteneurs

### Lister tous les conteneurs SaaS

```bash
docker ps --format "{{.Names}}" | grep saas
```

**Résultat attendu :**
```
saas-odoo-dev
saas-postgres-dev
```

### Voir l'état détaillé

```bash
docker compose -f config/docker-compose.simple.yml ps
```

---

## 📝 Commandes Utiles

### Logs Odoo

```bash
# Logs du conteneur Odoo
docker logs saas-odoo-dev --tail 50

# Logs en temps réel
docker logs saas-odoo-dev -f

# Filtrer les logs
docker logs saas-odoo-dev --tail 100 | grep -i "error"
docker logs saas-odoo-dev --tail 100 | grep -i "saas_portal_start"
```

### Logs PostgreSQL

```bash
docker logs saas-postgres-dev --tail 50
docker logs saas-postgres-dev -f
```

### Accéder au shell

```bash
# Shell Odoo
docker exec -it saas-odoo-dev bash

# Shell PostgreSQL
docker exec -it saas-postgres-dev bash
```

### Exécuter des commandes

```bash
# Dans le conteneur Odoo
docker exec saas-odoo-dev ls -la /mnt/extra-addons/

# Vérifier la configuration
docker exec saas-odoo-dev cat /etc/odoo/odoo.conf | grep admin_passwd

# Vérifier les modules installés
docker exec saas-odoo-dev psql -h postgres -U odoo -d saas-portal-18.local -c "SELECT name, state FROM ir_module_module WHERE name LIKE 'saas%';"
```

---

## 🔄 Redémarrer les Conteneurs

### Redémarrer tous les conteneurs

```bash
docker compose -f config/docker-compose.simple.yml restart
```

### Redémarrer uniquement Odoo

```bash
docker restart saas-odoo-dev
```

### Redémarrer uniquement PostgreSQL

```bash
docker restart saas-postgres-dev
```

---

## 🛑 Arrêter les Conteneurs

### Arrêter tous les conteneurs

```bash
docker compose -f config/docker-compose.simple.yml stop
```

### Arrêter uniquement Odoo

```bash
docker stop saas-odoo-dev
```

---

## 🗑️ Supprimer les Conteneurs

### Arrêter et supprimer (données conservées)

```bash
docker compose -f config/docker-compose.simple.yml down
```

### Arrêter et supprimer (avec données)

```bash
docker compose -f config/docker-compose.simple.yml down -v
```

---

## ⚠️ Notes Importantes

### Changement de Nom

Les conteneurs créés par `docker-compose.simple.yml` utilisent le suffixe `-dev` :
- `saas-odoo-dev` (et non `saas-odoo`)
- `saas-postgres-dev` (et non `saas-postgres`)

### Anciens Conteneurs

Si vous avez des conteneurs avec les anciens noms (`saas-odoo`, `saas-postgres`), ils proviennent probablement d'une autre configuration Docker Compose.

**Pour les lister :**
```bash
docker ps -a | grep saas
```

**Pour les supprimer :**
```bash
docker rm saas-odoo saas-postgres 2>/dev/null
```

---

## 🔧 Alias Utiles

Vous pouvez créer des alias dans votre `.bashrc` ou `.zshrc` :

```bash
# Alias pour les logs Odoo
alias odoo-logs='docker logs saas-odoo-dev -f'

# Alias pour accéder au shell Odoo
alias odoo-shell='docker exec -it saas-odoo-dev bash'

# Alias pour redémarrer Odoo
alias odoo-restart='docker restart saas-odoo-dev'

# Alias pour voir l'état
alias odoo-status='docker compose -f config/docker-compose.simple.yml ps'
```

---

## 📚 Références

- Configuration Docker Compose : `config/docker-compose.simple.yml`
- Documentation Docker : `DOCKER_SETUP.md`
- Guide de dépannage : `docs/CORRIGER_MASTER_PASSWORD.md`

---

**Utilisez toujours `saas-odoo-dev` et `saas-postgres-dev` pour les commandes Docker !**

