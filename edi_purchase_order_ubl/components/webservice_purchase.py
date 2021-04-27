# Copyright 2020 Creu Blanca
# @author: Enric Tobella
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component
import requests, ftplib, os
from lxml import etree

class WebservicePurchase(Component):
    _name = "base.webservice.purchase"
    _usage = "webservice.request"
    _webservice_protocol = "http"

    def postHTTP(self, url, file_data, file_name):

        test_response = requests.post(url + 'post.php', files={"upfile":file_data}, data={"filename":'title.json'})
        if test_response.ok:
            print("Upload completed successfully!")
            print(test_response.text)
        else:
            print("Something went wrong!")

    def getHTTP(self, url):
        test_response = requests.get(url)
        if test_response.ok:
            print("Download completed successfully!")
        else:
            print("Something went wrong!")
        return test_response


    def uploadFTP(self, url, user, password, file_name):
        session = ftplib.FTP(url, user, password)

        localfilepath = '/home/ferran/odoo-dev13/edi_test/edi_purchase_order_ubl/temp_files/temp.xml'

        session.cwd('/home/ftpuser/uploads')
        session.storbinary('STOR temp.xml', open(localfilepath, 'rb'))
        session.quit()

        # Delete the temporary file
        #os.remove(localfilepath)


    def getFTP(self, url, user, password):
        session = ftplib.FTP(url, user, password)
        localfilepath = '/home/ferran/odoo-dev13/edi_test/edi_purchase_order_ubl/temp_files/temp.xml'

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