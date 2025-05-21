import socket
import threading

global stop_thread
stop_thread = False

def join_server():
    global name 
    name = input("Please enter your username: ")
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #hostip = input("Please enter the host's IP: ")
    client.connect(('10.5.0.2',5555))
    
        
        

    
def receiving_messages(client):
    while True:
        try:
            data = client.recv(1024)
            message = data.decode('utf-8')
            print(message)
        except Exception as e:
            print(f"There is an Error Receiving Message: {e}")
            break
        client.close()


def sending_messages(client):
    while True:     
        msg = f'{name}: {input("")}'
        client.send(msg.encode('utf-8'))




join_server()
      
threading.Thread(target=sending_messages(client), args=(client)).start()
threading.Thread(target=receiving_messages(client), args=(client)).start()   
