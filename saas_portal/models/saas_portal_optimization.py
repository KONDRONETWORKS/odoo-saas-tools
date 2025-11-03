"""
Performance optimizations for SaaS Portal.
- Database indexes for improved search performance
- Parallel server synchronization
"""
from odoo import models, api
import logging
import threading

_logger = logging.getLogger(__name__)


class SaasPortalClient(models.Model):
    """Optimizations for saas_portal.client."""
    _inherit = 'saas_portal.client'
    
    @api.model
    def _auto_init(self):
        """Create database indexes during installation/update."""
        super()._auto_init()
        
        try:
            self.env.cr.execute("""
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_state 
                ON saas_portal_client(state) 
                WHERE state IS NOT NULL;
                
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_expiration 
                ON saas_portal_client(expiration_datetime) 
                WHERE expiration_datetime IS NOT NULL;
                
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_partner 
                ON saas_portal_client(partner_id) 
                WHERE partner_id IS NOT NULL;
                
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_server 
                ON saas_portal_client(server_id) 
                WHERE server_id IS NOT NULL;
                
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_plan 
                ON saas_portal_client(plan_id) 
                WHERE plan_id IS NOT NULL;
                
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_exp_state 
                ON saas_portal_client(expiration_datetime, state) 
                WHERE expiration_datetime IS NOT NULL;
                
                CREATE INDEX IF NOT EXISTS idx_saas_portal_client_name 
                ON saas_portal_client(name);
            """)
            _logger.info("Database indexes created successfully")
        except Exception as e:
            _logger.warning("Error creating indexes: %s", e)


class SaasPortalServer(models.Model):
    """Optimizations for saas_portal.server with parallel synchronization."""
    _inherit = 'saas_portal.server'
    
    @api.model
    def _auto_init(self):
        """Create indexes for servers."""
        super()._auto_init()
        
        try:
            self.env.cr.execute("""
                CREATE INDEX IF NOT EXISTS idx_saas_portal_server_active 
                ON saas_portal_server(active) 
                WHERE active IS NOT NULL;
                
                CREATE INDEX IF NOT EXISTS idx_saas_portal_server_name 
                ON saas_portal_server(name);
            """)
            _logger.info("Indexes for saas_portal.server created successfully")
        except Exception as e:
            _logger.warning("Error creating server indexes: %s", e)
    
    def action_sync_server(self, updating_client_ID=None):
        """Optimized synchronization with parallel support."""
        if len(self) == 1:
            return super().action_sync_server(updating_client_ID=updating_client_ID)
        return self._sync_servers_parallel(updating_client_ID)
    
    def _sync_servers_parallel(self, updating_client_ID=None):
        """Synchronize multiple servers in parallel."""
        servers = self.filtered('active')
        
        if not servers:
            return True
        
        threads = []
        results = {}
        errors = {}
        
        def sync_server(server):
            """Function to synchronize a server in a thread."""
            try:
                _logger.info("Starting synchronization for server: %s", server.name)
                result = server.sudo().action_sync_server(updating_client_ID=updating_client_ID)
                results[server.id] = result
                _logger.info("Synchronization completed for server: %s", server.name)
            except Exception as e:
                errors[server.id] = str(e)
                _logger.error("Error synchronizing server %s: %s", server.name, e)
        
        for server in servers:
            thread = threading.Thread(target=sync_server, args=(server,))
            thread.daemon = True
            thread.start()
            threads.append((server, thread))
        
        for server, thread in threads:
            thread.join(timeout=300)
            if thread.is_alive():
                _logger.warning("Timeout during synchronization of server: %s", server.name)
                errors[server.id] = "Timeout"
        
        if errors:
            _logger.warning("Errors during synchronization: %s", errors)
        
        _logger.info("Parallel synchronization completed: %d servers, %d success, %d errors", 
                    len(servers), len(results), len(errors))
        
        return len(errors) == 0


class SaasPortalPlan(models.Model):
    """Optimizations for saas_portal.plan."""
    _inherit = 'saas_portal.plan'
    
    @api.model
    def _auto_init(self):
        """Create indexes for plans."""
        super()._auto_init()
        
        try:
            self.env.cr.execute("""
                CREATE INDEX IF NOT EXISTS idx_saas_portal_plan_state 
                ON saas_portal_plan(state) 
                WHERE state IS NOT NULL;
                
                CREATE INDEX IF NOT EXISTS idx_saas_portal_plan_server 
                ON saas_portal_plan(server_id) 
                WHERE server_id IS NOT NULL;
                
                CREATE INDEX IF NOT EXISTS idx_saas_portal_plan_sequence 
                ON saas_portal_plan(sequence);
            """)
            _logger.info("Indexes for saas_portal.plan created successfully")
        except Exception as e:
            _logger.warning("Error creating plan indexes: %s", e)
