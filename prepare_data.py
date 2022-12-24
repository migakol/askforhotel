from booking_parser import parse_hotel_by_url


def prepare_data():
    hotel_url = 'https://www.booking.com/hotel/us/park-lane-new-york.en-gb.html'
    # hotel_url = 'https://www.booking.com/reviewlist.html?cc1=us;dist=1;pagename=park-lane-new-york;type=total&&offset=1;rows=2'
    parse_hotel_by_url(hotel_url)

if __name__ == '__main__':
    print('Start processing')
    prepare_data()