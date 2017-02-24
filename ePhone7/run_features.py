from pymongo import MongoClient
import re
import sys

def run_features(features_dir):
    pass


def write_result_to_db(server, db_name, result):
    client = MongoClient(server)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='  runs behave test on specified features directory and saves' +
                                                 '  the results on a mongodb running on a specified server\n')
    parser.add_argument("-d", "--db_name", type=str, default='features', help="operation to perform")
    parser.add_argument("-f", "--features_directory", type=str, default='features', help="operation to perform")
    parser.add_argument("-s", "--server", type=str, default='vqda1',
                        help="(optional) specify mongodb server, default 'vqda1'")
    args = parser.parse_args()
    result = run_features(args.features_directory)
    write_result_to_db(args.server, args.db_name, result)


