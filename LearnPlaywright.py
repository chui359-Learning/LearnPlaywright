# pip install playwright
# playwright install
import time
import asyncio
from playwright.async_api import async_playwright

async def extract_price_with_playwright(url):
    strart_time = time.time()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # 設置user-agent
        await context.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36"
        })

        await page.goto(url)

        # 等待價格元素出現
        await page.wait_for_selector('.ProductCardNormalGrid__priceWrap__3XQGB')

        # 找到所有價格元素
        price_elements = await page.query_selector_all('.ProductCardNormalGrid__priceWrap__3XQGB')

        prices = []
        for price_element in price_elements:
            price_div = await price_element.query_selector('.ProductCardNormalGrid__price__1iXqP')
            if price_div:
                price = await price_div.inner_text()
                prices.append(price.strip())

        await browser.close()
        end_time = time.time()
        total_time = end_time - strart_time
        print(f"total_time: {total_time}")
        return prices if prices else "not exist"

url = "https://www.asus.com/tw/laptops/for-gaming/rog-republic-of-gamers/filter?SubSeries=ROG-Zephyrus"
prices_playwright = asyncio.run(extract_price_with_playwright(url))
print(prices_playwright)
