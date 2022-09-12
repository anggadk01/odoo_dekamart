from odoo import api, fields, models


class Barang(models.Model):
    _name = 'dekamart.barang'
    _description = 'Ini adalah salah satu contoh model tabel Barang!'

    name = fields.Char(string='Nama Barang')
    harga_beli = fields.Integer(string='Harga Modal',required=True)
    harga_jual = fields.Integer(string='Harga Jual', required=True)
    kelompokbarang_id = fields.Many2one(comodel_name='dekamart.kelompokbarang',
                                              string='Kelompok Barang',
                                            ondelete='cascade')
    
    # INI SINTAKS M2M ANTARA SUPPLIER DENGAN BARANG.PY
    supplier_id = fields.Many2many(comodel_name='dekamart.supplier', string='Supplier')
    stok = fields.Integer(string='Stok Barang')
    
    
    
    
