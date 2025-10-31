from odoo import models, fields


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    price_factor = fields.Float(
        string='Price Factor',
        default=1.0,
        digits=(16, 4),
        help='Price factor to apply when this attribute value is selected. '
             'The base price will be multiplied by this factor. '
             'Example: 1.0 = same price, 1.5 = 50% increase, 0.5 = 50% discount')

    def _get_price_factor(self):
        """
        Get the price factor for this attribute value.
        Returns 1.0 by default if not set.

        :return: float - Price factor
        """
        return self.price_factor if self.price_factor else 1.0


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _get_price_factor_total(self):
        """
        Calculate the total price factor for this product variant
        based on all its attribute values.

        :return: float - Total price factor
        """
        factor = 1.0
        for ptav in self.product_template_attribute_value_ids:
            attr_value = ptav.product_attribute_value_id
            if attr_value and hasattr(attr_value, 'price_factor'):
                factor *= attr_value._get_price_factor()
        return factor


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _compute_price_factor_helper(self):
        """
        Helper method to compute price factor for variants.
        This can be used by other modules that need to apply price factors.
        """
        for variant in self.product_variant_ids:
            factor = variant._get_price_factor_total()
            # This method can be extended by other modules to actually apply the factor
            # For example, in sale.order.line or product.pricelist
            return factor

