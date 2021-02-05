import requests
from bs4 import BeautifulSoup

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

def get_all_books_categories_url(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        uls = soup.findAll("ul")
        for ul in uls:
            books_state = ul.find("strong")

            if books_state != None:
                if books_state.text == "Books":
                    links = ul.findAll("a")
                    print(links)

            print("-------------")

url_page = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
url_main = 'http://books.toscrape.com/catalogue/category/books_1/index.html'

#get_datas_product_from_url
get_all_books_categories_url(url_main)





