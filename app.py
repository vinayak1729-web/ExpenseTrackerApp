from PyQt6.QtWidgets import*
from PyQt6.QtCore import QDate , Qt 
from database import fetch_expenses , add_expenses , delete_expenses


class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.load_table_data()

    def settings(self):
        self.setGeometry(300,300,550,500)
        self.setWindowTitle("Expense Tracker App")

#design

    def initUI(self):
        #Create all objects 
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount =QLineEdit()
        self.description = QLineEdit()
        self.btn_add = QPushButton("Add Expense")
        self.btn_delete = QPushButton("Delete Expense")
        self.table = QTableWidget(0,5)
        self.table.setHorizontalHeaderLabels(["ID","DATE","CATEGORY","AMOUNT","DESCRIPTION"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.populate_dropdown()
        self.btn_add.clicked.connect(self.add_expense)
        self.btn_delete.clicked.connect(self.delete_expense)
        #EDIT table with 

        # add widgets to a layout ( row / column )
        self.setup_layout()

    def setup_layout(self):
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        #Row 1 
        row1.addWidget(QLabel("Date"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.dropdown)

        #row 2 
        row2.addWidget(QLabel("Amount"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description"))
        row2.addWidget(self.description)
        
        #row3
        row3.addWidget(self.btn_add)
        row3.addWidget(self.btn_delete)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)

        self.setLayout(master)
    
    def populate_dropdown(self):
        categories = ["Food","Stock","Entertainment","Travel","Shopping"]
        self.dropdown.addItems(categories)

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def load_table_data(self):
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        for row_idx , expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for col_indx,data in enumerate(expense):
                self.table.setItem(row_idx,col_indx,QTableWidgetItem(str(data)))

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category=self.dropdown.currentText() #q combo
        amount=self.amount.text() #q line
        description = self.description.text()
        
        if not amount or not description :
            QMessageBox.warning(self,"Input Error","Amount and Description Can not be Empty")
            return 
        if add_expenses(date,category,amount,description):
            self.load_table_data()
            self.clear_inputs()
        else: 
            QMessageBox.critical(self,"Error,failed to add expenses")

    def delete_expense(self):
        selectedRow = self.table.currentRow()
        if selectedRow == -1:
            QMessageBox.warning(self, "Selection Error", "You need to choose a row to delete it.")
            return
        
        # Check if the item exists to avoid AttributeError
        item = self.table.item(selectedRow, 0)
        if not item:
            QMessageBox.warning(self, "Error", "Invalid row selected.")
            return
        
        expense_id = int(item.text())
        confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to delete this expense?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            if delete_expenses(expense_id):
                self.load_table_data()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete expense. Please try again.")
