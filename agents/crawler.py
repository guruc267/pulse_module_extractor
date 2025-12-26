

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


def crawl_docs(start_url, max_pages=20):
    visited = set()
    to_visit = [start_url]
    pages = {}

    domain = urlparse(start_url).netloc

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove junk
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()

            content_blocks = []

            # ✅ Preserve structure
            for tag in soup.find_all(["h1", "h2", "h3", "p", "li"]):
                text = tag.get_text(strip=True)
                if len(text.split()) >= 2:
                    content_blocks.append(text)

            pages[url] = "\n".join(content_blocks)
            visited.add(url)

            # Crawl internal links
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                if (
                    urlparse(full_url).netloc == domain
                    and full_url not in visited
                    and full_url not in to_visit
                ):
                    to_visit.append(full_url)

            time.sleep(0.5)

        except Exception:
            continue

    return pages
