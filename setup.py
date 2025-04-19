from setuptools import setup, find_packages

setup(
    name="omnissentry",
    version="0.1.0",
    description="Comprehensive OSINT Tool",
    author="OmniSentry Team",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.26.0",
        "beautifulsoup4>=4.10.0",
        "python-dotenv>=0.19.0",
        "argparse>=1.4.0",
        "whois>=0.9.5",
        "ratelimit>=2.2.1",
        "phonenumbers>=8.12.0",
        "tabulate>=0.8.9",
        "dnspython>=2.1.0",
    ],
    entry_points={
        "console_scripts": [
            "omnissentry=omnissentry.cli:main",
        ],
    },
    python_requires=">=3.6",
)
