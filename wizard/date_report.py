# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import UserError


class DateReportWizard(models.TransientModel):
    _name = "reporte"
    # covid_19.date.report.wizard
    _description = "Report between date and by country"
    
    
    start_date=fields.Date('Start Date',required=True)
    end_date=fields.Date('End Date',required=True)
    country_ids = fields.Many2many(
                                    "res.country", 
                                    string="Countries", 
                                    help="Countries you want to generate the report"
                                    )

    # def print_report(self):
    #     print('VAMOS BIEN')
    #     return True

    # El domain esta compuesto por tres operadores atributo, operador, dato
    def print_report(self):
        # Instamciamos el objeto donde quiero ir a buscar mis datos
        Covid19=self.env['libros']
        # Primer condicion que el atributo date sea mayor a la date del objeto wizard y que sea menor a la fecha final
        # Pór defecto ejecutamos un "y" logico
        domain=[
                ('date','>',self.start_date),
                ('date','<',self.end_date)
                ]
        # Ejecucion de un "o" logico, si el date es mayor o menor que la fecha del wizard
        # domain = ['!',
        #     ('date', '>', self.start_date),
        #     ('date', '<', self.end_date)
        # ]

        # Preguntamos si tiene algun registro adicionamos al dominio otro condicion "y"
        if self.country_ids:
            domain.append(('country_id','in',self.country_ids.ids))
        # Debemos especificar cuales son los campos que quiero que me traiga
        covidField=[
                'editorial',
                'country_id',
                'isbn',
                ]
        # CovidRecords = Covid19.search_read(domain)   TRAE TODOS LOS CAMPOS

        # Ejecutamos nuestro ORM y lo guardamos en el registro
        CovidRecords=Covid19.search_read(domain,covidField)

        # Definimos un diccionario Buscamos la data y lo colocamos en un diccionario
        data={
            'CovidRecords': CovidRecords,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'country_ids': self.country_ids,
                }
        print(data)
        # return True
        # Debemos devolver la instancia de id?externo y ejecuto el action report le paso self que es el que se esta ejecutando y los datos que quiero renderizar en mi template
        return self.env.ref('datesReportExternalayout').report_action(self, data)
