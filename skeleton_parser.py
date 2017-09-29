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

# Hao
def removeDuplicates(somelist):
    # Your codes below
    pre_contain = []
    for i in range(len(somelist)):
        if somelist[i][0] in pre_contain:
            somelist.remove(somelist[i])
        pre_contain.append(somelist[i][0])
    return somelist


# Hao
def saveAsDat(somelist):
    # Your codes below
    return


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
def writeItemTable(ItemList):
    # Your codes below
    Item_output = []
    for i in range(len(ItemList)):
        element = []
        for j in range(10):
            element.append(ItemList[i].getProperty(j) + '|')
        Item_output.append(element)
    # Call removeDuplicates, and saveAsDat methods below
    return removeDuplicates(Item_output)


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

# Hao
def writeBidTable(BidList):
    # Your codes below
    Item_output = []
    for i in range(len(BidList)):
        element = []
        for j in range(4):
            element.append(BidList[i].getProperty(j) + '|')
        Item_output.append(element)
    # Call removeDuplicates, and saveAsDat methods below
    return removeDuplicates(Item_output)


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
class User:
    # Your codes below
    def __init__(self, UserID, Rating, Location, Country):
    return


# Zhaoyin
def writeUserTable(UserList):
    # Your codes below

    # Call removeDuplicates, and saveAsDat methods below
    return


def parseJson(json_file):
    ItemList = []
    BidList = []
    UserList = []
    CategoryList = []
    ItemCatList = []
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items']  # creates a Python dictionary of Items for the supplied json file
        for item in items:
            # Collect info needed for object constructors below
            # i.e. ItemID = item[u'Item_ID']

            ############################
            # Item Object Initialization
            if len(item) == 14:
                #Item Object with no Buy_Price
                my_item = Item(item[u'Item_ID'], item[u'Name'], item[u'Seller'][u'UserID'], transformDollar(item[u'Buy_Price']), transformDollar(item[u'Currently']),
                            transformDollar(item[u'First_Bid']), item[u'Number_of_Bids'], transformDttm(item[u'Started']), transformDttm(item[u'End']), item[u'Description'])
            else:
                #Item Object with Buy_Price
                my_item = Item(item[u'Item_ID'], item[u'Name'], item[u'Seller'][0][u'UserID'], None, transformDollar(item[u'Currently']),
                            transformDollar(item[u'First_Bid']), item[u'Number_of_Bids'], transformDttm(item[u'Started']), transformDttm(item[u'End']), item[u'Description'])
            # Add created object to corresponding list
            ItemList.append(my_item)
            ############################

            ############################
            # Bids Object Initialization
            if item[u'Bids'] is not None:
                for bids in item[u'Bids']:
                    BidderID = bids[u'Bid'][u'Bidder'][u'UserID']
                    Time = transformDttm(bids[u'Bid'][u'Time'])
                    Amount = transformDollar(bids[u'Bid'][u'Amount'])
                    my_bids = Bids(item[u'Item_ID'], BidderID, Time, Amount)
                    # Add created object to corresponding list
                    BidList.append(my_bids)
            ############################

    # Call writer methods here
    # i.e. writeUserTable(UserList)
    writeItemTable(ItemList)
    writeBidTable(BidList)


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
