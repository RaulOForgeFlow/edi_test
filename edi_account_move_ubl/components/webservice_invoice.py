import ftplib
import os

from odoo.addons.component.core import Component


class WebserviceInvoice(Component):
    _name = "base.webservice.invoice"
    _usage = "webservice.request"
    _webservice_protocol = "sftpInvoice"

    def uploadFTP(self, url, user, password, file_name, ftpDirectory, ftp_subdirectory):
        session = ftplib.FTP(url, user, password)

        # the path is the current one + the folder where
        # temporary files are stored and later on deleted
        filepath = (
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            + "/temp_files/"
            + file_name
        )

        # Change server directory
        session.cwd(ftpDirectory + "/" + ftp_subdirectory)
        # Upload the file
        session.storbinary("STOR " + file_name, open(filepath, "rb"))
        session.quit()

        # Delete the temporary file
        os.remove(filepath)

    def getFTP(self, url, user, password, ftpDirectory, ftp_subdirectory):
        session = ftplib.FTP(url, user, password)

        filepath = (
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/temp_files/"
        )

        session.cwd(ftpDirectory + "/" + ftp_subdirectory)

        # Sort the files by date and get the oldest one in the SFTP server
        file_name = sorted(session.nlst(), key=lambda x: session.voidcmd(f"MDTM {x}"))[
            0
        ]
        filepath += file_name

        # Get the file
        session.retrbinary("RETR " + file_name, open(filepath, "wb").write)

        # Delete the file since it has already been downloaded
        session.delete(file_name)

        xml_string = open(filepath).read()
        xml_bytes = xml_string.encode(encoding="UTF-8")
        os.remove(filepath)
        session.quit()

        return xml_bytes
