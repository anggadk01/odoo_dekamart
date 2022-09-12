from odoo import api, fields, models


class KelompokBarang(models.Model):
    _name = 'dekamart.kelompokbarang'
    _description = 'Ini adalah salah satu contoh model tabel Kelompok Barang!'

    #INI TEKS YG LAMA HARUS ISI MANUAL DI NAMA KELOMPOK
    #name = fields.Char(string='Nama Kelompok') 
    #---------------------------------------------
    #MEMBUAT SELECTION/OTOMATIS DI KELOMPOK BARANG DENGAN SINTAKS OFSE
    # Supaya tidak mengahasilan ouput  ganda 
    name = fields.Selection([
        ('makananbasah', 'Makanan Basah'),('makanankering','Makanan Kering'),('minuman','Minuman')
    ], string='Nama Kelompok')
    #-------------------------------------------------

    #INI TEKS YG LAMA HARUS ISI MANUAL DI KODE KELOMPOK
    #kode_kelompok = fields.Char(string='Kode Kelompok')
    #--------------------------------------------------
    # MEMBUAT COMPUTE ONCHANGE KODE KELOMPOK TO NAMA KELOMPOK DENGAN SINTAKS OFCO,
    #JADI TUH SEKALI GANTI NYESUAIN SAMA NAMA KELOMPOK DI FORM
    kode_kelompok = fields.Char(onchange='_compute_kode_kelompok', string='Kode Kelompok')
    @api.onchange('name') # name karna nyesuain dengan nama kelompok diatas
    def _compute_kode_kelompok(self):
        if (self.name == 'makananbasah'): # == isi dengan key yg ada di nama kelompok diatas
            self.kode_kelompok = 'mak01'
        elif (self.name == 'makanankering'):
            self.kode_kelompok = 'mak02'
        elif (self.name == 'minuman'):
            self.kode_kelompok = 'min'

    kode_rak = fields.Char(string='Kode Rak')
    #INI SINTAKS MAKE ONE TO MANY (OFO)
    barang_ids = fields.One2many(comodel_name='dekamart.barang', #INI NGAMBIL MODULENYA DI CLASS BARANG FILE BARANG.PY  
                                inverse_name='kelompokbarang_id', # MASIH SAMA DIATAS DAN ARAHIN KE KEY MTO BARANG 
                                      string='Daftar Barang')
            
    #SCRIPT HITUNG JML ITEM BARANG MENGGUNAKAN OFCO,
    jml_item = fields.Char(compute='_compute_jml_item', string='Jumlah Item')
    
    @api.depends('barang_ids') # NYESUAIIN NAME BARANG_IDS di dalamnynya
    def _compute_jml_item(self):
        for rec in self:
            a = self.env['dekamart.barang'].search([('kelompokbarang_id','=', rec.id)]).mapped('name')
            b = len(a)
            rec.jml_item = b
            rec.daftar = a
    
    # MEMBUAT DESK KELOMPOK BARANG APA SAJA ISINYA, DENGAN SINTAKS OFCHAR
    daftar = fields.Char(string='Daftar Isi')
    