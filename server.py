import socket
import threading


hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,5555))
server.listen()


#List of the clients that are connecting and their respective usernames
global clients
clients = []
usernames = []



#Recieve method 
def receive():
    while True:
        client, address = server.accept()
        # Asks the clients for their Usernames
        client.send('USERNAME'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        print(f"Connected with {username} {str(address)}")
        

        usernames.append(username)
        clients.append(client)
#Broadcasting Method
def broadcast():
    for client in clients:
        message = client.recv(1024).decode('utf-8')
        client.send(message)
       






threading.Thread(target=broadcast).start()
threading.Thread(target=receive).start()


#Calls the recieve method
print('ROOM IS OPEN ...')
receive()
broadcast()
