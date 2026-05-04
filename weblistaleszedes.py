# #webscraping
# import requests
# import requests_cache
# from bs4 import BeautifulSoup
#
# def scraping_os():
#     os_list = []
#     session = requests_cache.CachedSession("wiki_os_hu")
#     response = session.get("https://hu.wikipedia.org/wiki/Oper%C3%A1ci%C3%B3s_rendszer")
#     print (f"From cache: {hasattr(response, 'from_cache')}")
#     soup = BeautifulSoup(response.text, features="html.parser")
# # itt kitöltöttem az OMHV-t, és "kicsit illegálisan" leszedtük a wikipédia html-jét
#
#     sections = soup.find_all(attrs={"aria-labelledby": "Operációs_rendszer_változatok"})
#     for section in sections:
#         all_link = soup.find_all('a')
#         for link in all_link:
#             print(f"{link.get_text(strip=True)} ({link.get('href')})")
#     return os_list
# #ez még rohadtul hibás és hiányos és leszarom, mert ha másolom sem vagyok vele előrébb mert nem értem faszom
#
#
# if __name__ == '__main__':
#     os_list = scraping_os()

# #deepseek innentől

import requests
import requests_cache
from bs4 import BeautifulSoup
from typing import List, Tuple


def scraping_os() -> List[Tuple[str, str]]:
    """
    Kigyűjti az operációs rendszerek neveit és linkjeit a Wikipédiáról.
    """
    os_list = []

    # 1. HEADERS beállítása - ez KELL a tanár szerint!
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'hu-HU,hu;q=0.9,en;q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }

    # 2. Session létrehozása HEADERS-szel
    session = requests_cache.CachedSession("wiki_os_hu")

    # 3. HEADERS frissítése a sessionben (update headers)
    session.headers.update(headers)

    # 4. Lekérés
    url = "https://hu.wikipedia.org/wiki/Oper%C3%A1ci%C3%B3s_rendszer"
    response = session.get(url)

    print(f"Státusz kód: {response.status_code}")
    print(f"From cache: {hasattr(response, 'from_cache')}")

    if response.status_code != 200:
        print(f"Hiba: nem sikerült letölteni az oldalt ({response.status_code})")
        return os_list

    # 5. BeautifulSoup elemzés
    soup = BeautifulSoup(response.text, 'html.parser')

    # 6. MÓDSZER 1: Megkeressük az "Operációs rendszer változatok" fejezetet
    # A Wikipédia modern verziójában a fejezetek így néznek ki:

    # Keressük a span-t a fejezet címmel
    target_span = soup.find('span', {'id': 'Operációs_rendszer_változatok'})

    if not target_span:
        print("Nem található az 'Operációs rendszer változatok' fejezet")
        # Próbáljuk más módszerrel
        target_span = soup.find('span', string=lambda x: x and 'Operációs rendszer változatok' in x)

    if target_span:
        # A fejezet után következő div-ekben vannak a linkek
        # A szülő elem (általában h2 vagy h3)
        parent = target_span.find_parent()

        if parent:
            # A fejezet utáni elemeket gyűjtjük
            current = parent.find_next_sibling()
            counter = 0
            while current and counter < 10:  # max 10 siblinget nézünk
                # Kigyűjtjük az összes linket ebből az elemből
                links = current.find_all('a', href=True)
                for link in links:
                    href = link.get('href', '')
                    # Csak a belső wiki linkeket vesszük
                    if href.startswith('/wiki/') and ':' not in href:
                        name = link.get_text(strip=True)
                        if name and len(name) > 1 and name not in ['szerkesztés', 'edit']:
                            full_url = f"https://hu.wikipedia.org{href}"
                            if (name, full_url) not in os_list:  # duplikáció ellen
                                os_list.append((name, full_url))
                current = current.find_next_sibling()
                counter += 1

    # 7. MÓDSZER 2: Alternatív keresés - az egész oldalon a megfelelő szekcióban
    if len(os_list) == 0:
        print("Első módszer nem működött, próbálkozom alternatív módszerrel...")

        # Megkeressük az összes h2-t
        for h2 in soup.find_all(['h2', 'h3']):
            if 'Operációs rendszer változatok' in h2.get_text():
                # A következő testvérelemeket nézzük
                for sibling in h2.find_next_siblings():
                    if sibling.name in ['h2', 'h3']:  # új fejezet
                        break
                    # Kigyűjtjük a linkeket
                    links = sibling.find_all('a', href=True)
                    for link in links:
                        href = link.get('href', '')
                        if href.startswith('/wiki/') and ':' not in href:
                            name = link.get_text(strip=True)
                            if name and len(name) > 1:
                                full_url = f"https://hu.wikipedia.org{href}"
                                if (name, full_url) not in os_list:
                                    os_list.append((name, full_url))
                break

    print(f"Talált operációs rendszerek száma: {len(os_list)}")
    return os_list


if __name__ == '__main__':
    os_list = scraping_os()

    if os_list:
        print(f"\n=== TALÁLT OPERÁCIÓS RENDSZEREK ===\n")
        for i, (name, url) in enumerate(os_list[:15], 1):  # első 15
            print(f"{i}. {name}")
            print(f"   {url}\n")
    else:
        print("\nNem találtam semmit. Ellenőrizd az internetkapcsolatot és a URL-t.")
        print("URL: https://hu.wikipedia.org/wiki/Oper%C3%A1ci%C3%B3s_rendszer")

#ez sem működik...