import re
import pymongo


class Analysis(object):

    def __init__(self, MONGO_DB):
        self.MONGO_CLIENT = pymongo.MongoClient('localhost', 27017)
        self.db = self.MONGO_CLIENT[MONGO_DB]
        self.COLLECTIONS_LIST = self.db.list_collection_names(session=None)
        self.ROOMS = 1

    def get_info(self):
        for region in self.COLLECTIONS_LIST:
            if len(region) > 2 or region in ['白云', '黄埔', '萝岗']:
                continue
            collection = self.db[region]
            cursor = collection.find({'traffic': re.compile('距[123568]?号线'),
                                      'rooms': re.compile(str(self.ROOMS)+'室1厅'),
                                      'price': {'$lte': 1200 * self.ROOMS}})
            print(region, ':', cursor.count())
            for item in cursor:
                print(item)


if __name__ == '__main__':
    a = Analysis('ZuFang')
    a.get_info()







