#ALL SQL STUFF

from PyQt6.QtSql import QSqlDatabase ,QSqlQuery
import logging

logging.basicConfig(
    filename='expense_tracker.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def init_db(db_name):
    """
    Initialize SQLite database and create expenses table.
    Returns True if successful, False otherwise.
    """
    
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)

    if not database.open():
            logging.error("Failed to open database")
            return False

    query = QSqlQuery()
        # Create expenses table
    query.exec("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        """)
    return True

def fetch_expenses():
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    expenses = []
    while query.next():
        expenses.append([query.value(i) for i in range(5)])  
    return expenses

def add_expenses(date,category,amount,description):
    query = QSqlQuery()
    query.prepare("""
            INSERT INTO expenses(date,category,amount,description)
            VALUES(?,?,?,?)  
                    """)
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    return query.exec()

def delete_expenses(expense_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id = ?")
    query.addBindValue(expense_id)
    return query.exec()
     
