from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
import time
# import re
from pathlib import Path
import csv

class Recheck:
  def __init__(self,biz_name):
    self.biz_name = biz_name
    self.driver = webdriver.Chrome()
    self.driver.get("https://www.google.com/localservices/prolist?g2lbs=AAEPWCtmCa0U69yT4gyIoz1-hE1uART3Y_k2-yqhQwXwSWd3Fou0NCljJb8MwaVVAeWbYryuXWnD5ZXf68m1l2qfyARWV9Di3A%3D%3D&hl=en-GH&gl=gh&cs=1&ssta=1&slp=MgBSAggCYACSAakCCg0vZy8xMWNzMXd3dzdzCg0vZy8xMWdfeDA0bXZwCg0vZy8xMWh6XzU2ajJ4Cg0vZy8xMWdobmJtbjRzCg0vZy8xMWxrMHR5cTYxCg0vZy8xMXZqX2syMnpmCg0vZy8xMXQ3dnYxZjVwCgsvZy8xdHMzZ3pzNgoNL2cvMTFsMnhfd3NuMgoNL2cvMTF2OXl6MTlwMAoNL2cvMTFiejA4cGJ6OQoNL2cvMTFmeGR0dF84bAoNL2cvMTFjNl9kdzhyeQoNL2cvMTFiNnA3bGdsYgoNL2cvMTFobjZmODAwdwoNL2cvMTF2OXk0amZ0dwoNL2cvMTFuczM5M3psNgoNL2cvMTFzMjI2cHc3MQoNL2cvMTFqNHZtdmcxbgoML2cvMXB0dzl6X25jmgEGCgIXGRAA&src=2&serdesk=1&sa=X&sqi=2&ved=2ahUKEwj7y_2w96KMAxV10AIHHbqcGdsQjGp6BAgrEAE&lci=20&scp=CghnY2lkOmd5bRJWEhIJQwTRApiZ3w8Rxi_wGbDLoAEaEglzp7eyhJDfDxHTLQ5l2E7RviIUT2thaWtvaSBTb3V0aCwgQWNjcmEqFA0y2U8DFUQU1_8dchlbAyWhyN7_MAEaBGd5bXMiDGd5bXMgbmVhciBtZSoDR3lt")

  def recheck(self):
    print("Rechecking...")
    try:
      search_form = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form[jsname='jZGSjc']"))
      )
      search_input = search_form.find_element(By.CSS_SELECTOR, "input[name='q']")
      search_input.send_keys(f"{self.biz_name}")
      search_form.submit()
      self.run()
    except Exception as e:
      print("Error:", e)
      self.driver.quit()

  def run(self):
    print("Running...")
    try:
      cards = WebDriverWait(self.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ykYNg > div[jscontroller]"))
      )
      for card in cards:
        name = card.find_element(By.CSS_SELECTOR, ".dbg0pd").text
        address = card.find_element(By.CSS_SELECTOR, ".LrzXr").text
        phone = card.find_element(By.CSS_SELECTOR, ".Us2Fyb").text
        availability = card.find_element(By.CSS_SELECTOR, ".VZqTOd").text
        self.businesses.append({
          "Name": name,
          "Address": address,
          "Phone": phone,
          "Availability": availability
        })
    except Exception as e:
      print("Error:", e)
      self.driver.quit()