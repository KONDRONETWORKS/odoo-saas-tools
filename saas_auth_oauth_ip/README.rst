OAuth IP Validation
===================

Validation OAuth par adresse IP locale.

**Description:**
Ce module permet de valider les tokens OAuth par des requêtes sur le réseau local. Il ajoute deux champs à auth.oauth.provider pour spécifier l'hôte et le port local.

**Dépendances:**
- base
- auth_oauth

**Champs ajoutés:**
- local_host : Adresse IP locale
- local_port : Port local

**Fonctionnement:**
Le module utilise une astuce pour rediriger les requêtes vers l'adresse locale :
```python
# host - origin host for the URL
# url - original host is replaced by local_host and local_port 
urllib2.Request(url, headers={'host': host})
```

**Cas d'usage:**
- Communication inter-bases en réseau local
- OAuth entre Portal et Server sur même réseau
- Sécurisation des communications internes

**Relations:**
- Utilisé par saas_portal pour la communication avec saas_server
- Nécessaire pour la validation des tokens OAuth en environnement local
- Complément de oauth_provider

**Credits:**
- Ivan Yelizariev <yelizariev@it-projects.info>
- IT-Projects LLC / ITExperts4Africa <https://www.itexperts4africa.com>

**Documentation:**
- Usage: `<doc/index.rst>`__
- Changelog: `<doc/changelog.rst>`__
- Apps: https://apps.odoo.com/apps/modules/8.0/saas_auth_oauth_ip/

**Compatibilité:**
- Testé sur Odoo 8.0 à 18.0 
