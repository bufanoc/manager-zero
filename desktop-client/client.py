import sys
import json
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'KVM Authenticate Management Client'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 320, 200)

        # Layout and widgets
        layout = QVBoxLayout()

        self.label = QLabel('Enter server IP:', self)
        layout.addWidget(self.label)

        self.ip_input = QLineEdit(self)
        layout.addWidget(self.ip_input)

        self.username_label = QLabel('Username:', self)
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_input)

        self.password_label = QLabel('Password:', self)
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password text
        layout.addWidget(self.password_input)

        self.connect_button = QPushButton('Connect', self)
        self.connect_button.clicked.connect(self.connect_to_server)
        layout.addWidget(self.connect_button)

        self.connection_status = QLabel('Status: Disconnected', self)
        layout.addWidget(self.connection_status)

        self.setLayout(layout)
        self.show()

    def connect_to_server(self):
        ip = self.ip_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        port = 5000  # Default port for your server
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                # Send login details after connecting
                command = {"action": "login", "username": username, "password": password}
                s.send(json.dumps(command).encode('utf-8'))
                response = s.recv(1024).decode('utf-8')
                response_data = json.loads(response)
                
                if response_data.get('status') == 'success':
                    self.connection_status.setText('Status: Connected')
                else:
                    self.connection_status.setText(f"Status: {response_data.get('message', 'Authentication Failed')}")
        except Exception as e:
            QMessageBox.warning(self, 'Connection Failed', f'Failed to connect to {ip}\n{str(e)}')
            self.connection_status.setText('Status: Disconnected')

app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
