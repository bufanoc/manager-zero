import socket
import json

def server_program():
    # Setup the server to listen on all interfaces at a specified port
    host = '0.0.0.0'
    port = 5000

    server_socket = socket.socket()  # Create a socket object for network communication
    server_socket.bind((host, port))  # Bind the socket to all IP addresses of this host at port 5000
    server_socket.listen(2)  # Setup the socket to allow up to 2 simultaneous connections
    print("Server is listening on port:", port)

    while True:
        conn, address = server_socket.accept()  # Wait for a connection, accept it, and get the connection object
        print("Connection from:", address)

        try:
            while True:
                data = conn.recv(1024).decode()  # Receive data from the client, 1024 bytes at a time
                if not data:
                    break  # If no data is received, break out of the loop to close the connection

                data_json = json.loads(data)  # Try to parse the received data as JSON
                response = process_command(data_json)  # Process the parsed JSON data
                conn.send(json.dumps(response).encode())  # Send the response back as a JSON encoded string
        except json.JSONDecodeError:
            # Handle JSON decoding errors (if received data is not valid JSON)
            conn.send(json.dumps({"status": "error", "message": "Invalid JSON format"}).encode())
        except Exception as e:
            # General exception handling for any other errors
            print("Error:", str(e))
        finally:
            # Close the connection and print a message
            conn.close()
            print("Disconnected from:", address)

def process_command(data_json):
    # A function to process the received commands based on the 'action' key
    if data_json.get('action') == 'login':
        username = data_json.get('username')
        password = data_json.get('password')
        if username == 'admin' and password == 'admin123':
            return {"status": "success"}
        else:
            return {"status": "error", "message": "Authentication failed"}
    return {"status": "error", "message": "Unknown command"}

if __name__ == '__main__':
    server_program()
# In this snippet, we have defined a function process_command(data_json) to handle the received commands based on the 'action' key in the JSON data. If the action is 'login', it checks the username and password and returns a success or error response accordingly. If the action is not recognized, it returns an error response with a message "Unknown command".

