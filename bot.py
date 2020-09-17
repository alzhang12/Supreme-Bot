#!/usr/bin/env python3
import os
import requests
from requests import Request, Session
import click
import sys
import urllib
from harvester import fetch


# command line inputs
@click.command()
@click.option('--item', prompt='Next Cop', help='Item you want to cop.')
@click.option('--style', prompt='Style', help='Style of item you want to cop (color, etc).')
@click.option('--size', prompt='Size', help='Size of item you want to cop (Small, Medium, Large, XLarge).')


def run_app(item, style, size):
    """Run the application."""
    # get product
    product_info = get_product(item, style, size)

    # add to cart
    s = add_to_cart(product_info)

    # checkout
    checkout(s, product_info)


""" ------------------------------------------------------------------------ """
""" ----------------------------- Get Products ----------------------------- """
""" ------------------------------------------------------------------------ """
def get_product(item_input, style_input, size_input):
    """Get products list."""
    # get all products in json format
    response = requests.get("http://www.supremenewyork.com/mobile_stock.json")
    response = response.json()
    
    # state
    product_info = {
        "style_id": "",
        "size_id": "",
        "product_id": ""
    }
    
    # find product id
    for category in response["products_and_categories"]:
        for item in response["products_and_categories"][category]:
            # product found
            if (item_input.lower() == item["name"].lower()):
                # add product id
                product_info["product_id"] = item["id"]
                
                # get product styles
                url = "https://www.supremenewyork.com/shop/{id}.json".format(id=item["id"])
                r = requests.get(url).json()
                
                # get style_id
                for style in r["styles"]:
                    if style_input:
                        if style["name"].lower() == style_input.lower():
                            # set style_id
                            product_info["style_id"] = style["id"]
                            # get size_id
                            for size in style["sizes"]:
                                if size["name"].lower() == size_input.lower():
                                    product_info["size_id"] = size["id"]
                            break
#                    else:
#                        # set style_id
#                        product_info["style_id"] = style["id"]
#                        # get size_id
#                        for size in style["sizes"]:
#                            if size["name"].lower() == size_input.lower():
#                                product_info["size_id"] = size["id"]
#                        break

                return product_info


""" ------------------------------------------------------------------------ """
""" --------------------------- Add Item To Cart --------------------------- """
""" ------------------------------------------------------------------------ """
def add_to_cart(product):
    """Add product to cart."""
    # create session
    s = requests.Session()

    # custom header: user-agent must be mobile
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "content-type": "application/x-www-form-urlencoded",
        "Origin": "https://www.supremenewyork.com",
        "Referer": "https://www.supremenewyork.com/mobile/",
        "Connection": "keep-alive"
    }

    # post add to cart end point
    url = "https://www.supremenewyork.com/shop/{id}/add.json".format(id=str(product["product_id"]))
    data = {
        "s": str(product["size_id"]),
        "st": str(product["style_id"]),
        "qty": "1"
    }
    response = s.post(url, data=data, headers=headers).json()

    # return the session
    return s


""" ------------------------------------------------------------------------ """
""" ------------------------------- Checkout ------------------------------- """
""" ------------------------------------------------------------------------ """
def checkout(s, product_info):
    """Checkout."""
    # get captcha token
    token = fetch.token('supremenewyork.com')
    print('Token: ', token)

    # MOBILE CHECKOUT ENDPOINT
    url = "https://www.supremenewyork.com/checkout.json"
    
    # headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Host": "www.supremenewyork.com",
        "Origin": "https://www.supremenewyork.com",
        "Referer": "https://www.supremenewyork.com/mobile/",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    cookie_sub = {
        product_info["size_id"]: 1
    }
    cookie_sub = urllib.parse.quote(str(cookie_sub))

    # form data
    data = {
        "MIME Type": "application/x-www-form-urlencoded",
        "store_credit_id": "",                             # should be blank
        "from_mobile": 1,
        "cookie-sub": cookie_sub,
        "same_as_billing_address": 1,
        "scerkhaj": "CKCRSUJHXH",
        "order[billing_name]": "",                         # should be blank
        "order[bn]": "",
        "order[email]": "",
        "order[tel]": "",
        "order[billing_address]": "",
        "order[billing_address_2]": "",                    # should be blank
        "order[billing_zip]": "",
        "order[billing_city]": "",
        "order[billing_state]": "",
        "order[billing_country]": "",
        "credit_card[type]": "credit card",
        "riearmxa": "0",
        "credit_card[month]": "",
        "credit_card[year]": "",
        "rand": "",                                        # should be blank
        "credit_card[meknk]": "",
        "order[terms]": "",
        "order[terms]": 1,
        "g-recaptcha-response": token
    }

    # get form data
    with open("input.txt") as file:
        lines = file.readlines()
        for line in lines:
            key, val = line.strip().split(" ")
            data[key] = val

    # post data
    r = s.post(url, data=data, headers=headers)



""" ------------------------------------------------------------------------ """
""" -------------------------- Python Entry Point -------------------------- """
""" ------------------------------------------------------------------------ """
if __name__ == "__main__":
    run_app()
