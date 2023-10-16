import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


url1 = "https://m.blog.naver.com/balbalbalbal/222957983030"
url2 = "https://m.blog.naver.com/balbalbalbal/223155559822"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

data = requests.get(url2)
soup = BeautifulSoup(data.text, 'html.parser')
driver = webdriver.Chrome()

places = list(soup.select(".se-placesMap .se-module-map-text a"))

with open("./data.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

increaseId = 20000
for place in places:
    placeInfo = json.loads(place["data-linkdata"])
    detailData = requests.get(
        f"https://m.place.naver.com/restaurant/{placeInfo['placeId']}/home")

    html = detailData.content.decode('utf-8', 'replace')

    soup2 = BeautifulSoup(html, 'html.parser')
    if soup2.select_one(".DJJvD"):
        placeType = soup2.select_one(".DJJvD").text

        driver.get(
            f"https://m.place.naver.com/restaurant/{placeInfo['placeId']}/home")
        images_container = driver.find_element(By.CLASS_NAME, "CB8aP")
        images = images_container.find_elements(By.CLASS_NAME, "K0PDV")
        images_src = []
        for image in images:
            images_src.append(image.value_of_css_property(
                "background-image").split("\"")[1])

        placeObj = {
            "id": increaseId,
            "latitude": placeInfo["latitude"],
            "longtitude":  placeInfo["longitude"],
            "name": placeInfo["name"],
            "description": None,
            "type": placeType.split(","),
            "naverId": placeInfo["placeId"],
            "images": images_src,
        }
        if soup2.select_one(".zPfVt"):
            placeObj["description"] = soup2.select_one(".zPfVt").text

        increaseId = increaseId + 1
        data.append(placeObj)

with open("./data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

driver.quit()

print("✨done!")
