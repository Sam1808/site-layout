import argparse
import json
import logging
import os
import requests
from requests.exceptions import ConnectionError, HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin

def get_book_raw_catalog(url, page_id):
    page_url=f'{url}{page_id}/'
    response = requests.get(page_url, allow_redirects=False)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    book_catalog_selector = '.bookimage a'
    book_catalog = soup.select(book_catalog_selector)
    return book_catalog

def get_book_properties(soup):
    book_properties_selector = 'h1'
    book = soup.select_one(book_properties_selector)
    separated_book = book.text.split('::')
    book_title = separated_book[0].strip()
    book_author = separated_book[1].strip()
    return book_title, book_author

def get_book_image_url(soup):
    book_image_selector = '.bookimage img'
    book_image = soup.select_one(book_image_selector)
    book_image_src = book_image['src']
    book_image_url = urljoin('http://tululu.org', book_image_src)
    return book_image_url

def get_book_comments(soup):
    book_comments_selector = '.texts'
    book_comments = soup.select(book_comments_selector)
    comments_scroll = []
    for comment in book_comments:
        comment_text = comment.text
        separated_comment_text = comment_text.split(')')
        real_comment = separated_comment_text[-1]
        if real_comment:
            comments_scroll.append(real_comment)
    return comments_scroll

def get_book_genres(soup):
    book_genres_selector = 'span.d_book a'
    book_genres = soup.select(book_genres_selector)
    genres_scroll = []
    for genre in book_genres:
        genres_scroll.append(genre.text)
    return genres_scroll

def download_image(url, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    image_filename = url.split('/')[-1]
    image_path = os.path.join(folder, image_filename)
    response = requests.get(url, allow_redirects=False)
    if response.status_code != 200:
        return None
    with open(image_path, 'wb') as file:
        file.write(response.content)
    return image_path

def download_txt(url, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    book_filename = '{}.txt'.format(sanitize_filename(filename))
    book_path = os.path.join(folder, book_filename)
    response = requests.get(url, allow_redirects=False)
    if response.status_code != 200:
        logging.info(f'Book: "{book_filename}" not available... Skiping...')
        return None
    with open(book_path, 'wb') as file:
        file.write(response.content)
    return book_path

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Book downloader (tululu.org)')
    parser.add_argument('--start_page', help='First page')
    parser.add_argument('--end_page', help='End page')
    parser.add_argument('--url', help='Url of section to download')
    parser.add_argument('--showlog', help='YES - to show log message')
    args = parser.parse_args()

    if not args.start_page:
        args.start_page = 1

    if not args.end_page:
        args.end_page = 1000

    url = args.url
    if not url:
        url = 'http://tululu.org/l55/'

    if args.showlog:
        logging.basicConfig(level=logging.INFO)

    # --------start TESTS -------

    try:
        response = requests.get(url, allow_redirects=False)
        response.raise_for_status()
    except ConnectionError:
        logging.error(f'Connection Error: Please check your Internet connection and try later.')
        exit()
    except HTTPError:
        logging.error(f'HTTP Error: Please check your URL and try again.')
        exit()

    if response.status_code != 200:
        logging.error(f'URL Error: Please check your URL and try again.')
        exit()

    try:
        start_page = int(args.start_page)
    except ValueError:
        logging.error(f'Start page error: only digits may be used.')
        exit()

    try:
        end_page = int(args.end_page)
    except ValueError:
        logging.error(f'End page error: only digits may be used.')
        exit()

    if end_page <= start_page:
        logging.error(f'Start page number can not be less or equal than End page number.')
        exit()

    # --------end TESTS -------

    books_description = []

    for page_id in range(start_page,end_page):

        book_catalog = get_book_raw_catalog(url,page_id)

        if not book_catalog:
            logging.info(f'There are no any pages with books to download. Last page number is {page_id -1}.')
            break

        for book in book_catalog:
            book_url = book['href']
            book_abs_url = urljoin('http://tululu.org', book_url)

            response = requests.get(book_abs_url, allow_redirects=False)
            response.raise_for_status()
            if response.status_code != 200:
                logging.info(f'URL {book_url} not available... Skiping...')
                continue

            soup = BeautifulSoup(response.text, 'lxml')

            book_title, book_author = get_book_properties(soup)

            book_image_url = get_book_image_url(soup)
            img_src = download_image(book_image_url)

            book_id = str(book_url[2:])
            download_url = f'http://tululu.org/txt.php?id={book_id}'
            book_path = download_txt(download_url, book_title)

            comments = get_book_comments(soup)
            genres = get_book_genres(soup)

            book_description = {
                'title': book_title,
                'book_author': book_author,
                'img_src': img_src,
                'book_path': book_path,
                'comments': comments,
                'genres': genres,
            }

            print(f'|-> Download: {book_path}')

            books_description.append(book_description)

    with open('books_description.json', 'w') as file:
        json.dump(books_description, file)
