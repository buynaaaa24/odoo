{
    "name": "Real Estate Ads",
    "website": "https://www.odoo17_b.com",
    "author": "Buynaa",
    "description": """
        Real Estate module to show available properties
        """,
    "category": "Sales",
    "depends": ["base", "mail", "website","hr"],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "views/property_view.xml",
        "views/property_type_view.xml",
        "views/property_tag_view.xml",
        "views/property_offer_view.xml",
        "views/menu_items.xml",
        "views/property_web_template.xml",
        "views/employee_view.xml",
        "data/estate.property.type.csv",
        "data/mail_template.xml",
        "report/report_template.xml",
        "report/property_report.xml"
    ],
    "demo": [
        "demo/property_tag.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "real_estate_ads/static/src/js/custom_action.js"
        ],
        "web.assets_qweb": [
            "real_estate_ads/static/src/xml/my_custom_tag.xml"
        ],
        "website.assets_frontend": [
            "real_estate_ads/static/static-description-index.html"
        ]
    },
    "installable": True,
    "application": True,
    "license": "GPL-3",
    "currency": "MNT",
    "price": "590.000",
    "images": ["/main_screenshot.png"]
}
