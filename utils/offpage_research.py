from urllib.parse import urlparse
import whois
from duckduckgo_search import DDGS

def search_ddg(query, num_results=5):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=num_results):
                if r.get('href'):
                    results.append(r['href'])
        return results
    except Exception:
        return []

def research_offpage_seo(url, niche_keyword):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        results = {}

        try:
            domain_info = whois.whois(domain)
            creation_date = domain_info.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            results['domain_age'] = {'creation_date': str(creation_date) if creation_date else 'Unknown'}
        except Exception:
            results['domain_age'] = {'creation_date': 'Unknown'}

        guest_post_sites = search_ddg(f"{niche_keyword} write for us")
        directory_sites = search_ddg(f"{niche_keyword} business directory submit")
        competitors = search_ddg(niche_keyword)
        competitors = [c for c in competitors if domain not in c]

        results['guest_post_opportunities'] = guest_post_sites
        results['directory_opportunities'] = directory_sites
        results['competitors'] = competitors[:5]
        results['niche_keyword'] = niche_keyword

        return results

    except Exception as e:
        return {'error': str(e)}