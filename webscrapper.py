from bs4 import BeautifulSoup
import requests

from tools import from_dict_to_json

NEXT_PAGE_TITLE="Especial:Todas"
FIRST_TOC_PAGE ="/es/wiki/Especial:Todas?from=1"
NEXT_PAGE_TEXT="Página siguiente"

URL_BASE = "https://onepiece.fandom.com"
def create_beautifull_object(url: str):
    """Create a BeautifulSoup object from a URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None
def extract_links_webpage(soup: BeautifulSoup)-> list:
    """Extract all links from a BeautifulSoup object."""
    links = {}
    tag = soup.find("ul", class_="mw-allpages-chunk")
    for link in tag.find_all('a', href=True):
        if link['href'].startswith('/es/wiki/'):
            if 'title' in link.attrs and len(link['title']) > 0:
                title = link['title']
                links[title] = link['href']
    return links

def nextpage(soup: BeautifulSoup) -> str:
    """Get the URL for the next page from the BeautifulSoup object."""
    next_page_links = soup.find_all('a', title=NEXT_PAGE_TITLE)
    for link in next_page_links:
        if link.text.strip().startswith(NEXT_PAGE_TEXT):
            return link['href']
    return ""

def get_all_wiki_content():
    soup = create_beautifull_object(URL_BASE + FIRST_TOC_PAGE)
    links = extract_links_webpage(soup)
    url = nextpage(soup)
    while len(url) > 0:
        soup = create_beautifull_object(URL_BASE + url)
        links.update(extract_links_webpage(soup))
        url = nextpage(soup)
    return links

if __name__ == "__main__":
    links = get_all_wiki_content()
    for title, link in links.items():
        print(f"{title}: {URL_BASE + link}")
    print(f"Total links found: {len(links)}")

    from_dict_to_json(links, "chopper_links.json")