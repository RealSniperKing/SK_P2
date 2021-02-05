import requests
from bs4 import BeautifulSoup

def count_element_in_list(list, element):
    items_count = []
    for i_elem, item in enumerate(list, 0):
        if item == element:
            items_count.append(item)
    return items_count

def count_directories_parents(path):
    try:
        path_split = path.split("../")
        value_parents = count_element_in_list(path_split, "")
        count = len(value_parents)
    except:
        count = 0
    return count

def convert_array_to_string(tableau, separator):
    newLine = ''
    for i, elem in enumerate(tableau, 0):
        if i == 0:
            newLine += str(elem)
        else:
            newLine += str(separator) + str(elem)
    return newLine

def get_datas_product_from_url(url):
    response = requests.get(url)
    if response.ok:
        print("response = " + str(response))
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title")
        print("title = " + str(title.text))

        tds = soup.findAll("tr")
        print(len(tds))
        print("-----> ")
        # [print(td) for td in tds]
        for tr in tds:
            print(str(tr.find("th").text))
            print(str(tr.find("td").text))
            print("----------")

def merge_link_to_url(url, link):
    url_split = url.split("/")
    value = count_directories_parents(link)

    for i in range(0, value + 1):
        del url_split[len(url_split) - 1]

    path_OK = convert_array_to_string(url_split, '/') + "/" + link.replace("../", "")

    return path_OK

def get_all_books_categories_urls(url):
    response = requests.get(url)
    titles_and_links = []
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        uls = soup.findAll("ul")
        for ul in uls:
            books_state = ul.find("strong")

            if books_state != None:
                if books_state.text == "Books":
                    a_contents = ul.findAll("a")
                    for a_content in a_contents:
                        link_title = a_content.text.strip()  # delete all ending spaces
                        link = a_content["href"]
                        new_url = merge_link_to_url(url, link)
                        titles_and_links.append([link_title, new_url])
    return titles_and_links

def get_all_books_items_urls(url, list_pages):
    next_link = ""
    response = requests.get(url)
    if response.ok:
        #print("get_all_books_items_urls")
        soup = BeautifulSoup(response.text, "html.parser")
        sec = soup.find("section")

        a_contents = sec.findAll("a")
        for a_content in a_contents:
            link_title = a_content.text.strip()  # delete all ending spaces
            link = a_content["href"]
            if link_title != "":
                new_url = merge_link_to_url(url, link)
                #print(link_title + "    " + str(new_url))
                list_pages.append(new_url)
                if link_title == "next":
                    next_link = new_url
                    #print("next = " + str(new_url))
    return list_pages, next_link
# test = "../../../changing-the-game-play-by-play-2_317/index.html"
# value = count_directories_parents(test)
# print("value = " + str(value))

# for i in range(0,1):
#     print("i = " + str(i))

url_main = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
# Get urls categories from main page
titles_urls = get_all_books_categories_urls(url_main)

for title_url in titles_urls:
    title = title_url[0]
    url = title_url[1]

    if title != "Books":
        #if title == "Romance":
        books_pages = []
        books_pages, next_page = get_all_books_items_urls(url, books_pages)
        #print(title + "    " + str(len(books_pages)) + "    " + str(next_page))

        while next_page != "":
            books_pages, next_page = get_all_books_items_urls(next_page, books_pages)

        print(title + "    " + str(len(books_pages)) + "    " + str(next_page))







