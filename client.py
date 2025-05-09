import socket
import threading

stop_thread = False

def join_server():
    global username 
    username = input("Please enter your username: ")
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    hostip = input("Please enter the host's IP: ")
    client.connect((hostip,5555))
    
        
        

    
def receiving_messages():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            nameid = client.recv(1024).decode('ascii')
            if nameid == 'USERNAME':
                client.send(username.encode('ascii'))
            else:
                message = client.recv(1024).decode('utf-8')
                print(message)
        except socket.error:
            print('Error Occured while Connecting')
            client.close()
            break

def sending_messages():
    while True:     
        message = f'{username}: {input("")}'
        client.send(message.encode('utf-8'))




join_server()
sending_messages()
receiving_messages()
      
threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()   