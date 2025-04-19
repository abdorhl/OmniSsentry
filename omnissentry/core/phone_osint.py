import phonenumbers
from phonenumbers import carrier, geocoder
import requests
from ..config import NUMVERIFY_API

def phone_osint(phone_number: str) -> dict:
    try:
        # Start with an empty result dictionary
        result = {}
        
        # Try to parse the phone number
        try:
            parsed = phonenumbers.parse(phone_number, None)
            is_valid = phonenumbers.is_valid_number(parsed)
            
            result = {
                'valid': is_valid,
                'e164': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                'international': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'national': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                'country_code': parsed.country_code,
                'country': phonenumbers.region_code_for_number(parsed) or 'Unknown'
            }
            
            # Add carrier information if available
            carrier_name = carrier.name_for_number(parsed, 'en')
            if carrier_name:
                result['carrier'] = carrier_name
                
            # Add geocoder information if available
            location = geocoder.description_for_number(parsed, 'en')
            if location:
                result['location'] = location
                
        except Exception as e:
            result['parse_error'] = f"Could not parse phone number: {str(e)}"
            result['valid'] = False
        
        # Try numverify API if we have a key
        if NUMVERIFY_API and result.get('valid', False):
            try:
                # Format for the API - remove "+" prefix
                formatted_number = phone_number.lstrip('+')
                
                response = requests.get(
                    f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API}&number={formatted_number}",
                    timeout=10
                )
                
                api_data = response.json() if response.status_code == 200 else {}
                
                if api_data and api_data.get('success') is True:
                    result['line_type'] = api_data.get('line_type')
                    # Add any additional API data we didn't get from phonenumbers
                    if not result.get('carrier') and api_data.get('carrier'):
                        result['carrier'] = api_data.get('carrier')
                    if not result.get('location') and api_data.get('location'):
                        result['location'] = api_data.get('location')
                elif api_data and api_data.get('error'):
                    result['api_error'] = api_data.get('error', {}).get('info', 'Unknown API error')
                else:
                    result['api_error'] = f"API returned status code: {response.status_code}"
            except Exception as e:
                result['api_error'] = f"API request error: {str(e)}"
        else:
            result['api_status'] = "No API key provided or invalid number"
            
        return result
        
    except Exception as e:
        # Fallback if everything else fails
        return {
            'error': f"Unexpected error: {str(e)}",
            'valid': False
        }