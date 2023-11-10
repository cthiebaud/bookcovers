import requests
import os

# Liste des codes ISBN-13 de vos livres
isbn_list = []
with open('isbn-ja.txt') as my_file:
    for line in my_file:
        isbn_list.append(line.replace('-',''))

# Fonction pour récupérer la couverture d'un livre par ISBN-13
def get_book_cover(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url)
    data = response.json()

    if 'items' in data:
        book_data = data['items'][0]['volumeInfo']
        title = book_data.get('title', 'Titre inconnu')
        authors = ', '.join(book_data.get('authors', ['Auteur inconnu']))
        cover_link = book_data['imageLinks']['thumbnail'] if 'imageLinks' in book_data else None

        print(f"{isbn} - Titre: {title} - Auteurs: {authors}")
        if cover_link:
            print(f"URL de la couverture: {cover_link}. Fetching ...")

            import urllib.request

            urllib.request.urlretrieve(cover_link, f"covers_google/{isbn}.jpeg")            # .replace('zoom=1', 'zoom=2')

            print("... fetched.")

        else:
            print("Couverture non trouvée.")
    else:
        print(f"Livre avec ISBN {isbn} non trouvé.")

# Récupérer les couvertures pour chaque ISBN-13
for isbn in isbn_list:
    isbn = isbn.strip()
    if not os.path.isfile(f"covers_google/{isbn}.jpeg"):
        get_book_cover(isbn)    
