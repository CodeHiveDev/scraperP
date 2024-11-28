from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import cloudscraper
import time
from PIL import Image
from io import BytesIO
import asyncio
from pyppeteer import launch
import requests

app = Flask(__name__)

# Encabezados simulando un motor de búsqueda
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}
timestamp = time.time()

def capture_screenshot(url, filename="error_screenshot.png", proxy=None):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        # if proxy:
        #     options.add_argument(f'--proxy-server={proxy}')
        
        driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
        driver.get(url)
        time.sleep(2)
        screenshot = driver.get_screenshot_as_png()
        driver.quit()
        image = Image.open(BytesIO(screenshot))
        image.save(filename)
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")


def get_html_with_requests(url, proxy=None):
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, proxies=proxies, timeout=10, headers=headers)
        response.raise_for_status()
        capture_screenshot(url, filename=f"{timestamp}_error.png", proxy=proxy)
        return response.text
    except Exception as e:
        capture_screenshot(url, filename=f"{timestamp}_error.png", proxy=proxy)
        raise RuntimeError(f"Requests failed: {e}")

def get_html_with_cloudscraper(url, proxy=None):
    try:
        scraper = cloudscraper.create_scraper()
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = scraper.get(url, proxies=proxies, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise RuntimeError(f"Cloudscraper failed: {e}")

def get_html_with_selenium(url, proxy=None):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
    
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        
        driver = webdriver.Chrome(service=Service("chromedriver"), options=options)
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        driver.quit()
        return html
    except Exception as e:
        driver.quit()
        raise RuntimeError(f"Selenium failed: {e}")

async def get_html_with_puppeteer(url, proxy=None):
    try:
        args = ['--no-sandbox', '--disable-setuid-sandbox']
        if proxy:
            args.append(f'--proxy-server={proxy}')
        
        browser = await launch(headless=True, args=args)
        page = await browser.newPage()
        await page.setUserAgent(
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        )
        await page.goto(url, {"waitUntil": "networkidle2"})
        html = await page.content()
        await browser.close()
        return html
    except Exception as e:
        raise RuntimeError(f"Puppeteer failed: {e}")

def scrape_url(url, proxy=None):
    methods = [
        get_html_with_requests,
        get_html_with_cloudscraper,
        get_html_with_selenium,
        get_html_with_puppeteer
    ]
    
    for method in methods:
        try:
            if method == get_html_with_puppeteer:
                html = asyncio.run(method(url, proxy=proxy))
            else:
                html = method(url, proxy=proxy)
            print(f"Successfully scraped with {method.__name__}")
            return html
        except Exception as e:
            print(e)
    raise RuntimeError("All scraping methods failed.")

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get("url")
    proxy = data.get("proxy")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        html_content = scrape_url(url, proxy=proxy)
        return jsonify({"success": True, "html": html_content})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

