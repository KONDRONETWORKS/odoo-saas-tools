from odoo import http
from odoo.http import request
from odoo.tools.translate import _
import json

class PwaWebApp(http.Controller): 

    @http.route('/pwa/service_worker', type='http', auth="public", sitemap=False)
    def service_worker(self):
        qweb = request.env['ir.qweb'].sudo() 
        website = request.env['website'].sudo().get_current_website()
        languages = website.sudo().get_current_website().language_ids
        lang_code = request.env.lang
        current_lang = request.env['res.lang']._lang_get(lang_code)
        mimetype = 'text/javascript;charset=utf-8'
        content = qweb._render('theme_crest.service_worker_bits', {
            'website_id': website.id,
        })
        return request.make_response(content, [('Content-Type', mimetype)])
    

    @http.route('/get/pwa/manifest', type='http', auth="public", website=True)
    def get_pwa_manifest(self, website_id=None):
        website = request.env['website'].sudo().get_current_website() 
        vals =  {
            "name": website.pwa_app_name or "My E-commerce PWA",
            "short_name": website.pwa_short_name or "PWA",
            "start_url": website.pwa_start_url or "/shop",
            "display": "standalone", 
            "scope": "/",
            "background_color": website.pwa_background_color or "#ffffff",
            "theme_color": website.pwa_theme_color or "#000000",
            "icons": [
                {
                    "src": '/web/image/website/%s/pwa_image_192/512x512' % (website.id),
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": '/web/image/website/%s/pwa_image_512/512x512' % (website.id),
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }
        shortcuts = [{
            "name": sid.name,
            "short_name": sid.short_name,
            "description": sid.description,
            "url": sid.url,
            "icon": [{
                "src": "/web/image/pwa.shortcuts/%s/icon" %sid.id,
                "sizes": "192x192",
                "type": "image/png"
            }]
        }for sid in website.pwa_shortcuts_ids]
        vals.update({"shortcuts": shortcuts}) 

        return request.make_response(json.dumps(vals), [('Content-Type', 'application/json;charset=utf-8')]) 
