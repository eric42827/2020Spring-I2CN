#import socket module
import socket
import time
import sys # In order to terminate the program

#Prepare a sever socket
HOST, PORT = '127.0.0.1', 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((HOST,PORT))
s.listen(5)

while True:
    #Establish the connection
    print('Ready to serve...')
    client, address = s.accept()
    try:
        # Receive http request from the clinet
        message = str(client.recv(4096))
        #print(message)
        if len(message)>1:
            filename = message.split()[1] #URL
            print('Filename: '+filename)
            # Read data from the file that the client requested
            f = open('.'+filename) #open html
            # Split the data into lines for future transmission 
            html_body = f.read()
            f.close()
            #print(outputdata)
            # send HTTP status, content type, body to client
            response = message.split()[2]+\
                ' 200 OK\r\nContent-Type: text/html\r\n\r\n'+\
                html_body
            print(response+'\n')
            client.sendall(response.encode())
            client.close()
    except IOError:
        #Send response message for file not found
        response = message.split()[2]+' 404 Not Found\r\n'+\
            'Content-Type: text/html\r\n\r\n'+\
                '<html><head><title>404 Not Found</title></head><body bgcolor=white><h1>404 Not Found</h1><p>The requested URL was not found on this server.</p></body></html>'
        print(response+'\n')
        client.sendall(response.encode())
        #Close client socket
        client.close()
s.close()
sys.exit() #Terminate the program after sending the corresponding data
