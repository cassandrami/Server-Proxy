#!/usr/bin/env python3

import argparse

import sys
import itertools
import socket
from socket import socket as Socket

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
        server_socket.bind(('0.0.0.0', args.port))

        server_socket.listen(0)
        print("server ready")

        while True:

            with server_socket.accept()[0] as connection_socket:

                data_str = connection_socket.recv(1024).decode('ascii')
                print(data_str)

                connection_socket.send(http_handle(data_str).encode('ascii'))
                connection_socket.close()

    return 0


def http_handle(request_string):

    assert not isinstance(request_string, bytes)

    response = ""
    host = ""
    request_data = {}

    try:
        '''
        sorts request data by line, and then into a dictionary with appropriate
        keys and values. port num not required at this point
        '''
        request_split = request_string.split("\r\n")
        request_data["request_type"] = request_split[0]

        for index in range(1, len(request_split)):
            if (request_split[index] == ""):
                continue
            request_data[request_split[index].split(": ")[0]] = request_split[index].split(": ")[1]


        host += request_data["request_type"].split(" ")[1]
        #port_num = request_data["Host"].split(":")[1]


    except:

        '''
        data is formatted incorrectly if excepted
        '''

        response += "HTTP/1.0 400 Bad Request\n"
        response += "Content-Type: text/html; encoding=ascii\n"
        response += "Content-Length: %d\n" % len( "<html><body><h1>400: Bad Request </h1></body></html>")
        response += "Connection: close\n"
        response += "\n"
        response += "<html><body><h1>400: Bad Request </h1></body></html>"
        return response


    if (not "GET" in request_data["request_type"]):

        '''
        if not "GET", then if not another valid request, bad request. otherwise not implemented
        '''
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

        return response

    try:
        print(host)
        temp_host = host.replace("http://", "")
        if ("/" in temp_host):
            path = temp_host[temp_host.find("/")+1 ::]
        else:
            raise FileNotFoundError

        file = open(path, 'r')
        file_data = file.read()
        file.close()

        '''
        if all gucci, upload file
        '''

        response += "HTTP/1.0 200 OK\n"
        response += "Content-Type: text/html; encoding=ascii\n"
        response += "Content-Length: %d\n" % len(file_data)
        response += "Connection: close\n"
        response += "\n"
        response += file_data

        '''
        if not gucci, file not found
        '''
        
    except FileNotFoundError:
        response += "HTTP/1.0 404 Not Found\n"
        response += "Content-Type: text/html; encoding=ascii\n"
        response += "Content-Length: %d\n" % len( "<html><body><h1>404: Not Found</h1></body></html>")
        response += "Connection: close\n"
        response += "\n"
        response += "<html><body><h1>404: Not Found</h1></body></html>"


    return response

if __name__ == "__main__":
    sys.exit(main())
