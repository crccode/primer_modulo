# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
	'name': 'Curso de programacion odoo',
	'summary': 'Invoices & Payments',
	'author': 'christian',
	'category': 'General',
	'application': True,
	'version': '1.2',
	# Instlamaos el modlo mail para tener registro de las modificaciones
	'depends': ['mail', 'base'],
	'data': [
		'views/menu_view.xml',
		'views/libros_view.xml',
		'report/daily_external_layout.xml',
		'security/libreria_security.xml',
		'security/ir.model.access.csv'
	],

}
