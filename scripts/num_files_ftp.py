import ftplib

def count_files(webservice_backend, ftp_subdirectory):
    url = webservice_backend.server_env_defaults['url_env_default']
    user = webservice_backend.server_env_defaults['username_env_default']
    password = webservice_backend.server_env_defaults['password_env_default']

    directory = webservice_backend.ftpDirectory + '/' + ftp_subdirectory

    session = ftplib.FTP(url, user, password)
    session.cwd(directory)
    files = session.nlst()
    return files
