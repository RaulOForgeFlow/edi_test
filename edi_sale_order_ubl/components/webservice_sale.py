# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
import ftplib, os

class WebserviceSale(Component):

    _name = "base.webservice.sale"
    _inherit = "base.webservice.adapter"
    _webservice_protocol = "sftpSale"

    def uploadFTP(self, url, user, password, file_name):
        session = ftplib.FTP(url, user, password)

        localfilepath = '/home/ferran/odoo-dev13/edi_test/edi_sale_order_ubl/temp_files/temp.xml'

        session.cwd('/home/ftpuser/sales')
        session.storbinary('STOR temp.xml', open(localfilepath, 'rb'))
        session.quit()

        # Delete the temporary file
        os.remove(localfilepath)


    def getFTP(self, url, user, password):
        session = ftplib.FTP(url, user, password)
        localfilepath = '/home/ferran/odoo-dev13/edi_test/edi_sale_order_ubl/temp_files/temp.xml'

        # Change server directory
        session.cwd('/home/ftpuser/purchases')

        # Get the file
        session.retrbinary("RETR temp.xml", open(localfilepath, 'wb').write)
        # Delete the file since it has been downloaded
        session.delete('temp.xml')

        xml_string = open(localfilepath).read()
        xml_bytes = xml_string.encode(encoding="UTF-8")
        session.quit()
        return xml_bytes