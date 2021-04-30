# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
import ftplib, os

class WebserviceInvoice(Component):
    _name = "base.webservice.invoice"
    _usage = "webservice.request"
    _webservice_protocol = "sftpInvoice"

    def uploadFTP(self, url, user, password, file_name):
        session = ftplib.FTP(url, user, password)

        localfilepath = '/home/ferran/odoo-dev13/edi_test/edi_account_move_ubl/temp_files/temp.xml'

        session.cwd('/home/ftpuser/uploads')
        session.storbinary('STOR temp.xml', open(localfilepath, 'rb'))
        session.quit()

        # Delete the temporary file
        os.remove(localfilepath)


    def getFTP(self, url, user, password):
        session = ftplib.FTP(url, user, password)
        localfilepath = '/home/ferran/odoo-dev13/edi_test/edi_account_move_ubl/temp_files/temp.xml'

        # Change server directory
        session.cwd('/home/ftpuser/uploads')

        # Get the file
        session.retrbinary("RETR temp.xml", open(localfilepath, 'wb').write)
        # Delete the file since it has been downloaded
        session.delete('temp.xml')

        xml_string = open(localfilepath).read()
        xml_bytes = xml_string.encode(encoding="UTF-8")
        os.remove(localfilepath)
        session.quit()
        return xml_bytes