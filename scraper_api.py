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
from playwright.async_api import async_playwright
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Encabezados simulando un motor de búsqueda
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}
timestamp = time.time()

headers2 = {
  'Host': ' www.walmart.com',
  'User-Agent': ' Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0',
  'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': ' es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': ' gzip, deflate, br, zstd',
  'Connection': ' keep-alive',
  'Cookie': ' AID=wmlspartner=0:reflectorid=0000000000000000000000:lastupd=1733251728204; com.wm.reflector="reflectorid:0000000000000000000000@lastupd:1733251730000@firstcreate:1733251728204"; ACID=cac0b95b-07bd-4deb-b9fa-db8045556cdb; _intlbu=false; _m=9; _shcc=US; assortmentStoreId=3081; auth=MTAyOTYyMDE4oRm7p3wcKFaSk1Sa%2BeFOWnteX18v9kXZPeESmiv0CbM3xzlVYCW1n26WoPGsVUiOjmTx%2BYl%2Fr8HUEU6EH4mxEQUOxP4v61iM1Ov35RsxFCOO8%2BgWPmwn%2Fyx1o2RajHeU767wuZloTfhm7Wk2Kcjygp0i2CSRVbB3L7ys%2FtvUzQf4VoC0PYa0Ovtg0T1Fw2nOKCdHK9ys3T9RDOw86dzFRCGExOFInGYexd7%2BG2xG19YUMk70P8glgOEpLOprhDfMJ0tmvH1FCaN9tZDh4SCrHbGY0y779bVjCk397ISaN9DIAR9%2FIL0pc1oHf5Txs5iMTtm0Vs3UCpSP2yDbTT83tdXo6pn8RKcNpbDiuu6V9ElM%2BmGraqo3%2FbQBjwCKMQHmJllclp%2FJeO9aaTT3vFAmaEjyrOXbKKhH072NS%2FW0j%2FU%3D; hasACID=true; hasLocData=1; locDataV3=eyJpc0RlZmF1bHRlZCI6dHJ1ZSwiaXNFeHBsaWNpdCI6ZmFsc2UsImludGVudCI6IlNISVBQSU5HIiwicGlja3VwIjpbeyJub2RlSWQiOiIzMDgxIiwiZGlzcGxheU5hbWUiOiJTYWNyYW1lbnRvIFN1cGVyY2VudGVyIiwiYWRkcmVzcyI6eyJwb3N0YWxDb2RlIjoiOTU4MjkiLCJhZGRyZXNzTGluZTEiOiI4OTE1IEdFUkJFUiBST0FEIiwiY2l0eSI6IlNhY3JhbWVudG8iLCJzdGF0ZSI6IkNBIiwiY291bnRyeSI6IlVTIn0sImdlb1BvaW50Ijp7ImxhdGl0dWRlIjozOC40ODI2NzcsImxvbmdpdHVkZSI6LTEyMS4zNjkwMjZ9LCJzY2hlZHVsZWRFbmFibGVkIjp0cnVlLCJ1blNjaGVkdWxlZEVuYWJsZWQiOnRydWUsInN0b3JlSHJzIjoiMDY6MDAtMjM6MDAiLCJhbGxvd2VkV0lDQWdlbmNpZXMiOlsiQ0EiXSwic3VwcG9ydGVkQWNjZXNzVHlwZXMiOlsiUElDS1VQX1NQRUNJQUxfRVZFTlQiLCJQSUNLVVBfSU5TVE9SRSIsIlBJQ0tVUF9DVVJCU0lERSJdLCJ0aW1lWm9uZSI6IlBTVCIsInN0b3JlQnJhbmRGb3JtYXQiOiJXYWxtYXJ0IFN1cGVyY2VudGVyIiwic2VsZWN0aW9uVHlwZSI6IkRFRkFVTFRFRCJ9XSwic2hpcHBpbmdBZGRyZXNzIjp7ImxhdGl0dWRlIjozOC40ODI2NzcsImxvbmdpdHVkZSI6LTEyMS4zNjkwMjYsInBvc3RhbENvZGUiOiI5NTgyOSIsImNpdHkiOiJTYWNyYW1lbnRvIiwic3RhdGUiOiJDQSIsImNvdW50cnlDb2RlIjoiVVMiLCJsb2NhdGlvbkFjY3VyYWN5IjoibG93IiwiZ2lmdEFkZHJlc3MiOmZhbHNlLCJhbGxvd2VkV0lDQWdlbmNpZXMiOlsiQ0EiXX0sImFzc29ydG1lbnQiOnsibm9kZUlkIjoiMzA4MSIsImRpc3BsYXlOYW1lIjoiU2FjcmFtZW50byBTdXBlcmNlbnRlciIsImludGVudCI6IlBJQ0tVUCJ9LCJpbnN0b3JlIjpmYWxzZSwiZGVsaXZlcnkiOnsibm9kZUlkIjoiMzA4MSIsImRpc3BsYXlOYW1lIjoiU2FjcmFtZW50byBTdXBlcmNlbnRlciIsImFkZHJlc3MiOnsicG9zdGFsQ29kZSI6Ijk1ODI5IiwiYWRkcmVzc0xpbmUxIjoiODkxNSBHRVJCRVIgUk9BRCIsImNpdHkiOiJTYWNyYW1lbnRvIiwic3RhdGUiOiJDQSIsImNvdW50cnkiOiJVUyJ9LCJnZW9Qb2ludCI6eyJsYXRpdHVkZSI6MzguNDgyNjc3LCJsb25naXR1ZGUiOi0xMjEuMzY5MDI2fSwic2NoZWR1bGVkRW5hYmxlZCI6ZmFsc2UsInVuU2NoZWR1bGVkRW5hYmxlZCI6ZmFsc2UsImFjY2Vzc1BvaW50cyI6W3siYWNjZXNzVHlwZSI6IkRFTElWRVJZX0FERFJFU1MifV0sImlzRXhwcmVzc0RlbGl2ZXJ5T25seSI6ZmFsc2UsImFsbG93ZWRXSUNBZ2VuY2llcyI6WyJDQSJdLCJzdXBwb3J0ZWRBY2Nlc3NUeXBlcyI6WyJERUxJVkVSWV9BRERSRVNTIl0sInRpbWVab25lIjoiUFNUIiwic3RvcmVCcmFuZEZvcm1hdCI6IldhbG1hcnQgU3VwZXJjZW50ZXIiLCJzZWxlY3Rpb25UeXBlIjoiREVGQVVMVEVEIn0sImlzZ2VvSW50bFVzZXIiOmZhbHNlLCJtcERlbFN0b3JlQ291bnQiOjAsInJlZnJlc2hBdCI6MTczMzI3MzMyODI2MCwidmFsaWRhdGVLZXkiOiJwcm9kOnYyOmNhYzBiOTViLTA3YmQtNGRlYi1iOWZhLWRiODA0NTU1NmNkYiJ9; locGuestData=eyJpbnRlbnQiOiJTSElQUElORyIsImlzRXhwbGljaXQiOmZhbHNlLCJzdG9yZUludGVudCI6IlBJQ0tVUCIsIm1lcmdlRmxhZyI6ZmFsc2UsImlzRGVmYXVsdGVkIjp0cnVlLCJwaWNrdXAiOnsibm9kZUlkIjoiMzA4MSIsInRpbWVzdGFtcCI6MTczMzI1MTcyODI1Nywic2VsZWN0aW9uVHlwZSI6IkRFRkFVTFRFRCJ9LCJzaGlwcGluZ0FkZHJlc3MiOnsidGltZXN0YW1wIjoxNzMzMjUxNzI4MjU3LCJ0eXBlIjoicGFydGlhbC1sb2NhdGlvbiIsImdpZnRBZGRyZXNzIjpmYWxzZSwicG9zdGFsQ29kZSI6Ijk1ODI5IiwiZGVsaXZlcnlTdG9yZUxpc3QiOlt7Im5vZGVJZCI6IjMwODEiLCJ0eXBlIjoiREVMSVZFUlkiLCJ0aW1lc3RhbXAiOjE3MzMyNTE3MjgyNTIsImRlbGl2ZXJ5VGllciI6bnVsbCwic2VsZWN0aW9uVHlwZSI6IkRFRkFVTFRFRCIsInNlbGVjdGlvblNvdXJjZSI6bnVsbH1dLCJjaXR5IjoiU2FjcmFtZW50byIsInN0YXRlIjoiQ0EifSwicG9zdGFsQ29kZSI6eyJ0aW1lc3RhbXAiOjE3MzMyNTE3MjgyNTcsImJhc2UiOiI5NTgyOSJ9LCJtcCI6W10sIm1zcCI6eyJub2RlSWRzIjpbXSwidGltZXN0YW1wIjpudWxsfSwibXBEZWxTdG9yZUNvdW50IjowLCJ2YWxpZGF0ZUtleSI6InByb2Q6djI6Y2FjMGI5NWItMDdiZC00ZGViLWI5ZmEtZGI4MDQ1NTU2Y2RiIn0%3D; userAppVersion=us-web-1.171.4-22e8dcfe70ac4c2a97ebec1ee1cf1bdff5c8ff5d-112018; abqme=true; vtc=Zh5rM5c_spMZxVl1j1EYPk; bstc=Zh5rM5c_spMZxVl1j1EYPk; mobileweb=0; xpth=x-o-mart%2BB2C~x-o-mverified%2Bfalse; xpa=69a0j|fdm-7; xpm=0%2B1733251730%2BZh5rM5c_spMZxVl1j1EYPk~%2B0; exp-ck=fdm-71; _pxhd=c289dcb9cf2b1098135f9e550c6583152e8399f23d9d933876dfac7bcd155592:3b239947-b1a7-11ef-8f51-0a828f7499b7; xptwg=4021235912:118916E1D72F1B0:2B73E27:48A1E90A:5C17DE24:6374447F:; xptwj=uz:9b4e1654bdc99569019c:GfN7zU3z0PZhkYCse0zSdPCVZaq55p7s8lyNINrhLPVGZfw5yX2CPiHdOLVS3Ty6QGd2p+2D/ofkPGWrRz/1PIOQu/FGndrUIa/sDf55zrKJmH0IjPG5JZztv+fex+leHnNPDbBpm/KB4J6Nhq7+pMwggfvErAbSX1UFA10W2EnqaSrlBt4B; TS012768cf=01f76c8b07708e0e32702eb30b7f1c43f0bcc7f4c056270726a5a66b648122f477ebeef6c883276c3ace997df80be356aa85e43a34; TS01a90220=01f76c8b07708e0e32702eb30b7f1c43f0bcc7f4c056270726a5a66b648122f477ebeef6c883276c3ace997df80be356aa85e43a34; TS2a5e0c5c027=08acb5a182ab2000f1fd7b5d287b438d0306c6ad24b5e2c120d277d84f09cd55d4114c85d8b7129208bf076b8c11300031f8f080494e25d250721bb3ba39d40ff3daf2e3d42708faad010e746199cfbc8fac55def243e8f3874171d1c19fdde3; akavpau_p2=1733252330~id=2496ee7c6f4c54bdd0ba46cbac218bab; ak_bmsc=706F22ABCFE9F09D39CA791A3DA999E1~000000000000000000000000000000~YAAQPyj3SHu6j2mTAQAAhIXajRkg6AbipF+eCG191opynHDlq41xk0jh6CNjIOAEHe/u/3sB6y2Uhu1EzyLovGmiB7naAx4iNQflx0O3bRgydnchPSPP2r3z+apxdNqG+hYT6Uwk7HGjbhdjad2VpVb2p++F7f57C8SVOtQWqFeVxYxDRuKdqnztZsAeVln2iUZU3AdioPrSZ254hbmVYat+JKXbqXibe2OXTdJxdl7fY2slXpr2nWfIcNS9hm6EyanTpOje0BzVw/y6z+R4RAsXGJ+Z+KVnPQSZ7sVZFLfuWhmyDZMRwzWe/SKa1dikjyF+MVAvIDzHHOdKcznfiJ0nffFumWmUaQHa/QmSp18e5iHNFw8XMdvuVilZJzWvE+hrSSAS8n1aVTg=; _astc=609dc4930fdeb596e1ed5bc87f420a43; adblocked=false; xptc=assortmentStoreId%2B3081~_m%2B9; bm_sv=343778B71DEC03971DD3A7313C28AA2B~YAAQPyj3SGW7j2mTAQAANqLajRn04bW3/gcahPmCaRUDG1c2ys5SqpQGvlElaaREGySAcNhWxpcglQN62U5zO523AqR4WAaDZhCIFDd9q5CecaDbG6tRfJDvl7CX8DvzyiKYM6oUpLUAtz8DtqOxhMQ1j3+RmIPBkwGsyMI1BoJkyHiD+n7yrJjoChdJouwhowTIP78Yi1JgIIeXejNIbIreKMJu+1JUUQUQc+VQ6JZIXrtigpYzzxbmLSoSQzx9Eg==~1; pxcts=3bfda996-b1a7-11ef-a589-db05ce8ab217; _pxvid=3b239947-b1a7-11ef-8f51-0a828f7499b7; _pxde=e420c16ae8c149980ef2cf6e71da38150703d08208894c2c843cb48ae6e7e68b:eyJ0aW1lc3RhbXAiOjE3MzMyNTE3MzIxNjN9; _px3=9d8ca0ea372b38a9f33bcc56733185d27dc59ade69ab34d597fdc60f6c9beee8:CDF4ebnrd0KMzGezrbdPReXl/PuaxJBvNwyh7E4cAIfeVXT2D54hM533VdbyqvVIZxg0zYzBOo3Qda0G5cYwiQ==:1000:Jw4UVIs1fd3nH8l8H/U8reZ3XE11ZaxDlfi5BPNAA9wXhr1Ga3WemI7yZ6kBpp3CpWHVrTKiDbBPyUjjvKhZMe8bSgnrPt3k7DumIMKUb9lY4IeSfSSt1VV+INcoZQfkOhBsUvQOxros1nLE6i/yfy5UiiHtkRUMkJnba51nWHogWfUZ9MVu/Lmw56gH2ZnNq1610LOB40Qnxn1AOhQfa7l+VVQUUSV6Tg4Yd/BVc5U=; wm_accept_language=es-US; io_id=a8e5a937-7065-487b-a9af-442ecee18b4e; if_id=FMEZARSFmy8lpc/x1G2/ipXw9rtIR+O/uXgCmSDoBuTXB1HfLWVC0JAlJ693tXIQOzx5gGhLGD+n/l1C5RjF20/oiVLlRDAVs0/NzXjg4WvGwlvDzq48HveajYxe7dUqORzlMT/E4TD16frBnozxNIeD/44DWIb8p3Bj7SiBZ2f6Qh5TEdx1+sUHHEzkIxPpaiRr02VMriWB5QiBrPB9rtBtmuK3ndNbld4OYH7oxZ26euWS9HjtTLAtgEQ1bCdRVC7i0fOuEMtzjD9ZT6o=; TS016ef4c8=01fc4b99c7c80ba5f6705330d6ca83f90134f6f3da7f723bda96dc83f85cbe4d4d994630e1a93bb11c0899903181677c05ff562ac0; TS01f89308=01fc4b99c7c80ba5f6705330d6ca83f90134f6f3da7f723bda96dc83f85cbe4d4d994630e1a93bb11c0899903181677c05ff562ac0; TS8cb5a80e027=08f715dd0dab20006449e8fecab08dd94c68b26eeaa891bbcafd9e2f30ae7ce1132a9ad9c42565e1088c1c1d0a1130000f65e944a0b90227b7cbc2543e68456cd6455eca30497a94947d97fc8eafc57aa3f80af36547406008214f2ed4612166',
  'Upgrade-Insecure-Requests': ' 1',
  'Sec-Fetch-Dest': ' document',
  'Sec-Fetch-Mode': ' navigate',
  'Sec-Fetch-Site': ' none',
  'Sec-Fetch-User': ' ?1',
  'Priority': ' u=0, i',
  'TE': ' trailers'
}

