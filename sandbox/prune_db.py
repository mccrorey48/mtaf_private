from pymongo import MongoClient
# import lib.logging_esi as logging
import argparse
from os import getenv
from time import strptime
import datetime

# log = logging.get_logger('esi.run_features')


def prune_db(db_name, server, operation, number_to_keep, max_age):
    print 'pruning %s on server %s to latest %d test runs' % (db_name, server, number_to_keep)
    client = MongoClient(server)
    db = client[db_name]
    # configs = db['test_starts'].distinct('configuration')
    # dates = db['test_starts'].distinct('date')
    starts = db['test_starts'].find({}, {'date': 1, 'time': 1, 'configuration': 1})
    starts_by_cfg={}
    now = datetime.datetime.now()
    for start in starts:
        timestamp = '%s-%s' % (start['date'], start['time'])
        dt = datetime.datetime.strptime(timestamp, "%m/%d/%y-%H:%M:%S")
        age = now - dt
        days = age.total_seconds() / datetime.timedelta(1).total_seconds()
        cfg = start['configuration']
        _id = start['_id']
        d = {'_id': _id, 'timestamp': timestamp, 'cfg': cfg, 'days': days}
        if cfg in starts_by_cfg:
            starts_by_cfg[cfg].append(d)
        else:
            starts_by_cfg[cfg] = [d]
    for cfg in starts_by_cfg:
        print '%s:' % cfg
        for i, d in enumerate(sorted(starts_by_cfg[cfg], key=lambda x: x['days'], reverse=False)):
            if operation=='list':
                print d,
                if i >= number_to_keep:
                    print 'N',
                if d['days'] > max_age:
                    print "A",
                print
            elif operation=='prune' and (i >= number_to_keep or d['days'] > max_age):
                db['test_starts'].delete_one({'_id': d['_id']})
                db['features'].delete_many({'_id': d['_id']})
    # for config in  configs:
    #     print "%2d  %s" % (db['test_starts'].count({"configuration": config}), config)
    # now = datetime.datetime.now()
    # for date in sorted(dates, key=lambda x: datetime.datetime.strptime(x, "%m/%d/%y"), reverse=True):
    #     td = datetime.datetime.strptime(date, "%m/%d/%y")
    #     print date, (now - td).days, td
    # for ts_datetime in ts_datetimes:
    #     print ts_datetime

if __name__ == '__main__':

    try:
        # get db hostfrom environment
        mtaf_db_host = getenv('MTAF_DB_HOST')
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description='  runs behave test on specified features directory and saves' +
                                                     '  the results on a mongodb running on a specified server\n')
        parser.add_argument("-d", "--db_name", type=str, default='e7_results', help="name of db")
        parser.add_argument("-s", "--server", type=str, default=mtaf_db_host,
                            help="(optional) specify mongodb server, default vqda1")
        parser.add_argument("-n", "--number_to_keep", type=int, default=10,
                            help="number of test runs to keep for each configuration")
        parser.add_argument("-a", "--age", type=int, default=30,
                            help="max age in days to keep in database")
        parser.add_argument("-o", "--operation", type=str, choices=['list', 'prune'], default='list',
                            help="operation to perform")
        args = parser.parse_args()
        prune_db(args.db_name, args.server, args.operation, args.number_to_keep, args.age)
    except:
        pass
