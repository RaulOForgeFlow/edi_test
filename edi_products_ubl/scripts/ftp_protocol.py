import ftplib
import json
import time
import os

def uploadFTP():
    session = ftplib.FTP('192.168.1.50','ftpuser','userftpPassword')

    filename = 'second_updated.json'
    file = open('/home/ferran/odoo-dev13/edi_test/my_library/temp_files/'+filename, 'rb')

    session.cwd('/home/ftpuser/uploads')
    session.storbinary('STOR '+ filename, file)

    file.close()
    session.quit()

def getFTP():
    session = ftplib.FTP('192.168.1.50', 'ftpuser', 'userftpPassword')

    # Change server directory
    session.cwd('/home/ftpuser/uploads')
    # Sort the files by date and select the oldest [0] // newest = [-1]
    list = session.nlst()
    for name in list:
        if 'third' in name:
            file_name = name
    print(list)
    print(type(list))

    #file_name = sorted(session.nlst(), key=lambda x: session.voidcmd(f"MDTM {x}"))[0]
    # Get the file
    session.retrbinary("RETR " + file_name, open(file_name, 'wb').write)
    # Delete the file since it has been downloaded
    session.delete(file_name)


    with open(file_name, 'r') as file:
        file_data = json.dumps(json.load(file))
        print(file_data)
        print(type(file_data))
    session.quit()

if (__name__ == "__main__"):
    getFTP()


#https://stackoverflow.com/questions/12613797/python-script-uploading-files-via-ftp