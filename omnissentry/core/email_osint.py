import requests
import re
from ..config import HUNTER_API_KEY, HAVEI_BEEN_PWNED_API

def validate_email(email):
    """Basic email validation using regex"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def email_breach_check(email):
    """Check if email appears in breaches using HaveIBeenPwned"""
    headers = {'hibp-api-key': HAVEI_BEEN_PWNED_API} if HAVEI_BEEN_PWNED_API else {}
    try:
        response = requests.get(
            f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}',
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"breaches": 0, "message": "No breaches found"}
        else:
            return {"status_code": response.status_code, "message": "API error or rate limited"}
    except Exception as e:
        return {"error": str(e)}

def email_osint_full(email):
    if not validate_email(email):
        return {"error": "Invalid email format"}
    
    results = {}
    
    # Hunter.io verification
    if HUNTER_API_KEY:
        try:
            headers = {
                'User-Agent': 'OmniSentry OSINT Tool',
                'Content-Type': 'application/json'
            }
            hunter_resp = requests.get(
                f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}",
                headers=headers,
                timeout=10
            )
            
            if hunter_resp.status_code == 200:
                results['hunter'] = hunter_resp.json()
            elif hunter_resp.status_code == 401:
                results['hunter_error'] = "API Authentication failed - invalid API key"
            else:
                results['hunter_error'] = f"API Error: {hunter_resp.status_code}"
        except Exception as e:
            results['hunter_error'] = str(e)
    else:
        results['hunter_error'] = "No Hunter API key provided"
    
    # Breach check
    if HAVEI_BEEN_PWNED_API:
        results['breaches'] = email_breach_check(email)
    else:
        results['breaches'] = {"message": "No HaveIBeenPwned API key provided"}
    
    return results