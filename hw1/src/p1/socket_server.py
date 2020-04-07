import socket

# Specify the IP addr and port number 
# (use "127.0.0.1" for localhost on local machine)
# Create a socket and bind the socket to the addr
# TODO start
HOST, PORT = '127.0.0.1', 7777
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((HOST,PORT))
# TODO end

while(True):
    # Listen for any request
    # TODO start
    s.listen(0)
    # TODO end
    print("The Grading server for HW2 is running..")

    while(True):
        # Accept a new request and admit the connection
        # TODO start
        client, address = s.accept()
        # TODO end
        print(str(address)+" connected")
        try:
            while (True):
                client.send(b"Welcom to the calculator server. Input your problem ?\n")
                # Recieve the data from the client and send the answer back to the client
                # Ask if the client want to terminate the process
                # Terminate the process or continue
                # TODO start
                data = client.recv(1024).decode('utf-8')
                data_sep = data.split()
                ans = 0
                if data_sep[1]=='+':
                    ans = int(data_sep[0]) + int(data_sep[-1])
                elif data_sep[1]=='-':
                    ans = int(data_sep[0]) - int(data_sep[-1])
                elif data_sep[1]=='*':
                    ans = int(data_sep[0]) * int(data_sep[-1])
                elif data_sep[1]=='/':
                    ans = int(data_sep[0]) / int(data_sep[-1])
                sol = 'The answer is '+str(ans)+'.\nDo you have any question? (Y/N)\n'            
                client.send(sol.encode('utf-8'))
                res = client.recv(1024).decode('utf-8')
                if res == 'y':
                    continue
                elif res == 'n':
                    client.shutdown(2)
                    client.close()
                    break

                # TODO end
        except ValueError:
            print("except")
s.close()