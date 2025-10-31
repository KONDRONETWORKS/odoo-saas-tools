SaaS Portal Quotas
==================

Gestion automatique des quotas et limites pour les instances SaaS.

**Description:**
Ce module permet de définir et faire respecter des quotas pour chaque plan SaaS. Il surveille l'utilisation en temps réel, envoie des alertes avant les limites, et bloque automatiquement si nécessaire.

**Dépendances:**
- saas_portal
- base_automation
- mail

**Fonctionnalités principales:**

1. **Types de Quotas Supportés**
   - Utilisateurs maximum
   - Stockage (MB)
   - Appels API par heure/jour
   - Modules installables
   - Records par modèle
   - Bandwidth mensuel

2. **Configuration par Plan**
   - Définition des limites pour chaque plan
   - Seuils d'alerte configurables (%, grace period)
   - Activation/désactivation par type de quota
   - Plan de mise à niveau automatique

3. **Surveillance en Temps Réel**
   - Suivi automatique de l'utilisation
   - Calcul de pourcentage d'utilisation
   - Historique des quotas
   - Dashboard de consommation

4. **Système d'Alertes Multi-Niveaux**
   - **Alert**: Notification à X% (par défaut 80%)
   - **Warning**: Avertissement à Y% (par défaut 90%)
   - **Blocked**: Blocage à Z% (par défaut 100%)

5. **Enforcement Automatique**
   - Vérification avant chaque opération
   - Blocage des opérations si limite atteinte
   - Messages d'erreur clairs
   - Suggestion d'upgrade automatique

6. **Auto-Upgrade**
   - Mise à niveau automatique vers plan supérieur
   - Configuration du plan de destination
   - Notification au client

**Configuration:**

1. **Configurer un Plan:**
   - Aller dans SaaS > Plans
   - Ouvrir un plan
   - Onglet "Quotas & Limits"
   - Définir les limites pour chaque quota
   - Configurer les seuils d'alerte

2. **Exemple de Configuration:**
   - Plan Starter:
     * Max Users: 5
     * Max Storage: 1000 MB
     * Alert at: 80%
     * Warning at: 90%
     * Block at: 100%

   - Plan Professional:
     * Max Users: 20
     * Max Storage: 10000 MB
     * Upgrade Plan: Enterprise

**Utilisation:**

**Pour les Administrateurs:**
1. Configurer les quotas dans chaque plan
2. Surveiller l'utilisation via le dashboard
3. Voir les alertes dans SaaS > Quota Usage

**Pour les Clients:**
- Les quotas sont vérifiés automatiquement
- Alertes email envoyées automatiquement
- Bouton "Upgrade Plan" visible quand warning
- Blocage automatique si limite atteinte

**Vérification des Quotas:**

Le système vérifie automatiquement les quotas avant:
- Création d'utilisateur (si quota_enforce_users)
- Upload de fichiers (si quota_enforce_storage)
- Appels API (si quota_enforce_api)
- Installation de modules (si quota_enforce_modules)

**Codes d'Exemple:**

```python
# Vérifier un quota avant une opération
client.check_quota('users', required_value=1)

# Mettre à jour l'utilisation
client.update_quota_usage('users', current_user_count)

# Obtenir l'utilisation actuelle
usage = quota_model.get_current_usage(client_id)
```

**Seuils par Défaut:**

- Alert: 80% d'utilisation
- Warning: 90% d'utilisation
- Block: 100% d'utilisation
- Grace Period: 3 jours

**Cron Jobs:**

- Mise à jour des quotas: Toutes les heures
- Synchronise automatiquement avec les données clients

**Améliorations futures:**

- Quotas personnalisés par client
- Quotas périodiques (reset mensuel)
- Graphiques de consommation détaillés
- Export des rapports de quotas
- Intégration avec facturation
- Quotas basés sur l'activité

