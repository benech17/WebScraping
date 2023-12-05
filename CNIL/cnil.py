from bs4 import BeautifulSoup as bs
import requests 
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

start_time = time.time()
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

base = 'https://www.cnil.fr/'
articles_data = []  # Liste pour stocker les données de chaque article

for i in range(86):
    cnil_url = 'https://www.cnil.fr/fr/actualites?page='+str(i)
    page = session.get(cnil_url)
    soup = bs(page.text, "lxml")
    view = soup.find("div", class_="view-content")
    try : 
        articles = view.find_all("div", class_="views-row")
        for article in articles: 
            link = base + article.find("a")["href"]
            page_article = session.get(link)
            soup_article = bs(page_article.text, "lxml")
            content = soup_article.find("div", class_="ctn-gen")
            texte = content.find_all("p")
            contenu = " ".join([text.text for text in texte])  # Concaténation du texte
            date= soup_article.find("div", class_="ctn-gen-auteur")
            articles_data.append({
                'lien': link,
                'source': 'CNIL',
                'contenu': contenu,
                'date': date
            })
    except Exception as e:
        print(f"Erreur lors du traitement de la page {i}: {e}")
end_time = time.time()
print(f"Temps d'exécution: {end_time - start_time} secondes")

# Création du DataFrame
df = pd.DataFrame(articles_data)
print(df)