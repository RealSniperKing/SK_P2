import requests
from bs4 import BeautifulSoup
import os

import csv

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
            print("This folder already exist")
    return tempoNewFolder

# CSV OPERATIONS
def write_csv_file(path, list):
    listOK = list
    pathNewCSV = path

    with open(pathNewCSV, "w", newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t')
        for line in listOK:
            spamwriter.writerow(line)
            # string_line = " ".join(map(str, line))
            # csv_file.write(string_line)
            # csv_file.write('\n')
    return pathNewCSV

    # with open(pathNewCSV, "w", newline='', encoding='utf-8') as csv_file:
    #     for line in listOK:
    #         string_line = " ".join(map(str, line))
    #         csv_file.write(string_line)
    #         csv_file.write('\n')
    # return pathNewCSV

# SCRAPPING OPERATIONS
def get_datas_product_from_url(url, category):
    items = [None] * 10
    items[0] = url  # add product_page_url
    items[7] = category  # add category

    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')

        # GET LINK IMAGE
        product_gallery = soup.find('div', {'id': 'product_gallery'})
        img = product_gallery.find('img')
        path_img = img['src']
        url_img = merge_link_to_url(url, path_img)
        items[9] = url_img  # add product_page_url

        # GET TITLE
        title = soup.find('title').text.strip()
        items[2] = title.split(' | ')[0]  # add title

        # GET DESCRIPTION
        product_page = soup.find('article', class_='product_page')
        product_page_all_p = product_page.findAll('p')

        description = ""
        for p in product_page_all_p:
            if len(p) == 1:
                paragraph_text = p.text
                if len(paragraph_text) > len(description):
                    description = paragraph_text.encode('iso-8859-1').decode('utf8')
        #print(description)
        items[6] = description  # add product_description

        #decode('iso-8859-1').encode('utf8')

        # GET OTHERS ITEMS
        tds = soup.findAll('tr')
        for tr in tds:
            element = tr.find('th').text.lower()
            value = tr.find('td').text.replace('Â', '')
            if 'upc' in element:
                items[1] = value  # add product_code
            elif 'incl' in element:
                items[3] = value  # add price_including_tax
            elif 'excl' in element:
                items[4] = value  # add price_excluding_tax
            elif 'availability' in element:
                items[5] = value.split('(')[1].replace(' available)', '')  # add number_available
            elif 'reviews' in element:
                items[8] = value  # add review_rating
    return items

def get_all_books_categories_urls(url):
    response = requests.get(url)
    titles_and_links = []
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        uls = soup.findAll('ul')
        for ul in uls:
            books_state = ul.find('strong')

            if books_state != None:
                if books_state.text == 'Books':
                    a_contents = ul.findAll('a')
                    for a_content in a_contents:
                        link_title = a_content.text.strip()  # delete all ending spaces
                        link = a_content['href']
                        new_url = merge_link_to_url(url, link)
                        titles_and_links.append([link_title, new_url])
    return titles_and_links

def get_all_books_items_urls(url, list_pages):
    next_link = ''
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        sec = soup.find('section')
        a_contents = sec.findAll('a')

        for a_content in a_contents:
            link_title = a_content.text.strip()  # delete all ending spaces
            link = a_content['href']
            if link_title != '':
                new_url = merge_link_to_url(url, link)
                #print("link_title = " + str(link_title))
                if link_title == 'next':
                    next_link = new_url
                    #print('next = ' + str(new_url))
                elif link_title != 'previous':
                    list_pages.append(new_url)
    return list_pages, next_link

# MAIN SCRIPT
url_main = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
titles_urls = get_all_books_categories_urls(url_main)  # Get urls categories from main page

base_dir_script = os.getcwd()
print('base_dir_script = ' + str(base_dir_script))

header_csv = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
              'price_excluding_tax', 'number_available', 'product_description', 'category',
              'review_rating', 'image_url']
path_csv_folder = addFolder(base_dir_script, "CSV")

for i_title, title_url in enumerate(titles_urls, 0):
    title = title_url[0]
    url = title_url[1]

    # GET ALL CATEGORIES EXCEPT BOOKS
    if title != 'Books':
        # if title == 'Romance':
        # GET ALL BOOKS FOR THIS CATEGORY
        books_pages = []
        books_pages, next_page = get_all_books_items_urls(url, books_pages)

        while next_page != '':
            books_pages, next_page = get_all_books_items_urls(next_page, books_pages)
        print(title + '    ' + str(len(books_pages)) + '    ' + str(next_page))

        # GET ALL INFORMATIONS FOR EACH BOOKS
        all_products_for_this_category = []
        all_products_for_this_category.append(header_csv)
        for i_b, book_page in enumerate(books_pages, 0):
            #if i_b < 1:
            product_line = get_datas_product_from_url(book_page, title)
            all_products_for_this_category.append(product_line)

        # WRITE CSV FILE FOR THIS CATEGORY
        write_csv_file(os.path.join(path_csv_folder, str(i_title) + "_" + title + ".csv"), all_products_for_this_category)