##/usr/bin/chromedriver

##/usr/local/bin/chromedriver



def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
   
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        },
    )
    return driver


def capture_screenshot(url, filename="error_screenshot.png", proxy=None):
    driver = None  # Inicializa el driver como None
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        # if proxy:
        #     options.add_argument(f'--proxy-server={proxy}')
        
        driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)
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
        #capture_screenshot(url, filename=f"{timestamp}_error.png", proxy=proxy)
        return response.text
    except Exception as e:
        capture_screenshot(url, filename=f"{timestamp}_error.png", proxy=proxy)
        raise RuntimeError(f"Requests failed: {e}")

def get_html_with_cloudscraper(url, proxy=None):
    try:
        scraper = cloudscraper.create_scraper()
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = scraper.get(url, proxies=proxies, timeout=10)
        print(response)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise RuntimeError(f"Cloudscraper failed: {e}")

async def scrape_with_playwright(url, proxy=None):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(

            )
            page = await context.new_page()

            # if proxy:
            #     context.set_proxy({"server": proxy})

            await page.goto(url, wait_until="load")
            html = await page.content()
            await browser.close()
            return html
    except Exception as e:
        raise RuntimeError(f"Playwright failed: {e}")
    
async def get_html_with_selenium(url, proxy=None):
    driver = None  # Inicializa el driver como None
    try:

        driver = setup_driver()
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        print("HTML====",html)
        return driver.page_source
    except Exception as e:
        raise RuntimeError(f"Selenium failed: {e}")
    finally:
        if driver:
            print("Closing WebDriver...")
            driver.quit()
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
        #get_html_with_cloudscraper,
        #get_html_with_puppeteer,
        #scrape_with_playwright,
        get_html_with_selenium,
        #get_html_with_requests,
        

    ]
    
    for method in methods:
        try:
            if method == get_html_with_puppeteer:
                html = asyncio.run(method(url, proxy=proxy))
            else:

                html = asyncio.run(method(url, proxy=proxy))

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

