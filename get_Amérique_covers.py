import requests
from bs4 import BeautifulSoup

def get_book_covers(keyword):
    base_url = "https://www.amazon.com"
    search_url = f"{base_url}/s?k={keyword.replace(' ', '+')}&page="

    covers = []

    for page_number in range(1, 6):  # Récupérer les résultats des 5 premières pages
        page_url = f"{search_url}{page_number}"
        response = requests.get(page_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', {'class': 's-result-item'})

            for result in results:
                try:
                    title = result.find('span', {'class': 'a-text-normal'}).text
                    if keyword.lower() in title.lower():
                        cover_url = result.find('img')['src']
                        covers.append(cover_url)
                except (TypeError, KeyError):
                    pass

    return covers

keyword = "Amérique"
book_covers = get_book_covers(keyword)

for i, cover_url in enumerate(book_covers, start=1):
    print(f"Cover {i}: {cover_url}")
