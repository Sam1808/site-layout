
import json
import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin

def get_book_raw_catalog(url, page_id):
    page_url=f'{url}{page_id}/'
    response = requests.get(page_url)
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
        return None
    with open(book_path, 'wb') as file:
        file.write(response.content)
    return book_path

if __name__ == '__main__':



    books_description = []

    for page_id in range(1,2):

        url = 'http://tululu.org/l55/'
        book_catalog = get_book_raw_catalog(url,page_id)

        for book in book_catalog:
            book_url = book['href']
            book_abs_url = urljoin('http://tululu.org', book_url)

            response = requests.get(book_abs_url, allow_redirects=False)
            response.raise_for_status()
            if response.status_code != 200:
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

            books_description.append(book_description)

    with open('books_description.json', 'w') as file:
        json.dump(books_description, file)
