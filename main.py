from PyQt6.QtWidgets import QApplication  # Importing QApplication to create the application
from login import LoginDialog  # Importing LoginDialog class from login module
from database import create_tables  # Importing create_tables function from database module

# Initialize Database
create_tables()  # Creating the necessary tables in the database

app = QApplication([])  # Creating the application instance
login_dialog = LoginDialog(None)  # Creating the login dialog
if login_dialog.exec():  # Executing the login dialog and checking if login was successful
    print("Login successful.")  # Printing a success message
app.exec()  # Running the application event loop