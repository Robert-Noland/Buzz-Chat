import socket
import threading
from loguru import logger

# Sets up logging file
logger.add("Buzzlogs.log",  rotation="500 MB", format="{time} {level} {message}", colorize=True, compression="zip")

hostname = socket.gethostname()
global ip
ip = socket.gethostbyname(hostname)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip,5555))

#The Clients dictionary is used to store information about client connection
clients = {}

#Broadcasting Method
def broadcast(msg):
   # Iterates through the clients dictionary and sends the message to each client
   for client in clients:
      try:
         client.send(msg.encode('utf-8'))
      except Exception as e:
         #Logs errors automatically 
         logger.exception(e)
         logger.error(f"Error sending message to {clients[client]}: {e}")

def accept_connection():
   while True:
    global client, address
    client, address = server.accept()
    #Adds the ip address value to the client key within the clients dictionary 
    clients[client] = address
    #Logs new connections without giving out the ip and port being used by the connected client to the other connected clients
    logger.success(f'Connected with {str(address)}')
    #Displays the currently connected clients
    logger.info(f'{clients}')
    #Informs connected clients that someone has joined the chatroom
    broadcast(f"A new user has connected!")
    #Calls the handle_client function with a thread for handling multiple clients
    threading.Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    #Receives messages in a loop and broadcasts them 
     while True:
      try:
         global msg
         msg = client.recv(1024).decode('utf-8')
         logger.info(f'{str(address)} {msg}' ) 
         broadcast(msg)
      except Exception as e:
            logger.exception(e)
            if client in clients:
                #The client is removed from the dictionary after getting disconnected
                logger.warning(f"Lost connection with {str(address)}")
                del clients[client]
                #Informs currently connected clients that someone is no longer in the chatroom
                broadcast('A user has disconnected!')
                client.close()
                #Displays the updated dictionary / list of connected users
                logger.info(f'{clients}')
                break

if __name__ == "__main__":
   #Accepts 20 clients at once at the most
   server.listen(20)
   logger.success(f"ROOM IS OPEN ... now listening on {ip ,5555} ")
   #Calls the accept_connection function with a thread for handling multiple requests at once
   t = threading.Thread(target=accept_connection)
   t.start()
   t.join()

threading.Thread(target=broadcast, args=(msg,)).start()
