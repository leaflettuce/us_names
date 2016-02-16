from pymongo import MongoClient
import matplotlib.pyplot as plt
import pprint
client = MongoClient('localhost:27017')
db = client['babyNames']
names= db.stateNames


#prep code

#search for state names (used to create states.txt file)
## DO NOT UN-COMMENT
# states = []
# file = open('states.txt','w')
#
# for row in names.find():
#     if row['State'] not in states:
#         states.append(row['State'])
#
# for state in states:
#     file.write("%s\n" % state)
# file.close()


#Pipelines

#overall
def topOverallNames():
    pprint.pprint(names.aggregate([{"$group":{"_id":"$Name",
                                "count":{"$sum": '$Count'}}},
                                { "$sort":{"count":-1}},
                                {'$limit': 10}]))
#top male
def topMaleNames():
    pprint.pprint(names.aggregate([{'$match': {'Gender' : 'M'}},
                                 {"$group":{"_id":"$Name",
                                "count":{"$sum":'$Count'}}},
                                { "$sort":{"count":-1}},
                                {'$limit': 10}]))
#top Female
def topFemaleNames():
    pprint.pprint(names.aggregate([{'$match': {'Gender' : 'F'}},
                                {"$group":{"_id":"$Name",
                                "count":{"$sum":'$Count'}}},
                                { "$sort":{"count":-1}},
                                {'$limit': 10}]))
#top by state
def getStateNames():
    states = open('states.txt', 'r')
    for state in states:
        state = state.replace('\n', '')
        print '--' + state + '--'
        pprint.pprint(names.aggregate([{'$match': {'State' : state}},
                                {"$group":{"_id":"$Name",
                                "count":{"$sum":'$Count'}}},
                                { "$sort":{"count":-1}},
                                {'$limit': 3}]))


def queryUser():
    while True:
        initial = raw_input('Name or State or Year? ').lower()

        if initial == 'name':
            userQueryNames()
            break
        elif initial == 'state':
            userQueryStates()
            break
        elif initial == 'year':
            userQueryYears()
            break
        else:
            print 'Input Invalid... Try Again!'

def goAgain():
    more = raw_input('Browse more?  "y" or "n"').lower()
    if more == 'y': queryUser()
    else : quit()

def userQueryNames():
    name = raw_input('What name do you want to explore?').capitalize()


    print 'total %s\'s born since 1910.. ' %name
    print names.aggregate([{'$match' : {'Name' : name}},
                          {'$group' : {'_id' : 0,
                                       'total' : {'$sum' : '$Count'}}},
                           {'$project' : {'_id' : 0,
                                          'total' : '$total'}}])

    print 'Top 5 States for this Name.. '
    pprint.pprint(names.aggregate([{'$match' : {'Name' : name}},
                                    {'$group' : {'_id' : '$State',
                                                "count":{"$sum":'$Count'}}},
                                   {'$sort' : {'count' : -1}},
                                   {'$limit' : 5}]))

    print '\n \n Top 5 Years for this Name.. '
    pprint.pprint(names.aggregate([{'$match' : {'Name' : name}},
                                    {'$group' : {'_id' : '$Year',
                                                "count":{"$sum":'$Count'}}},
                                   {'$sort' : {'count' : -1}},
                                   {'$limit' : 5}]))
    goAgain()

def userQueryStates():
    state = raw_input('What state do you want to explore?').upper()

    print 'Top 5 Names for this State.. '
    pprint.pprint(names.aggregate([{'$match' : {'State' : state}},
                                    {'$group' : {'_id' : '$Name',
                                                "count":{"$sum":'$Count'}}},
                                   {'$sort' : {'count' : -1}},
                                   {'$limit' : 5}]))
    goAgain()

def userQueryYears():
    year = int(raw_input('What year do you want to explore?'))

    print 'Top 5 Names for this Year.. '
    pprint.pprint(names.aggregate([{'$match' : {'Year' : year}},
                                    {'$group' : {'_id' : '$Name',
                                                "count":{"$sum":'$Count'}}},
                                   {'$sort' : {'count' : -1}},
                                   {'$limit' : 5}]))
    goAgain()


#output
# print '--------top 10 names---------'
# topOverallNames()
# print '--------top 10 Male names---------'
# topMaleNames()
# print '--------top 10 Female names---------'
# topFemaleNames()
#print '--------top Name per State---------'
#getStateNames()

queryUser()