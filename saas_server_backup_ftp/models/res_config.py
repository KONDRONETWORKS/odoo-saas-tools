import base64
import paramiko

from odoo import models, fields, api
from odoo import _, exceptions

import logging
_logger = logging.getLogger(__name__)
try:
    import pysftp
except ImportError:
    _logger.debug(
        '''saas_server_backup_ftp requires the python library
        pysftp which is not found on your installation''')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sftp_server = fields.Char(
        string='SFTP Server Address',
        config_parameter='saas_server.sftp_server',
        help='IP address of your remote server. For example 192.168.0.1'
    )
    
    sftp_username = fields.Char(
        string='Username on SFTP Server',
        config_parameter='saas_server.sftp_username',
        help='The username where the SFTP connection should be made with. This is the user on the external server.'
    )
    
    sftp_password = fields.Char(
        string='Password User SFTP Server',
        config_parameter='saas_server.sftp_password',
        help='The password from the user where the SFTP connection should be made with. This is the password from the user on the external server.'
    )
    
    sftp_path = fields.Char(
        string='Path external server',
        config_parameter='saas_server.sftp_path',
        help='The location to the folder where the dumps should be written to. For example /odoo/backups/. Files will then be written to /odoo/backups/ on your remote server.'
    )
    
    sftp_public_key = fields.Char(
        string='SFTP-Server public key',
        config_parameter='saas_server.sftp_public_key',
        help='Verify SFTP server\'s identity using its public rsa-key. The host key verification protects you from man-in-the-middle attacks'
    )
    
    rsa_key_path = fields.Char(
        string='Path to RSA key on Odoo server',
        config_parameter='saas_server.rsa_key_path',
        help='The location to the folder where the rsa key is saved. For example /opt/odoo/.ssh/id_rsa.'
    )
    
    rsa_key_passphrase = fields.Char(
        string='Passphrase for RSA key',
        config_parameter='saas_server.rsa_key_passphrase',
        help='Passphrase used when rsa key was generated'
    )

    def test_sftp_connection(self):
        params = {
            "host": self.sftp_server,
            "username": self.sftp_username,
        }

        try:
            # Connect with external server over SFTP,
            # so we know sure that everything works.
            if self.rsa_key_path:
                params["private_key"] = self.rsa_key_path
                if self.rsa_key_passphrase:
                    params["private_key_pass"] = self.rsa_key_passphrase
            else:
                params["password"] = self.sftp_password

            # not empty sftp_public_key means that we should verify sftp server with it
            cnopts = pysftp.CnOpts()
            if self.sftp_public_key:
                key = paramiko.RSAKey(data=base64.b64decode(self.sftp_public_key))
                cnopts.hostkeys.add(self.sftp_server, 'ssh-rsa', key)
            else:
                cnopts.hostkeys = None

            with pysftp.Connection(**params, cnopts=cnopts):
                raise exceptions.Warning(_("Connection Test Succeeded!"))

        except (pysftp.CredentialException,
                pysftp.ConnectionException,
                pysftp.SSHException):
            _logger.info("Connection Test Failed!", exc_info=True)
            raise exceptions.Warning(_("Connection Test Failed!"))
