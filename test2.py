from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://m.place.naver.com/restaurant/1239997161/home')

images_container = driver.find_element(By.CLASS_NAME, "CB8aP")
images = images_container.find_elements(By.CLASS_NAME, "K0PDV")

for image in images:
    print(image.value_of_css_property("background-image").split("\"")[1])
driver.quit()
