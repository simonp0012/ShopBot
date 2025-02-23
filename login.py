import sqlite3  # Importing sqlite3 to interact with SQLite databases
import hashlib  # Importing hashlib to hash passwords
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox  # Importing PyQt6 widgets
from database import get_user  # Importing get_user function from database module
from register import RegisterDialog  # Importing RegisterDialog class from register module

DB_FILE = "users.db"  # Defining the database file name

class LoginDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Login / Register")  # Setting the window title
        self.setGeometry(300, 300, 350, 250)  # Setting the window geometry
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

        # Login Button
        self.login_button = QPushButton("Login", self)  # Creating a login button
        self.login_button.clicked.connect(self.login_user)  # Connecting the button to the login function
        self.layout.addWidget(self.login_button)  # Adding the login button to the layout

        # Register Button
        self.register_button = QPushButton("Register", self)  # Creating a register button
        self.register_button.clicked.connect(self.register_user)  # Connecting the button to the register function
        self.layout.addWidget(self.register_button)  # Adding the register button to the layout

        self.setLayout(self.layout)  # Setting the main layout

    def hash_password(self, password):
        """ Hash the password using SHA-256. """
        return hashlib.sha256(password.encode()).hexdigest()  # Returning the hashed password

    def login_user(self):
        """ Handle user login. """
        username = self.username_input.text().strip()  # Getting the username
        password = self.hash_password(self.password_input.text())  # Hashing the password

        conn = sqlite3.connect(DB_FILE)  # Connecting to the database
        cursor = conn.cursor()  # Creating a cursor
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))  # Executing the query
        user = cursor.fetchone()  # Fetching the user
        conn.close()  # Closing the connection

        if user:
            QMessageBox.information(self, "Login Success", f"Welcome back, {username}!")  # Showing success message
            self.accept()  # Accepting the dialog
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")  # Showing failure message

    def register_user(self):
        """ Open the registration dialog. """
        register_dialog = RegisterDialog(self)  # Creating a register dialog
        register_dialog.exec()  # Executing the dialog