{
    'name': 'Product Price Factor',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'Sales',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Add price factor to product attribute values',
    'description': """
Product Price Factor
====================

This module adds the ability to define price factors on product attribute values.
When creating product variants, the price can be calculated using these factors.

Features:
---------
* Add price_factor field to product.attribute.value
* Calculate variant prices based on attribute value price factors
* Multiplier effect for pricing based on product attributes

Use Cases:
----------
* Different pricing for different product attributes (size, color, etc.)
* Subscription period multipliers (monthly, quarterly, yearly)
* User-based pricing multipliers
    """,
    'depends': ['product', 'sale'],
    'data': [
        'views/product_attribute_value_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'sequence': 10,
    'auto_install': False,
}

