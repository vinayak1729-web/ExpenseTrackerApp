import sys
from PyQt6.QtWidgets import QApplication , QMessageBox
from app import ExpenseTracker
from database import init_db
def main():
    app = QApplication(sys.argv)
    if not init_db("expense.db"):
        QMessageBox.critical(None,"Error","Could Not Load Your Database")
        sys.exit(1)

    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec())


if __name__ =="__main__":
    main()
