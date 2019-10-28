import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_spirit(wine):
    start_index = wine.find(':') + 1
    spirit = wine[start_index:]
    spirit = spirit.strip()
    return spirit

def get_total_wine_list(wine_description):
    total_wine_list = []
    wine_specification = {}
    wine_description = wine_description.split('\n')
    for wine in reversed(wine_description): # order matters!
        if 'Название' in wine:
            wine_specification.update({'title': get_spirit(wine)})
            total_wine_list.append(wine_specification)
            wine_specification = {}
        elif 'Сорт' in wine:
            wine_specification.update({'sort': get_spirit(wine)})
        elif 'Цена' in wine:
            wine_specification.update({'price': get_spirit(wine)})
        elif 'Картинка' in wine:
            wine_specification.update({'image': get_spirit(wine)})
        elif 'Выгодное предложение' in wine:
            wine_specification.update({'discount': 'yes'})
    return total_wine_list


if __name__ == '__main__':

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    year_of_foundation = 1920
    now = datetime.datetime.now()
    current_year = now.year
    winery_age = current_year - year_of_foundation

    with open('action.txt', 'r', encoding='UTF-8-sig') as file:
        beverages_description = file.read()

    beverages_description = beverages_description.split('#')
    types_of_beverages = []
    for type in beverages_description:
        if len(type):
            type_index = type.find('\n')
            type_of_beverages = type[:type_index]
            type_of_beverages = type_of_beverages.strip()
            types_of_beverages.append(type_of_beverages)

    total_beverages_info = {}

    for beverage in beverages_description:
        for type in types_of_beverages:
            if type in beverage:
                wines_list = get_total_wine_list(beverage)
                total_beverages_info.update({type: wines_list})

    rendered_page = template.render(
        winery_age=winery_age,
        types_of_beverages = types_of_beverages,
        total_beverages_info = total_beverages_info,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()