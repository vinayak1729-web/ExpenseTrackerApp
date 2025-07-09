#ALL SQL STUFF

from PyQt6.QtSql import QSqlDatabase ,QSqlQuery

def init_db(Expense_db):
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(Expense_db)
    
    if not database.open():
        return False
    
    query = QSqlQuery()
    query.exec("""
            CREATE TABLE IF NOT EXISTS expenses(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               date TEXT ,
               category TEXT,
               amount REAL ,
               description TEXT
               )

            """)