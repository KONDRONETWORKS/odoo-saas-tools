# 🚀 Déploiement Rapide - VM Ubuntu 22.04.5

## Déploiement sur VM OVH (10.10.10.40)

### Méthode Rapide (Recommandée)

```bash
# 1. Transférer le script sur la VM
scp infrastructure/deploy-ubuntu-vm.sh root@10.10.10.40:/root/

# 2. Se connecter et exécuter
ssh root@10.10.10.40
chmod +x /root/deploy-ubuntu-vm.sh
sudo ./deploy-ubuntu-vm.sh
```

### Configuration Optionnelle

Avant d'exécuter le script, vous pouvez définir ces variables :

```bash
export DOMAIN_NAME="votre-domaine.com"  # Pour SSL
export EMAIL="votre-email@example.com"  # Pour Let's Encrypt
```

### Fichiers Créés

- ✅ `infrastructure/deploy-ubuntu-vm.sh` - Script de déploiement automatique
- ✅ `config/docker-compose.ubuntu-vm.yml` - Configuration Docker Compose
- ✅ `config/odoo.ubuntu-vm.conf` - Configuration Odoo
- ✅ `infrastructure/nginx-odoo.conf` - Configuration Nginx
- ✅ `infrastructure/env.example` - Exemple de variables d'environnement
- ✅ `infrastructure/GUIDE_DEPLOIEMENT_UBUNTU_VM.md` - Guide complet

### Documentation Complète

Consultez le guide détaillé : **[GUIDE_DEPLOIEMENT_UBUNTU_VM.md](GUIDE_DEPLOIEMENT_UBUNTU_VM.md)**

### Support

En cas de problème, consultez la section [Dépannage](GUIDE_DEPLOIEMENT_UBUNTU_VM.md#dépannage) du guide complet.

