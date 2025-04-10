from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
import time
# import re
from pathlib import Path
import csv

class GetBusinessData:
  def __init__(self,filename):
    # self.driver = webdriver.Chrome()
    # self.chrome_options = Options()
    # self.chrome_options.add_argument("--headless=new")
    # self.chrome_options.add_argument("--disable-gpu")
    # self.chrome_options.add_argument("--window-size=1920,1080")
    self.driver = None
    self.businesses = []
    self.unique_businesses = set()
    self.CHUNK_SIZE = 50
    self.industry = None
    self.cards = []
    # self.timestamp = time.strftime("%Y%m%d")
    self.filename = filename

  def _is_phone_number(self, s):
    return s.replace(" ", "").isdigit()

  def _is_availability(self, s):
    keys = ["Open", "Closed", "Temporarily closed"]
    for key in keys:
      if key in s:
        return True
    return False
  
  def search_for_businesses(self, keys=None):
    print("Opening Chrome...")
    self.industry = keys
    self.driver = webdriver.Chrome()
    self.driver.get("https://www.google.com/localservices/prolist?g2lbs=AAEPWCtmCa0U69yT4gyIoz1-hE1uART3Y_k2-yqhQwXwSWd3Fou0NCljJb8MwaVVAeWbYryuXWnD5ZXf68m1l2qfyARWV9Di3A%3D%3D&hl=en-GH&gl=gh&cs=1&ssta=1&slp=MgBSAggCYACSAakCCg0vZy8xMWNzMXd3dzdzCg0vZy8xMWdfeDA0bXZwCg0vZy8xMWh6XzU2ajJ4Cg0vZy8xMWdobmJtbjRzCg0vZy8xMWxrMHR5cTYxCg0vZy8xMXZqX2syMnpmCg0vZy8xMXQ3dnYxZjVwCgsvZy8xdHMzZ3pzNgoNL2cvMTFsMnhfd3NuMgoNL2cvMTF2OXl6MTlwMAoNL2cvMTFiejA4cGJ6OQoNL2cvMTFmeGR0dF84bAoNL2cvMTFjNl9kdzhyeQoNL2cvMTFiNnA3bGdsYgoNL2cvMTFobjZmODAwdwoNL2cvMTF2OXk0amZ0dwoNL2cvMTFuczM5M3psNgoNL2cvMTFzMjI2cHc3MQoNL2cvMTFqNHZtdmcxbgoML2cvMXB0dzl6X25jmgEGCgIXGRAA&src=2&serdesk=1&sa=X&sqi=2&ved=2ahUKEwj7y_2w96KMAxV10AIHHbqcGdsQjGp6BAgrEAE&lci=20&scp=CghnY2lkOmd5bRJWEhIJQwTRApiZ3w8Rxi_wGbDLoAEaEglzp7eyhJDfDxHTLQ5l2E7RviIUT2thaWtvaSBTb3V0aCwgQWNjcmEqFA0y2U8DFUQU1_8dchlbAyWhyN7_MAEaBGd5bXMiDGd5bXMgbmVhciBtZSoDR3lt")
    print("Searching for businesses...")
    try:
      search_form = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form[jsname='jZGSjc']"))
      )
      search_input = search_form.find_element(By.CSS_SELECTOR, "input[name='q']")
      search_input.send_keys(f"{keys} near me")
      search_form.submit()
      self.run()
    except Exception as e:
      print("Error:", e)
      self.driver.quit()
  
  def write_to_csv(self):
    print("Writing to CSV...")
    file_exists = Path(self.filename).exists()
    with open(self.filename, "a", newline="", encoding='utf-8') as csvfile:
      fieldnames = ["Name", "Address", "Phone", "Availability", "Industry"]
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      if not file_exists:
        writer.writeheader()

      for business in self.businesses:
        writer.writerow({
          "Name": business["name"],
          "Address": business["address"],
          "Phone": business["phone"],
          "Availability": business["availability"],
          "Industry": business["industry"]
        })

  def get_business_data(self, card, index):
    if not card.find_elements(By.XPATH, ".//button[.//span[normalize-space(text())='Website']]"):
      for _ in range(3):
        if card.find_elements(By.XPATH, ".//button[.//span[normalize-space(text())='Website']]"):
          return None
        try:
            name = card.find_element(By.CSS_SELECTOR, ".rgnuSb.xYjf2e").text.strip()
            info = card.find_elements(By.CSS_SELECTOR, ".I9iumb:nth-of-type(3) > span")
                
            business = {
              "name": name,
              "address": "N/A",
              "phone": "N/A",
              "availability": "N/A",
              "industry": self.industry
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
          print("Stale element. Retrying...")
          self.driver.refresh()
          time.sleep(10)
          self.cards = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ykYNg > div[jscontroller]"))
          )
          card = self.cards[index]
          continue
    return None

  def run(self):
    print("Scraping...")
    while True:
      try:
        self.cards = WebDriverWait(self.driver, 10).until(
          EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ykYNg > div[jscontroller]"))
        )
        # cards = self.driver.find_elements(By.CSS_SELECTOR, ".ykYNg > div[jscontroller]")

        for i in range(len(self.cards)):
          business = self.get_business_data(self.cards[i], i)
          if not business:
            continue
          phone = business["phone"].replace(" ", "")
          key = f"{business['name']} - {phone}"
          if key not in self.unique_businesses:
            self.unique_businesses.add(key)
            self.businesses.append(business)
        
        if len(self.businesses) >= self.CHUNK_SIZE:
          self.write_to_csv()
          self.businesses = []
        
        btn_next = WebDriverWait(self.driver, 10).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Next']"))
        )
        btn_next.click()
        WebDriverWait(self.driver, 10).until(
          EC.staleness_of(self.cards[0])
        )

        # time.sleep(5)

      except (NoSuchElementException, TimeoutException):
        print("End of search results.")
        self.write_to_csv()
        self.driver.quit()
        break
      except Exception as e:
        self.write_to_csv()
        print('Error:', e)
        # self.driver.quit()
        break

    self.driver.quit()


if __name__ == "__main__":
  GetBusinessData('matchoudi_businesses.csv').search_for_businesses("gyms")
