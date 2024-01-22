# import urllib3
import requests

def check_proxy_url(proxy_url):
    """
    Checks the validity of a proxy URL by attempting to establish a connection to a specified website using the provided proxy.

    Args:
        proxy_url (str): The proxy URL to check.

    Returns:
        bool: True if the proxy URL is valid, False otherwise.
    """

    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    try:
        response = requests.get('https://www.example.com', proxies=proxies, timeout=5)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        # Log the error message
        # print(f"Proxy check failed for {proxy_url}: {e}")
        return False

    return True