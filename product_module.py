# -*- coding: utf-8 -*-

class Product_Fields:
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
        all_attributes = [self.product_page_url, self.universal_product_code, self.title, self.price_including_tax,
                          self.price_excluding_tax, self.number_available, self.product_description,
                          self.product_description, self.category, self.review_rating, self.image_url]
        return all_attributes
