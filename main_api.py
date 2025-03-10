from httpx import get
import cloudscraper
import os

def get_response_from(keyword, result_per_page, pages=1):
    scraper=cloudscraper.create_scraper()
    url=f"https://unsplash.com/napi/search/photos?page={pages}&per_page={result_per_page}&query={keyword}&xp=free-semantic-perf%3Acontrol"
    resp=scraper.get(url)
    if resp != 200:
        return resp.json()

def get_img_url_from(data):
    results=data["results"]
    img_urls=[x["urls"]["raw"] for x in results if x["premium"] is False]
    return img_urls
    
def download_image(img_urls, max_photos=0, dest_dir="images", tag=""):
    completed_downloads=0
    i=0
    for url in img_urls:
        if completed_downloads < max_photos:
            resp=get(url, timeout=(10,30))
            file_name=f"photo-{i}"
            i+=1
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            with open(f"{dest_dir}/{tag}{file_name}.jpeg", "wb") as f:
                f.write(resp.content)
                completed_downloads+=1
        else:
            break
    return completed_downloads 

def scrape(keyword, num_of_results):
    number_of_pages=1
    success_count=0
    while success_count < num_of_results:
        max_downloads=num_of_results-success_count
        data=get_response_from(keyword, result_per_page=30, pages=number_of_pages)
        if data:
            img_urls=get_img_url_from(data)
            succeeded_downloads=download_image(img_urls, max_downloads, keyword, tag=keyword)
            success_count+=succeeded_downloads
            number_of_pages+=1
        else:
            print("Error: no data found")
            break            
    print("completed!")


if __name__=="__main__":
    search=input("what do u want to search for? ")
    amount=int(input("how much? "))
    scrape(search, amount)