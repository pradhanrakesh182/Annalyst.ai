import requests
import re
from flask import Flask, render_template

app = Flask(__name__)

def scrape_amazon_products():
    url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    response = requests.get(url)

    if response.status_code == 200:
        webpage_content = response.text
    else:
        return None

    # Extract product titles and prices using regex
    product_details = []
    titles_prices = re.findall(r'<span class="a-size-medium a-color-base a-text-normal">(.+?)</span>.*?<span class="a-offscreen">(.+?)</span>', webpage_content)

    for title, price in titles_prices:
        product_details.append({
            "title": title.strip(),
            "price": price.strip()
        })

    return product_details

@app.route('/')
def index():
    products = scrape_amazon_products()
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
