from get_numbers import GetBusinessData

class App:
  def __init__(self):
    self.user_name = input("Enter your name: ")
    self.filename = f"{self.user_name.lower()}_businesses.csv"
    self.scraper = GetBusinessData(self.filename)
    if self.user_name.strip():
      self.run()
    else:
      print("Name cannot be empty. Please try again.")
      self

  def welcome(self):
    print(f"Welcome {self.user_name} to the Business Finder App!\n")
    print("This app will help you find businesses based on your search query.\n")
    print("Let's get started!\n")
    print("Please choose from the following options:\n")
    print("1. Search for businesses")
    print("2. Exit\n")

  def run(self):
    self.welcome()
    while True:
      try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
          query = input("Enter your search query: ")
          if not query.strip():
            print("Query cannot be empty. Please try again.")
            continue
          self.scraper.search_for_businesses(query)
          # break
        elif choice == 2:
          print("Exiting...")
          break
        else:
          print("Invalid choice. Please try again.")
      except ValueError:
        print("Invalid choice. Please try again.")


if __name__ == "__main__":
  App()