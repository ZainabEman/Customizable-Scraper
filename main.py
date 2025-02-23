import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from requests.exceptions import RequestException

# Function to analyze available tags on the page
def analyze_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        useful_tags = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'img', 'ul', 'ol', 'li'}
        available_tags = {tag.name for tag in soup.find_all(True) if tag.name in useful_tags}
        return list(available_tags)
    except RequestException as e:
        st.error(f"Failed to fetch the page: {str(e)}")
        return None

# Function to scrape selected tags
def scrape_data(url, selected_tags):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
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
    except RequestException as e:
        st.error(f"Error scraping data: {str(e)}")
        return None

# Main Streamlit app
def main():
    st.title("Live Web Scraper")
    st.write("Enter a URL and select the HTML tags you want to scrape!")

    # URL input
    url = st.text_input("Enter the URL to scrape:", key="url_input")

    if url:
        with st.spinner("Analyzing the page..."):
            available_tags = analyze_page(url)

        if available_tags:
            # Tag selection
            selected_tags = st.multiselect("Select tags to scrape:", available_tags, key="tag_select")

            if st.button("Scrape Now", key="scrape_button"):
                with st.spinner("Scraping data..."):
                    df = scrape_data(url, selected_tags)

                if df is not None and not df.empty:
                    st.success("Scraping complete!")
                    st.write("### Scraped Data:")
                    st.dataframe(df)

                    # Download options
                    col1, col2 = st.columns(2)
                    with col1:
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download as CSV",
                            data=csv,
                            file_name="scraped_data.csv",
                            mime="text/csv",
                            key="csv_download"
                        )
                    with col2:
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
            st.error("Couldn’t analyze the page. Check the URL and try again.")

    # Footer section
    st.markdown("""
    ---
    **Connect with me:**  
    [LinkedIn](https://www.linkedin.com/in/zainab-eman18/) | [GitHub](https://github.com/ZainabEman) | [Medium](https://medium.com/@zainabeman976) | [Instagram](https://www.instagram.com/zainab_.eman/)  
    
    *"Crafted with ❤️ by a curious mind. Keep exploring, keep building!"*  
    
    © 2025 All Rights Reserved.
    """)

if __name__ == "__main__":
    main()