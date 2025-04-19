# OmniSentry

<div align="center">
    <img src="https://img.shields.io/badge/Python-3.6+-blue.svg" alt="Python 3.6+">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
</div>

## 📊 Overview

OmniSentry is a comprehensive OSINT (Open Source Intelligence) command-line tool designed to streamline intelligence gathering on various digital entities. It provides structured data about emails, domains, social media accounts, and phone numbers through a unified interface.

## ✨ Key Features

- **Email Intelligence**: Validate email addresses, detect disposable emails, and check for data breaches
- **Domain Analysis**: Collect domain WHOIS information, DNS records, and subdomain enumeration
- **Social Media Reconnaissance**: Check username existence across multiple platforms (Twitter, GitHub, Instagram, Reddit, Medium, Keybase)
- **Phone Number Verification**: Validate international phone numbers, identify carriers, and obtain geolocation data
- **Flexible Output**: Display results in either formatted tables or structured JSON

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/abdorhl/OmniSsentry.git
cd omnissentry

# Install the package
pip install -e .
```

## ⚙️ Configuration

Create a `.env` file in the root directory with your API keys. OmniSentry leverages multiple APIs to enhance its capabilities:

```
# API Configuration
HUNTER_API_KEY=your_hunter_api_key        # Email verification (https://hunter.io/api)
HAVEI_BEEN_PWNED_API=your_hibp_api_key    # Data breach checking (https://haveibeenpwned.com/API)
VIRUSTOTAL_API=your_virustotal_api_key    # Domain analysis (https://www.virustotal.com)
NUMVERIFY_API=your_numverify_api_key      # Phone validation (https://numverify.com)
```

> **Note**: OmniSentry provides basic functionality even without API keys, but enhanced features require valid keys.

## 📖 Usage

### Email Investigation

```bash
# Basic email analysis
omnissentry email user@example.com

# Output in JSON format
omnissentry email user@example.com -f json
```

### Social Media Analysis

```bash
# Search for username across platforms
omnissentry social johndoe

# With JSON output
omnissentry social johndoe -f json
```

### Domain Intelligence

```bash
# Basic domain information
omnissentry domain example.com

# With subdomain enumeration and DNS records
omnissentry domain example.com --subdomains --dns
```

### Phone Number Analysis

```bash
# Phone number validation and carrier information
omnissentry phone +14155552671
```

## 📋 Output Examples

### Email Analysis (Table Format)
```
+---------------+-----------------------------------+
| Key           | Value                             |
+===============+===================================+
| hunter        | {"result": "deliverable", ...}    |
| breaches      | {"count": 3, "names": [...]}      |
+---------------+-----------------------------------+
```

### Social Media (JSON Format)
```json
{
  "twitter": {
    "url": "https://twitter.com/username",
    "exists": true,
    "status_code": 200
  },
  "github": {
    "url": "https://github.com/username",
    "exists": true,
    "status_code": 200
  },
  ...
}
```

## 🧪 Testing

Run the test suite to verify functionality:

```bash
pytest
```

## 📚 API Reference

OmniSentry uses the following external APIs:

- [Hunter.io](https://hunter.io/api) - Email verification (25 searches/month free)
- [HaveIBeenPwned](https://haveibeenpwned.com/API) - Data breach checking (paid API)
- [VirusTotal](https://developers.virustotal.com) - Domain intelligence (free tier available)
- [Numverify](https://numverify.com/) - Phone validation (250 requests/month free)

## 🔒 Privacy & Ethics

OmniSentry is designed for legitimate security research, penetration testing, and personal data management. Users must:

- Obtain proper authorization before investigating targets
- Comply with all applicable laws and regulations
- Respect privacy and use the tool responsibly

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
