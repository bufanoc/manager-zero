import sys
import json
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'KVM Management Client'
        self.initUI()

    def initUI(self):
        # Initialize the UI elements
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 320, 200)

        layout = QVBoxLayout()  # Create a vertical layout

        # Create and add label, input box for server IP
        self.label = QLabel('Enter server IP:', self)
        layout.addWidget(self.label)
        self.ip_input = QLineEdit(self)
        layout.addWidget(self.ip_input)

        # Create and add label, input box for username
        self.username_label = QLabel('Username:', self)
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        # Create and add label, input box for password
        self.password_label = QLabel('Password:', self)
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Create and add connect button
        self.connect_button = QPushButton('Connect', self)
        self.connect_button.clicked.connect(self.connect_to_server)
        layout.addWidget(self.connect_button)

        # Create and add disconnect button
        self.disconnect_button = QPushButton('Disconnect', self)
        self.disconnect_button.clicked.connect(self.disconnect_from_server)
        self.disconnect_button.setEnabled(False)
        layout.addWidget(self.disconnect_button)

        # Create and add a status label
        self.connection_status = QLabel('Status: Disconnected', self)
        layout.addWidget(self.connection_status)

        self.setLayout(layout)
        self.show()

    def connect_to_server(self):
        # Handle connection logic
        ip = self.ip_input.text()
        port = 5000  # Server's port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((ip, port))
            # Send login command after connecting
            command = {"action": "login", "username": self.username_input.text(), "password": self.password_input.text()}
            self.client_socket.send(json.dumps(command).encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            response_data = json.loads(response)

            if response_data.get('status') == 'success':
                self.connection_status.setText('Status: Connected')
                self.disconnect_button.setEnabled(True)
                self.connect_button.setEnabled(False)
            else:
                self.connection_status.setText(f"Status: {response_data.get('message', 'Authentication Failed')}")
        except Exception as e:
            QMessageBox.warning(self, 'Connection Failed', f'Failed to connect to {ip}\n{str(e)}')
            self.connection_status.setText('Status: Disconnected')

    def disconnect_from_server(self):
        # Handle disconnection logic
        if self.client_socket:
            self.client_socket.close()
            self.connection_status.setText('Status: Disconnected')
            self.disconnect_button.setEnabled(False)
            self.connect_button.setEnabled(True)

app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
