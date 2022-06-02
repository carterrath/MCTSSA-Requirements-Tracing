import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QGridLayout, QVBoxLayout, QLineEdit, QPushButton, QTableView, QLabel, QHeaderView, QDialog, QListWidget, QListWidgetItem, QProgressBar, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from main3 import *


componenets_list = []
dictionary = main2()

class AppDemo(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        
        self.groupBoxLayout = QGridLayout()
        self.groupBox = QGroupBox() #group box surrounding all widgets
        self.groupBox.setStyleSheet( 'QGroupBox {'
                'font-size: 17px;'
                'background-color: cornflowerblue;'
                'color: gold; }'
                'QGroupBox:title {'
                'subcontrol-origin: margin;'
                'subcontrol-position: top center;'
                'padding-left: 10px;'
                'padding-right: 10px; }')

        self.groupBox.setFlat(False)
        self.groupBox.setLayout(self.groupBoxLayout)

        #gets dimensions of screen and fits app to window
        screen = app.primaryScreen()
        size = screen.size()
        width = size.width()
        height = size.height()
        self.resize(width, height)
        layout.addWidget(self.groupBox)

        self.setWindowTitle('Requirements Tracing')

        search = QLabel('Search') #search label
        search.setStyleSheet('background-color: red; color: gold; font-size: 40px;')
        search.setAlignment(Qt.AlignHCenter)
        self.groupBoxLayout.addWidget(search, 0 ,0 ,1, 3)
        
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)

        results = QLabel('Results') #results label
        results.setStyleSheet('background-color: red; color: gold; font-size: 40px;')
        results.setAlignment(Qt.AlignHCenter)
        self.groupBoxLayout.addWidget(results, 0,3, 1, 3)

        store = QLabel('Store') #results label
        store.setStyleSheet('background-color: red; color: gold; font-size: 40px;')
        store.setAlignment(Qt.AlignHCenter)
        self.groupBoxLayout.addWidget(store, 0,6, 1, 3)

        search = QLabel('Enter Query:') #search label
        search.setStyleSheet('color: gold; font-size: 30px;')
        self.groupBoxLayout.addWidget(search, 1,0)

        self.search_field = QLineEdit() #text bar
        self.search_field.setStyleSheet('font-size: 20px; height: 50px; background-color: white; color: black')
        self.groupBoxLayout.addWidget(self.search_field, 2,0, 1, 2)

        search_button = QPushButton('Go') #search button
        search_button.setStyleSheet('color: gold; background-color: red; font-size: 20px;')
        self.groupBoxLayout.addWidget(search_button, 2,2)
        search_button.clicked.connect(self.search)

        export_button = QPushButton('Export') #export button
        export_button.setStyleSheet('color: gold; background-color: red; font-size: 20px;')
        self.groupBoxLayout.addWidget(export_button, 11,8)
        
        self.file_name = QLineEdit() #file name
        self.file_name.setStyleSheet('font-size: 20px; height: 50px; background-color: white; color: black')
        self.groupBoxLayout.addWidget(self.file_name, 11, 6, 1, 2)

        self.results_list = QListWidget() #results section
        self.results_list.setStyleSheet('font-size: 25px; background-color: cornflowerblue; color: white')
        self.groupBoxLayout.addWidget(self.results_list, 1, 3, 10, 3)
        self.results_list.setDragEnabled(True)

        self.store_list = QListWidget() #store section
        self.store_list.setStyleSheet('font-size: 25px; background-color: cornflowerblue; color: white')
        self.groupBoxLayout.addWidget(self.store_list, 1, 6, 10, 3)
        self.store_list.setAcceptDrops(True)

        undo_button = QPushButton('Delete Selected') #undo button
        undo_button.setStyleSheet('color: gold; background-color: red; font-size: 20px;')
        self.groupBoxLayout.addWidget(undo_button, 12,8)
        undo_button.clicked.connect(self.delete)

        self.setLayout(layout)

        self.results_list.itemDoubleClicked.connect(self.launchPop)
        self.store_list.itemDoubleClicked.connect(self.launchPop)
        export_button.clicked.connect(self.save)
        # export_button.connect(export_button, SIGNAL('clicked()'), self.remove)

    #initiated when go button is pressed, this function searches for a specific requirement typed by user in each component
    def search(self):

        #empty both lists at the start to avoid repetition
        componenets_list.clear()
        self.results_list.clear()

        #map both keys and values from dictionary
        for key, values in dictionary.items():
            #loop through values array for each requirement
            for requirement in values:
                #if specified requirement is in requirement
                if self.search_field.text() in requirement:
                    #add component name if not already in component list
                    if key not in componenets_list:
                        self.results_list.addItem(key)
                        componenets_list.append(key)  
        if self.results_list.count() == 0:
            self.results_list.addItem("No results found")                 
    def launchPop(self, item):
        if item:
            screen = app.primaryScreen()
            size = screen.size()
            width = size.width()
            height = size.height()
            self.mainLayout = QVBoxLayout()
            self.table = TableWidget()
            self.table.setStyleSheet('font-size: 15px; background-color: cornflowerblue; color: white')
            self.table.resize(width, height)
            self.mainLayout.addWidget(self.table)
            for key, values in dictionary.items():
                    for i in range(len(dictionary[item.text()])):
                        if key == item.text():
                            self.table.insertRow(i)
                            self.table.setItem(i, 0, QTableWidgetItem(values[i]))
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
            self.table.show()
    def delete(self):
        listItems = self.store_list.selectedItems()
        if not listItems: return
        for item in listItems:
            self.store_list.takeItem(self.store_list.row(item))
    def save(self, item):
        
        file = self.file_name.text() + ".txt"
        if not self.store_list: return
        f = open(file, 'w')
        # j = self.store_list.count()
        #self.store_list.item()
        #while j >0:
        j = 0
        # print(self.store_list.count())
        for j in range(self.store_list.count()):
            for key, values in dictionary.items():
                # for i in range(len(dictionary[item.text()])):
                if key == self.store_list.item(j).text():
                        my_text = key 
                        f.write(my_text)
                        f.write('\n')
                for i in range(len(dictionary[self.store_list.item(j).text()])):
                    if key == self.store_list.item(j).text():
                        num = i+1
                        my_text = str(num) + " "
                        f.write(my_text)
                        my_text = values[i]
                        f.write(my_text)
                        f.write('\n')
                        # self.store_list.takeItem(item)
            
                            
        

class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__(1, 1)

        self.setHorizontalHeaderLabels([' '])
        self.setWindowTitle('REQUIREMENTS')
        
        self.setRowCount(0)
        self.verticalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(250)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')