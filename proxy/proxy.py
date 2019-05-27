#!/usr/bin/env python3

import argparse

import sys
import itertools
import socket
import threading
from threading import Thread
from socket import socket as Socket

'''
class thread(threading.Thread):
    def __init__(self, data):

        threading.Thread.__init__(self)
        self.data = data

    def run(self):
'''

def main():

    sys.stdout.flush()
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=2080, type=int,
                        help='Port to use')
    args = parser.parse_args()
    print(args.port)

    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # does not work in python3 with -p
        server_socket.bind(('', args.port))

        server_socket.listen(0)


        print("server ready")

        while True:

            connection_socket, address = server_socket.accept()


            while (threading.activeCount() >= 20):
                continue

            Thread(target = http_handle, args = (connection_socket, address) ).start()

    return 0


def http_handle(connection, address):

    request_string = connection.recv(1024).decode('ascii')
    print( request_string )
    print( address )

    response = ""

    assert not isinstance(request_string, bytes)

    host = ""
    request_data = {}


    try:

        request_split = request_string.split("\r\n")

        request_data["request_type"] = request_split[0]

        for index in range(1, len(request_split)):
            if (request_split[index] == ""):
                continue
            request_data[request_split[index].split(": ")[0]] = request_split[index].split(": ")[1]

        host += request_data["request_type"].split(" ")[1]
        #port_num = request_data["Host"].split(":")[1]


    except:

        response += "HTTP/1.0 400 Bad Request\n"
        response += "Content-Type: text/html; encoding=ascii\n"
        response += "Content-Length: %d\n" % len( "<html><body><h1>400: Bad Request </h1></body></html>")
        response += "Connection: close\n"
        response += "\n"
        response += "<html><body><h1>400: Bad Request </h1></body></html>"
        connection.send(response.encode("ascii"))
        connection.close()
        return


    if (not "GET" in request_data["request_type"]):

        if (not "HEAD" in request_data["request_type"] and \
            not "POST" in request_data["request_type"] and \
            not "PUT" in request_data["request_type"] and \
            not "DELETE" in request_data["request_type"] and \
            not "TRACE" in request_data["request_type"] and \
            not "CONNECT" in request_data["request_type"]):

            response += "HTTP/1.0 400 Bad Request\n"
            response += "Content-Type: text/html; encoding=ascii\n"
            response += "Content-Length: %d\n" % len( "<html><body><h1>400: Bad Request </h1></body></html>")
            response += "Connection: close\n"
            response += "\n"
            response += "<html><body><h1>400: Bad Request </h1></body></html>"

        else:

            response += "HTTP/1.0 501 Not Implemented\n"
            response += "Content-Type: text/html; encoding=ascii\n"
            response += "Content-Length: %d\n" % len( "<html><body><h1>501: Not Implemented </h1></body></html>")
            response += "Connection: close\n"
            response += "\n"
            response += "<html><body><h1>501: Not Implemented </h1></body></html>"

        connection.send(response.encode("ascii"))
        connection.close()
        return

    '''
    removed from webserver

    # try:
    #     new_connection = Socket(socket.AF_INET, socket.SOCK_STREAM)
    #     new_connection.connect((host, 80))
    #     new_connection.sendall("GET / HTTP/1.0\r\n\r\n")
    #     request_string = new_connection.recv(1024)
    #     new_connection.close()
    #
    #     temp_host = host.replace("http://", "")
    #     if ("/" in temp_host):
    #         path = temp_host[temp_host.find("/")+1 ::]
    #     else:
    #         raise FileNotFoundError
    #
    #     file = open(path, 'r')
    #     file_data = file.read()
    #     file.close()
    #
    #     response += "HTTP/1.0 200 OK\n"
    #     response += "Content-Type: text/html; encoding=ascii\n"
    #     response += "Content-Length: %d\n" % len(file_data)
    #     response += "Connection: close\n"
    #     response += "\n"
    #     response += file_data
    #
    # except FileNotFoundError:
    #     response += "HTTP/1.0 404 Not Found\n"
    #     response += "Content-Type: text/html; encoding=ascii\n"
    #     response += "Content-Length: %d\n" % len( "<html><body><h1>404: Not Found</h1></body></html>")
    #     response += "Connection: close\n"
    #     response += "\n"
    #     response += "<html><body><h1>404: Not Found</h1></body></html>"
    '''

    try:
        print( host )
        new_connection = Socket(socket.AF_INET, socket.SOCK_STREAM)
        new_connection.connect((host.replace("http://", "").replace("https://", ""), 80))
        new_connection.sendall(str.encode("GET /index.html HTTP/1.0\r\nHost: %s\r\n\r\n" % host.replace("http://", "").replace("https://", "")))
        request_string = new_connection.recv(1024).decode("ascii")
        new_connection.close()

        response += request_string

        connection.send(response.encode("ascii"))
        connection.close()
        return

    except:
        response += "HTTP/1.0 400 Bad Request\n"
        response += "Content-Type: text/html; encoding=ascii\n"
        response += "Content-Length: %d\n" % len( "<html><body><h1>400: Bad Request </h1></body></html>")
        response += "Connection: close\n"
        response += "\n"
        response += "<html><body><h1>400: Bad Request </h1></body></html>"
        connection.send(response.encode("ascii"))
        connection.close()
        return



if __name__ == "__main__":
    sys.exit(main())
