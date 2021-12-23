import requests
from bs4 import BeautifulSoup
from typing import Dict
import csv
import sys

n = 1

titre = []

def fetch_html(url) -> str:
    '''
    Récupérer le code html de la page web et confirmer si requete http OK
    :param url: le contenu html
    :return: le contenu html en format texte
    '''
    contenu = requests.get(url)
    if contenu.ok:
        print("Le request marche bien\n")
        contenu_texte = BeautifulSoup(contenu.text, "html.parser")
        # print(soup)

    else:
        print("Il y a un problème de request")

    return contenu_texte

def recuperer_urls_categories(url: str) -> list[str]:
    retour = fetch_html(url)
    list_html_categories = retour.find('aside').find_next('li').find_all('li')
    liens_categories = []
    index = url.replace('books_1/index.html', '')

    for nb_categories in range(0, len(list_html_categories)):
        liens_categories.append(index + list_html_categories[nb_categories].find('a')['href'].replace('../',''))

    return liens_categories

def recuperer_urls_livres(url_categories: list[str]) -> list[str]:
    # retour = []
    retour = fetch_html(url_categories[0])
    list_html_livres = retour.find_all('h3')
    print(list_html_livres)
    liens_livres = []
    index_categories = 'http://books.toscrape.com/catalogue/'

    for nb_livres in range(0, len(list_html_livres)):
        liens_livres.append(index_categories + list_html_livres[nb_livres].find_next('a')['href'].replace('../../../',''))
        print(liens_livres)

# def extract_categorie_info(soup):
#     '''
#     titre des livres dans une liste
#     :param soup:
#     :return:
#     '''
#
#     liste_livres, pager = enregistrer_livres(soup)
#
#     while pager == 'next':
#         global n
#         n += 1
#         nouvelle_page = url_categorie.replace('index.html', 'page-' + str(n) + '.html')
#         print(nouvelle_page)
#         reponse = fetch_html(nouvelle_page)
#         liste_livres, pager = enregistrer_livres(reponse)
#
#     print("TITRES : ", liste_livres)
#     print("Nb de livres : ", len(liste_livres))

# def enregistrer_livres(soup):
#     h3 = soup.find_all('h3')
#
#     for i in range(0, len(h3)):
#         titre.append(h3[i].find_next('a')['title'])  # "h3" contient "a", dont l'attribut "title" va dans une liste vide
#
#     print(titre)
#     pager = soup.findAll('li')
#     pager = pager[len(pager) - 1].text
#     print(pager)
#     return titre, pager


# def extract_book_info(soup: str):
#     '''
#     Récupérer l'info du livre et le retourner comme un dictionnaire
#     :param soup:
#     :return:
#     '''
#     # titre du livre #
#     titre = soup.find('h1')
#     titre = titre.text
#     print("Titre: ", titre)
#
#     # UPC, Prix sans taxe, Prix avec taxe, disponibilité et Review #
#     td = soup.findAll('td')  # UPC, les prix, la dispo et les reviews se trouvent dans les seuls "td" qu'il y a dans le code
#     # print(td)
#     upc = td[0].text
#     prix_exc = td[2]
#     prix_inc = td[3]
#     dispo = td[5]
#     review = td[6].text
#     # print(type(dispo))
#     prix_exc = prix_exc.text.replace('Â', '')
#     prix_inc = prix_inc.text.replace('Â', '')
#     dispo = dispo.text.replace('In stock (', '')  # Au début, dispo a un type : <class 'bs4.element.Tag'>
#     dispo = dispo.replace(' available)',
#                           '')  # Mais après avoir utilisé "replace", c'est du type <class 'str'>, c'est pour ça qu'il accepte pas .text
#
#     # print(type(dispo))
#     print("UPC : ", upc)
#     print("Prix sans taxe : ", prix_exc)
#     print("Prix avec taxe : ", prix_inc)
#     print("Disponibilité : ", dispo + " livres")
#     print("Reviews : ", review + " reviews")
#
#     # Description #
#     p = soup.find_all('p')
#     description = p[3].text
#     print("Description : ", description)
#
#     # Categorie #
#     a = soup.find_all('a')
#     categorie = a[3].text
#     print("Categorie : ", categorie)
#
#     # URL Image #
#     img = soup.find_all('img')
#     image = img[0]
#     image_url = image['src']  # Pour recuperer un attribut
#     image_url = image_url.replace('../../', '')
#     image_url = 'http://books.toscrape.com/' + image_url
#     # URL = 'http://books.toscrape.com/'
#     print("URL de l'image : ", image_url)
#
#     info_livre = {
#         'titre': titre,
#         'upc': upc,
#         'prix_exc': prix_exc,
#         'prix_inc': prix_inc,
#         'stock': dispo,
#         'review': review,
#         'description': description,
#         'categorie': categorie,
#         'image': image_url
#     }
#
#     return info_livre

def main():
    url_index = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
    url_categorie = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'
    url_livre = 'http://books.toscrape.com/catalogue/i-had-a-nice-time-and-other-lies-how-to-find-love-sht-like-that_814/index.html'

    urls_categories = recuperer_urls_categories(url_index)
    print("liens des categories : ", urls_categories)

    recuperer_urls_livres(urls_categories)

    # reponse = fetch_html(url_categorie)
    # info = extract_categorie_info(reponse)
    # print(info)

    # reponse = fetch_html(url_livre)
    # info = extract_book_info(reponse)
    # print(info)
    #
    # with open('livre.csv', 'w', encoding = 'utf8', newline='') as csvfile:
    #     tetes = list(info.keys())
    #     print(tetes)
    #     donnes_livres = list(info.values())
    #     print(donnes_livres)
    #
    #     writer = csv.DictWriter(csvfile, fieldnames=tetes)
    #     writer.writeheader()
    #     writer.writerow({tetes[0]:donnes_livres[0],tetes[1]:donnes_livres[1],tetes[2]:donnes_livres[2],tetes[3]:donnes_livres[3],tetes[4]:donnes_livres[4],tetes[5]:donnes_livres[5],tetes[6]:donnes_livres[6],tetes[7]:donnes_livres[7],tetes[8]:donnes_livres[8]})

if __name__ == '__main__':
    main()