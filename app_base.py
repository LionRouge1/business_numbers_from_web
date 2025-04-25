class AppBase:
  def __init__(self, name):
    self.name = name.strip()
    self.unique_businesses = set()
    self.filename = f"{self.name.lower()}_businesses.csv"

  def add_to_unique(self, name, phone):
    key = f"{name.strip()} - {phone.strip()}"
    if key in self.unique_businesses:
      return False
    
    self.unique_businesses.add(key)
    return True