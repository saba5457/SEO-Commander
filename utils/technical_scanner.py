import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scan_technical_seo(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}

        # Page Speed (basic load time check)
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=15)
        load_time = round(time.time() - start_time, 2)

        soup = BeautifulSoup(response.text, 'html.parser')
        results = {}

        # Load Time
        results['load_time'] = {
            'seconds': load_time,
            'status': 'Good' if load_time < 2 else ('Average' if load_time < 4 else 'Slow - Needs Optimization')
        }

        # HTTPS Check
        results['https'] = {
            'enabled': url.startswith('https://'),
            'status': 'Good' if url.startswith('https://') else 'Not Secure - Missing SSL'
        }

        # Mobile Viewport Check
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        results['mobile_viewport'] = {
            'found': bool(viewport),
            'status': 'Good' if viewport else 'Missing - Not Mobile Optimized'
        }

        # Robots.txt Check
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        try:
            robots_response = requests.get(urljoin(base_url, '/robots.txt'), headers=headers, timeout=5)
            robots_exists = robots_response.status_code == 200
        except:
            robots_exists = False
        results['robots_txt'] = {
            'found': robots_exists,
            'status': 'Good' if robots_exists else 'Missing robots.txt'
        }

        # Sitemap Check
        try:
            sitemap_response = requests.get(urljoin(base_url, '/sitemap.xml'), headers=headers, timeout=5)
            sitemap_exists = sitemap_response.status_code == 200
        except:
            sitemap_exists = False
        results['sitemap'] = {
            'found': sitemap_exists,
            'status': 'Good' if sitemap_exists else 'Missing sitemap.xml'
        }

        # Heading Structure Check
        headings = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}
        results['heading_structure'] = headings

        # Canonical Tag Check
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        results['canonical_tag'] = {
            'found': bool(canonical),
            'status': 'Good' if canonical else 'Missing canonical tag'
        }

        # Broken Links Check (sample first 10 links only, for speed)
        links = soup.find_all('a', href=True)[:10]
        broken_links = []
        for link in links:
            href = link['href']
            full_url = urljoin(url, href)
            if full_url.startswith('http'):
                try:
                    r = requests.head(full_url, headers=headers, timeout=5)
                    if r.status_code >= 400:
                        broken_links.append(full_url)
                except:
                    broken_links.append(full_url)
        results['broken_links'] = {
            'checked': len(links),
            'broken_count': len(broken_links),
            'broken_urls': broken_links,
            'status': 'Good' if len(broken_links) == 0 else f'{len(broken_links)} broken links found'
        }

        return results

    except Exception as e:
        return {'error': str(e)}