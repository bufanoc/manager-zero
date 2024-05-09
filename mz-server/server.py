import socket
import json

def server_program():
    host = '0.0.0.0'
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind server to all interfaces
    server_socket.listen(2)
    print("Server is listening on port:", port)

    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from:", address)
        
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break  # if data is not received break the loop
                # Process the received data
                data_json = json.loads(data)
                if 'action' in data_json and data_json['action'] == 'login':
                    # Check credentials (this should be replaced with your auth system)
                    if data_json['username'] == 'admin' and data_json['password'] == 'admin123':
                        response = {"status": "success"}
                    else:
                        response = {"status": "error", "message": "Authentication failed"}
                else:
                    response = {"status": "error", "message": "Invalid command"}
                
                conn.send(json.dumps(response).encode())  # send JSON response
            except json.JSONDecodeError:
                error_response = json.dumps({"status": "error", "message": "Invalid JSON format"})
                conn.send(error_response.encode())
            except Exception as e:
                print("Error:", str(e))
                break  # In case of other errors, break the loop
        
        conn.close()  # close the connection after the while loop

if __name__ == '__main__':
    server_program()

