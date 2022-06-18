import socket
from urllib import response
from matplotlib.font_manager import json_load
from sympy import *
import json
import os

def main():
    SERVER_HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    SERVER_PORT = 8080         # Port to listen on (non-privileged ports are > 1023)

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)

    while True:    
        # Wait for client connections
        client_connection, client_address = server_socket.accept()

        # Get the client request
        request = client_connection.recv(1024).decode()

        # Request parsing
        lines = request.split("\n")
        info = lines[0].split(" ")

        # Parameter parsing and empty parameter list control
        if len(info[1]) == 1:
            info[1] = ''
        else:
            info[1] = info[1].replace('/?','')

        # Different request branching
        if info[0] == 'GET':
            if "number" in info[1]:
                response = getRequestIsPrime(info[1])
            elif "fileName" in info[1]:
                response = getRequestDownload(info[1], client_connection)
            else:
                response = 'HTTP/1.0 400 Bad Request\n\n'
        elif info[0] == 'POST':
            response = postRequest(lines, client_connection)
        elif info[0] == 'PUT':
            response = putRequest(info[1])
        elif info[0] == 'DELETE':
            response = deleteRequest(info[1])
        else:
            response = 'HTTP/1.0 400 NOT FOUND\n\n'
            return response

        # Send HTTP response
        client_connection.sendall(response.encode())
        client_connection.close()

    # Close socket
    server_socket.close()

# This method is written for POST request and also enables client to upload a file to server
def recvall(sock):
    BUFF_SIZE = 2048 # 2 KB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def getRequestIsPrime(param):
    
    value = param.split('=')[1]

    try:
        value = int(value)
    except ValueError:
        json_object = {'message':'Please enter an integer'}
        response = 'HTTP/1.0 400 Bad Request\n\n' + json.dumps(json_object)
        return response

    primeFlag = isprime(int(value))
    json_object = {'number':value, 'isPrime':primeFlag}
    response = 'HTTP/1.0 200 OK\n\n' + json.dumps(json_object)
    return response

def getRequestDownload(param, conn):
    fileName = param.split('=')[1]
    with open(fileName, 'rb') as f:
        data = f.read()
    response = 'HTTP/1.0 200 OK\n\n' + data.decode()
    return response

def postRequest(lines, sock):

    # File Name parsing through request string
    nameLine = lines[-4]
    fileNameBlock = nameLine.split(";")[-1]
    fileName = fileNameBlock[11:-2]

    if fileName == '':
        response = 'HTTP/1.0 400 Bad Request\n\n'
        return response
    data = recvall(sock)

    # Deleting the bytes ,located at the end of file, that are not in the original file. 
    # Those bytes involve 2 newlines and boundary number located in the request string
    data = data[:-58]

    with open(fileName, 'bw') as f:
        f.write(data)
        f.close()
    response = 'HTTP/1.0 200 OK\n\n'
    return response

def putRequest(param):
    
    # param list error
    if 'oldFileName' not in param or 'newName' not in param:
        response = 'HTTP/1.0 400 Bad Request\n\n'
        return response

    fileNames = param.split('&')

    # More than 2 parameters
    if len(fileNames) > 2:
        response = 'HTTP/1.0 400 Bad Request\n\n'
        return response

    # Parameter parsing
    oldFileName = fileNames[0].split('=')[1]
    newFileName = fileNames[1].split('=')[1]

    if not os.path.exists(oldFileName):
        json_object = {'message':'File is not found'}
        response = 'HTTP/1.0 200 OK\n\n' + json.dumps(json_object)
        return response
    else:
        os.rename(oldFileName, newFileName)
        json_object = {'message':'File is successfully renamed'}
        response = 'HTTP/1.0 200 OK\n\n' + json.dumps(json_object)
        return response

def deleteRequest(param):
    # param list error
    if 'fileName' not in param:
        json_object = {'message':'fileName parameter is missing'}
        response = 'HTTP/1.0 400 Bad Request\n\n' + json.dumps(json_object)
        return response

    fileName = param.split('=')[1]

    if not os.path.exists(fileName):
        json_object = {'message':'File is not found'}
        response = 'HTTP/1.0 200 OK\n\n' + json.dumps(json_object)
        return response
    else:
        os.remove(fileName)
        json_object = {'message':'File is successfully deleted'}
        response = 'HTTP/1.0 200 OK\n\n' + json.dumps(json_object)
        return response

if __name__ == '__main__':
    main()