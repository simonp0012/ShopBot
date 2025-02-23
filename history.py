import sqlite3  # Importing sqlite3 to interact with SQLite databases
import csv  # Importing csv to handle CSV file operations
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTextBrowser, QHBoxLayout, QDateEdit, QMessageBox  # Importing PyQt6 widgets
from PyQt6.QtCore import QDate  # Importing QDate to handle date operations

DB_FILE = "users.db"  # Defining the database file name

class HistoryUI(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username  # Storing the username
        self.setWindowTitle("Purchase History")  # Setting the window title
        self.setGeometry(400, 200, 600, 400)  # Setting the window geometry

        layout = QVBoxLayout()  # Creating the main layout

        # Search & Filter Row
        search_layout = QHBoxLayout()  # Creating a horizontal layout for search and filter

        self.search_input = QLineEdit()  # Creating a line edit for search input
        self.search_input.setPlaceholderText("Search by product URL")  # Setting placeholder text
        search_layout.addWidget(self.search_input)  # Adding the search input to the layout

        self.date_filter = QDateEdit()  # Creating a date edit for date filter
        self.date_filter.setCalendarPopup(True)  # Enabling calendar popup
        self.date_filter.setDate(QDate.currentDate())  # Setting the current date
        search_layout.addWidget(self.date_filter)  # Adding the date filter to the layout

        self.search_button = QPushButton("Search")  # Creating a search button
        self.search_button.clicked.connect(self.load_purchase_history)  # Connecting the button to the search function
        search_layout.addWidget(self.search_button)  # Adding the search button to the layout

        layout.addLayout(search_layout)  # Adding the search layout to the main layout

        # History Display
        self.history_box = QTextBrowser()  # Creating a text browser to display history
        layout.addWidget(QLabel("Your Purchase History:"))  # Adding a label
        layout.addWidget(self.history_box)  # Adding the text browser to the layout

        # Refresh & Export Buttons
        button_layout = QHBoxLayout()  # Creating a horizontal layout for buttons

        self.refresh_button = QPushButton("Refresh")  # Creating a refresh button
        self.refresh_button.clicked.connect(lambda: self.load_purchase_history(True))  # Connecting the button to the refresh function
        button_layout.addWidget(self.refresh_button)  # Adding the refresh button to the layout

        self.export_button = QPushButton("Export to CSV")  # Creating an export button
        self.export_button.clicked.connect(self.export_history_to_csv)  # Connecting the button to the export function
        button_layout.addWidget(self.export_button)  # Adding the export button to the layout

        layout.addLayout(button_layout)  # Adding the button layout to the main layout

        self.setLayout(layout)  # Setting the main layout

        # Load history initially
        self.load_purchase_history(True)  # Loading the purchase history initially

    def load_purchase_history(self, show_all=False):
        """ Load and filter purchase history for the logged-in user. """
        search_query = self.search_input.text().strip().lower()  # Getting the search query
        selected_date = self.date_filter.date().toString("yyyy-MM-dd")  # Getting the selected date

        conn = sqlite3.connect(DB_FILE)  # Connecting to the database
        cursor = conn.cursor()  # Creating a cursor

        query = "SELECT timestamp, product_url, status FROM bot_actions WHERE username=?"  # Defining the query
        params = [self.username]  # Defining the parameters

        if not show_all:
            query += " AND product_url LIKE ? AND DATE(timestamp) = ?"  # Adding conditions to the query
            params.extend([f"%{search_query}%", selected_date])  # Adding parameters

        query += " ORDER BY timestamp DESC"  # Adding order by clause

        cursor.execute(query, params)  # Executing the query
        history = cursor.fetchall()  # Fetching the results
        conn.close()  # Closing the connection

        # Update UI
        self.history_box.clear()  # Clearing the text browser
        if history:
            for entry in history:
                timestamp, product_url, status = entry  # Unpacking the entry
                self.history_box.append(f"{timestamp} - {product_url} - {status}")  # Adding the entry to the text browser
        else:
            self.history_box.append("No matching records found.")  # Adding a message if no records found

    def export_history_to_csv(self):
        """ Export purchase history to a CSV file. """
        conn = sqlite3.connect(DB_FILE)  # Connecting to the database
        cursor = conn.cursor()  # Creating a cursor
        cursor.execute("SELECT timestamp, product_url, status FROM bot_actions WHERE username=?", (self.username,))  # Executing the query
        history = cursor.fetchall()  # Fetching the results
        conn.close()  # Closing the connection

        if not history:
            QMessageBox.warning(self, "Export Failed", "No purchase history to export.")  # Showing a warning if no history
            return

        filename = f"{self.username}_purchase_history.csv"  # Defining the filename
        with open(filename, "w", newline="", encoding="utf-8") as file:  # Opening the file
            writer = csv.writer(file)  # Creating a CSV writer
            writer.writerow(["Timestamp", "Product URL", "Status"])  # Writing the header
            writer.writerows(history)  # Writing the history

        QMessageBox.information(self, "Export Successful", f"History saved as {filename}")  # Showing a success message