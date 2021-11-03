from odoo import models, fields
#Creamos un modelo a partir de una clase
class Libros(models.Model):
    #_name es la palabra reservada para crear tablas en la BD
    _name = 'libros'
    # Nombre de los campos
    #  required=True de esta forma evitamos valores nulos a nivel de BD
    # Heredamos el mail y habilitar la funcionalidad en la vista descpues de la etiqueta </sheet>
    _inherit= ['mail.thread','mail.activity.mixin']
    name = fields.Char(string="Nombre del libro", required=True, tracking=True)  #tracking=True esta propiedad poner en los campos que quieras saber cuando se modifiquen
    editorial = fields.Char(string="Editorial", required=True)
    isbn = fields.Char(string="ISBN", required=True)
    #relacion Many palabras reservada conmdel_name= autor agragar a la vista este campo "libros_view"
    autor_id = fields.Many2one(comodel_name="autor", string="Autor", required=True)
    # Funcion related permite traer informacion de otro moodelo recibe el id . el campo ejm related="autor_id.last_name"
    lastname_autor = fields.Char(related="autor_id.last_name",string="Apellido del autor")
    # Creamos imagen para el libro
    image = fields.Binary(string="Image")
    # Badge estados  draft y published-< agregamos en la vista TREE
    state = fields.Selection([('draft','Borrador'),('published','Publicado')], default='draft')

    # Campo calculado  el store=true es para que se guarde en la BD
    description = fields.Char(string="Descripcion", compute="_compute_description")
    # Hce que se actualiza cada ves que se modifique el campo name   @api.depends('name')
    def _compute_description(self):
        self.description = self.name + '|' + self.isbn

    # Esta funcion no permite valores repetidos , caso de ya no querer la validacion se la debe quitar en postgre video16
    # nombre del sql contraint, unique(campo), mensaje de error
    _sql_constraints=[("name_uniq","unique(name,isbn)","El nombre del libro ya existe")]



