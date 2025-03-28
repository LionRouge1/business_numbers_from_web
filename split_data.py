import csv
from pathlib import Path
from colorama import Fore, Style, init, Back
import time

class SplitData:
  def __init__(self, filename):
    self.filename = filename
    self.businesses = []
    self.read_from_csv()
    init()

  def read_from_csv(self):
    with open(self.filename, "r") as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        self.businesses.append(row)

  def write_to_csv(self, filename, data):
    print(Fore.GREEN + f"Writing to {filename}..." + Style.RESET_ALL)
    try:
      with open(filename, "w", newline="", encoding='utf-8') as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=["Name", "Address", "Phone", "Availability"])
          writer.writeheader()

          writer.writerows(
              {
                  "Name": biz["Name"],
                  "Address": biz["Address"],
                  "Phone": biz["Phone"],
                  "Availability": biz["Availability"]
              } 
              for biz in data
          )
    except Exception as e:
      print(Fore.RED + "Error: " + str(e) + Style.RESET_ALL)

  def split_data(self):
    if not self.businesses:
      print(Fore.RED + "No data to split. Please run the scraper first." + Style.RESET_ALL)
      return

    total_buz = len(self.businesses)
    num_files = int(input(f"Enter the number of files to split the data into (1-{total_buz}): "))
    if num_files < 1 or num_files > total_buz:
      print(Fore.RED + "Invalid number of files. Please try again." + Style.RESET_ALL)
      return
    
    counter = 0
    i = total_buz // num_files
    for j in range(num_files):
      if counter >= total_buz:
        data = self.businesses[counter:]
      else:
        data = self.businesses[counter:counter+i]

      self.write_to_csv(f"agent_{j+1}.csv", data)
      counter += i

if __name__ == "__main__":
  filename = input("Enter the filename to split: ").strip()
  if not filename:
    print(Fore.RED + "Filename cannot be empty. Please try again." + Style.RESET_ALL)
    exit()
  splitter = SlitData(filename)
  splitter.read_from_csv()
  splitter.split_data()
    