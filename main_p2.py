import requests
from bs4 import BeautifulSoup
import os
import os.path
import csv
import re

# BASIC OPERATIONS
def count_element_in_list(list, element):
    items_count = []
    for i_elem, item in enumerate(list, 0):
        if item == element:
            items_count.append(item)
    return items_count

def count_directories_parents(path):
    try:
        path_split = path.split('../')
        value_parents = count_element_in_list(path_split, '')
        count = len(value_parents)
    except:
        count = 0
    return count

def merge_link_to_url(url, link):
    url_split = url.split('/')
    value = count_directories_parents(link)

    for i in range(0, value + 1):
        del url_split[len(url_split) - 1]

    path_OK = convert_array_to_string(url_split, '/') + '/' + link.replace('../', '')

    return path_OK

def convert_array_to_string(tableau, separator):
    newLine = ''
    for i, elem in enumerate(tableau, 0):
        if i == 0:
            newLine += str(elem)
        else:
            newLine += str(separator) + str(elem)
    return newLine

def addFolder(pathRootFolder, nameNewFolder):
    tempoNewFolder = os.path.join(pathRootFolder, nameNewFolder)
    if not os.path.exists(tempoNewFolder):
        try:
            os.makedirs(tempoNewFolder)
        except:
            print('This folder already exist')
    return tempoNewFolder

# CSV OPERATIONS
def write_csv_file(path, list):
    listOK = list
    pathNewCSV = path

    with open(pathNewCSV, 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t')
        for line in listOK:
            spamwriter.writerow(line)
    return pathNewCSV

# SCRAPPING OPERATIONS
def download_file(url, local_path):
    r = requests.get(url)
    if r.ok:
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(32 * 1024):
                f.write(chunk)
            f.close()

class Remove_all_special_characters:
    def __init__(self, string_item):
        self.string_item = string_item
        self.cleaned_string = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", self.string_item)
    def text(self):
        return self.cleaned_string

class Product_Infos:
    def __init__(self):
        # lister les champs
        self.product_page_url = ""
        self.universal_product_code = ""
        self.title = ""
        self.price_including_tax = ""
        self.price_excluding_tax = ""
        self.number_available = ""
        self.product_description = ""
        self.category = ""
        self.review_rating = ""
        self.image_url = ""

    def to_list(self):
        return [self.product_page_url, self.universal_product_code, self.title, self.price_including_tax, self.price_excluding_tax, self.number_available, self.product_description,
                self.product_description, self.category, self.review_rating, self.image_url]

class Scrapping:
    def __init__(self, url):
        self.url = url
        response = requests.get(self.url)
        if response.ok:
            self.soup = BeautifulSoup(response.text, 'html.parser')
        else:
            self.soup = ""

    def get_all_books_categories_urls(self):
        uls = self.soup.findAll('ul')
        titles_and_links = []
        for ul in uls:
            books_state = ul.find('strong')
            if books_state != None:
                if books_state.text == 'Books':
                    a_contents = ul.findAll('a')
                    for a_content in a_contents:
                        link_title = a_content.text.strip()  # delete all ending spaces
                        link = a_content['href']
                        new_url = merge_link_to_url(self.url, link)
                        #print(self.url)
                        titles_and_links.append([link_title, new_url])
        return titles_and_links

    def get_all_books_items_urls(self, list_pages):
        next_link = ''
        sec = self.soup.find('section')
        a_contents = sec.findAll('a')

        for a_content in a_contents:
            link_title = a_content.text.strip()  # delete all ending spaces
            link = a_content['href']
            if link_title != '':
                new_url = merge_link_to_url(url, link)
                # print('link_title = ' + str(link_title))
                if link_title == 'next':
                    next_link = new_url
                    # print('next = ' + str(new_url))
                elif link_title != 'previous':
                    list_pages.append(new_url)
        return list_pages, next_link

    def get_datas_product_from_url(self):
        product_infos = Product_Infos
        product_infos.product_page_url = self.url

        product_gallery = self.soup.find('div', {'id': 'product_gallery'})

        # GET LINK IMAGE
        path_img = product_gallery.find('img')['src']
        url_img = merge_link_to_url(self.url, path_img)
        product_infos.image_url = url_img  # add product_page_url

        # GET TITLE
        title = self.soup.find('title').text.strip()
        tile_temp = title.split(' | ')[0].encode('iso-8859-1').decode('utf8')
        product_infos.title = Remove_all_special_characters(tile_temp).text()  # add title

        # GET DESCRIPTION
        product_page = self.soup.find('article', class_='product_page')
        product_page_all_p = product_page.findAll('p')

        description = ''
        for p in product_page_all_p:
            if len(p) == 1:
                paragraph_text = p.text
                if len(paragraph_text) > len(description):
                    description = paragraph_text.encode('iso-8859-1').decode('utf8')
        product_infos.product_description = description  # add product_description

        # GET OTHERS ITEMS
        tds = self.soup.findAll('tr')
        for tr in tds:
            element = tr.find('th').text.lower()
            value = tr.find('td').text.replace('Â', '')
            if 'upc' in element:
                product_infos.universal_product_code = value  # add product_code
            elif 'incl' in element:
                product_infos.price_including_tax = value  # add price_including_tax
            elif 'excl' in element:
                product_infos.price_excluding_tax = value  # add price_excluding_tax
            elif 'availability' in element:
                product_infos.number_available = value.split('(')[1].replace(' available)', '')  # add number_available
            elif 'reviews' in element:
                product_infos.review_rating = value  # add review_rating

        return product_infos

# INIT VARIABLES
url_main = 'http://books.toscrape.com/catalogue/category/books_1/index.html'

base_dir_script = os.getcwd()

header_csv = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
              'price_excluding_tax', 'number_available', 'product_description', 'category',
              'review_rating', 'image_url']

