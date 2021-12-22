import os.path
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
import csv
from urllib import parse
from datetime import datetime
from pytz import timezone


class DataHeadServer(BaseHTTPRequestHandler):
    def _set_response(self, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == '/index.js':
            print(self.path)
            file_to_open = open(self.path[1:]).read()
            self._set_response(200)
            self.wfile.write(bytes(file_to_open, 'utf-8'))
            return
        if self.path == '/':
            self.path = '/index.html'
        try:
            file_to_open = open(self.path[1:]).read()
            with open('website.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                data = []
                for row in reader:
                    data.append(row[0])
                options = ''
                for website in data:
                    options = options + '<option value="{}">{}</option>'.format(website, website)
                print(options)
                file_to_open = file_to_open.format(options=options)
            self._set_response(200)
        except:
            file_to_open = "File Not Found"
            self._set_response(404)
        self.wfile.write(bytes(file_to_open, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)
        data = dict(parse.parse_qsl(post_data.decode('utf-8')))

        try:
            workers = []
            if not os.path.exists('workers.csv'):
                with open('workers.csv', 'w'):
                    pass
            with open('workers.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    workers.append(row[0])

            websites = []
            if not os.path.exists('website.csv'):
                with open('website.csv', 'w'):
                    pass
            with open('website.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    websites.append(row[0])

            worker = data['worker_id']
            website = data['website']
            group_id = data['group_id']
            size = data['size']

            if worker not in workers:
                self._set_response(500)
                self.wfile.write("Worker Doesnt Exist {}".format(worker).encode('utf-8'))
                return

            if website not in websites:
                self._set_response(500)
                self.wfile.write("Website Doesnt Exist {}".format(website).encode('utf-8'))
                return

            groups = []

            if not os.path.exists(website + '.csv'):
                with open(website + '.csv', 'w'):
                    pass

            with open(website + '.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    groups.append(row[0])

            if group_id not in groups:
                with open(website + '.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([group_id])

            invites = []
            if not os.path.exists(group_id + '.csv'):
                with open(group_id + '.csv', 'w'):
                    pass
            with open(group_id + '.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    invites.append(row[1])

            if worker in invites:
                self._set_response(500)
                self.wfile.write("Invitation Already Exist {}".format(group_id).encode('utf-8'))
                return

            with open(group_id + '.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                tz = timezone('EST')
                now = datetime.now(tz)
                writer.writerow([size, worker, now])
            self._set_response(200)
            self.wfile.write("Invitation added successfully".encode('utf-8'))
        except:
            self._set_response(500)
            self.wfile.write("There is ERROR".encode('utf-8'))


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, help='port number')
args = parser.parse_args()
port = args.port

httpd = HTTPServer(('0.0.0.0', port), DataHeadServer)
print("Server Running on port ", port)
httpd.serve_forever()
print("Server Running")