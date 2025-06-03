import socket
import threading


hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip,5555))


#A Clients list is used to store info about client connection
clients = []


#Broadcasting Method
def broadcast(msg):
   # Iterates through the clients dictionary and sends the message to each client
   for client in clients:
      try:
         client.send(msg.encode('utf-8'))
      except Exception as e:
         print(f"Error sending message to {clients[client]}: {e}")

def accept_connection():
   while True:
    global client, address
    client, address = server.accept()
    clients.append(client)
    print(f"Connected with {str(address)}")
    broadcast(f"A new user has connected!")
    #calls the handle_client function with a thread for handling multiple clients
    threading.Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    #Receives messages in a loop and broadcasts them 
     while True:
      try:
         global msg
         msg = client.recv(1024).decode('utf-8')
         print(f'{str(address)} {msg}' )
         broadcast(msg)
      except Exception as e:
            if client in clients:
                # Index is used to remove client from list after getting disconnected
                index = clients.index(client)
                print(f"Lost connection with {str(address)}")
                clients.remove(client)
                broadcast('A user has disconnected!')
                client.close()
                break

       
if __name__ == "__main__":
   #Accepts 20 clients at once at the most
   server.listen(20)
   print('ROOM IS OPEN ...')
   #Calls the accept_connection function with a thread for handling multiple requests at once
   t = threading.Thread(target=accept_connection)
   t.start()
   t.join()


threading.Thread(target=broadcast, args=(msg,)).start()
