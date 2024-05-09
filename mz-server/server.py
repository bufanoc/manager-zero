# server.py
import socket
import json
from command_processor import process_command

def server_program():
    """
    Main server program to listen and respond to client requests.
    """
    host = '0.0.0.0'
    port = 5000
    server_socket = socket.socket()  # Create a new socket for network communication
    server_socket.bind((host, port))  # Bind the socket to the host and port
    server_socket.listen(2)  # Listen for up to 2 simultaneous connections
    print("Server is listening on port:", port)

    while True:
        conn, address = server_socket.accept()  # Accept a new connection
        print("Connection from:", address)  # Display the IP address of the connected client

        try:
            while True:
                data = conn.recv(1024).decode()  # Receive data from the client
                if not data:
                    break  # Exit the loop if no data is received

                data_json = json.loads(data)  # Parse the received data as JSON
                response = process_command(data_json)  # Process the command using command_processor
                conn.send(json.dumps(response).encode())  # Send back the response as JSON
        except json.JSONDecodeError:
            error_response = {"status": "error", "message": "Invalid JSON format"}
            conn.send(json.dumps(error_response).encode())  # Send error message if JSON decoding fails
        except Exception as e:
            print(f"An error occurred: {str(e)}")  # Log other exceptions to the console
            error_response = {"status": "error", "message": "An error occurred"}
            conn.send(json.dumps(error_response).encode())
        finally:
            conn.close()  # Close the connection
            print("Disconnected from:", address)  # Log disconnection

if __name__ == '__main__':
    server_program()

