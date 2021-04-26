import json

def genJSON(book):

    data = {
        'name':book.name,
        'short_name': book.short_name,
        'cost_price': book.cost_price,
        'description': book.description,
        'date_release': str(book.date_release),
        'author_ids': book.author_ids.ids,
        'currency': book.currency.id,
        'pages': book.pages,
    }

    if book.cover != False:
        data['cover'] = book.cover.decode('utf-8')

    dict_file = json.dumps(data).encode('utf-8')
    file_name = book.short_name + '.json'
    return dict_file, file_name

if (__name__ == "__main__"):
    dict = genJSON('Harry Potter', 'HarryPoPoTah', 15)



