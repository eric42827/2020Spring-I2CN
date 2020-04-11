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
        print(message)
        if len(message)>1:
            filename = message.split()[1] #URL
            #print(filename)
            # Read data from the file that the client requested
            f = open('.'+filename) #open html
            # Split the data into lines for future transmission 
            outputdata = f.read()
            f.close()
            #print(outputdata)
            # send HTTP status to client
            client.send(message.split()[2]+' 200 OK\r\n'.encode())
            # send content type to client
            client.send('Content-Type: text/html\r\n\r\n'.encode())
            # Send the content of the requested file to the client  
            #for i in range(0, len(outputdata)):
            client.send(outputdata.encode()+"\r\n".encode())
            client.close()
    except IOError:
        #Send response message for file not found
        client.send(message.split()[2]+' 404 Not Found\r\n'.encode())
        # send content type to client
        client.send('Content-Type: text/html\r\n\r\n'.encode())
        client.send('<html><head><title>404 Not Found</title></head><body bgcolor=white><h1>404 Not Found</h1><p>The requested URL was not found on this server.</p></body></html>')
        #Close client socket
        client.close()
s.close()
sys.exit() #Terminate the program after sending the corresponding data
