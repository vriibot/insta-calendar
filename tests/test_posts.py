from eventminer import posts
import datetime

currentYear = datetime.datetime.now().year

def test_parse_date():

    #expected results table
    tests = {
        "1st": None,
        '19:00/19:30': None,
        '21:45-22:15': None,
        "2025.7.1": datetime.datetime(2025, 7, 1),
        '2025.6.13.Fri': datetime.datetime(2025, 6, 13, 0, 0),
        '7/19': datetime.datetime(currentYear, 7, 19, 0, 0),
        '22.HARD': None,
        '2MAN': None,
        '+1drink': None,
        '20250501': None, 
        '7月21日': datetime.datetime(currentYear, 7, 21, 0, 0),
        #27th june
        #june 27th
    }

    for t in tests:
        assert posts.__parse_date(t) == tests[t]