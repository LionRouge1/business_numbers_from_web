import csv
from pathlib import Path
import time

class SlitData:
  def __init__(self, filename):
    self.filename = filename
    self.businesses = []

  def read_from_csv(self):
    with open(self.filename, "r") as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        self.businesses.append(row)

  def write_to_csv(self, filename, data):
    print(f"Writing to {filename}...")
    with open(filename, "w", newline="", encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Name", "Address", "Phone", "Availability"])
        writer.writeheader()
        writer.writerows(
            {
                "Name": biz["name"],
                "Address": biz["address"],
                "Phone": biz["phone"],
                "Availability": biz["availability"]
            } 
            for biz in data
        )

  def split_data(self):
    if not self.businesses:
      print("No data to split. Please run the scraper first.")
      return

    self.read_from_csv()
    print(f"Splitting data from {self.filename}...")
    for business in self.businesses:
      print(f"Name: {business['Name']}")
      print(f"Address: {business['Address']}")
      print(f"Phone: {business['Phone']}")
      print(f"Availability: {business['Availability']}")
      print("\n")
      time.sleep(1)