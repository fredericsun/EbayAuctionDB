# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 23:15:50 2017

@author: Hao Yuan, Zhaoyin Qin, Yue Sun
"""

"""
REFERENCE FILE: skeleton_parser.py
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
MONTHS = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
          'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

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

'''# Yue
def removeDuplicates(somelist):
    # Your codes below
    pre_contain = []
    for i in range(len(somelist)):
        if somelist[i][0] in pre_contain:
            somelist.remove(somelist[i])
        pre_contain.append(somelist[i][0])
    return somelist'''


# Hao
def saveAsDat(somelist, filename):
    with open(filename, "a") as f:
        f.writelines("\n".join(somelist))


# Yue
class Item:
    # Your codes below
    def __init__(self, ItemID, Name, Seller_ID, Buy_Price, Currently,
                 First_Bid, Number_of_Bids, Started, Ends, Description):
        self.ItemID = ItemID
        self.Name = Name
        self.Seller_ID = Seller_ID
        self.Buy_Price = Buy_Price
        self.Currently = Currently
        self.First_Bid = First_Bid
        self.Number_of_Bids = Number_of_Bids
        self.Started = Started
        self.Ends = Ends
        self.Description = Description

    def getProperty(self, index):
        if index == 0:
            return self.ItemID
        if index == 1:
            return self.Name
        if index == 2:
            return self.Seller_ID
        if index == 3:
            return self.Buy_Price
        if index == 4:
            return self.Currently
        if index == 5:
            return self.First_Bid
        if index == 6:
            return self.Number_of_Bids
        if index == 7:
            return self.Started
        if index == 8:
            return self.Ends
        if index == 9:
            return self.Description



# Yue
def writeItemTable(ItemList, filename):
    # Your codes below
    Item_output = []
    for i in range(len(ItemList)):
        element = []
        for j in range(10):
            element.append(ItemList[i].getProperty(j) + '|')
        Item_output.append(element)
    # Call removeDuplicates, and saveAsDat methods below
    saveAsDat(Item_output, filename)


# Yue
class Bids:
    # Your codes below
    def __init__(self, ItemID, BidderID, Time, Amount):
        self.ItemID = ItemID
        self.BidderID = BidderID
        self.Time = Time
        self.Amount = Amount

    def getProperty(self, index):
        if index == 0:
            return self.BidderID
        if index == 1:
            return self.ItemID
        if index == 2:
            return self.Time
        if index == 3:
            return self.Amount

# Yue
def writeBidTable(BidList, filename):
    # Your codes below
    Item_output = []
    for i in range(len(BidList)):
        element = []
        for j in range(4):
            element.append(BidList[i].getProperty(j) + '|')
        Item_output.append(element)
    # Call removeDuplicates, and saveAsDat methods below
    saveAsDat(Item_output, filename)


# Hao
def writeCategoryTable(CategoryList, filename):
    saveAsDat(CategoryList, filename)


# Hao
def writeItemCatTable(ItemCatList, filename):
    saveAsDat(ItemCatList, filename)


# Zhaoyin
class User:
    # Your codes below
    def __init__(self, id, rating):
        self.id = id
        self.rating = rating
        self.location = None
        self.country = None


# Zhaoyin
def writeUserTable(UserList, filename):
    # Your codes below
    user_dat = []
    # Your codes below
    for user in UserList:
        dat = str(user.id) + "|" + str(user.rating) + "|" + user.location + \
              user.country
        user_dat.append(dat)
    # removeDuplicates(user_dat)
    saveAsDat(user_dat, filename)

# Yue, Hao, Zhaoyin
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
            #buy_price = transformDollar(item[u'Buy_Price'])
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
                my_item = Item(item_id, item_name, seller_id, transformDollar(item[u'Buy_Price']),
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
        writeItemTable(ItemList, "ItemTable.dat")
        writeBidTable(BidList, "BidTable.dat")
        writeCategoryTable(CategoryList, "CategoryTable.dat")
        writeItemCatTable(ItemCatList, "ItemCategoryTable.dat")
        writeUserTable(UserList, "UserTable.dat")

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
