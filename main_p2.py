import requests
from bs4 import BeautifulSoup

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

                        relative_infos = link.split("/")[0]
                        if ".." in relative_infos:
                            url_split = url.split("/")

                            # delete last item for each '.'
                            for i in relative_infos:
                                del url_split[len(url_split)-1]

                            cleaned_path = convert_array_to_string(url_split, '/') + link.replace("..", "")
                            titles_links.append([link_title, cleaned_path])
    return titles_links

def get_all_books_items_urls(url):
    print("get books")

url_main = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
# Get urls categories from main page
titles_urls = get_all_books_categories_urls(url_main)

for title_url in titles_urls:
    title = title_url[0]
    url = title_url[1]

    if title == "Romance":
        get_all_books_items_urls(url)








