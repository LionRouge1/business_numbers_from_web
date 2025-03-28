# Business Finder App

The **Business Finder App** is a Python-based application designed to help users search for businesses, scrape their details, and manage the data efficiently. The app uses web scraping techniques to gather business information and provides functionality to split the data into smaller files for better organization.

## Features

1. **Search for Businesses**:
   - Scrape business details such as name, address, phone number, availability, and industry.
   - Save the scraped data into a CSV file.

2. **Split Data**:
   - Split large CSV files into smaller chunks for easier management.

3. **Interactive CLI**:
   - User-friendly command-line interface for seamless interaction.

## Project Structure

### File Descriptions

- **`app.py`**: The main entry point of the application. It provides a CLI for users to interact with the app.
- **`get_numbers.py`**: Contains the `GetBusinessData` class, which handles web scraping to gather business details.
- **`split_data.py`**: Contains the `SplitData` class, which handles splitting large CSV files into smaller chunks.
- **`berlinder_businesses.csv`** and **`matchoudi_businesses.csv`**: Sample CSV files containing business data.
- **`.gitignore`**: Specifies files and directories to be ignored by Git.

## How to Use

1. **Install Dependencies**:
   - Ensure you have Python installed.
   - Install required libraries using pip:
     ```sh
     pip install selenium colorama
     ```

2. **Run the App**:
   - Execute the [app.py](http://_vscodecontentref_/6) file:
     ```sh
     python app.py
     ```

3. **Follow the CLI Instructions**:
   - Enter your name to start.
   - Choose an option from the menu:
     - Search for businesses.
     - Split data.
     - Exit the app.

## Requirements

- Python 3.7 or higher
- Selenium
- Colorama
- Google Chrome and ChromeDriver (for web scraping)

## Notes

- Ensure the ChromeDriver version matches your installed Google Chrome version.
- The [.gitignore](http://_vscodecontentref_/7) file is configured to ignore temporary files, cache, and CSV files generated during runtime.

## License

This project is licensed under the MIT License.