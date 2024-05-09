import sys
import json
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'KVM Management Client'
        self.initUI()
        self.client_socket = None

    def initUI(self):
        # Set up the main window properties
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 320, 250)  # Adjusted height to accommodate new button

        # Create and arrange widgets with QVBoxLayout
        layout = QVBoxLayout()

        # Server IP input
        self.label = QLabel('Enter server IP:', self)
        layout.addWidget(self.label)
        self.ip_input = QLineEdit(self)
        layout.addWidget(self.ip_input)

        # Username input
        self.username_label = QLabel('Username:', self)
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        # Password input
        self.password_label = QLabel('Password:', self)
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Connect button
        self.connect_button = QPushButton('Connect', self)
        self.connect_button.clicked.connect(self.connect_to_server)
        layout.addWidget(self.connect_button)

        # Disconnect button
        self.disconnect_button = QPushButton('Disconnect', self)
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        self.disconnect_button.setEnabled(False)  # Disabled until connected
        layout.addWidget(self.disconnect_button)

        # Button to trigger VM creation
        self.create_vm_button = QPushButton('Create VM', self)
        self.create_vm_button.clicked.connect(self.create_vm)
        self.create_vm_button.setEnabled(False)  # Disabled until connected
        layout.addWidget(self.create_vm_button)

        # Connection status label
        self.connection_status = QLabel('Status: Disconnected', self)
        layout.addWidget(self.connection_status)

        self.setLayout(layout)
        self.show()

    def connect_to_server(self):
        # Handle the server connection
        ip = self.ip_input.text()
        port = 5000
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((ip, port))
            # Send login command
            command = {"action": "login", "username": self.username_input.text(), "password": self.password_input.text()}
            self.client_socket.send(json.dumps(command).encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            response_data = json.loads(response)

            if response_data.get('status') == 'success':
                self.connection_status.setText('Status: Connected')
                self.disconnect_button.setEnabled(True)
                self.connect_button.setEnabled(False)
                self.create_vm_button.setEnabled(True)
            else:
                self.connection_status.setText(f"Status: {response_data.get('message', 'Login Failed')}")
        except Exception as e:
            QMessageBox.warning(self, 'Connection Failed', f'Failed to connect to {ip}\n{str(e)}')
            self.connection_status.setText('Status: Disconnected')

    def disconnect_from_server(self):
        # Handle disconnection from the server
        if self.client_socket:
            self.client_socket.close()
            self.connection_status.setText('Status: Disconnected')
            self.disconnect_button.setEnabled(False)
            self.connect_button.setEnabled(True)
            self.create_vm_button.setEnabled(False)

    def create_vm(self):
        # Send a command to create a virtual machine
        command = {"action": "create_vm"}
        try:
            self.client_socket.send(json.dumps(command).encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            response_data = json.loads(response)
            QMessageBox.information(self, 'VM Creation', f"Server response: {response_data.get('message', 'No response')}")
        except Exception as e:
            QMessageBox.warning(self, 'Action Failed', f'Failed to execute action\n{str(e)}')

app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())

