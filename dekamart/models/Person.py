# SINTKAS MEMBUAT  CLASS NEW MODEL OMO
# JANGAN LUPA KALO UDH COMPALTE CONNETING FILE PERSON KE __INIT__.PY
# DAN CONNTING SEMUA CLASSNYA KE SECURITY ACCESS
from odoo import api, fields, models

# CLASS PERSON
class Person(models.Model):
    _name = 'dekamart.person'
    _description = 'FILE MODEL PERSON UNTUK KEBUTUHAN USER DI DEKAMART'

    name = fields.Char(string='Nama')
    alamat = fields.Char(string='Alamat')
    tgl_lahir = fields.Datetime(string='Tanggal Lahir')
    
# CLASS KASIR
class Kasir(models.Model):   # INI ADALAH CONTOH CLASS NAME KASIR DENGAN MENGGUNAKAN INHERIT 
    _name = 'dekamart.kasir' # NAMENYA DI LINE INI MENGHASILLKAN "NEW TABLE KASIR"
    _description = 'FILE MODEL KASIR UNTUK KEBUTUHAN USER DI DEKAMART'
    _inherit = 'dekamart.person'  # INHERIT ITU AKAN NYAMBUNG OTOMATIS KE CLASS PERSON
    
    id_kasir = fields.Char(string='ID Kasir')
        
# CLASS CLEANING SERVICE
class CleaningService(models.Model):
    _name = 'dekamart.cleaningservice'
    _description = 'FILE MODEL CLEANING SERVICE UNTUK KEBUTUHAN USER DI DEKAMART'
    _inherit = 'dekamart.person'
    
    id_cln = fields.Char(string='ID Cleaning Service')
    
