# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 23:15:50 2017

@author: Hao Yuan
"""

"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = dict(Jan='01', Feb='02', Mar='03', Apr='04', May='05', Jun='06',
              Jul='07', Aug='08', Sep='09', Oct='10', Nov='11', Dec='12')

"""
Returns true if a file ends in .json
"""


def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'


"""
Converts month to a number, e.g. 'Dec' to '12'
"""


def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon


"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""


def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]


"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""


def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""


# Hao
def removeDuplicates(somelist):
    # Your codes below
    return


# Hao
def saveAsDat(somelist, filename):
    # Your codes below
    return


# Yue
class Item():
    def __init__(self, item_id, name, seller_id, price, current, first_bid,
                 num_of_bid, start, end, description):
        return

def writeItemTable(ItemList):
    # Your codes below

    # Call removeDuplicates, and saveAsDat methods below
    return


# Yue
class Bids():
    def __init__(self, item_id, bidder_id,time, amount):
        return

def writeBidTable(BidList):
    # Your codes below

    # Call removeDuplicates, and saveAsDat methods below
    return


# Hao
def writeCategoryTable(CategoryList):
    # Your codes below
    return


# Hao
def writeItemCatTable(ItemCatList):
    # Your codes below

    # Call removeDuplicates, and saveAsDat methods below
    return


# Zhaoyin
class User():
    '''Represent a user.'''

    def __init__(self, id, rating):
        self.id = id
        self.rating = rating
        self.location = None
        self.country = None


# Zhaoyin
def writeUserTable(UserList):
    user_dat = []
    # Your codes below
    for user in UserList:
        dat = str(user.id) + "|" + str(user.rating) + "|" + user.location + \
              user.country
        user_dat.append(dat)
    # Call removeDuplicates, and saveAsDat methods below
    # removeDuplicates(user_dat)
    saveAsDat(user_dat, 'user.dat')


def parseJson(json_file):
    ItemList = []
    BidList = []
    UserList = []
    CategoryList = []
    ItemCatList = []
    with open(json_file, 'r') as f:
        items = loads(f.read())[
            'Items']  # creates a Python dictionary of Items for the supplied json file
        for item in items:
            # Collect info needed for object constructors below
            # i.e. ItemID = item[u'Item_ID']
            ############################
            item_id = item[u'Item_ID']
            item_name = item[u'Name']
            seller_id = item[u'Seller'][u'UserID']
            buy_price = transformDollar(item[u'Buy_Price'])
            currently = transformDollar(item[u'Currently'])
            first_bid = transformDollar(item[u'First_Bid'])
            number_of_bids = item[u'Number_of_Bids']
            started = transformDttm(item[u'Started'])
            end = transformDttm(item[u'End'])
            description = item[u'Description']
            ############################

            ############################
            # Item Object Initialization
            if len(item) == 14:
                # Item Object with no Buy_Price
                my_item = Item(item_id, item_name, seller_id, buy_price,
                               currently,
                               first_bid, number_of_bids, started, end,
                               description)
            else:
                # Item Object with Buy_Price
                my_item = Item(item_id, item_name, seller_id, None, currently,
                               first_bid, number_of_bids, started, end,
                               description)
            # Add created object to corresponding list
            ItemList.append(my_item)
            ############################

            ############################
            # Bids Object Initialization
            if item[u'Bids'] is not None:
                for bids in item[u'Bids']:
                    keys = bids[u'Bid'][u'Bidder'].keys()
                    bidder = bids[u'Bid'][u'Bidder']

                    BidderID = bids[u'Bid'][u'Bidder'][u'UserID']
                    Time = transformDttm(bids[u'Bid'][u'Time'])
                    Amount = transformDollar(bids[u'Bid'][u'Amount'])
                    my_bids = Bids(item[u'Item_ID'], BidderID, Time, Amount)
                    # Add created object to corresponding list
                    BidList.append(my_bids)

                    user = User(BidderID, bidder[u'Rating'])
                    if 'Location' in keys:
                        user.location = bidder[u'Location']
                    if 'Country' in keys:
                        user.country = bidder[u'Country']
                    UserList.append(user)


            user = (seller_id, item[u'Seller'][u'Rating'], item[u'Location'],
                    item[u'Country'])
            UserList.append(user)

            ############################

            ############################
            # Prepare category list and itemcat list
            jsonItemCat = []
            jsonItemCat = item[u'Category']
            if jsonItemCat != None:
                for cat in jsonItemCat:
                    itemcat = item_id + "|" + cat
                    ItemCatList.append(itemcat)
                    if cat not in CategoryList:
                        CategoryList.append(cat)



        # Call writer methods here
        # i.e. writeUserTable(UserList)
        writeItemTable(ItemList)
        writeBidTable(BidList)
        writeCategoryTable(CategoryList)
        writeItemCatTable(ItemCatList)
        writeUserTable(UserList)



"""
Loops through each json files provided on the command line and passes each file
to the parser
"""


def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f


if __name__ == '__main__':
    main(sys.argv)

