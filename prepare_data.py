from booking_parser import parse_hotel_by_url
import pickle

def prepare_data():
    # hotel_url = 'https://www.booking.com/hotel/us/park-lane-new-york.en-gb.html'
    # hotel_url = 'https://www.booking.com/reviewlist.html?cc1=us;dist=1;pagename=park-lane-new-york;type=total&&offset=1;rows=2'
    # parse_hotel_by_url(hotel_url)


    full_data = []

    file_hotels = open('/Users/michaelko/Desktop/hotelstxt.txt', 'r')
    hotel_names = file_hotels.readlines()
    for k, hotel_url in enumerate(hotel_names):
        if k <= 375:
            continue
        if 'searchresults' in hotel_url:
            continue
        description, facilities, all_reviews = parse_hotel_by_url(hotel_url[hotel_url.find('http'):].replace('\n', ''))
        if description is not None:
            full_data.append([description, facilities, all_reviews, hotel_url])
        if k % 25 == 0 and k > 0:
            print('Running hotel ', k)
            with open('/Users/michaelko/Data/askforhotel/new_york_375.pkl', 'wb') as dump_f:
                pickle.dump(full_data, dump_f)

    with open('/Users/michaelko/Data/askforhotel/new_york_final.pkl', 'wb') as dump_f:
        pickle.dump(full_data, dump_f)

def unite_several_files():
    with open('/Users/michaelko/Data/askforhotel/new_york.pkl', 'rb') as dump_f:
        data1 = pickle.load(dump_f)

    with open('/Users/michaelko/Data/askforhotel/new_york_final.pkl', 'rb') as dump_f1:
        data2 = pickle.load(dump_f1)

    pass

    data1 = data1 + data2

    with open('/Users/michaelko/Data/askforhotel/new_york_last.pkl', 'wb') as dump_f2:
        pickle.dump(data1, dump_f2)

if __name__ == '__main__':
    print('Start processing')
    unite_several_files()
    prepare_data()