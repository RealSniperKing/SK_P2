# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from product_module import Product_Fields
from basics_operations import merge_link_to_url, remove_all_special_characters

def download_file(url, local_path):
    r = requests.get(url)
    if r.ok:
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(32 * 1024):
                f.write(chunk)
            f.close()


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
                new_url = merge_link_to_url(self.url, link)
                if link_title == 'next':
                    next_link = new_url
                elif link_title != 'previous':
                    list_pages.append(new_url)
        return list_pages, next_link

    def get_attributes_product_from_url(self):
        product_attributes = Product_Fields
        product_attributes.product_page_url = self.url

        product_gallery = self.soup.find('div', {'id': 'product_gallery'})

        # GET LINK IMAGE
        path_img = product_gallery.find('img')['src']
        url_img = merge_link_to_url(self.url, path_img)
        product_attributes.image_url = url_img  # add product_page_url

        # GET TITLE
        title = self.soup.find('title').text.strip()
        tile_temp = title.split(' | ')[0].encode('iso-8859-1').decode('utf8')
        product_attributes.title = remove_all_special_characters(tile_temp)  # add title

        # GET DESCRIPTION
        product_page = self.soup.find('article', class_='product_page')
        product_page_all_p = product_page.findAll('p')

        description = ''
        for p in product_page_all_p:
            if len(p) == 1:
                paragraph_text = p.text
                if len(paragraph_text) > len(description):
                    description = paragraph_text.encode('iso-8859-1').decode('utf8')
        product_attributes.product_description = description  # add product_description

        # GET OTHERS ITEMS
        tds = self.soup.findAll('tr')
        for tr in tds:
            element = tr.find('th').text.lower()
            value = tr.find('td').text.replace('Â', '')
            if 'upc' in element:
                product_attributes.universal_product_code = value  # add product_code
            elif 'incl' in element:
                product_attributes.price_including_tax = value  # add price_including_tax
            elif 'excl' in element:
                product_attributes.price_excluding_tax = value  # add price_excluding_tax
            elif 'availability' in element:
                product_attributes.number_available = value.split('(')[1].replace(' available)',
                                                                                  '')  # add number_available
            elif 'reviews' in element:
                product_attributes.review_rating = value  # add review_rating

        return product_attributes
