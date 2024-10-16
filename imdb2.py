import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import bs4
import os
import urllib.request
import json

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

parser = argparse.ArgumentParser()
parser.add_argument("url", help="the url of the page of which you want to download the photos")
args = parser.parse_args()
url = args.url

if "mediaindex" not in url:
    url = url.rstrip("/") + "/mediaindex"

driver.get(url)

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(30)
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break

    last_height = new_height

source_code = driver.page_source

driver.quit()

soup = bs4.BeautifulSoup(source_code, "lxml")

images_elements = soup.select(".ipc-image.sc-f1b78590-1.sLhej")

if "name" in url:
    type = "people"
    title = soup.select("title")[0].getText().split(" - Foto - IMDb")[0]
    code = url.split("name/")[-1].split("/")[0]
else:
    type = "movies"
    script_element = soup.select("#__NEXT_DATA__")[0].getText()
    title = json.loads(script_element)["props"]["pageProps"]["contentData"]["entityMetadata"]["originalTitleText"]["text"] + " (" + str(json.loads(script_element)["props"]["pageProps"]["contentData"]["entityMetadata"]["releaseYear"]["year"]) + ")"
    code = url.split("title/")[-1].split("/")[0]

directory = f"images/{type}/{title} - {code}"

if not os.path.exists(directory):
    os.makedirs(directory)

total = len(images_elements)

paths = []
duplicates = 1
image_sources = []

for count, image_element in enumerate(images_elements):
    print(f"Saving image {count + 1}/{total}...")
    image_source = image_element.attrs["src"].rsplit("@", 1)[0] + "@._V1_." + image_element.attrs["src"].split(".")[-1]
    image_alt = image_element.parent.attrs["href"].split("mediaviewer/")[-1].split("/")[0]
    image_extension = image_source.split(".")[-1]
    path = f"{directory}/{image_alt}.{image_extension}"
    '''if path not in paths:
        urllib.request.urlretrieve(image_source, path)
    else:
        image_alt = image_alt + f" ({duplicates})"
        path = f"{directory}/{image_alt}.{image_extension}"
        urllib.request.urlretrieve(image_source, path)
        duplicates = duplicates + 1'''
    paths.append(path)
    image_sources.append(image_source)

with open("images_urls.txt", "w", encoding="utf-8") as f:
    for i in image_sources:
        f.write(i + "\n")
