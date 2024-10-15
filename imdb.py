import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import bs4
import os
import urllib.request

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
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break

    last_height = new_height

source_code = driver.page_source

driver.quit()

soup = bs4.BeautifulSoup(source_code, "lxml")

title = soup.select("title")[0].getText().split(" - Foto - IMDb")[0]

images_elements = soup.select(".ipc-image.sc-f1b78590-1.sLhej")

if "name" in url:
    type = "people"
else:
    type = "movies"

directory = f"images/{type}/{title}"

if not os.path.exists(directory):
    os.makedirs(directory)

total = len(images_elements)

paths = []
duplicates = 1

for count, image_element in enumerate(images_elements):
    print(f"Saving image {count + 1}/{total}...")
    image_source = image_element.attrs["src"]
    image_alt = image_element.attrs["alt"].replace("?", "").replace("?", "").replace("/", "").replace(":", "").replace('"', '').replace(".", "")
    image_extension = image_source.split(".")[-1]
    path = f"{directory}/{image_alt}.{image_extension}"
    if path not in paths:
        urllib.request.urlretrieve(image_source, path)
    else:
        image_alt = image_alt + f" ({duplicates})"
        path = f"{directory}/{image_alt}.{image_extension}"
        urllib.request.urlretrieve(image_source, path)
        duplicates = duplicates + 1
    paths.append(path)
