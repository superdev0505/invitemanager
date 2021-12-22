import argparse
import csv
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', required=False, help='action type eg: add or remove')
    parser.add_argument('--worker', required=False, help='add worker')
    parser.add_argument('--website', required=False, help='add website')
    args = parser.parse_args()

    action = args.action

    if action == 'add':
        if args.worker:
            worker = [args.worker]
            with open('workers.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(worker)

        if args.website:
            website = [args.website]
            with open('website.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(website)

    if action == 'remove':
        if args.worker:
            workers = []
            worker = args.worker
            if not os.path.exists('workers.csv'):
                with open('workers.csv', 'w'):
                    pass
            with open('workers.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == worker:
                        workers.append(row)

            with open('workers.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in workers:
                    writer.writerow(row)

        if args.website:
            websites = []
            website = args.worker
            if not os.path.exists('websites.csv'):
                with open('websites.csv', 'w'):
                    pass
            with open('websites.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == website:
                        websites.append(row)

            with open('websites.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for row in websites:
                    writer.writerow(row)
