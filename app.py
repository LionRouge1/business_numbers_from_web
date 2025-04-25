from pathlib import Path
from app_base import AppBase
from split_data import SplitData
from get_numbers import GetBusinessData
from colorama import Fore, Style, init, Back

class App():
  def __init__(self):
    self.__user_name = input("Enter your name: ")
    self.app_base = AppBase(self.__user_name)
    self.scraper = GetBusinessData(self.app_base)
    init()
    if self.__user_name.strip():
      self.run()
    else:
      print("Name cannot be empty. Please try again.")
      self


  def welcome(self):
    print(Fore.BLUE + f"Welcome {self.__user_name} to the Business Finder App!\n" + Style.RESET_ALL)
    print("This app will help you find businesses based on your search query.\n")
    print("Let's get started!\n")
    self.app_options()

  def app_options(self):
    print(Fore.CYAN + "\nPlease choose from the following options:\n" + Style.RESET_ALL)
    print("1. Search Search businesses without website")
    print("2. Search businesses with website")
    print("3. Load a file")
    print("4. Split data")
    print("5. Categorize the data")
    print("6. Remove duplicates businesses")
    print("7. Remove all businesses")
    print("8. Exit\n")
    print(Fore.YELLOW + "Note: Please ensure the file is in the correct format." + Style.RESET_ALL)

  def run(self):
    self.welcome()
    spliter = SplitData(self.app_base)
    while True:
      try:
        choice = int(input("Enter your choice: "))
        match choice:
          case 1:
            query = input("Enter your search query: ")
            if not query.strip():
              print(Fore.RED + "Query cannot be empty. Please try again." + Style.RESET_ALL)
              continue
            self.scraper.search_for_businesses(query)
            self.app_options()

          case 2:
            query = input("Enter your search query: ")
            if not query.strip():
              print(Fore.RED + "Query cannot be empty. Please try again." + Style.RESET_ALL)
              continue
            self.scraper.search_for_businesses(query, website=True)
            self.app_options()
          case 3:
            file = input("Enter the filename: ").strip()
            if not Path(file).exists() and not file.endswith(".csv") and not file:
              print(Fore.RED + "Sorry we can't foud the file" + Style.RESET_ALL)
              continue
            spliter.laod_data(file)
            self.app_options()
          case 4:
            spliter.split_data()
            self.app_options()

          case 5:
            spliter.sort_by_category()
            self.app_options()

          case 6:
            spliter.write_unique_businesses()
            print(Fore.GREEN + "Unique businesses have been written to unique_businesses.csv" + Style.RESET_ALL)
            self.app_options()

          case 7:
            spliter.empty_businesses()
            print(Fore.GREEN + "All businesses have been removed." + Style.RESET_ALL)
            self.app_options()

          case 8:
            print(Fore.GREEN + "Exiting..." + Style.RESET_ALL)
            break
          case _:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
      except ValueError:
        print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


if __name__ == "__main__":
  App()