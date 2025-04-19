import os
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry

load_dotenv()

# API Configuration
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")
HAVEI_BEEN_PWNED_API = os.getenv("HAVEI_BEEN_PWNED_API")
VIRUSTOTAL_API = os.getenv("VIRUSTOTAL_API")
NUMVERIFY_API = os.getenv("NUMVERIFY_API")

# Rate limiting decorator (10 calls/minute)
@sleep_and_retry
@limits(calls=10, period=60)
def rate_limited_api_call():
    """Empty function to apply rate limiting to other functions"""
    pass