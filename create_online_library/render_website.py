import json
import math
import os

from http.server import HTTPServer, SimpleHTTPRequestHandler
from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape

def on_reload():
    create_template(books_description)
    print('DONE!')


def create_template(books_description):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')



    pagenumber = 1
    step = 20
    books_count = len(books_description)

    folder = 'pages'
    total_pages = math.ceil(books_count/step)
    page_numbers = list(range(1,total_pages+1))


    os.makedirs(folder, exist_ok=True)


    for books in range(0,books_count, step):
        rendered_page = template.render(
            books_description=books_description[books:books+step],
            page_numbers=page_numbers,
        )
        filename = f'index{pagenumber}.html'
        filename_path = os.path.join(folder, filename)
        with open(filename_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)
        pagenumber = pagenumber + 1



with open("books_description.json", "r") as my_file:
  books_description_json = my_file.read()

books_description = json.loads(books_description_json)
print (books_description[0])


server = Server()
server.watch('template.html', on_reload)
server.serve(root='.')