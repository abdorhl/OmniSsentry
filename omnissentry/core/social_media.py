import requests
from bs4 import BeautifulSoup
from typing import Dict

SOCIAL_PLATFORMS = {
    'twitter': 'https://twitter.com/{}',
    'github': 'https://github.com/{}',
    'instagram': 'https://instagram.com/{}',
    'reddit': 'https://reddit.com/user/{}',
    'medium': 'https://medium.com/@{}',
    'keybase': 'https://keybase.io/{}'
}

def social_media_scrape(username: str) -> Dict:
    results = {}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for platform, url_template in SOCIAL_PLATFORMS.items():
        try:
            url = url_template.format(username)
            response = requests.get(url, timeout=15, allow_redirects=False, headers=headers)
            exists = response.status_code == 200
            
            profile_data = {
                'url': url,
                'exists': exists,
                'status_code': response.status_code
            }
            
            # Skip detailed scraping for Twitter/X as it's mostly JavaScript-rendered now
            # and requires more advanced techniques
            
            # For GitHub, we can extract additional info easily
            if exists and platform == 'github':
                soup = BeautifulSoup(response.text, 'html.parser')
                bio = soup.find('div', {'class': 'p-note user-profile-bio'})
                profile_data['bio'] = bio.text.strip() if bio else None
                
            results[platform] = profile_data
            
        except Exception as e:
            results[platform] = {'error': str(e)}
    
    return results