import requests
from bs4 import BeautifulSoup

def scan_onpage_seo(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = {}

        # Title Tag Check
        title = soup.find('title')
        results['title'] = {
            'found': bool(title),
            'text': title.text.strip() if title else None,
            'length': len(title.text.strip()) if title else 0,
            'status': 'Good' if title and 50 <= len(title.text.strip()) <= 60 else 'Needs Improvement'
        }

        # Meta Description Check
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        desc_text = meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else None
        results['meta_description'] = {
            'found': bool(desc_text),
            'text': desc_text,
            'length': len(desc_text) if desc_text else 0,
            'status': 'Good' if desc_text and 120 <= len(desc_text) <= 160 else 'Needs Improvement'
        }

        # H1 Tag Check
        h1_tags = soup.find_all('h1')
        results['h1'] = {
            'count': len(h1_tags),
            'text': [h.text.strip() for h in h1_tags],
            'status': 'Good' if len(h1_tags) == 1 else 'Needs Improvement (should have exactly 1 H1)'
        }

        # H2 Tags
        h2_tags = soup.find_all('h2')
        results['h2_count'] = len(h2_tags)

        # Image Alt Tags Check
        images = soup.find_all('img')
        missing_alt = [img.get('src', 'unknown') for img in images if not img.get('alt')]
        results['images'] = {
            'total': len(images),
            'missing_alt_count': len(missing_alt),
            'status': 'Good' if len(missing_alt) == 0 else f'{len(missing_alt)} images missing alt text'
        }

        # Word Count
        text_content = soup.get_text()
        word_count = len(text_content.split())
        results['word_count'] = {
            'count': word_count,
            'status': 'Good' if word_count >= 300 else 'Content might be too thin (under 300 words)'
        }

        # Internal & External Links
        links = soup.find_all('a', href=True)
        internal_links = [l for l in links if url in l['href'] or l['href'].startswith('/')]
        external_links = [l for l in links if l['href'].startswith('http') and url not in l['href']]
        results['links'] = {
            'internal': len(internal_links),
            'external': len(external_links)
        }

        return results

    except Exception as e:
        return {'error': str(e)}