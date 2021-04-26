import ftplib

def count_files():
    session = ftplib.FTP('192.168.1.50','ftpuser','userftpPassword')
    session.cwd('/home/ftpuser/uploads')
    files = session.nlst()
    return files


if(__name__ == "__main__"):
    num_files = count_files()
    print (num_files)


#https://stackoverflow.com/questions/12613797/python-script-uploading-files-via-ftp