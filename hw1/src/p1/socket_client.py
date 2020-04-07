import socket

HOST, PORT = '127.0.0.1', 7777
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

c.connect((HOST, PORT))
while True:
    #Welcom to the calculator server. Input your problem ?\n
    res = input(c.recv(1024).decode('utf-8')).encode('utf-8')
    c.send(res)
    #The answer is '+str(ans)+'.\nDo you have any question? (Y/N)\n

c.close()