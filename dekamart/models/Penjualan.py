from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError



class Penjualan(models.Model):
    _name = 'dekamart.penjualan'
    _description = 'FILE MODEL PENJUALAN UNTUK KEBUTUHAN USER DI DEKAMART'

    name = fields.Char(string='No. Nota')
    nama_pembeli = fields.Char(string='Nama Pembeli')
    tgl_penjualan = fields.Datetime(string='Tanggal Transaksi',
    default= fields.Datetime.now()
    )
    total_bayar = fields.Integer(compute='_compute_totalbayar',string='Total Pembayaran')
    detailpenjualan_ids = fields.One2many(comodel_name='dekamart.detailpenjualan', 
                        inverse_name='penjualan_id', 
                        string='Detail Penjualan')
    
    # INI RUMUS UNTUK MENGHITUNG JUMLAH SUBTOTAL YG ADA DI FORM & TREE TRANSAKSI
    @api.depends('detailpenjualan_ids')
    def _compute_totalbayar(self):
        for rec in self :
            a = sum (self.env['dekamart.detailpenjualan'].search([('penjualan_id','=',rec.id)]).mapped('subtotal'))
            rec.total_bayar = a
    

    # UNTUK MENGHAPUS ADA 2 METODE (ONDELETE DAN UNLINK)
    #MOTODE 1 ONDELETE INI RUMUS UNTUK MENSINKRONISASIKAN STOK DELETE BARANG DENGAN PENJUALAN YG BATAL
    # @api.ondelete(at_uninstall=False)
    # def __ondelete_penjualan(self):
    #     if self.detailpenjualan_ids:
    #         a = []
    #         for rec in self:
    #             a = self.env['dekamart.detailpenjualan'].search([('penjualan_id','=',rec.id)])
    #             print(a)
    #         for obj in a :
    #             print(str(obj.barang_id.name) + ' ' + str(obj.qty))
    #             obj.barang_id.stok += obj.qty # INI YG PENTING COK

    #MOTODE 2 UNLINK INI RUMUS UNTUK MENSINKRONISASIKAN STOK DELETE BARANG DENGAN PENJUALAN YG BATAL
    def unlink(self):
        if self.detailpenjualan_ids:
            a = []
            for rec in self:
                a = self.env['dekamart.detailpenjualan'].search([('penjualan_id','=',rec.id)])
                print(a)
            for obj in a :
                print(str(obj.barang_id.name) + ' ' + str(obj.qty))
                obj.barang_id.stok += obj.qty # INI YG PENTING COK
        record = super(Penjualan,self).unlink()

    # INI SINTAKS UNTUK MENGSINGKRONISASIKAN EDIT PENJUALAN DAN DAFTAR BARANG YG KE CANCEL
    def write(self,vals):
        for rec in self:
            a = self.env['dekamart.detailpenjualan'].search([('penjualan_id','=',rec.id)])
            print(a)
            for data in a:
                print(str(data.barang_id.name)+' '+str(data.qty)+' '+str(data.barang_id.stok))
                data.barang_id.stok += data.qty
        record = super(Penjualan,self).write(vals)
        for rec in self:
            b = self.env['dekamart.detailpenjualan'].search([('penjualan_id','=',rec.id)])
            print(a)
            print(b)
            for databaru in b:
                if databaru in a:
                    print(str(databaru.barang_id.name)+' '+str(databaru.qty)+' '+str(databaru.barang_id.stok))
                    databaru.barang_id.stok -= databaru.qty
                else:
                    pass
        return record
    

    #  INI SINTAKS UNTUK SQL CONSTRAIN GUNA MEMBUAT NO NOTA TIDAK BOLEH SAMA
    ('NAMA CONTARUNS'),('CONTARINS'),('PESAN YG AKAN DIKELUARKAN')
    _sql_constraints = [
        ('no_nota_unik','unique(name)',('Nota {} sudah ada yang menggunakannya!'))

    ]

class DetailPenjualan(models.Model):
    _name = 'dekamart.detailpenjualan'
    _description = 'FILE MODEL DETAIL PENJUALAN UNTUK KEBUTUHAN USER DI DEKAMART'

    name = fields.Char(string='Nama')
    penjualan_id = fields.Many2one(comodel_name='dekamart.penjualan', string='Detail Penjualan')
    barang_id = fields.Many2one(comodel_name='dekamart.barang', string='List Barang')
    harga_satuan = fields.Integer(string='Harga Satuan')
    qty = fields.Integer(string='Quantity')

    # OFCOMP SINTAKS UTK MENGAKUMULASIKAN HARGA SATUAN DAN QUANTITY USE API DEPENS FOR  
    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')
    
    @api.depends('harga_satuan','qty')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.harga_satuan * rec.qty

    # OFCAHNGE SINTAKSNYA UTK MENGOTOMATISKAN NOMINAL DI BARANG ID
    @api.onchange('barang_id')
    def _onchange_barang_id(self):
        if (self.barang_id.harga_jual):
            self.harga_satuan = self.barang_id.harga_jual
    
    # API CREATE UTK MENYAMAKAN JUMLAH STOK BARANG DENGAN PENJUALAN
    @api.model
    def create(self,vals):
        record = super(DetailPenjualan,self).create(vals)
        if record.qty:
            self.env['dekamart.barang'].search([('id','=',record.barang_id.id)]).write({'stok':record.barang_id.stok - record.qty})
            return record

    # API CONSTRAIN UTK SYARAT KRITERIA PENJUALAN < 1 DAN >= STOK BARANG
    @api.constrains('qty')
    def check_quantity(self):
        for rec in self:
            if rec.qty < 1:  # INI UNTUK PENUALAN < 1
                raise ValidationError("Anda belom memasukan jumlah {} yang ini dibeli!".format(rec.barang_id.name)) 
            elif (rec.barang_id.stok < rec.qty): # INI UNTUK >= STOK BARANG
                raise ValidationError("Stok {} tidak mencukupi!,hanya tersedia {}".format(rec.barang_id.name,rec.barang_id.stok))

    
    
    
    
    

    
    
