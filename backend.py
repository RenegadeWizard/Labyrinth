#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3

data_base = ''


class Server:
    """Class for server work (showing ranking in a browser)"""
    def __init__(self):
        pass

    def run(self):
        server = HTTPServer(('', 1234), HTTPHandler)
        print('Started httpserver on port ', 1234)
        server.serve_forever()


class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            global data_base
            if self.path == "/":
                dane = 'Top 10:\n\n%2s%9s%14s\n' % ("lp", "nick", "wynik")
                for x, y in enumerate(data_base.select_data()):
                    if x > 9:
                        break
                    dane += "%2d.%9s%12d\n" % (x+1, y[0], y[1])
                    print(dane)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                # with open("index.html", 'r') as f:
                #     dane = f.read()
                b = bytes(dane, 'utf-8')
                self.wfile.write(b)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


class HandleDataBase:
    def __init__(self, file):
        self.conn = sqlite3.connect(file)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE results (nick VARCHAR2, result NUMBER(4))''')
        self.conn.commit()

    def select_data(self):
        cursor = self.conn.cursor()
        data = cursor.execute('''SELECT * FROM results ORDER BY result''')
        return data

    def insert_data(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO results VALUES ('renegade', 75)")
        self.conn.commit()

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    data_base = HandleDataBase("dane.db")
    server = Server()
    server.run()
