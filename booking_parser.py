import urllib.request
import ssl
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pickle

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

def filter_facilities(facilities):
    facilities = [f for f in facilities.split('\n') if f != '']
    return facilities

def filter_description(description):
    description = [f for f in description.split('\n') if f != '' and 'Genius' not in f]
    return description

def month_in_sent(sent):
    if 'January' in sent or 'February' in sent or 'March' in sent or 'April' in sent or 'May' in sent or 'June' in \
            sent or 'July' in sent or 'August' in sent or 'September' in sent or 'October' in sent or 'November' in \
            sent or 'December' in sent:
        return True
    return False

def filter_reviews(all_reviews):

    saved_reviews = []
    for review_list in all_reviews:
        reviews = [r for r in review_list.split('\n') if r != '']
        # Go over everything and find the start and the end of every review
        state = 'init'
        where_from = ''
        who = ''
        summary = ''
        grade = 0
        liked = ''
        disliked = ''
        when = ''
        for k, sent in enumerate(reviews):
            if state == 'init':
                if month_in_sent(sent) and 'Reviewed' in sent:
                    state = 'start'
                    step_back = 0
                    if 'Reviewers' in reviews[k - 1]:
                        step_back = 1
                    where_from = reviews[k - 5 - step_back]
                    summary = reviews[k + 1]
                    who = reviews[k - 1 - step_back]
                    when = sent.replace('Reviewed: ', '')
            elif state == 'start':
                if month_in_sent(sent) and 'Reviewed' in sent:
                    saved_reviews.append([when, who, where_from, summary, grade, liked, disliked])
                    step_back = 0
                    if 'Reviewers' in reviews[k - 1]:
                        step_back = 1
                    where_from = reviews[k - 5 - step_back]
                    summary = reviews[k + 1]
                    who = reviews[k - 1 - step_back]
                    when = sent.replace('Reviewed: ', '')
                elif sent.replace(' ', '').isnumeric():
                    grade = int(sent.replace(' ', ''))
                elif 'Liked \xa0·\xa0' in sent:
                    liked = sent.replace('Liked \xa0·\xa0', '')
                elif 'Disliked \xa0·\xa0' in sent:
                    disliked = sent.replace('Disliked \xa0·\xa0', '')

        if len(saved_reviews) > 0:
            if saved_reviews[-1][0] != when and saved_reviews[-1][1] != who and saved_reviews[-1][2] != where_from and \
                    saved_reviews[-1][3] != summary and saved_reviews[-1][4] != grade and saved_reviews[-1][5] != liked and \
                    saved_reviews[-1][6] != disliked:
                saved_reviews.append([when, who, where_from, summary, grade, liked, disliked])
    return saved_reviews


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
        return None, None, None

    html_bytes = response.read()
    html_str = html_bytes.decode("utf8")
    description, facilities = get_description(html_str)

    # Get the reviews
    all_reviews = get_reviews(hotel_url)

    # with open('/Users/michaelko/Data/askforhotel/example.pkl', 'wb') as dump_f:
    #     pickle.dump([description, facilities, all_reviews], dump_f)

    # req = requests.get(url2, verify=False, params={'cc1': 'us', 'dist': '1', 'pagename': 'park-lane-new-york'})
    # fp = urllib.request.urlopen(hotel_url)

    facilities = filter_facilities(facilities)
    description = filter_description(description)
    all_reviews = filter_reviews(all_reviews)

    return description, facilities, all_reviews

if __name__ == '__main__':
    print('Start filtering')

    with open('/Users/michaelko/Data/askforhotel/example.pkl', 'rb') as dump_f:
        description, facilities, all_reviews = pickle.load(dump_f)

    facilities = filter_facilities(facilities)
    description = filter_description(description)
    all_reviews = filter_reviews(all_reviews)
    pass