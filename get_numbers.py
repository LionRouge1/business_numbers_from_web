from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
import time
import re
from pathlib import Path
import csv

class GetBusinessData:
  def __init__(self):
    # self.driver = webdriver.Chrome()
    self.chrome_options = Options()
    self.chrome_options.add_argument("--headless=new")  # New headless mode in Chrome 109+
    self.chrome_options.add_argument("--disable-gpu")  # GPU acceleration isn't needed
    self.chrome_options.add_argument("--window-size=1920,1080")  # Set window size

    # Initialize driver
    self.driver = webdriver.Chrome()
    self.businesses = {}
    self.CHUNK_SIZE = 50
    self.timestamp = time.strftime("%Y%m%d")
    self.filename = f"businesses_{self.timestamp}.csv"
    self.driver.get("https://www.google.com/localservices/prolist?g2lbs=AAEPWCtmCa0U69yT4gyIoz1-hE1uART3Y_k2-yqhQwXwSWd3Fou0NCljJb8MwaVVAeWbYryuXWnD5ZXf68m1l2qfyARWV9Di3A%3D%3D&hl=en-GH&gl=gh&cs=1&ssta=1&q=gyms%20near%20me&oq=gyms%20near%20me&slp=MgBSAggCYACSAakCCg0vZy8xMWNzMXd3dzdzCg0vZy8xMWdfeDA0bXZwCg0vZy8xMWh6XzU2ajJ4Cg0vZy8xMWdobmJtbjRzCg0vZy8xMWxrMHR5cTYxCg0vZy8xMXZqX2syMnpmCg0vZy8xMXQ3dnYxZjVwCgsvZy8xdHMzZ3pzNgoNL2cvMTFsMnhfd3NuMgoNL2cvMTF2OXl6MTlwMAoNL2cvMTFiejA4cGJ6OQoNL2cvMTFmeGR0dF84bAoNL2cvMTFjNl9kdzhyeQoNL2cvMTFiNnA3bGdsYgoNL2cvMTFobjZmODAwdwoNL2cvMTF2OXk0amZ0dwoNL2cvMTFuczM5M3psNgoNL2cvMTFzMjI2cHc3MQoNL2cvMTFqNHZtdmcxbgoML2cvMXB0dzl6X25jmgEGCgIXGRAA&src=2&serdesk=1&sa=X&sqi=2&ved=2ahUKEwj7y_2w96KMAxV10AIHHbqcGdsQjGp6BAgrEAE&scp=CghnY2lkOmd5bRJWEhIJQwTRApiZ3w8Rxi_wGbDLoAEaEglzp7eyhJDfDxHTLQ5l2E7RviIUT2thaWtvaSBTb3V0aCwgQWNjcmEqFA0y2U8DFUQU1_8dchlbAyWhyN7_MAEaBGd5bXMiDGd5bXMgbmVhciBtZSoDR3lt")

  def _is_phone_number(self, s):
    return s.replace(" ", "").isdigit()

  def _is_availability(self, s):
    keys = ["Open", "Closed", "Temporarily closed"]
    for key in keys:
      if key in s:
        return True
    return False
  
  def write_to_csv(self):
    file_exists = Path(self.filename).exists()
    with open(self.filename, "a", newline="", encoding='utf-8') as csvfile:
      fieldnames = ["Name", "Address", "Phone", "Availability"]
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      if not file_exists:
        writer.writeheader()

      for business in self.businesses.values():
        writer.writerow({
          "Name": business["name"],
          "Address": business["address"],
          "Phone": business["phone"],
          "Availability": business["availability"]
        })

  def safe_find_text(self, element, selector, default="N/A"):
    """Safely extract text from an element with error handling"""
    try:
        return element.find_elements(By.CSS_SELECTOR, selector)[0].text.strip()
    except:
        # print(f"Could not find element with Item {element} and selector {selector}")
        return default

  def get_business_data(self, card, index):
    for _ in range(3):  # Retry up to 3 times
      try:
          name = self.safe_find_text(card, ".rgnuSb.xYjf2e")
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
        cards = WebDriverWait(self.driver, 5).until(
          EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ykYNg > div[jscontroller]"))
        )
        card = cards[index]
        continue
    return None

  def run(self):
    while True:
      try:
        WebDriverWait(self.driver, 10).until(
          EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ykYNg > div[jscontroller]"))
        )
        cards = self.driver.find_elements(By.CSS_SELECTOR, ".ykYNg > div[jscontroller]")

        for i in range(len(cards)):
          business = self.get_business_data(cards[i], i)
          phone = business["phone"].replace(" ", "")
          key = f"{business['name']} - {phone}"
          if key not in self.businesses:
            self.businesses[key] = business
        
        if len(self.businesses) >= self.CHUNK_SIZE:
          print("Writing to CSV...")
          self.write_to_csv()
          self.businesses = {}
        
        btn_next = WebDriverWait(self.driver, 10).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Next']"))
        )
        btn_next.click()
        WebDriverWait(self.driver, 10).until(
          EC.staleness_of(cards[0])
        )

      except (NoSuchElementException, TimeoutException):
        self.write_to_csv()
        break
      except Exception as e:
        self.write_to_csv()
        print('Error:', e)
        break

    self.driver.quit()


if __name__ == "__main__":
  GetBusinessData().run()


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