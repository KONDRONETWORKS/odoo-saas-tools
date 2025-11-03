"""
Modèle de cache pour saas_portal_cache
"""
from odoo import models, api
import json
import logging
import hashlib

_logger = logging.getLogger(__name__)

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    _logger.warning("Redis n'est pas installé. Le cache Redis ne sera pas disponible.")


class SaasPortalCache(models.Model):
    """Gestionnaire de cache Redis pour SaaS Portal"""
    _name = 'saas_portal.cache'
    _description = 'SaaS Portal Cache Manager'
    
    def _get_redis_client(self):
        """Obtenir le client Redis"""
        if not REDIS_AVAILABLE:
            return None
        
        try:
            # Configuration Redis depuis les paramètres système
            redis_host = self.env['ir.config_parameter'].sudo().get_param(
                'saas_portal_cache.redis_host', 'localhost')
            redis_port = int(self.env['ir.config_parameter'].sudo().get_param(
                'saas_portal_cache.redis_port', '6379'))
            redis_db = int(self.env['ir.config_parameter'].sudo().get_param(
                'saas_portal_cache.redis_db', '0'))
            redis_password = self.env['ir.config_parameter'].sudo().get_param(
                'saas_portal_cache.redis_password', '')
            
            client = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                password=redis_password if redis_password else None,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test de connexion
            client.ping()
            return client
        except Exception as e:
            _logger.warning("Impossible de se connecter à Redis: %s", e)
            return None
    
    def _get_cache_key(self, prefix, *args):
        """Générer une clé de cache"""
        key_parts = [prefix] + [str(arg) for arg in args]
        key = ':'.join(key_parts)
        # Limiter la longueur et utiliser hash pour les longues clés
        if len(key) > 250:
            key_hash = hashlib.md5(key.encode()).hexdigest()
            key = f"{prefix}:{key_hash}"
        return f"saas_portal:{key}"
    
    def get(self, prefix, *args, default=None):
        """Récupérer une valeur du cache"""
        if not REDIS_AVAILABLE:
            return default
        
        client = self._get_redis_client()
        if not client:
            return default
        
        try:
            cache_key = self._get_cache_key(prefix, *args)
            value = client.get(cache_key)
            if value:
                return json.loads(value)
            return default
        except Exception as e:
            _logger.warning("Erreur lors de la récupération du cache: %s", e)
            return default
    
    def set(self, prefix, *args, value=None, ttl=300):
        """
        Mettre une valeur en cache
        :param prefix: Préfixe de la clé
        :param args: Arguments pour construire la clé
        :param value: Valeur à mettre en cache
        :param ttl: Time To Live en secondes (défaut: 5 minutes)
        """
        if not REDIS_AVAILABLE:
            return False
        
        client = self._get_redis_client()
        if not client:
            return False
        
        try:
            cache_key = self._get_cache_key(prefix, *args)
            json_value = json.dumps(value)
            client.setex(cache_key, ttl, json_value)
            return True
        except Exception as e:
            _logger.warning("Erreur lors de la mise en cache: %s", e)
            return False
    
    def delete(self, prefix, *args):
        """Supprimer une valeur du cache"""
        if not REDIS_AVAILABLE:
            return False
        
        client = self._get_redis_client()
        if not client:
            return False
        
        try:
            cache_key = self._get_cache_key(prefix, *args)
            client.delete(cache_key)
            return True
        except Exception as e:
            _logger.warning("Erreur lors de la suppression du cache: %s", e)
            return False
    
    def delete_pattern(self, pattern):
        """Supprimer toutes les clés correspondant à un pattern"""
        if not REDIS_AVAILABLE:
            return False
        
        client = self._get_redis_client()
        if not client:
            return False
        
        try:
            full_pattern = f"saas_portal:{pattern}"
            keys = client.keys(full_pattern)
            if keys:
                client.delete(*keys)
            return True
        except Exception as e:
            _logger.warning("Erreur lors de la suppression par pattern: %s", e)
            return False
    
    def clear_all(self):
        """Vider tout le cache SaaS Portal"""
        return self.delete_pattern("*")
    
    def get_stats(self):
        """Obtenir les statistiques du cache"""
        if not REDIS_AVAILABLE:
            return {'available': False}
        
        client = self._get_redis_client()
        if not client:
            return {'available': False, 'connected': False}
        
        try:
            info = client.info()
            keys = client.keys("saas_portal:*")
            return {
                'available': True,
                'connected': True,
                'total_keys': len(keys),
                'memory_used': info.get('used_memory_human', 'N/A'),
                'hits': info.get('keyspace_hits', 0),
                'misses': info.get('keyspace_misses', 0),
            }
        except Exception as e:
            _logger.warning("Erreur lors de la récupération des stats: %s", e)
            return {'available': True, 'connected': False, 'error': str(e)}


