import csv
from colorama import Fore, Style, init, Back

class SplitData():
  def __init__(self, app_base):
    self.app_base = app_base
    self.businesses = []
    self.categories = {}
    init()

  def read_from_csv(self, file = None):
    n_file = file if file != None else self.app_base.filename
    with open(n_file, "r") as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        if self.app_base.add_to_unique(row["Name"], row["Phone"]):
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

  def laod_data(self, file):
    self.read_from_csv(file)
    print(Fore.GREEN + "All businesses has been loaded" + Style.RESET_ALL)

  def sort_by_category(self):
    for biz in self.businesses:
      if biz['Industry'] in self.categories:
        self.categories[biz['Industry']].append(biz)
      else:
        self.categories[biz['Industry']] = [biz]


if __name__ == "__main__":
  filename = input("Enter the filename to split: ").strip()
  if not filename:
    print(Fore.RED + "Filename cannot be empty. Please try again." + Style.RESET_ALL)
    exit()
  splitter = SplitData(filename)
  splitter.read_from_csv()
  splitter.split_data()
    