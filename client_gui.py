import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()

        # Create the name input box
        self.name_label = QLabel("Name:", self)
        self.name_input = QLineEdit(self)

        # Create the message display box
        self.messages = QTextEdit(self)
        self.messages.setReadOnly(True)

        # Create the message input box
        self.message_input = QLineEdit(self)

        # Connect the returnPressed signal of the message input box to the send_message function
        self.message_input.returnPressed.connect(self.send_message)

        # Create the send button
        self.send_button = QPushButton("Send", self)

        # Lay out the widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.messages)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

        # Connect the send button to a function that will handle sending the message
        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        name = self.name_input.text()
        message = self.message_input.text()

        # Validate the name and message
        if not name:
            # Show an error message if the name is blank
            self.show_error("Please enter a name.")
            return
        if not re.match(r"^[\w]+$", name):
            # Show an error message if the name is not alpha-numeric or contains characters other than "_"
            self.show_error("Name must be alpha-numeric and may contain '_' only.")
            return
        if not message:
            # Show an error message if the message is blank
            self.show_error("Please enter a message.")
            return

        # Add the message to the display box
        self.messages.append(f"{name}: {message}")

        # Clear the message input box
        self.message_input.clear()

    def show_error(self, message: str):
        self.messages.append(f" * Error: {message}")

    def client_loop(self):
        # Connect to the server
        self.connect_to_server()

        # Start the client loop
        while True:
            # Get the message from the server
            message = self.receive_message()

            # Add the message to the display box
            self.messages.append(message)

    def connect_to_server(self):
        pass

    def receive_message(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.setWindowTitle("Chat App")
    chat_app.resize(600, 600)
    chat_app.show()
    sys.exit(app.exec_())
