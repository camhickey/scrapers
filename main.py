import requests
from bs4 import BeautifulSoup
import tkinter as tk

def get_article_links(url):
    with open("queries.csv", "a") as f:
        clothing_style = input("Enter default clothing style: ")
        clothing_article = input("Enter default article type: ")
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        products = soup.findAll("a", {"class":"grid-product__link"})
        print("Finishing block...")
        for product in products:
            clothing_link = "https://techwear-outfits.com"+product['href']
            page = requests.get(clothing_link)
            soup = BeautifulSoup(page.text, 'html.parser')
            clothing_name = soup.find("h1", {"class": "h2 product-single__title"}).text.strip()
            clothing_price = soup.find("span", {"class": "product__price"}).text.strip()
            clothing_price = clothing_price.replace('$', '')
            if soup.find("fieldset", {"name": "Color"}):
                colors = soup.find("fieldset", {"name": "Color"})
                colors = colors.findAll("div", {"class": "variant-input"})
                for color in colors:
                    clothing_color = color['data-value'].lower()
                    clothing_image = color.find("label", {"class":"variant__button-label"})['style']
                    clothing_image = clothing_image[clothing_image.find("(")+1:clothing_image.find(")")]
                    clothing_image = "http:"+clothing_image
                    clothing_image = clothing_image.replace("_100x", "_1800x1800")
                    insert = "'{name}', '{style}', '{article}', '{color}', {price}, '{link}', '{image}'".format(
                        name=clothing_name, style=clothing_style, article=clothing_article, color=clothing_color,
                        price=clothing_price,
                        link=clothing_link, image=clothing_image
                    )
                    print(insert, file=f)
            else:
                image_list = soup.findAll("div", {"class":"product__thumb-item"})
                try:
                    clothing_image = image_list[0]
                except:
                    continue
                clothing_image = clothing_image.find('a')['href']
                clothing_image = "http:"+clothing_image
                insert = "'{name}', '{style}', '{article}', '{color}', {price}, '{link}', '{image}'".format(
                    name=clothing_name, style=clothing_style, article=clothing_article, color='black', price=clothing_price,
                    link=clothing_link, image=clothing_image
                )
                print(insert, file=f)
    print("Finished block")

#get_article_links('https://techwear-outfits.com/collections/techwear-shirt?page=3')