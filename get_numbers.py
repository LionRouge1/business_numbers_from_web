from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
import time
import re
import csv

class GetBusinessData:
  def __init__(self):
    self.driver = webdriver.Chrome()
    self.businesses = {}
    self.driver.get("https://www.google.com/localservices/prolist?g2lbs=AAEPWCtmCa0U69yT4gyIoz1-hE1uART3Y_k2-yqhQwXwSWd3Fou0NCljJb8MwaVVAeWbYryuXWnD5ZXf68m1l2qfyARWV9Di3A%3D%3D&hl=en-GH&gl=gh&cs=1&ssta=1&q=gyms%20near%20me&oq=gyms%20near%20me&slp=MgBSAggCYACSAakCCg0vZy8xMWNzMXd3dzdzCg0vZy8xMWdfeDA0bXZwCg0vZy8xMWh6XzU2ajJ4Cg0vZy8xMWdobmJtbjRzCg0vZy8xMWxrMHR5cTYxCg0vZy8xMXZqX2syMnpmCg0vZy8xMXQ3dnYxZjVwCgsvZy8xdHMzZ3pzNgoNL2cvMTFsMnhfd3NuMgoNL2cvMTF2OXl6MTlwMAoNL2cvMTFiejA4cGJ6OQoNL2cvMTFmeGR0dF84bAoNL2cvMTFjNl9kdzhyeQoNL2cvMTFiNnA3bGdsYgoNL2cvMTFobjZmODAwdwoNL2cvMTF2OXk0amZ0dwoNL2cvMTFuczM5M3psNgoNL2cvMTFzMjI2cHc3MQoNL2cvMTFqNHZtdmcxbgoML2cvMXB0dzl6X25jmgEGCgIXGRAA&src=2&serdesk=1&sa=X&sqi=2&ved=2ahUKEwj7y_2w96KMAxV10AIHHbqcGdsQjGp6BAgrEAE&scp=CghnY2lkOmd5bRJWEhIJQwTRApiZ3w8Rxi_wGbDLoAEaEglzp7eyhJDfDxHTLQ5l2E7RviIUT2thaWtvaSBTb3V0aCwgQWNjcmEqFA0y2U8DFUQU1_8dchlbAyWhyN7_MAEaBGd5bXMiDGd5bXMgbmVhciBtZSoDR3lt")

  def _is_phone_number(s):
    return s.replace(" ", "").isdigit()

  def _is_availability(s):
    keys = ["Open", "Closed", "Temporarily closed"]
    for key in keys:
      if key in s:
        return True
    return False

  def get_business_data(self, card):
    for _ in range(3):  # Retry up to 3 times
      try:
          name = card.find_element(By.CSS_SELECTOR, ".rgnuSb.xYjf2e").text
          info = card.find_elements(By.CSS_SELECTOR, ".I9iumb:nth-of-type(3) > span")
              
          business = {
            "name": name,
            "address": "N/A",
            "phone": "N/A",
            "availability": "N/A"
          }
              
          for element in info:
            text = element.text
            if self._is_phone_number(text):
              business["phone"] = text
            elif self._is_availability(text):
              business["availability"] = text
            else:
              business["address"] = text
              
          return business
      except StaleElementReferenceException:
        continue
    return None

  def run(self):
    # businesses = []
    while True:
      try:
        WebDriverWait(self.driver, 10).until(
          EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ykYNg > div[jscontroller]"))
        )
        cards = self.driver.find_elements(By.CSS_SELECTOR, ".ykYNg > div[jscontroller]")

        for card in cards:
          business = self.get_business_data(card)
          key = f"{business['name']} - {business['phone']}"
          if key not in self.businesses:
            self.businesses[key] = business
        
        btn_next = WebDriverWait(self.driver, 10).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Next']"))
        )
        btn_next.click()
        WebDriverWait(self.driver, 10).until(
          EC.staleness_of(cards[0])
        )
      except (NoSuchElementException, TimeoutException):
        print("No more pages to navigate.")
        break
      except Exception as e:
        print('Error:', e)
        break

    # print(businesses)
    self.driver.quit()

# while True:
#   try:
#     WebDriverWait(self.driver, 10).until(
#       EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ykYNg > div[jscontroller]"))
#     )
#     cards = self.driver.find_elements(By.CSS_SELECTOR, ".ykYNg > div[jscontroller]")

#     for card in cards:
#       business = self.get_business_data(card)
#       if business:
#         businesses.append(business)
    
#     btn_next = WebDriverWait(driver, 10).until(
#       EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Next']"))
#     )
#     btn_next.click()
#     WebDriverWait(driver, 10).until(
#       EC.staleness_of(cards[0])
#     )
#   except (NoSuchElementException, TimeoutException):
#     print("No more pages to navigate.")
#     break
#   except Exception as e:
#     print('Error:', e)
#     break

# print(businesses)
# driver.quit()