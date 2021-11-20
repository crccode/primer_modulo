from odoo import models, fields
#Creamos un modelo a partir de una clase
class Autor(models.Model):
    # _name es la palabra reservada para crear tablas en la BD
    _name = 'autor'
    # La propiedad Recname devulve el valor que quieres mostrar en libros id
    _rec_name = 'last_name'
    # Nombre de los campos
    #  required=True de esta forma evitamos valores nulos a nivel de BD
    name = fields.Char(string="Nombre", required=True)
    last_name = fields.Char(string="Apellido")
    # CAMPOS ONE2MANY
    #clave = fields.Many2one('libros', string="Seleccione el libro que escribio")