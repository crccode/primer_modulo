from odoo import models, fields, api
#Creamos un modelo a partir de una clase
class Autor(models.Model):
    # _name es la palabra reservada para crear tablas en la BD
    _name = 'autor'
    # La propiedad Recname devulve el valor que quieres mostrar en libros id
    _rec_name = 'last_name'
    # Nombre de los campos
    #  required=True de esta forma evitamos valores nulos a nivel de BD
    name = fields.Char(string="Nombre", required=True, related="avaluo_id.isbn")
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
