import urllib.request
import ssl
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

def get_description(html_str: str):
    # Find the relevant part
    # description = html_str.find('property_description_content')
    soup = BeautifulSoup(html_str, 'html.parser')
    description = soup.find(id='property_description_content').text
    # Now remove the first line if it has Genius
    'div.js-k2-hp--block.k2-hp--popular_facilities'
    a = soup.find_all('div', {'class': 'js-k2-hp--block k2-hp--popular_facilities'})
    facilities = a[0].text
    # Check that a is not empty
    # url2 = 'https://www.booking.com/reviewlist.html'
    # req = requests.get(url2, verify=False, params={'cc1': 'us', 'dist': '1', 'pagename': 'park-lane-new-york'})
    # url1 = 'https://www.booking.com/reviewlist.html?cc1=us;dist=1;pagename=park-lane-new-york;'
    # req = requests.get(url1, verify=False)
    # soup = BeautifulSoup(req.content, 'html.parser')

    return description, facilities


def get_name_from_url(hotel_url):
    """
    Get hotel name from the url
    :param hotel_url:
    :return:
    """
    last_slash = hotel_url.rfind('/')
    hotel_name = hotel_url[last_slash + 1:last_slash + hotel_url[last_slash + 1:].find('.') + 1]
    return hotel_name

def get_reviews(hotel_url):
    # find the last /
    name = get_name_from_url(hotel_url)
    review_url = 'https://www.booking.com/reviewlist.html'
    browser = webdriver.Chrome()
    time.sleep(10)
    # maximum 2000 reviews
    review_url = review_url + '?cc1=us;dist=1;pagename=' + name + ';type=total&&'
    all_reviews = []
    for k in range(20):
        # build the link
        get_url = review_url + 'offset=' + str(k*100) + ';rows=100'
        browser.get(get_url)
        # html = browser.page_source
        reviews = BeautifulSoup(browser.page_source, 'html.parser').text
        # Check is there is new text or not
        pass
        if reviews.find('Reviewed') == -1:
            break
        else:
            all_reviews.append(reviews)

    return all_reviews

def parse_hotel_by_url(hotel_url):
    """
    :param hotel_url: the url of a hotel in booking.com
    :return: the description, address, and reviews of the hotel.
    TODO: images
    """
    # Prevent firewall verification problem
    ssl._create_default_https_context = ssl._create_unverified_context

    request = urllib.request.Request(hotel_url)
    try:
        response = urllib.request.urlopen(request)
    except:
        print("URL is not working")

    html_bytes = response.read()
    html_str = html_bytes.decode("utf8")
    description, facilities = get_description(html_str)

    # Get the reviews
    get_reviews(hotel_url)

    # req = requests.get(url2, verify=False, params={'cc1': 'us', 'dist': '1', 'pagename': 'park-lane-new-york'})
    # fp = urllib.request.urlopen(hotel_url)

    pass