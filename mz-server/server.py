# server.py
import socket
import json
from command_processor import process_command

def server_program():
    """
    Main server program that listens for incoming connections and processes data.
    """
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 5000       # Port number for the server

    server_socket = socket.socket()  # Create a new socket for network communication
    server_socket.bind((host, port))  # Bind the socket to the host and port
    server_socket.listen(2)  # Listen for incoming connections (max 2 in the queue)
    print("Server is listening on port:", port)

    while True:
        conn, address = server_socket.accept()  # Accept a new connection
        print("Connection from:", address)  # Print the address of the connected client

        try:
            while True:
                data = conn.recv(1024).decode()  # Receive data from the client
                if not data:
                    break  # If no data is received, exit the loop

                data_json = json.loads(data)  # Parse the JSON data
                response = process_command(data_json)  # Process the command
                conn.send(json.dumps(response).encode())  # Send the response back as JSON
        except json.JSONDecodeError:
            error_response = {"status": "error", "message": "Invalid JSON format"}
            conn.send(json.dumps(error_response).encode())  # Handle JSON errors
        except Exception as e:
            print(f"An error occurred: {str(e)}")  # Print other exceptions
            error_response = {"status": "error", "message": "An error occurred"}
            conn.send(json.dumps(error_response).encode())
        finally:
            conn.close()  # Close the connection
            print("Disconnected from:", address)  # Print a disconnection message

if __name__ == '__main__':
    server_program()

