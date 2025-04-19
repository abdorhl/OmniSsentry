import pytest
from omnissentry.core.domain_osint import domain_whois, check_dns_records

def test_domain_whois():
    result = domain_whois("example.com")
    assert 'registrar' in result
    assert isinstance(result.get('name_servers', []), list)

def test_dns_records():
    result = check_dns_records("google.com")
    assert 'A' in result
    assert len(result['A']) > 0