SaaS Portal Monitoring
=======================

Monitoring et métriques en temps réel pour les instances SaaS.

**Description:**
Ce module permet de monitorer en temps réel toutes les instances SaaS, collecter des métriques de performance, et générer des alertes automatiques en cas de problème.

**Dépendances:**
- saas_portal
- base_automation
- mail

**Fonctionnalités principales:**

1. **Collecte de Métriques**
   - CPU, RAM, Disk usage
   - Temps de réponse
   - Uptime
   - Taux d'erreur
   - Utilisateurs actifs
   - Requêtes par minute

2. **Dashboard de Monitoring**
   - Vue d'ensemble de la santé des instances
   - Graphiques de tendances
   - Alertes en temps réel
   - Historique des métriques

3. **Alertes Automatiques**
   - Seuils configurables (warning, critical)
   - Notifications email
   - Détection d'instances down
   - Escalade automatique

4. **Intégrations**
   - API REST pour métriques
   - Endpoint de health check
   - Webhooks (à venir)

**Configuration:**

1. Aller dans SaaS > Clients
2. Ouvrir un client
3. Activer "Monitoring Enabled"
4. Configurer les seuils dans le plan si nécessaire
5. Les métriques seront collectées automatiquement toutes les 5 minutes

**Utilisation:**

**Collecte manuelle:**
- Ouvrir un client
- Cliquer sur "Collect Metrics" dans le header

**Vue des métriques:**
- Onglet "Monitoring" dans le formulaire client
- Menu SaaS > Monitoring Metrics

**API:**

``GET /saas_portal/monitoring/metrics/<client_id>``
- Retourne les dernières métriques d'un client
- Authentification requise

``GET /saas_portal/monitoring/health``
- Health check public
- Retourne {"status": "ok"}

**Seuils par défaut:**

- CPU: Warning 70%, Critical 90%
- RAM: Warning 75%, Critical 90%
- Disk: Warning 80%, Critical 95%
- Response Time: Warning 1000ms, Critical 3000ms
- Error Rate: Warning 1%, Critical 5%

Ces seuils peuvent être configurés par plan dans une future version.

**Cron Jobs:**

- Collecte des métriques: Toutes les 5 minutes
- Nettoyage des anciennes métriques: Tous les jours (garde 30 jours)

**Status de Santé:**

- **Healthy**: Toutes les métriques sont OK
- **Warning**: Au moins une métrique dépasse le seuil warning
- **Critical**: Au moins une métrique dépasse le seuil critical
- **Down**: Instance inaccessible ou métriques à 0
- **Unknown**: Aucune métrique collectée

**Alertes:**

Les alertes sont envoyées automatiquement lorsque:
- Le statut devient "critical"
- L'instance est détectée comme "down"
- Les seuils critiques sont dépassés

**Améliorations futures:**

- Dashboard graphique avancé
- Configurations de seuils par plan
- Webhooks pour intégrations externes
- Intégration Prometheus/Grafana
- Rapports de performance
- Prédiction d'incidents (ML)

