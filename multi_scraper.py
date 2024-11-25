import requests
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

# Encabezados simulando un motor de búsqueda (como Googlebot)
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

def get_html_with_requests(url, proxy=None):
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, proxies=proxies, timeout=10,headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
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
  );
        await page.goto(url, {"waitUntil": "networkidle2"})
        html = await page.content()
        await browser.close()
        return html
    except Exception as e:
        raise RuntimeError(f"Puppeteer failed: {e}")

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
            capture_screenshot(url, filename=f"{method.__name__}_error.png", proxy=proxy)
            return html
        except Exception as e:
            print(e)
            capture_screenshot(url, filename=f"{method.__name__}_error.png", proxy=proxy)
    raise RuntimeError("All scraping methods failed.")

# Ejemplo de uso
url = "https://www.amazon.com/stores/page/D06BAEB4-0EC0-4F06-A7E5-2AA32381126D"
proxy = "https://sp11k0ggf4:2jTgk6n2d8qgxLSr+R@dc.smartproxy.com:10000"  # Cambiar si se desea usar un proxy o dejar como None
try:
    html_content = scrape_url(url, proxy=proxy)
    soup = BeautifulSoup(html_content, 'html.parser')
    #print(soup.prettify())
except Exception as e:
    print(f"Scraping failed: {e}")
