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
    time.sleep(10)
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        break

    last_height = new_height

source_code = driver.page_source

soup = bs4.BeautifulSoup(source_code, "lxml")

title = soup.select("title")[0].getText().split(" - Foto - IMDb")[0]

images_elements = soup.select("a[id*='-img-']")

if "name" in url:
    type = "people"
    code = url.split("name/")[-1].split("/")[0]
else:
    type = "movies"
    code = url.split("title/")[-1].split("/")[0]

directory = f"images/{type}/{title} ({code})"

if not os.path.exists(directory):
    os.makedirs(directory)

total = len(images_elements)

paths = []
duplicates = 1
original_window = driver.current_window_handle

for count, image_element in enumerate(images_elements):
    print(f"Saving image {count + 1}/{total}...")
    driver.execute_script("window.open('');")
    time.sleep(1)
    new_window = [window for window in driver.window_handles if window != original_window][0]
    driver.switch_to.window(new_window)
    driver.get("https://www.imdb.com" + image_element.attrs["href"])
    soup_image = bs4.BeautifulSoup(driver.page_source, "lxml")
    image_source = soup_image.select("meta[property='og:image']")[0].attrs["content"].rsplit("@", 1)[0] + "@._V1_." + soup_image.select("meta[property='og:image']")[0].attrs["content"].split(".")[-1]
    image_alt = soup_image.select("meta[property='og:description']")[0].attrs["content"].replace("?", "").replace("?", "").replace("/", "").replace(":", "").replace('"', '').replace(".", "")
    image_extension = image_source.split(".")[-1]
    driver.close()
    driver.switch_to.window(original_window)
    path = f"{directory}/{image_alt}.{image_extension}"
    if path not in paths:
        urllib.request.urlretrieve(image_source, path)
    else:
        image_alt = image_alt + f" ({duplicates})"
        path = f"{directory}/{image_alt}.{image_extension}"
        urllib.request.urlretrieve(image_source, path)
        duplicates = duplicates + 1
    paths.append(path)

driver.quit()
