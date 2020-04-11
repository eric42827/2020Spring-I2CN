from socket import *
import sys
import time
import threading

if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server & Web server.')
	sys.exit(2)
# Environment : Python 3.8
# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# Fill in start.
tcpSerSock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
tcpSerSock.bind(('', 8080))
tcpSerSock.listen(5)
# Fill in end.
def routine(tcpCliSock):
    # Strat receiving data from the client
    message = tcpCliSock.recv(1024).decode('utf-8')
    
    #fileExist = "false"
    # Extract the filename from the given message
    #print(message.split()[1])
    filename = message.split()[1].partition("/")[2]
    #if filename == 'favicon.ico':
        #return
    print(filename)
    filetouse = "./" + filename
    #print(filetouse)
    #print(message)
    try:
        # Check wether the file exist in the cache
        f = open(filetouse)
        outputdata = f.read()
        #fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
        # Fill in start.
        for i in range(0,len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
        tcpCliSock.send("\r\n".encode())
        tcpCliSock.close()
        # Fill in end.
        print('Read from cache\n')
	# Error handling for file not found in cache
    except IOError:
        #if fileExist == "false":
            # Create a socket on the proxyserver
        c = socket(AF_INET, SOCK_STREAM)
        try:
            # Connect to the socket to port 80
            c.connect((sys.argv[1],80))
            # ask port 127.0.0.1:80 for the file requested by the client
            request = "GET " + "/" + filename + " HTTP/1.1\n\n"
            c.send(request.encode())
            # receive the response 
            status = c.recv(1024).decode('utf-8')
            contenttype = c.recv(1024).decode('utf-8')
            html_content = c.recv(4096).decode('utf-8')
            print(status)
            #print(html_content)
            #print(contenttype)
            # Create a new file in the cache for the requested file.
            # Also send the response in the buffer to client socket and the corresponding file in the cache
            if status == 'HTTP/1.1 200 OK\r\n':
                tmpFile = open("./" + filename,"w")
                tmpFile.write(html_content)
                tmpFile.close()
            response = 'HTTP/1.1 200 OK\r\n\r\n' + html_content
            tcpCliSock.send(response.encode())
        except:
            print("Illegal request")
        c.close()
        ''' 
       elif filename!='favicon.ico':
            # HTTP response message for file not found
            # Fill in start.
            tcpCliSock.send(message.split()[2]+' 404 Not Found\r\n'.encode())
            # send content type to client
            tcpCliSock.send('Content-Type: text/html\r\n\r\n'.encode())
            tcpCliSock.send('<html><head><title>404 Not Found</title></head><body bgcolor=white><h1>404 Not Found</h1><p>The requested URL was not found on this server.</p></body></html>')
            #Close client socket
            tcpCliSock.close()
            # Fill in end.
        '''
    
    # Close the client and the server sockets. For testing multi-user, you should comment the tcpCliSock.close()
    #tcpCliSock.close()

# Fill in start. Change this part, such that multi-users can connect to this proxy server
while True:
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    routine(tcpCliSock)
tcpSerSock.close()
# Fill in end.
