from odoo import http
from odoo.http import request
from odoo.tools.translate import _

class CrmLeadController(http.Controller):
    @http.route('/form/product-inquiry-form', auth='public', type="json", website=True)
    def productinquiry_form(self,product_id=None,product_name=None,**kwargs,):
        
       return {
        'productinquiry_dialog': request.env["ir.ui.view"]._render_template("theme_crest.productinquiry_dialog_bits", {
            'product_id': product_id,
            'product_name': product_name,
        }),
        "product_id": product_id,
        "product_name": product_name
        }
       
    @http.route(['/form/crm'], type='json', auth="public", website=True)
    def create_crm_lead(self, **kwargs):
        # Check if required fields are present and not empty
        required_fields = ['name', 'email_from', 'phone']
        for field in required_fields:
            if not kwargs.get(field):
                return {'success': False, 'message': _("Please fill in all required fields.")}

        # Validate email format
        if '@' not in kwargs.get('email_from', ''):
            return {'success': False, 'message': _("Please enter a valid email address.")}

        # Validate phone number (basic check for non-empty string)
        if not kwargs.get('phone').strip():
            return {'success': False, 'message': _("Please enter a valid phone number.")}

        # If all checks pass, continue with lead creation
        lead_vals = {
            'name': kwargs.get('name'),
            'email': kwargs.get('email_from'),
            'phone': kwargs.get('phone'),
            'message': kwargs.get('description'),
            'product_id': int(kwargs.get('product_id')) if int(kwargs.get('product_id')) else False, 
        }
        request.env['product.inquiry'].sudo().create(lead_vals)
        
        return {'success': True, 'message': _("Thank you for your inquiry. We will get back to you soon.")}