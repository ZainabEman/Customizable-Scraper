import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def analyze_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        useful_tags = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'img', 'ul', 'ol', 'li'}
        available_tags = {tag.name for tag in soup.find_all(True) if tag.name in useful_tags}
        return list(available_tags)
    else:
        return None

def scrape_data(url, selected_tags):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        data = []
        for tag in selected_tags:
            for item in soup.find_all(tag):
                if tag == 'img':
                    data.append({'Type': tag, 'Src': item.get('src', ''), 'Alt Text': item.get('alt', '')})
                elif tag == 'a':
                    data.append({'Type': tag, 'URL': item.get('href', ''), 'Text': item.get_text(strip=True)})
                else:
                    data.append({'Type': tag, 'Content': item.get_text(strip=True)})
        return pd.DataFrame(data)
    else:
        return None

def main():
    st.title("Customizable Web Scraper")
    url = st.text_input("Enter the URL to scrape:")
    
    if url:
        available_tags = analyze_page(url)
        if available_tags:
            selected_tags = st.multiselect("Select tags to scrape:", available_tags)
            if st.button("Scrape Data"):
                df = scrape_data(url, selected_tags)
                if df is not None and not df.empty:
                    st.write("### Scraped Data:")
                    st.dataframe(df)
                    
                    # CSV Download
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name="scraped_data.csv",
                        mime="text/csv",
                        key="csv_download"
                    )
                    
                    # JSON Download
                    json_data = df.to_json(orient='records')
                    st.download_button(
                        label="Download as JSON",
                        data=json_data,
                        file_name="scraped_data.json",
                        mime="application/json",
                        key="json_download"
                    )
                else:
                    st.warning("No data found for the selected tags.")
        else:
            st.error("Failed to analyze the page. Check the URL.")

if __name__ == "__main__":
    main()