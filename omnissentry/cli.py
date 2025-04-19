import argparse
import json
from tabulate import tabulate
from .core import (
    email_osint_full,
    social_media_scrape,
    domain_whois,
    domain_subdomains,
    check_dns_records,
    phone_osint
)

class OutputFormatter:
    @staticmethod
    def print_json(data):
        print(json.dumps(data, indent=2))
    
    @staticmethod
    def truncate_value(value, max_length=70):
        """Truncate long values to make tables readable"""
        if isinstance(value, (dict, list)):
            # Convert to compact JSON with limited width
            value_str = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
            if len(value_str) > max_length:
                return value_str[:max_length-3] + "..."
            return value_str
        else:
            value_str = str(value)
            if len(value_str) > max_length:
                return value_str[:max_length-3] + "..."
            return value_str
    
    @staticmethod
    def print_table(data):
        if isinstance(data, dict):
            # Format dictionary values to be more readable
            table = []
            for k, v in data.items():
                table.append([k, OutputFormatter.truncate_value(v)])
            print(tabulate(table, headers=["Key", "Value"], tablefmt="grid"))
        
        elif isinstance(data, list):
            if data and isinstance(data[0], dict):
                # For lists of dictionaries, truncate each field value
                processed_data = []
                for item in data:
                    processed_item = {}
                    for k, v in item.items():
                        processed_item[k] = OutputFormatter.truncate_value(v)
                    processed_data.append(processed_item)
                print(tabulate(processed_data, headers="keys", tablefmt="grid"))
            else:
                # Simple list
                print(tabulate([[OutputFormatter.truncate_value(i)] for i in data], 
                              headers=["Value"], tablefmt="grid"))
    
    @staticmethod
    def format(data, fmt='json'):
        if fmt == 'json':
            OutputFormatter.print_json(data)
        else:
            OutputFormatter.print_table(data)

def main():
    # Create a parent parser with common arguments
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("-f", "--format", choices=["json", "table"], default="table",
                          help="Output format (default: table)")
    
    # Create the main parser
    parser = argparse.ArgumentParser(description="OmniSentry - Comprehensive OSINT Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Email command
    email_parser = subparsers.add_parser("email", help="Email investigation", parents=[parent_parser])
    email_parser.add_argument("email", help="Email address to investigate")
    
    # Social media command
    social_parser = subparsers.add_parser("social", help="Social media search", parents=[parent_parser])
    social_parser.add_argument("username", help="Username to search")
    
    # Domain command
    domain_parser = subparsers.add_parser("domain", help="Domain investigation", parents=[parent_parser])
    domain_parser.add_argument("domain", help="Domain name to investigate")
    domain_parser.add_argument("--subdomains", action="store_true", help="Find subdomains")
    domain_parser.add_argument("--dns", action="store_true", help="Check DNS records")
    
    # Phone command
    phone_parser = subparsers.add_parser("phone", help="Phone number analysis", parents=[parent_parser])
    phone_parser.add_argument("number", help="Phone number to investigate")
    
    args = parser.parse_args()
    
    try:
        if args.command == "email":
            result = email_osint_full(args.email)
        elif args.command == "social":
            result = social_media_scrape(args.username)
        elif args.command == "domain":
            result = domain_whois(args.domain)
            if args.subdomains:
                result['subdomains'] = domain_subdomains(args.domain)
            if args.dns:
                result['dns'] = check_dns_records(args.domain)
        elif args.command == "phone":
            result = phone_osint(args.number)
        else:
            parser.print_help()
            return
        
        OutputFormatter.format(result, args.format)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()