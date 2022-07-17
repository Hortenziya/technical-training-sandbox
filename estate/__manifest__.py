{
	'name': 'Estate',
	'depends': [
		'base'
	],
	'data': [
		'security/ir.model.access.csv',
		'security/security.xml',
		'security/ir_rule.xml',
		
		'views/res_users_view.xml',
		'views/estate_property_offer_views.xml',
		'views/estate_property_tag_views.xml',
		'views/estate_tag_menu_views.xml',
		'views/estate_property_type_views.xml',
		'views/estate_type_menu_views.xml',
		'views/estate_property_views.xml',
		'views/estate_menu_views.xml'
	],
	
	'application': True
}