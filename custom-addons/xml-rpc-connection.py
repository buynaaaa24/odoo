# import xmlrpc.client
#
# url = 'http://localhost:8017/'
# username = 'admin'
# password = 'admin'
# db = 'odoo17_b'
#
# # Authenticate user
# common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
# user_uid = common.authenticate(db, username, password, {})
#
# if user_uid:
#     models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
#
#     # Search for estate.property records
#     property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'search', [[]])
#     print("search ==> ", property_ids)
#
#     # Get the count of estate.property records`
#     count_property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'search_count', [[]])
#     print("count ==> ", count_property_ids)
#
#     # Read property names
#     read_property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'read', [property_ids], {'fields': ['name']})
#     print("read ==> ", read_property_ids)
#
#     # Search and read property names
#     search_read_property_ids = models.execute_kw(db, user_uid, password, 'estate.property', 'search_read', [[]], {'fields': ['name']})
#     print("search_read ==> ", search_read_property_ids)
#
#     #Create a new property
#     create_property_id = models.execute_kw(db, user_uid, password, 'estate.property', 'create', [{'name': 'Property from RDC', 'sales_id':7}])
#     print("create property ==> ", create_property_id)
#     #Write a new property
#     write_property_id = models.execute_kw(db, user_uid, password, 'estate.property', 'write',[[17], {'name': 'Property from RDC Updated V2'}])
#     read_name_get = models.execute_kw(db, user_uid, password, 'estate.property', 'name_get',[[17]])
#     print("update property ==> ", read_name_get)
#
#     unlink_property_id = models.execute_kw(db, user_uid, password, 'estate.property', 'unlink',[[17]])
#     print("unlink property ==> ", unlink_property_id)
# else:
#     print("Authentication failed.")
