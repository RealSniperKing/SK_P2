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

def get_all_books_categories_urls(url):
    response = requests.get(url)
    titles_links = []
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
                        #print("link = " + str(link))
                        value = count_directories_parents(link)

                        #print("url = " + str(url))
                        url_split = url.split("/")
                        #print("url_split = " + str(url_split))
                        for i in range(0, value + 1):
                            del url_split[len(url_split) - 1]

                        cleaned_path = convert_array_to_string(url_split, '/') + link.replace("..", "")
                        #print("cleaned_path = " + str(cleaned_path))
                        titles_links.append([link_title, cleaned_path])
    return titles_links

def get_all_books_items_urls(url):
    response = requests.get(url)
    if response.ok:
        print("get_all_books_items_urls")
        soup = BeautifulSoup(response.text, "html.parser")
        sec = soup.find("section")

        # get link in current pages
        ols = sec.findAll("ol")
        print("ols = " + str(ols))


        print("--------------------------------")

        # check if exist others page


        # a_contents = soup.findAll("a")
        # for a_content in a_contents:
        #     print("a_content = " + str(a_content))

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
    #print("url = " + str(url))

    if title == "Romance":
        print("test")
        print("url = " + str(url))
        get_all_books_items_urls(url)








