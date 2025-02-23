import sqlite3  # Importing sqlite3 to interact with SQLite databases
import hashlib  # Importing hashlib to hash passwords
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox  # Importing PyQt6 widgets

DB_FILE = "users.db"  # Defining the database file name

class RegisterDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Register New User")  # Setting the window title
        self.setGeometry(300, 300, 350, 300)  # Setting the window geometry
        self.layout = QVBoxLayout()  # Creating the main layout

        # Username Input
        self.username_input = QLineEdit(self)  # Creating a line edit for username input
        self.username_input.setPlaceholderText("Enter Username")  # Setting placeholder text
        self.layout.addWidget(QLabel("Username:"))  # Adding a label for username
        self.layout.addWidget(self.username_input)  # Adding the username input to the layout

        # Password Input
        self.password_input = QLineEdit(self)  # Creating a line edit for password input
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Setting echo mode to hide password
        self.password_input.setPlaceholderText("Enter Password")  # Setting placeholder text
        self.layout.addWidget(QLabel("Password:"))  # Adding a label for password
        self.layout.addWidget(self.password_input)  # Adding the password input to the layout

        # Email Input
        self.email_input = QLineEdit(self)  # Creating a line edit for email input
        self.email_input.setPlaceholderText("Enter Email")  # Setting placeholder text
        self.layout.addWidget(QLabel("Email:"))  # Adding a label for email
        self.layout.addWidget(self.email_input)  # Adding the email input to the layout

        # Phone Input
        self.phone_input = QLineEdit(self)  # Creating a line edit for phone input
        self.phone_input.setPlaceholderText("Enter Phone Number")  # Setting placeholder text
        self.layout.addWidget(QLabel("Phone Number:"))  # Adding a label for phone number
        self.layout.addWidget(self.phone_input)  # Adding the phone input to the layout

        # Register Button
        self.register_button = QPushButton("Register", self)  # Creating a register button
        self.register_button.clicked.connect(self.register_user)  # Connecting the button to the register function
        self.layout.addWidget(self.register_button)  # Adding the register button to the layout

        self.setLayout(self.layout)  # Setting the main layout

    def hash_password(self, password):
        """ Hash the password using SHA-256. """
        return hashlib.sha256(password.encode()).hexdigest()  # Returning the hashed password

    def register_user(self):
        """ Handle user registration. """
        username = self.username_input.text().strip()  # Getting the username
        password = self.hash_password(self.password_input.text())  # Hashing the password
        email = self.email_input.text().strip()  # Getting the email
        phone = self.phone_input.text().strip()  # Getting the phone number

        if not username or not password or not email or not phone:
            QMessageBox.warning(self, "Registration Failed", "All fields are required.")  # Showing a warning if any field is empty
            return

        conn = sqlite3.connect(DB_FILE)  # Connecting to the database
        cursor = conn.cursor()  # Creating a cursor

        try:
            cursor.execute("INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)",
                           (username, password, email, phone))  # Inserting the new user into the database
            conn.commit()  # Committing the changes
            QMessageBox.information(self, "Registration Successful", "You can now log in!")  # Showing a success message
            self.accept()  # Accepting the dialog
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Registration Failed", "Username already exists.")  # Showing a warning if the username already exists
        finally:
            conn.close()  # Closing the connection