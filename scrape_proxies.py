import csv
import concurrent.futures
import check_proxy as c
import requests
import re
import argparse
proxies_result={}
def handle_proxy_check(proxy):
    # handler function to write to csv every 10 proxies tested
    r=c.check_proxy_url(proxy_url=proxy)
    proxies_result[proxy]=r
    if(len(proxies_result)%10==0):
        write_to_csv(proxies_result)

def test_proxies(proxy_list):
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Use submit to schedule the check_proxy function for each proxy in the list
        futures = {executor.submit(handle_proxy_check, proxy): proxy for proxy in proxy_list}
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)
        # for f in futures:
        #     proxy, status = f.result()
        #     proxies[proxy] = status

def get_proxies(url):
    r = requests.get(url)
    match_string = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]+\b'
    match_pattern = re.compile(match_string)
    proxies = match_pattern.findall(r.text)
    return proxies

def write_to_csv(proxies, filename="out.csv"):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Proxy', 'Status'])
        for proxy in proxies:
            csvwriter.writerow([proxy, proxies[proxy]])

def main():
    parser = argparse.ArgumentParser(description='Proxy Tester with Command Line Interface')
    parser.add_argument('-u', '--url', help='URL to scrape proxies from (default: https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt)', default='https://github.com/TheSpeedX/PROXY-List/blob/master/http.txt')
    parser.add_argument('-t', '--threads', help='Number of concurrent threads to use (default: 10)', default=10, type=int)
    # parser.add_argument('-o', '--output', help='Output CSV file name (default: proxies.csv)', default='proxies.csv')
    args = parser.parse_args()
    proxies = get_proxies(args.url)
    test_proxies(proxies)
    write_to_csv(proxies)

if __name__ == '__main__':
    main()