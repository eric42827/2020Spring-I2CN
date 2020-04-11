from socket import *
import sys
import time
import threading

if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server & Web server.')
	sys.exit(2)
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
tcpSerSock.bind(('', 8080))
tcpSerSock.listen(5)
def routine(tcpCliSock):
    # Strat receiving data from the client
    message = tcpCliSock.recv(1024).decode('utf-8')
    if len(message) <=1:
        return
    # Extract the filename from the given message
    filename = message.split()[1].partition("/")[2]
    filetouse = "./" + filename
    print('Fliename: '+filename,flush=True)
    #print(filetouse)
    #print(message)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse)
        html_body = f.read()
        # ProxyServer finds a cache hit and generates a response message
        response = "HTTP/1.1 200 OK\r\n"+\
            "Content-Type:text/html\r\n\r\n"+\
                html_body
        print('Read from cache\n',flush=True)
	# Error handling for file not found in cache
    except IOError:
        # Create a socket on the proxyserver
        c = socket(AF_INET, SOCK_STREAM)
        # Connect to the socket to port 80
        c.connect((sys.argv[1],80))
        # ask port 127.0.0.1:80 for the file requested by the client
        request = "GET " + "/" + filename + " HTTP/1.1\r\n"
        c.send(request.encode())
        # receive the response 
        raw_resp = c.recv(4096).decode('utf-8')
        status = raw_resp.splitlines()[0]
        bodyStart = raw_resp.index('\r\n\r\n')+4
        html_body = raw_resp[bodyStart:]
        print(repr(status)+'\n',flush=True)
        # Create a new file in the cache for the requested file.
        # Also send the response in the buffer to client socket and the corresponding file in the cache
        if status.endswith('200 OK'):
            tmpFile = open("./" + filename,"w")
            tmpFile.write(html_body)
            tmpFile.close()
        response = raw_resp
        c.close()
    tcpCliSock.sendall(response.encode())
    tcpCliSock.close()
while True:
    print('Ready to serve...',flush=True)
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr,flush=True)
    #routine(tcpCliSock)
    threading.Thread(target=routine, args=(tcpCliSock,)).start()
tcpSerSock.close()
