#!/home/pt/myenv/bin/python3
import sys
import os
from PyQt5.QtWidgets import QHBoxLayout, QApplication, QFileDialog,QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
import fitz  # PyMuPDF


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.inputFile=""
        self.outputFile="split"
        self.startPage=1
        self.endPage=10
        self.bookMark = 0
        self.setWindowTitle("Main Window")
        self.setGeometry(400, 400, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setSpacing(30)

        self.startLable = QLabel()
        self.startLable.setText("start page: ")
        self.endLable = QLabel()
        self.endLable.setText("end page: ")

        self.startNumText = QLineEdit(self)
        self.startNumText.setPlaceholderText("Start page")
        self.startNumText.setFixedSize(150, 40)

        self.endNumText = QLineEdit(self)
        self.endNumText.setPlaceholderText("End page")
        self.endNumText.setFixedSize(150, 40)

        hboxText = QHBoxLayout()
        hboxText.setSpacing(20)
        hboxText.setContentsMargins(20, 20, 20, 20)
        hboxText.addWidget(self.startLable)
        hboxText.addWidget(self.startNumText)
        hboxText.addWidget(self.endLable)
        hboxText.addWidget(self.endNumText)
        layout.addLayout(hboxText)

        hboxOutput = QHBoxLayout()
        self.outputLabel = QLabel()
        self.outputLabel.setText("OutPut file: ")
        self.outputText = QLineEdit()
        self.outputText.setPlaceholderText("Enter output file name")
        self.outputText.setFixedSize(450, 40)
        hboxOutput.setSpacing(20)
        hboxOutput.setContentsMargins(20, 20, 20, 20)
        hboxOutput.addWidget(self.outputLabel, alignment=Qt.AlignLeft)
        hboxOutput.addStretch()
        hboxOutput.addWidget(self.outputText, alignment=Qt.AlignLeft)
        layout.addLayout(hboxOutput)

        hboxButton = QHBoxLayout()
        hboxButton.setSpacing(50)
        self.openfileButton = QPushButton("Open File", self)
        self.openfileButton.clicked.connect(self.openDataFileDialog)
        self.openfileButton.setFixedSize(150, 40)

        self.xSplitButton = QPushButton("X Split", self)
        self.xSplitButton.clicked.connect(self.split_pdf_with_bookmarks)
        self.xSplitButton.setFixedSize(150, 40)

        self.bookMarkButton = QPushButton("Use book Mark", self)
        self.bookMarkButton.clicked.connect(self.setBookMark)
        self.bookMarkButton.setFixedSize(150, 40)

        hboxButton.addWidget(self.openfileButton)
        hboxButton.addWidget(self.xSplitButton)
        hboxButton.addWidget(self.bookMarkButton)

        layout.addLayout(hboxButton)
        self.tipsLabel = QLabel("", self)
        self.tipsLabel.setText("Default: do not use book mark")
        layout.addWidget(self.tipsLabel)

        self.showInfoLabel = QLabel("", self)
        layout.addWidget(self.showInfoLabel)

        central_widget.setLayout(layout)

    def setBookMark(self):
        if self.bookMark == 0:
            self.bookMark = 1
            self.tipsLabel.setText("Warning: Use book mark to split, maybe fail")
        else:
            self.bookMark = 0
            self.tipsLabel.setText("Do not Use book mark to split")

        print(f"self.bookmark: {self.bookMark}")

    def open_new_window(self):
        print("click button")
        pass

    def openDataFileDialog(self):
        #open file dialog and get the pdf file path
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle('Open File')
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter('All Files (*);;Text Files (*.txt)')
        file_dialog.rejected.connect(self.handleCancel)

        if file_dialog.exec_():  #show the module dialog
            file_path = file_dialog.selectedFiles()[0]
            # If select one file, and show in the frame
            file_name = os.path.basename(file_path)
            str = "need x split file is " + file_name
            self.showInfoLabel.setText(str)
            self.inputFile = file_path
        pass

    def handleCancel(self):
        print("dialog cancled")
        pass


    def split_pdf_with_bookmarks(self):
        if self.outputText.text().strip() == "":
            print("use default output name")
            self.outputFile = "split.pdf"
        else:
            self.outputFile = self.outputText.text() + ".pdf"

        if self.inputFile == "":
            self.showInfoLabel.setText("No pdf is opened, please open one pdf file")
            return
        startNumStr = self.startNumText.text()
        self.startPage = int(startNumStr)
        endNumStr = self.endNumText.text()
        self.endPage = int(endNumStr)

        print(f"outpfile: {self.outputFile}")
        print(f"startPage: {self.startPage}")
        print(f"end: {self.endPage}")
        """
        special pages and get index

        :param input_pdf: pdf file path
        :param output_pdf: output file name
        :param start_page: start page
        :param end_page:  end page
        """
        # open input pdf file
        doc = fitz.open(self.inputFile)
        # creat new pdf file to save special pages
        new_doc = fitz.open()

        # select page to zero
        start_page_index = self.startPage - 1
        end_page_index = self.endPage - 1

        # get special pages to new PDF
        for page_num in range(start_page_index, end_page_index + 1):
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

        # get bookmark
        if self.bookMark == 1:
            bookmarks = []
            for bmk in doc.get_toc():
                # bookmark format：[level, title, page_number]
                level, title, page = bmk
                if self.startPage <= page <= self.endPage:  # if bookmark in start to end pages
                    bookmarks.append([level, title, page - start_page_index])
            # add new bookmark to pdf
            if bookmarks:
                new_doc.set_toc(bookmarks)

        # save and close file
        new_doc.save(self.outputFile)
        new_doc.close()
        doc.close()
        str = "success split to " +self.outputFile
        self.showInfoLabel.setText(str)
        #print(f"success to get from {self.startPage} to {self.endPage} pages，and save as {self.outputFile}")
class NewWindow(QWidget):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle("New Window")
        self.setGeometry(150, 150, 200, 150)

        layout = QVBoxLayout()
        label = QLabel(f"You entered: {text}", self)
        layout.addWidget(label)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
