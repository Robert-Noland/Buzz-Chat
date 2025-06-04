import socket
import threading


def join_server():
    global name 
    name = input("Please enter your username: ")
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    hostip = input("Please enter the host's IP: ")
    client.connect((hostip,5555))
    
def receiving_messages():
    while True:
        try:
            data = client.recv(1024)
            message = data.decode('utf-8')
            print(message)
        except Exception as e:
            print(f"There is an Error Receiving Message: {e}")
            break
        
def sending_messages():
    while True:      
        msg = f'{name}: {input(" ")}'
        client.send(msg.encode('utf-8'))
        if not msg:
         print(f"Error sending message")
         break
         
join_server()
      
threading.Thread(target=sending_messages).start()
threading.Thread(target=receiving_messages).start()   
