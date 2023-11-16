import asyncio
import requests

from pyppeteer import launch

async def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)

async def get_amazon_covers(keyword):
    browser = await launch(headless=True)
    page = await browser.newPage()

    # Navigate to Amazon search results page
    search_url = f'https://www.amazon.com/s?k={keyword.replace(" ", "+")}'
    await page.goto(search_url)

    await asyncio.sleep(2)  # Adjust the delay time as needed
    
    # Take a screenshot (optional)
    await page.screenshot({'path': 'screenshot.png'})

    # Extract cover URLs
    covers = await page.evaluate('''() => {
        const images = document.querySelectorAll('.s-image');
        return Array.from(images, img => img.src);
    }''')

    await browser.close()

    return covers

# if __name__ == "__main__":
keyword = "Amérique"

# Run the event loop
loop = asyncio.get_event_loop()
covers = loop.run_until_complete(get_amazon_covers(keyword))

for i, cover_url in enumerate(covers, start=1):
        print(f"Cover {i}: {cover_url}")
        filename = f"cover_{i}.jpg"  # You can modify the filename as needed
        loop.run_until_complete(download_image(cover_url, filename))
        print(f"Downloaded {filename}")