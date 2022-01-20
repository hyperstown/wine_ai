import socket

HOST = "127.0.0.1" 
PORT = 8001  # create a socket object 

def _convert_to_string(input_tuple):
    result = "[DEBUG] "
    for index, el in enumerate(input_tuple):
        result += el
        result += " " if index != len(input_tuple) - 1 else ""
    return result

def send_debug(value):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client.connect((HOST, PORT))
    if isinstance(value, tuple):
        value = _convert_to_string(value)
    client.send(value.encode())  
    client.close()
