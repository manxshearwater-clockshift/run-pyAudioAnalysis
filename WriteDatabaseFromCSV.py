import DatabaseHelper as dh
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("csvfile", help="name of the csvfile",
                    type=str)
parser.add_argument("birdname", help="name of the csvfile",
                    type=str)
parser.add_argument("--create", help="create a new table",
                    type=str)
args = parser.parse_args()

def create_db():
    dh.drop_db("TABLE_BIRDS")
    dh.create_db()

def add_to_db(csvfile, birdname):
    dh.csv_to_db("b73.csv", "b73")

if __name__ == '__main__':
    if args.create == "true":
        create_db()
    add_to_db(args.csvfile, args.birdname)