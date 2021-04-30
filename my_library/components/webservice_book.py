# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
import ftplib, json, os

class WebserviceBook(Component):
    _name = "base.webservice.book"
    _inherit = "base.webservice.adapter"
    _webservice_protocol = "sftpBook"

    def uploadFTP(self, url, user, password, file_data, file_name):
        session = ftplib.FTP(url, user, password)

        localfilepath = '/home/ferran/odoo-dev13/edi_test/my_library/temp_files/'

        # Create temporary json file to send it
        with open(localfilepath + file_name, 'w') as file:
            json.dump(json.loads(file_data), file)


        session.cwd('/home/ftpuser/my_library')
        session.storbinary('STOR '+file_name, open(localfilepath + file_name, 'rb'))
        session.quit()

        # Delete the temporary file
        os.remove(localfilepath+file_name)

    def getFTP(self, url, user, password):
        session = ftplib.FTP(url, user, password)
        localfilepath = '/home/ferran/odoo-dev13/edi_test/my_library/temp_files/'

        # Change server directory
        session.cwd('/home/ftpuser/my_library')
        # Sort the files by date and get the oldest one in the SFTP server
        file_name = sorted(session.nlst(), key=lambda x: session.voidcmd(f"MDTM {x}"))[0]

        session.retrbinary("RETR " + file_name, open(localfilepath+file_name, 'wb').write)
        # Delete the file since it has been downloaded
        session.delete(file_name)

        # Parse the json file into a string (it is needed to return a string)
        with open(localfilepath+file_name, 'r') as file:
            file_data = json.dumps(json.load(file))

        os.remove(localfilepath+file_name)
        session.quit()
        return file_data