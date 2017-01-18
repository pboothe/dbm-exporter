#!/usr/bin/env python

import argparse
import anydbm
import sys
import BaseHTTPServer
import SocketServer


class MetricRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    db_filename = None

    def do_GET(self):
        database = anydbm.open(self.db_filename)
        output = ['%s %s' % (k, database[k]) for k in database.keys()]
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        print >>self.wfile, '\n'.join(output)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Output the metrics stored in a dbm file')
    parser.add_argument(
        '--db_file',
        metavar='DB_FILE',
        required=True,
        help='The DBM file to read the metrics from')
    parser.add_argument(
        '--port',
        metavar='PORT',
        type=int,
        default=8080,
        help='The port on which the server should run')
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv[1:])
    MetricRequestHandler.db_filename = args.db_file
    httpd = SocketServer.TCPServer(("", args.port), MetricRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main(sys.argv)
