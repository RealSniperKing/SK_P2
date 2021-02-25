# -*- coding: utf-8 -*-
from scrapping_module import Scrapping, download_file
from basics_operations import add_folder
from csv_operations import write_csv_file

import os
import os.path


def main():
    url_main = 'http://books.toscrape.com/catalogue/category/books_1/index.html'

    base_dir_script = os.getcwd()

    header_csv = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
                  'price_excluding_tax', 'number_available', 'product_description', 'category',
                  'review_rating', 'image_url']

    #parent_directory = os.path.abspath(os.path.join(base_dir_script, '..'))

    # CREATE 'DATAS' FOLDER
    path_csv_folder = add_folder(base_dir_script, 'DATAS')

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

                # GET ALL ATTRIBUTES FOR EACH BOOKS
                path_category_folder = add_folder(path_csv_folder, str(i_title) + '_' + title + "_images")

                all_products_for_this_category = [header_csv]
                for i_b, book_link in enumerate(books_pages, 1):
                    scrap_book = Scrapping(book_link)
                    if scrap_book is not "":
                        product_attributes = scrap_book.get_attributes_product_from_url()
                        product_attributes.category = title

                        image_path = product_attributes.image_url
                        all_products_for_this_category.append(product_attributes.to_list(product_attributes))

                        if image_path is not None:
                            file_name, file_extension = os.path.splitext(image_path)
                            image_local = os.path.join(path_category_folder, str(
                                i_b) + '_' + title + '_' + product_attributes.title + file_extension)
                            download_file(image_path, image_local)

                # WRITE CSV FILE FOR THIS CATEGORY
                csv_path = write_csv_file(os.path.join(path_csv_folder, str(i_title) + '_' + title + '.csv'),
                                          all_products_for_this_category)

    print("---> Operation is completed")


if __name__ == '__main__':
    main()
