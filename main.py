from selectolax.parser import HTMLParser
import os
import cloudscraper
from httpx import get
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def image_tags_from(term=None):
    url=f"https://unsplash.com/s/photos/{term}"
    scraper=cloudscraper.create_scraper()
    resp=scraper.get(url)
    if not term:
        raise Exception("no such term")
    if resp.status_code != 200:
        raise Exception("error requesting")
    tree=HTMLParser(resp.text)
    img=tree.css("figure a img")
    return img 

def img_filter_out(url: str, keyword: list)->bool:
    return not any(x in url for x in keyword)

def get_high_res_img(img_node):
    srcset=[i.attrs["srcset"] for i in img_node if "srcset" in i.attrs]
    srcset_list=[i.split(", ") for i in srcset]
    url_res=[url.split(" ") for src in srcset_list for url in src if img_filter_out(url, ['profile', 'premium', 'plus'])]
    relevant_urls=[url[0] for url in url_res if '2000w' in url]
    return relevant_urls

def save_images(img_urls, des_dir="images", tag=""):
    i=0
    logging.info("Downloading -----")
    for url in img_urls:
        resp = get(url, timeout=(10, 30))
        file_name=f"photo-{i}"
        i+=1
        if not os.path.exists(des_dir):
            os.makedirs(des_dir)
        with open(f"{des_dir}/{tag}{file_name}.jpeg", "wb") as f:
            f.write(resp.content)
            logging.info(f"saved {file_name}")

if __name__ == "__main__":
    search=input("what do u want to search? ")
    dest_dir=input("enter destination directory: ")
    tag=input("enter tag name for the files: ")
    image_nodes=image_tags_from(search)
    all_img_urls=get_high_res_img(image_nodes)
    save_images(all_img_urls, search, search)
    print("images saved successfully")