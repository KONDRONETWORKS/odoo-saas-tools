from . import res_config

# Charger les extensions Mailgun seulement si saas_portal est installé
# Le fichier saas_sysadmin_mailgun.py hérite de saas_portal.client et saas_portal.plan
# qui ne sont disponibles que si le module saas_portal est installé.
# Pour éviter les erreurs, on ne charge ce fichier que si saas_portal est installé
# Pour l'instant, on ne charge que res_config qui fonctionne indépendamment
# Les extensions Mailgun seront chargées automatiquement si saas_portal est installé
# via la dépendance dans le manifest
