from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date
#Creamos un modelo a partir de una clase
class Autor(models.Model):
    # _name es la palabra reservada para crear tablas en la BD
    _name = 'autor'
    # La propiedad Recname devulve el valor que quieres mostrar en libros id
    _rec_name = 'last_name'
    # Nombre de los campos
    #  required=True de esta forma evitamos valores nulos a nivel de BD
    name = fields.Char(string="Nombre", related="avaluo_id.isbn")
    last_name = fields.Char(string="Apellido")
    # CAMPOS ONE2MANY
    #clave = fields.Many2one('libros', string="Seleccione el libro que escribio")
    avaluo_id = fields.Many2one('libros', string='Llave inversa', ondelete='cascade', index=True, copy=True)

    # CONFIGURACION PARA EL CAMPO ONE TO MANY
    valor = fields.Float(string="Valor", digits=(12, 2))
    codigo_id = fields.Many2one('libros', string='Codigo', ondelete='cascade', index=True, copy=True)
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    sequence = fields.Integer(string='Sequence', default=10)
    #
    # @api.onchange('name')
    # def _compute_description(self):
    #     self.name = 'hola'



    # TRABAJANDO CON FORMATOS DE FECHA
    def funcion_fecha(self):
        # Diccionarios de días y meses
        meses = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre",
        }

        dias = {
            0: "Domingo",
            1: "Lunes",
            2: "Martes",
            3: "Miércoles",
            4: "Jueves",
            5: "Viernes",
            6: "Sábado",
        }

        ahora = datetime.now()
        numero_mes = ahora.month
        # A entero para quitar los ceros a la izquierda en caso de que existan
        numero_dia = int(ahora.strftime("%w"))
        # Leer diccionario
        dia = dias.get(numero_dia)
        mes = meses.get(numero_mes)
        # Formatear
        fecha = "{}, {} de {} del {}".format(dia, ahora.day, mes, ahora.year)
        # Imprimir
        print(fecha)

        # Miércoles, 19 de Diciembre del 2018
    # Validation
    @api.onchange('last_name')
    def compute_campos(self):
        for rec in self:
            if (len(str(rec.last_name)) != 9):
                # raise ValidationError(('Numero no valido'))
                raise UserError('Error')

class Project(models.Model):
    _inherit = 'libros'
    # copy = FalsePara que cuando duplique un registro no trae la misma secuencia
    name = fields.Char(copy=False, default='New', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New')=='New':
            vals['name'] = self.env['ir.sequence'].next_by_code('task.1fpv') or 'New'
            res = super(Project, self).create(vals)
            return res
