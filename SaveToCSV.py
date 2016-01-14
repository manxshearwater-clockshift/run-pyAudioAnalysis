import csv
import os
import numpy as np
import datetime
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("directory", help="the directory with npy files",
                    type=str)
parser.add_argument("--name", help="the knn model to use",
                    type=str)
args = parser.parse_args()

csv_file_name = args.name
if not args.name:
    csv_file_name = "npytocsv"

def get_all_filesnames():
    return sorted(os.listdir(args.directory))

# EG: sk_csauth_fast_b73_150616_007_011016.npy
def extract_date_from_filename(filename):
    split_filename = filename.split("_")
    date = split_filename[4]
    time = split_filename[6][:-4]

    year = int(str(date)[:2])
    month = int(str(date)[2:4])
    day = int(str(date)[4:6])

    hours = int(str(time)[:2])
    minutes = int(str(time)[2:4])
    seconds = int(str(time)[4:6])

    date_time = datetime.datetime(2000 + year, month, day, hours, minutes, seconds)

    return date_time

def load_classes_from_file(filename):
    return np.load(args.directory + filename)

def create_new_csv_file():
    with open(csv_file_name + '.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["date time", "class"])


def write_new_lines_for_file(date_time, nclasses):
    with open(csv_file_name + '.csv', 'ab') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["date time", "class"])
        for nclass in nclasses:
            csvwriter.writerow([date_time, nclass])
            date_time = increment_date_time(date_time)

def increment_date_time(date_time):
    time_delta = datetime.timedelta(seconds=1)
    new_datetime = date_time + time_delta

    return new_datetime

def main():
    list_filenames = get_all_filesnames()
    create_new_csv_file()
    for filename in list_filenames:
        date_time = extract_date_from_filename(filename)
        nclasses = load_classes_from_file(filename)
        write_new_lines_for_file(date_time, nclasses)


if __name__ == "__main__":
    main()