import requests
from bs4 import BeautifulSoup

def post():
    #test_url = "http://httpbin.org/post"
    test_url = "http://localhost:80/post.php"
    test_file = open("/home/ferran/odoo-dev13/edi_test/my_library/files/cookbook.xml", "rb")
    test_response = requests.post(test_url, files={"upfile": test_file})
    if test_response.ok:
        print("Upload completed successfully!")
        print(test_response.text)
    else:
        print("Something went wrong!")


def get(test_url):
    test_response = requests.get(test_url)
    if test_response.ok:
        print("Download completed successfully!")
        #with open('/home/ferran/odoo-dev13/edi_test/my_library/files_get/file.xml', 'wb') as file:
        #    file.write(test_response.content)
    else:
        print("Something went wrong!")
    #print(type(test_response.content))
    #print(test_response.content)

def list_files(test_url):
    ext = 'xml'
    page = requests.get(test_url).text
    soup = BeautifulSoup(page, 'html.parser')
    files = [test_url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
    print(files)

if (__name__ == "__main__"):
    list_files("http://localhost/uploads")

