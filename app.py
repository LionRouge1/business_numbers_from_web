from app_base import AppBase
from split_data import SplitData
from get_numbers import GetBusinessData

class App(AppBase):
  def __init__(self):
    self.__user_name = input("Enter your name: ")
    super().__init__(self.__user_name)
    # self.unique_businesses = set()
    # self.filename = f"{self.__user_name.lower()}_businesses.csv"
    self.scraper = GetBusinessData()
    if self.__user_name.strip():
      self.run()
    else:
      print("Name cannot be empty. Please try again.")
      self

  # def save_file_name(self):


  def welcome(self):
    print(f"Welcome {self.__user_name} to the Business Finder App!\n")
    print("This app will help you find businesses based on your search query.\n")
    print("Let's get started!\n")
    self.app_options()

  def app_options(self):
    print("\nPlease choose from the following options:\n")
    print("1. Search for businesses")
    print("2. Split data")
    print("3. Exit\n")

  def run(self):
    self.welcome()
    while True:
      try:
        choice = int(input("Enter your choice: "))
        match choice:
          case 1:
            query = input("Enter your search query: ")
            if not query.strip():
              print("Query cannot be empty. Please try again.")
              continue
            self.scraper.search_for_businesses(query)
            self.app_options()
          case 2:
            SplitData().split_data()
            self.app_options()
          case 3:
            print("Exiting...")
            break
          case _:
            print("Invalid choice. Please try again.")
      except ValueError:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
  App()