{
    "name": "Real Estate Ads",
    # "version" : "1",
    "website" :"https//www.odoo17_b.com",
    "author":"Buynaa",
    "description":"""
        Real Estate module to show available properties
        """,
    "category":"Sales",
    "depends":["base"],
    "data":[
        'security/ir.model.access.csv',
        'security/res_groups.xml',

        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/property_offer_view.xml',
        'views/menu_items.xml',

        # Data Files
        #'data/property_type.xml'
        'data/estate.property.type.csv'
        ],
        'demo':[
            'demo/property_tag.xml'
        ],
        'assets': {
            'web.assets_backend': [
                'real_estate_ads/static/src/js/custom_action.js',
                ],
            'web.assets_qweb': [
                'real_estate_ads/static/src/xml/my_custom_tag.xml',
            ],
        },
        "installable": True,
        "application": True,
        "license":"GPL-3"
}