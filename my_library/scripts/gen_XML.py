import xml.etree.ElementTree as gfg
from lxml import etree
# name, short_name, cost_price, author_ids
def GenerateXML():
    '''
    root = etree.Element('odoo')

    record = etree.Element('record')
    record.text = 'id="book_cookbook" model="library.book">'
    root.append(record)

    field1 = etree.Element('field')
    field1.text ='name="name">Odoo Cookbook'
    record.append(field1)

    s = etree.tostring(root, pretty_print=True)

    tree = etree.ElementTree(root)
    with open('/home/ferran/odoo-dev13/edi_test/my_library/files/file.xml', "wb") as files:
        tree.write(files)
    print(s)
    '''

    root = gfg.Element("odoo")

    record = gfg.SubElement(root, "record")
    record.set("id", "book.exchange.title")
    record.set("model", "library.book")

    field1 = gfg.SubElement(record, "field")
    field1.set("name","name")
    '''
    field2 = gfg.SubElement(record, "field")
    field2.set("short_name", short_name)
    
    field3 = gfg.SubElement(record, "field")
    field3.set("name", date_release)
    
    field4 = gfg.SubElement(record, "field")
    field4.set("name", cost_price)

    field5 = gfg.SubElement(record, "field")
    field5.set("name", author_ids)

    
    tree = gfg.ElementTree(root)
        with open(fileName, "wb") as files:
            tree.write(files)
    '''
    move_file = gfg.tostring(root, encoding='utf8')
    return move_file

if (__name__ == "__main__"):
    file = GenerateXML()
    print(type(file))
