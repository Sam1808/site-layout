import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_spirit(fraction):
    separated_spirit = fraction.split(':')
    spirit = separated_spirit[1]
    return spirit.strip()

def get_total_wine_list(wine_description):
    total_wine_list = []
    wine_specification = {}
    separated_description = wine_description.split('\n')
    for fraction in reversed(separated_description): # order matters!
        if 'Название' in fraction:
            wine_specification['title'] = get_spirit(fraction)
            total_wine_list.append(wine_specification)
            wine_specification = {}
        elif 'Сорт' in fraction:
            wine_specification['sort'] = get_spirit(fraction)
        elif 'Цена' in fraction:
            wine_specification['price'] = get_spirit(fraction)
        elif 'Картинка' in fraction:
            wine_specification['image'] = get_spirit(fraction)
        elif 'Выгодное предложение' in fraction:
            wine_specification['discount'] = True
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
        raw_data = file.read()

    beverages_description = raw_data.split('#')
    del beverages_description[0]

    kinds_of_beverages = []

    for kind in beverages_description:
        separated_kind = kind.split('\n')
        kind_of_beverages = separated_kind[0].strip()
        kinds_of_beverages.append(kind_of_beverages)

    total_beverages_info = {}

    for beverage in beverages_description:
        for kind in kinds_of_beverages:
            if kind in beverage:
                wines_list = get_total_wine_list(beverage)
                total_beverages_info[kind] = wines_list

    total_beverages_items = total_beverages_info.items()

    rendered_page = template.render(
        winery_age=winery_age,
        total_beverages_items = total_beverages_items,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()