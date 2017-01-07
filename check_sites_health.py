import requests, whois, sys
from datetime import datetime, timedelta
from urllib.parse import urlparse

def load_urls4check(filepath):
    with open(filepath) as file_with_urls:
        urls = file_with_urls.read().split()
    return urls


def get_domain_name_from_url(url):
    return urlparse(url).netloc


def is_server_respond_with_200(url):
    status_ok = 200
    response = requests.head(url, allow_redirects=True)

    return status_ok == response.status_code


def get_domain_expiration_date(domain_name):
    whois_response = whois.query(domain_name)
    return(whois_response.expiration_date)
    

def is_close_to_expire(date):
    days_in_exp_offset = 31
    today = datetime.today()
    expiration_offset = timedelta(days=days_in_exp_offset)
    return expiration_offset > date - today


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Set path to file with list of URLs")
        exit(1)

    for url in load_urls4check(sys.argv[1]):
        status_ok = is_server_respond_with_200(url)

        domain_name = get_domain_name_from_url(url)
        domain_expiration_date = get_domain_expiration_date(domain_name)

        close_to_expire = is_close_to_expire(domain_expiration_date) if domain_expiration_date is not None else True

        print("URL: {}\nclose to expire: {}\nresponse 200: {}\n".format(url, close_to_expire, status_ok))
