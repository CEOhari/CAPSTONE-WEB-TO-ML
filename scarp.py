import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import re

# Base URL with pagination
BASE_URL = "https://www.flipkart.com/search?q=tv&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_8_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_8_0_na_na_na&as-pos=8&as-type=TRENDING&suggestionId=tv&requestId=9c9fa553-b7e5-454b-a65b-bbb7a9c74a29"
headers = {'User-Agent': 'Mozilla/5.0'}

# Lists to store scraped data
products, discount_prices, original_prices, discount_percents = [], [], [], []
ratings, reviews = [], []
apps, os_list, hd, sound = [], [], [], []

# Loop through pages 1 to 30
for page_num in range(1, 31):
    print(f"Scraping Page {page_num}...")
    URL = BASE_URL.format(page_num)

    # Get the page content
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page {page_num}, status code: {response.status_code}")
        continue

    soup = bs(response.content, 'html.parser')  # Make sure this line is inside the loop

    for data in soup.find_all('div', class_='yKfJKb row'):
        name = data.find('div', class_='KzDlHZ')
        discount_price = data.find('div', class_='Nx9bqj _4b5DiR')
        original_price = data.find('div', class_='H6-L0U')
        discount_percent = data.find('span', class_='_3Ay6Sb')
        rating = data.find('div', class_='XQDdHH')
        review = data.find('span', class_='Wphh3N')
        specification = data.find('div', class_='_6NESgJ')

        if name and discount_price and rating and specification:
            col = specification.find_all('li', class_='J+igdf')
            if len(col) >= 4:
                products.append(name.text.strip())

                # Only numbers from prices
                dp = re.sub(r'[^\d]', '', discount_price.text) if discount_price else "0"
                op = re.sub(r'[^\d]', '', original_price.text) if original_price else "0"
                discount_prices.append(dp)
                original_prices.append(op)

                discount_percents.append(discount_percent.text.strip() if discount_percent else "N/A")
                ratings.append(rating.text.strip())
                reviews.append(review.text.strip() if review else "N/A")
                apps.append(col[0].text.strip())
                os_list.append(col[1].text.strip())
                hd.append(col[2].text.strip())
                sound.append(col[3].text.strip())

    time.sleep(1)  # polite delay to avoid getting blocked

# Create DataFrame
df = pd.DataFrame({
    'Product Name': products,
    'Discounted Price': discount_prices,
    'Original Price': original_prices,
    'Discount %': discount_percents,
    'Rating': ratings,
    'Reviews': reviews,
    'Supported Apps': apps,
    'Operating System': os_list,
    'Resolution': hd,
    'Sound System': sound
})

# Save to CSV
df.to_csv('Flip_Data.csv', index=False)
print("\n✅ Data saved to 'Flip_Data.csv'")
