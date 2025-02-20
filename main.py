import requests
from bs4 import BeautifulSoup
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
from google.colab import files

def analyze_page(url):
    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Identify the types of useful tags present
        useful_tags = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'img', 'ul', 'ol', 'li'}
        available_tags = set()
        for tag in soup.find_all(True):  # Find all tags
            if tag.name in useful_tags:
                available_tags.add(tag.name)

        return list(available_tags)
    else:
        print("Failed to retrieve the webpage.")
        return None

def scrape_data(url, selected_tags):
    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data for the selected tags
        data = []
        for tag in selected_tags:
            for item in soup.find_all(tag):
                if tag == 'img':
                    data.append({'Type': tag, 'Src': item.get('src', ''), 'Alt Text': item.get('alt', '')})
                elif tag == 'a':
                    data.append({'Type': tag, 'URL': item.get('href', ''), 'Text': item.get_text(strip=True)})
                else:
                    data.append({'Type': tag, 'Content': item.get_text(strip=True)})

        # Convert the data to a DataFrame
        df = pd.DataFrame(data)
        return df
    else:
        print("Failed to retrieve the webpage.")
        return None

def main():
    # Input the URL to scrape
    url = input("Enter the URL to scrape: ")

    if url:
        # Analyze the webpage to find available useful tags
        available_tags = analyze_page(url)

        if available_tags:
            print("Useful tags available on the page:")

            # Create checkboxes for useful tag selection
            checkboxes = [widgets.Checkbox(value=False, description=tag, disabled=False) for tag in available_tags]
            for checkbox in checkboxes:
                display(checkbox)

            # Button to trigger scraping
            button = widgets.Button(description="Scrape Selected Tags")
            display(button)

            def on_button_click(b):
                # Get selected tags
                selected_tags = [checkbox.description for checkbox in checkboxes if checkbox.value]

                if selected_tags:
                    # Scrape data for the selected tags
                    df = scrape_data(url, selected_tags)

                    if df is not None:
                        print("Data scraped successfully!")

                        # Display the DataFrame
                        print(df)

                        # Save the DataFrame to a CSV file
                        csv_file = 'scraped_data.csv'
                        df.to_csv(csv_file, index=False)

                        # Provide a download link for the CSV file
                        files.download(csv_file)
                else:
                    print("No tags selected for scraping.")

            # Attach the button click event
            button.on_click(on_button_click)

if __name__ == "__main__":
    main()