parent_directory = os.path.abspath(os.path.join(base_dir_script, '..'))

# CREATE 'DATAS' FOLDER
path_csv_folder = addFolder(parent_directory, 'DATAS')

# MAIN SCRIPT
scrap_url_main = Scrapping(url_main)
if scrap_url_main is not "":
    titles_urls = scrap_url_main.get_all_books_categories_urls()

for i_title, title_url in enumerate(titles_urls, 0):
    title, url = title_url

    # GET ALL CATEGORIES EXCEPT BOOKS
    if title != 'Books':
        # GET ALL BOOKS FOR THIS CATEGORY
        books_pages = []
        scrap_url = Scrapping(url)
        if scrap_url is not "":
            books_pages, soup_page_next = scrap_url.get_all_books_items_urls(books_pages)

            while soup_page_next != '':
                books_pages, soup_page_next = Scrapping(soup_page_next).get_all_books_items_urls(books_pages)
            print(title + '    ' + str(len(books_pages)) + '    ' + str(soup_page_next))

            # GET ALL INFORMATIONS FOR EACH BOOKS
            path_category_folder = addFolder(path_csv_folder, str(i_title) + '_' + title + "_images")

            all_products_for_this_category = []
            all_products_for_this_category.append(header_csv)
            for i_b, book_link in enumerate(books_pages, 1):
                scrap_book = Scrapping(book_link)
                if scrap_book is not "":
                    product_infos = scrap_book.get_datas_product_from_url()
                    product_infos.category = title

                    image_path = product_infos.image_url
                    all_products_for_this_category.append(product_infos.to_list(product_infos))

                    if image_path != None:
                        file_name, file_extension = os.path.splitext(image_path)
                        image_local = os.path.join(path_category_folder, str(i_b) + '_' + title + '_' + product_infos.title + file_extension)
                        download_file(image_path, image_local)

            # WRITE CSV FILE FOR THIS CATEGORY
            csv_path = write_csv_file(os.path.join(path_csv_folder, str(i_title) + '_' + title + '.csv'), all_products_for_this_category)

print("---> Operation is completed")

