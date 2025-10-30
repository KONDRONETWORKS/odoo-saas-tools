SaaS Sysadmin AWS
=================

Module de base pour l'intégration Amazon AWS.

**Description:**
Ce module est la fondation pour tous les modules qui utilisent Amazon AWS. Il permet de configurer les credentials AWS (Access Key ID et Secret Access Key) pour que les autres modules puissent les utiliser avec la bibliothèque boto pour contrôler des services comme Route53, EC2, S3, etc.

**Dépendances:**
- saas_sysadmin

**Fonctionnalités:**
- Stockage sécurisé des credentials AWS
- Configuration centralisée des paramètres AWS
- API commune pour tous les modules AWS

**Modules utilisant saas_sysadmin_aws:**
- saas_sysadmin_aws_route53 : DNS avec Route53
- saas_server_backup_s3 : Sauvegarde S3
- saas_sysadmin_route53 : DNS générique

**Configuration:**
1. Aller dans Système > SaaS > Configuration AWS
2. Entrer AWS Access Key ID
3. Entrer AWS Secret Access Key
4. Sauvegarder

**Services AWS utilisés:**
- EC2 : Instances serveurs
- S3 : Stockage sauvegardes
- Route53 : Gestion DNS
- AutoScaling : Scaling automatique

**Sécurité:**
- Credentials chiffrés en base
- Pas d'exposition dans les logs
- Rotation des clés supportée

**Installation boto:**
```bash
pip install boto
```

**Crédits:**
- Ildar Nasyrov <Nasyrov@it-projects.info>
- Salton Massally <smassally@idtlabs.sl> (iDT Labs)
- Cheick Oumar Tidiane Traore <https://github.com/njeudy>

**Sponsor:**
- IT-Projects LLC / ITExperts4Africa <https://www.itexperts4africa.com>

**Documentation:**
- Usage: `<doc/index.rst>`__
- Changelog: `<doc/changelog.rst>`__

**Compatibilité:**
- Testé sur Odoo 9.0 à 18.0
