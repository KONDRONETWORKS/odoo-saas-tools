"""
Optimisations de performance pour saas_portal
- Index de base de données pour améliorer les recherches
- Synchronisation parallèle des serveurs
"""
from odoo import models, api
import logging
import threading

_logger = logging.getLogger(__name__)


class SaasPortalClient(models.Model):
    """Optimisations pour saas_portal.client"""
    _inherit = 'saas_portal.client'
    
    @api.model
    def _auto_init(self):
        """Créer les index lors de l'installation/mise à jour"""
        super()._auto_init()
        
        # Créer les index pour améliorer les performances de recherche
        try:
            self.env.cr.execute("""
                -- Index sur l'état (fréquemment recherché)
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_state 
                ON saas_portal_client(state) 
                WHERE state IS NOT NULL;
                
                -- Index sur la date d'expiration (pour les requêtes de cron)
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_expiration 
                ON saas_portal_client(expiration_datetime) 
                WHERE expiration_datetime IS NOT NULL;
                
                -- Index sur le partner (pour les recherches par client)
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_partner 
                ON saas_portal_client(partner_id) 
                WHERE partner_id IS NOT NULL;
                
                -- Index sur le serveur (pour les recherches par serveur)
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_server 
                ON saas_portal_client(server_id) 
                WHERE server_id IS NOT NULL;
                
                -- Index sur le plan (pour les recherches par plan)
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_plan 
                ON saas_portal_client(plan_id) 
                WHERE plan_id IS NOT NULL;
                
                -- Index composite pour les recherches fréquentes (expiration + état)
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_exp_state 
                ON saas_portal_client(expiration_datetime, state) 
                WHERE expiration_datetime IS NOT NULL;
                
                -- Index sur le nom (pour les recherches par nom)
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_name 
                ON saas_portal_client(name);
            """)
            _logger.info("Index de base de données créés avec succès")
        except Exception as e:
            _logger.warning("Erreur lors de la création des index: %s", e)


class SaasPortalServer(models.Model):
    """Optimisations pour saas_portal.server avec synchronisation parallèle"""
    _inherit = 'saas_portal.server'
    
    @api.model
    def _auto_init(self):
        """Créer les index pour les serveurs"""
        super()._auto_init()
        
        try:
            self.env.cr.execute("""
                -- Index sur l'état du serveur
                CREATE INDEX IF NOT EXISTS idx_saas_portal_server_active 
                ON saas_portal_server(active) 
                WHERE active IS NOT NULL;
                
                -- Index sur le nom du serveur
                CREATE INDEX IF NOT EXISTS idx_saas_portal_server_name 
                ON saas_portal_server(name);
            """)
            _logger.info("Index pour saas_portal.server créés avec succès")
        except Exception as e:
            _logger.warning("Erreur lors de la création des index serveur: %s", e)
    
    def action_sync_server(self, updating_client_ID=None):
        """
        Synchronisation optimisée avec support parallèle
        Vérifie d'abord si on synchronise un seul serveur ou plusieurs
        """
        # Si un seul serveur, utiliser la méthode originale pour compatibilité
        if len(self) == 1:
            return super().action_sync_server(updating_client_ID=updating_client_ID)
        
        # Pour plusieurs serveurs, synchroniser en parallèle
        return self._sync_servers_parallel(updating_client_ID)
    
    def _sync_servers_parallel(self, updating_client_ID=None):
        """
        Synchroniser plusieurs serveurs en parallèle
        """
        servers = self.filtered(lambda s: s.state == 'open')
        
        if not servers:
            return True
        
        # Utiliser threading pour paralléliser
        threads = []
        results = {}
        errors = {}
        
        def sync_server(server):
            """Fonction pour synchroniser un serveur dans un thread"""
            try:
                _logger.info("Début synchronisation serveur: %s", server.name)
                # Utiliser sudo() pour éviter les problèmes de permissions
                result = server.sudo().action_sync_server(updating_client_ID=updating_client_ID)
                results[server.id] = result
                _logger.info("Synchronisation terminée pour serveur: %s", server.name)
            except Exception as e:
                errors[server.id] = str(e)
                _logger.error("Erreur synchronisation serveur %s: %s", server.name, e)
        
        # Créer un thread pour chaque serveur
        for server in servers:
            thread = threading.Thread(target=sync_server, args=(server,))
            thread.daemon = True
            thread.start()
            threads.append((server, thread))
        
        # Attendre la fin de tous les threads (timeout de 5 minutes)
        for server, thread in threads:
            thread.join(timeout=300)  # 5 minutes max par serveur
            
            if thread.is_alive():
                _logger.warning("Timeout lors de la synchronisation du serveur: %s", server.name)
                errors[server.id] = "Timeout"
        
        # Logger les résultats
        if errors:
            _logger.warning("Erreurs lors de la synchronisation: %s", errors)
        
        _logger.info("Synchronisation parallèle terminée: %d serveurs, %d succès, %d erreurs", 
                    len(servers), len(results), len(errors))
        
        return len(errors) == 0
    
    @api.model
    def action_sync_server_all(self):
        """
        Synchroniser tous les serveurs en parallèle
        """
        servers = self.search([('state', '=', 'open')])
        if servers:
            return servers._sync_servers_parallel()
        return True


class SaasPortalPlan(models.Model):
    """Optimisations pour saas_portal.plan"""
    _inherit = 'saas_portal.plan'
    
    @api.model
    def _auto_init(self):
        """Créer les index pour les plans"""
        super()._auto_init()
        
        try:
            self.env.cr.execute("""
                -- Index sur l'état du plan
                CREATE INDEX IF NOT EXISTS idx_saas_portal_plan_state 
                ON saas_portal_plan(state) 
                WHERE state IS NOT NULL;
                
                -- Index sur le serveur
                CREATE INDEX IF NOT EXISTS idx_saas_portal_plan_server 
                ON saas_portal_plan(server_id) 
                WHERE server_id IS NOT NULL;
                
                -- Index sur la séquence (pour le tri)
                CREATE INDEX IF NOT EXISTS idx_saas_portal_plan_sequence 
                ON saas_portal_plan(sequence);
            """)
            _logger.info("Index pour saas_portal.plan créés avec succès")
        except Exception as e:
            _logger.warning("Erreur lors de la création des index plan: %s", e)
