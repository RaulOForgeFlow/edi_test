from odoo.addons.component.core import Component
from odoo.tools import file_open
import base64, os, logging

logger = logging.getLogger(__name__)

class EdiProductProcess(Component):
    _name = "edi.input.process.product"
    _usage = "input.process"
    _backend_type = "product"
    _exchange_type = "product_update"
    _inherit = ["edi.component.input.mixin"]

    def process(self):

        #file_content = self.exchange_record._get_file_content()
        #xml_root = ET.fromstring(file_content)

        #tree = ET.parse('/home/ferran/odoo-dev13/edi-13.0-add-edi_rest/sale_order_import_ubl/tests/files/UBL-Order-2.0-Example.xml')
        #xml_root = tree.getroot()

        #data = self.env['sale.order.import'].import_order_button()
        #print(type(data))

        #localfilepath = "/home/ferran/odoo-dev13/edi_test/edi_sale_order_ubl/temp_files/temp.xml"
        localfilepath = "/home/local-odoo/raul/odoo-dev13/edi_test/edi_sale_order_ubl/temp_files/temp.xml"
        f = file_open(localfilepath, "rb")
        xml_file = f.read()
        wiz = self.env["sale.order.import"].create({"order_file": base64.b64encode(xml_file), "order_filename": 'temp.xml'})
        f.close()
        os.remove(localfilepath)
        action = wiz.import_order_button()

        # Associate the SO record created to the Exchange Record as a related record
        self.exchange_record.write({
            'model': 'sale.order',
            'res_id': action["res_id"]})


        #TODO: use the update_order_button in order to update an existing order in case they have same ID
        '''
        # Check whether this short_name already exists or not (similar to a PO ID)
        self.env.cr.execute("""select id from library_book lb where short_name like '{}'""".format(short_name))
        book_ids = [rec[0] for rec in self.env.cr.fetchall()]
        recordset = self.env['library.book'].browse(book_ids)
        if len(recordset) != 0:
            for book_record_short_name in recordset:
                book_record_short_name.write(values)
                self.exchange_record.write({
                    'model': 'library.book',
                    'res_id': book_record_short_name.id})
        # If not, create a new book with the information in data
        else:
            lib_book_model = self.env['library.book']
            lib_book_rec = lib_book_model.create(values)
            self.exchange_record.write({
                'model': 'library.book',
                'res_id': lib_book_rec.id})'''