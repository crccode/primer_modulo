from odoo import models, fields, api
from odoo.exceptions import ValidationError
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import io
import base64
from datetime import date
import re
#Creamos un modelo a partir de una clase


class Libros(models.Model):
    #_name es la palabra reservada para crear tablas en la BD
    _name = 'libros'
    # Nombre de los campos
    #  required=True de esta forma evitamos valores nulos a nivel de BD
    # Heredamos el mail y habilitar la funcionalidad en la vista descpues de la etiqueta </sheet>
    _inherit= ['mail.thread','mail.activity.mixin']
    name = fields.Char(string="Nombre del libro", tracking=True)  #tracking=True esta propiedad poner en los campos que quieras saber cuando se modifiquen
    _order = "name desc"
    editorial = fields.Char(string="Editorial", required=True)
    isbn = fields.Char(string="ISBN", required=True)

    # WIZARD
    date = fields.Datetime(string='Date Time', required=True, default=fields.Datetime.now())
    country_id = fields.Many2one('res.country', required=True)


    #relacion Many palabras reservada conmdel_name= autor agragar a la vista este campo "libros_view"
    autor_id = fields.Many2one(comodel_name="autor", string="Autor", required=True)
    # Funcion related permite traer informacion de otro moodelo recibe el id . el campo ejm related="autor_id.last_name"
    lastname_autor = fields.Char(related="autor_id.last_name",string="Apellido del autor")
    # Creamos imagen para el libro
    image = fields.Binary(string="Image") #, compute="_upload_grafico"
    # Badge estados  draft y published-< agregamos en la vista TREE
    state = fields.Selection([('draft','Borrador'),('published','Publicado')], default='draft')
    perc_complete = fields.Float('% Complete', (3, 2))
    # CAMPOS ONE2MANY
    autores_ids= fields.Many2many('autor', string="Seleciione los autores")
    # RELACION ONE2MANY CON AGREGAR NOTA , ENCABEZADO
    # autores_id = fields.One2many('autor', 'avaluo_id', string="Seleciione los autores")

    autores_id = fields.One2many('autor', 'codigo_id', string='Seleciione',
                                           states={'cancel': [('readonly', True)], 'done': [('readonly', True)]},
                                           copy=True, auto_join=True)

    #FECHAS EN ODOO
    fecha = fields.Date()
    gravamen = fields.Boolean(string="Inscripcion Gravamen")

    # Campo calculado  el store=true es para que se guarde en la BD  , compute="_compute_description"
    description = fields.Char(string="Descripcion")
    notas_aclarativas  = fields.Char(string="Notas Aclarativas")
    polo = fields.Text(string="hola")
    texto = 'holllllll'




    new_field = fields.Char(string="test", required=False, )

    @api.model
    def my_function(self):
        print("Hello Word");
    def print_barcode(self):
        print('Am here')
    # CREANDO VALOR POR DEFECTO DENTRO UNA FUNCION
    @api.model
    def get_default_auType(self):
        default_auType = 'type1'
        return default_auType

    auType = fields.Selection(selection=[('type1', 'Type 1'), ('type2', 'Type 2'), ], string='Type',
                              default=get_default_auType)
    # PROBANDO BOTON INTELIGENTE
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')
    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['autor'].search_count([('avaluo_id', '=', rec.id)])
            rec.appointment_count = appointment_count
    def action_open_appointments(self):
        print('yes')
        print(self.appointment_count)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'autor',
            'domain': [('avaluo_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'view_mode': 'tree,form',
            'target': 'current',
        }
    # PROBANDO SECUENCIA AUTOMATICA
    # reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
    #                         default=lambda self: _('New'))
    # reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    #
    # @api.model
    # def create(self, vals):
    #     if vals.get('reference', _('New')) == _('New'):
    #         vals['reference'] = self.env['ir.sequence'].next_by_code('libros') or _('New')
    #     res = super(Libros, self).create(vals)
    #     print(res)
    #     return res

    #Como no tiene un apidepends esta funcion se ejecuta siempre
    def _upload_grafico(self):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4], [1, 2, 0, 0.5])
        img = io.BytesIO()
        fig.savefig(img, format='png',
                    bbox_inches='tight')
        img.seek(0)
        encoded = base64.b64encode(img.getvalue())
        # self.image = encoded

    def ejemplo(self):
         self.texto = 'viernes'
    @api.onchange('image', 'isbn')
    def onchange_method(self):
        # self.ejemplo()
        print(self.env['res.currency'])
        self.name = self.texto


    # Hce que se actualiza cada ves que se modifique el campo name
    @api.depends('name','isbn')
    def _compute_description(self):
        self.description = self.name + '|' + self.isbn
    # Esto solo se usa en el reporte


    def ejemplo_pdf(self):
        # fig, ax = plt.subplots()
        # ax.plot([1, 2, 3, 4], [1, 2, 0, 0.5])
        # img = io.BytesIO()
        # fig.savefig(img, format='png',
        #             bbox_inches='tight')
        # img.seek(0)
        # encoded = base64.b64encode(img.getvalue())
        #
        # my_html = '<img src="data:image/png;base64, {}"/>'.format(encoded.decode('utf-8'))
        # panda = '"data:image/png;base64, {}"'.format(encoded.decode('utf-8'))
        texto = 'comomoomomomomomomo'
        return texto
        # return '<img src="data:image/png;base64, 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"/>'
    #GRAFICOS
    def fig_to_base64(fig):
        img = io.BytesIO()
        fig.savefig(img, format='png',
                    bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue())


    def grafico(self):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3, 4], [1, 2, 0, 0.5])
        img = io.BytesIO()
        fig.savefig(img, format='png',
                    bbox_inches='tight')
        img.seek(0)
        encoded = base64.b64encode(img.getvalue())

        my_html = '<img src="data:image/png;base64, {}"/>'.format(encoded.decode('utf-8'))
        # my_html9 = '"data:image/png;base64, {}"'.format(encoded.decode('utf-8'))
        my_html9 = 'data:image/png;base64, {}'.format(encoded.decode('utf-8'))
        self.polo = my_html

        return my_html9
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
    # OVERRIDE DEL METHOD ONCREATE Y GENERAR UN VALOR SECUENCIAL
    # reference = fields.Char(string='Order', required=True, copy=False, readonly=True,
    #                         default=lambda self: _('New'))
    # note = fields.Text(string='Description')
    # @api.model
    # def default_get(self, fields):
    #     res = super(Libros, self).default_get(fields)
    #     res['note'] = 'NEW Patient Created'
    #     return res
    #
    # @api.model
    # def create(self, vals):
    #     if not vals.get('note'):
    #         vals['note'] = 'New Libro'
    #     if vals.get('reference', _('New')) == _('New'):
    #         vals['reference'] = self.env['ir.sequence'].next_by_code('libros') or _('New')
    #     res = super(Libros, self).create(vals)
    #     return res

    # VALIDACIONES
    age = fields.Integer(string="Age")
    reference = fields.Integer(string="Age")
    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['libros'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(_("Name %s Already Exists" % rec.name))

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(_("Age Cannot Be Zero .. !"))

    # Metodo que devuelve una lista de nombres
    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         name = '[' + rec.reference + '] ' + rec.name
    #         result.append((rec.id, name))
    #     return result
    # Validacion de email_sql_constraints
    # lista de  (name, sql_definition, message)


    # _sql_constraints = [
    #     ('email_uniq', 'unique(email)', 'Email id is unique change your custom email id'),
    # ]
    # @api.constrains('email')
    # def validate_email(self):
    #     for obj in self:
    #         if obj.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", obj.email) == None:
    #             raise ValidationError("Please Provide valid Email Address: %s" % obj.email)
    #     return True
    #
    # @api.constrains('date_end')
    # def _check_date_end(self):
    #     for record in self:
    #         if record.date_end < fields.Date.today():
    #             raise ValidationError("The end date cannot be set in the past")

    # USANDO CURSOR EN BASE DE DATOS CON ODOO

    def _compute_precio_lote12(self):
        today = date.today()
        gestion = format(today.year)
        zona = '99'
        ciudad = 'Santa Cruz de la Sierra'
        tipo_pavimento = 'cemento'
        sql = "select " + tipo_pavimento + " from  avaluo_tabla_parametro as lista where  gestion_id ='" + gestion + "' and zona= '" + zona + "' and ciudad_id= '" + ciudad + "'"
        print(sql)
        try:
            cursor = self.env.cr
            cursor.execute(sql)
            res = str(cursor.fetchall())
            print(res)
            if res != '[]':
                cadena = res
                cad1 = cadena.lstrip("[(")
                cad2 = cad1.rstrip(",)]")
                print(cad2)
            else:
                print('ESTA VACIO')
        except:
            print('ERROR!')

    # BOTOM GEOLOCALIZATION
    texto_geo = fields.Char(string="Texto Geo")
    @api.model
    def _geo_localize(self, street=''):
        if street is None:
            print('VACIO')
        else:
            print('API MODEL '+street)
        result= street
        return result

    def geo_localize(self):
        # We need country names in English below

        result = self._geo_localize('hola street')
        print(result)
        for partner in self.with_context(lang='en_US'):
            print(partner.date)
            partner.write({
                # 'texto_geo': 'fields.Date.context_today(partner)'
                'texto_geo': fields.Date.context_today(partner)
            })
        return True

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    impuesto_api_key = fields.Char(
        string='Google Maps View Api Key',
        config_parameter='web_google_maps.api_key')
