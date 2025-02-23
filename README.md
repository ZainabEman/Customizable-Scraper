# Customizable Web Scraper  

Check it out live Scrapper here : https://huggingface.co/spaces/ZainabEman/Customizable-Web-Scrapper
## Overview  
The **Customizable Web Scraper** is a lightweight Python tool that allows users to extract specific elements from any webpage using a simple graphical interface. Built with **Streamlit**, **BeautifulSoup**, and **Pandas**, this tool enables users to analyze HTML structure, select relevant tags, and download the extracted data in CSV format.  

## Features  
✅ **User-friendly Streamlit interface**  
🔍 **Automatic detection of available HTML tags**  
📌 **Custom tag selection** (`h1`, `h2`, `p`, `a`, `img`, `ul`, etc.)  
📊 **Displays scraped data in a structured table**  
📥 **Download extracted data as a CSV file**  

## Installation  

### Prerequisites  
Ensure you have **Python 3.x** installed on your system.  

### Steps  
1. Clone this repository or download the script:  
   ```sh
   git clone https://github.com/your-repository/Customizable-Scraper.git
   cd Customizable-Scraper
   ```  
2. Install the required dependencies:  
   ```sh
   pip install streamlit requests beautifulsoup4 pandas
   ```  
3. Run the Streamlit app:  
   ```sh
   streamlit run app.py
   ```  

## Usage  

1. **Enter a URL**: Provide the webpage link you want to scrape.  
2. **Analyze the page**: The scraper will identify available HTML tags.  
3. **Select tags**: Choose which elements (headings, paragraphs, links, images, lists, etc.) to extract.  
4. **Scrape Data**: Click the **"Scrape Data"** button to fetch and display the extracted content.  
5. **Download CSV**: Export the scraped data as a CSV file for offline use.  

## Technologies Used  
- **Streamlit** – Interactive UI for user-friendly operation  
- **Requests** – Fetching webpage content  
- **BeautifulSoup4** – Parsing and extracting HTML elements  
- **Pandas** – Structuring and exporting scraped data  

## Limitations  
⚠️ This scraper **cannot**:  
- Extract data from **JavaScript-rendered content**  
- Access **login-restricted** or **protected** pages  
- Scrape sites that block requests in **robots.txt**  

## License  
This project is **open-source** and available for personal and educational use.  

## Contributions  
🔹 Contributions are welcome!  
If you’d like to improve this project, feel free to fork the repository, make enhancements, and submit a **Pull Request**.  

