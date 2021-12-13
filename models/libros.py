from odoo import models, fields, api
from bs4 import BeautifulSoup
#Creamos un modelo a partir de una clase
class Libros(models.Model):
    #_name es la palabra reservada para crear tablas en la BD
    _name = 'libros'
    # Nombre de los campos
    #  required=True de esta forma evitamos valores nulos a nivel de BD
    # Heredamos el mail y habilitar la funcionalidad en la vista descpues de la etiqueta </sheet>
    _inherit= ['mail.thread','mail.activity.mixin']
    name = fields.Html(string="Nombre del libro", required=True, tracking=True)  #tracking=True esta propiedad poner en los campos que quieras saber cuando se modifiquen
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
    perc_complete = fields.Float('% Complete', (3, 2))
    # CAMPOS ONE2MANY
    autores_ids= fields.Many2many('autor', string="Seleciione los autores")
    # RELACION ONE2MANY
    autores_id = fields.One2many('autor', 'avaluo_id', string="Seleciione los autores")

    #FECHAS EN ODOO
    fecha = fields.Date()

    # Campo calculado  el store=true es para que se guarde en la BD  , compute="_compute_description"
    description = fields.Char(string="Descripcion")

    @api.depends('autor_id')
    def _compute_descripcion_general(self):
        if not self.name:
            self.name = "<table style='border-color:#fff;' class='table'><tbody>" \
                                       "<tr>" \
                                       "<td width='13%'><b>De la Ubicación</b></td>" \
                                       "<td width='87%'>Descripción de la Ubicacion</td>" \
                                       "</tr>" \
                                       "<tr><td><b>De la Zona</b></td><td>Descripción de la Zona</td></tr>" \
                                       "<tr><td><b>De la Delimitación</b></td><td>Descripción de la limitacion</td></tr>" \
                                       "<tr><td><b>De los Ambientes</b></td><td>Descripción de los ambientes</td></tr>" \
                                       "<tr><td><b>De la Distribución</b></td><td>Descripción de la distribución</td></tr>" \
                                       "<tr><td><b>Tipo de inmueble</b></td><td>Descripción de el tipo de inmueble</td></tr>" \
                                       "</tbody></table> "

        soup = BeautifulSoup(self.name, 'html.parser')
        rows = soup.findAll('td')[1::2]
        if self.autor_id:
            self.name = self.name.replace(str(rows[0]), '<td>' + str(self.name) + '</td>')
    # Hce que se actualiza cada ves que se modifique el campo name
    @api.depends('name','isbn')
    def _compute_description(self):
        self.description = self.name + '|' + self.isbn
    # Esto solo se usa en el reporte
    def ejemplo_pdf(self):
         description = "Funciom ejemplo_pdf()"
         return description
    # Recorrer una tabla One2many
    # def poner_lista(self)
    #     total = []
    #     for line in self.autores_id:
    #         if line.name != "Terreno":
    #             total.append(line.name)
    #     return total

    # Esta funcion no permite valores repetidos , caso de ya no querer la validacion se la debe quitar en postgre video16
    # nombre del sql contraint, unique(campo), mensaje de error
    _sql_constraints=[("name_uniq","unique(name,isbn)","El nombre del libro ya existe")]
    # FIN