class SaasPortalClient(models.Model):
    """Optimisations avec cache pour saas_portal.client"""
    _inherit = 'saas_portal.client'
    
    def read(self, fields=None, load='_classic_read'):
        """Override read() pour utiliser le cache"""
        result = super().read(fields=fields, load=load)
        
        # Si lecture d'un seul enregistrement, mettre en cache
        if len(self) == 1 and result:
            cache_mgr = self.env['saas_portal.cache']
            cache_key = ('client', 'data', self.id)
            cache_mgr.set(*cache_key, value=result[0], ttl=300)
        
        return result
    
    @api.model
    def get_client_data_cached(self, client_id):
        """Récupérer les données client avec cache"""
        cache_mgr = self.env['saas_portal.cache']
        
        # Essayer de récupérer depuis le cache
        cached_data = cache_mgr.get('client', 'data', client_id)
        if cached_data:
            return cached_data
        
        # Si pas en cache, charger depuis la DB
        client = self.browse(client_id)
        if not client.exists():
            return None
        
        data = {
            'id': client.id,
            'name': client.name,
            'state': client.state,
            'users_len': client.users_len,
            'max_users': client.max_users,
            'file_storage': client.file_storage,
            'db_storage': client.db_storage,
            'expiration_datetime': client.expiration_datetime.isoformat() if client.expiration_datetime else None,
            'partner_id': client.partner_id.id if client.partner_id else None,
            'plan_id': client.plan_id.id if client.plan_id else None,
            'server_id': client.server_id.id if client.server_id else None,
        }
        
        # Mettre en cache pour 5 minutes
        cache_mgr.set('client', 'data', client_id, value=data, ttl=300)
        
        return data
    
    def write(self, vals):
        """Invalider le cache lors des modifications"""
        result = super().write(vals)
        
        # Invalider le cache pour les clients modifiés
        cache_mgr = self.env['saas_portal.cache']
        for client in self:
            cache_mgr.delete('client', 'data', client.id)
            # Invalider aussi les caches liés
            cache_mgr.delete_pattern(f"client:*:{client.id}")
        
        return result
    
    def unlink(self):
        """Invalider le cache lors de la suppression"""
        cache_mgr = self.env['saas_portal.cache']
        for client in self:
            cache_mgr.delete('client', 'data', client.id)
            cache_mgr.delete_pattern(f"client:*:{client.id}")
        
        return super().unlink()


class SaasPortalServer(models.Model):
    """Optimisations avec cache pour saas_portal.server"""
    _inherit = 'saas_portal.server'
    
    @api.model
    def get_server_list_cached(self):
        """Récupérer la liste des serveurs avec cache"""
        cache_mgr = self.env['saas_portal.cache']
        
        # Essayer depuis le cache
        cached = cache_mgr.get('server', 'list')
        if cached:
            return cached
        
        # Charger depuis la DB
        servers = self.search([('state', '=', 'open')])
        server_list = [{
            'id': s.id,
            'name': s.name,
            'host': s.host,
            'state': s.state,
        } for s in servers]
        
        # Mettre en cache pour 10 minutes
        cache_mgr.set('server', 'list', value=server_list, ttl=600)
        
        return server_list
    
    def write(self, vals):
        """Invalider le cache lors des modifications"""
        result = super().write(vals)
        
        # Invalider le cache de la liste des serveurs
        cache_mgr = self.env['saas_portal.cache']
        cache_mgr.delete('server', 'list')
        
        return result

