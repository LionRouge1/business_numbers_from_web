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
    print("1. Search for businesses")
    print("2. Load a file")
    print("3. Split data")
    print("4. Categorize the data")
    print("5. Exit\n")

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
            file = input("Enter the filename: ").strip()
            if not Path(file).exists():
              print(Fore.RED + "Sorry we can't foud the file" + Style.RESET_ALL)
              continue
            spliter.laod_data(file)
            self.app_options()
          case 3:
            spliter.split_data()
            self.app_options()

          case 4:
            spliter.sort_by_category()
            self.app_options()
          case 5:
            print(Fore.GREEN + "Exiting..." + Style.RESET_ALL)
            break
          case _:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
      except ValueError:
        print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)


if __name__ == "__main__":
  App()