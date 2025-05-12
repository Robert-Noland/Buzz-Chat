import socket
import threading


hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip,5555))
server.listen(5)


#Clients dict used to store info about client connection
#global clients
clients = {}
#usernames = []


#adding this to move the commented section under receive to here
def handle_clients(conn)

#Recieve method 
def receive():
    while True:
        msg = conn.recv(1024)
        broadcast(msg, name + ":")
        #client, address = server.accept()
        # Asks the clients for their Usernames
        #client.send('USERNAME'.encode('ascii'))
        #username = client.recv(1024).decode('ascii')
        #print(f"Connected with {username} {str(address)}")
    
        

        #usernames.append(username)
        #clients.append(client)
#Broadcasting Method
def broadcast(msg, prefix=""):
    for client in clients:
        client.send(bytes(prefix,"utf-8") + msg)
       






threading.Thread(target=broadcast).start()
threading.Thread(target=receive).start()


#Calls the recieve method
print('ROOM IS OPEN ...')
receive()
broadcast()
