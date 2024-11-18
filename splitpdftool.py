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
        self.startLable.setText("start Num: ")
        self.endLable = QLabel()
        self.endLable.setText("end Num: ")

        self.startNumText = QLineEdit(self)
        self.startNumText.setPlaceholderText("Start Num")
        self.startNumText.setFixedSize(150, 40)

        self.endNumText = QLineEdit(self)
        self.endNumText.setPlaceholderText("End Num")
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
            self.tipsLabel.setText("Warning: Use book mark to split")
        else:
            self.bookMark = 0
            self.tipsLabel.setText("Do not Use book mark to split")

        print(f"self.bookmark: {self.bookMark}")

    def open_new_window(self):
        print("click button")
        pass

    def openDataFileDialog(self):
        # 打开文件对话框，获取文件路径
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle('Open File')
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter('All Files (*);;Text Files (*.txt)')
        file_dialog.rejected.connect(self.handleCancel)

        if file_dialog.exec_():  # 显示模态对话框
            file_path = file_dialog.selectedFiles()[0]
            # 如果选择了文件，则在输入框中显示文件名
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
        startNumStr = self.startNumText.text()
        self.startPage = int(startNumStr)
        endNumStr = self.endNumText.text()
        self.endPage = int(endNumStr)

        print(f"outpfile: {self.outputFile}")
        print(f"startPage: {self.startPage}")
        print(f"end: {self.endPage}")
        """
        从 PDF 文件中提取指定页范围，并保留对应的目录（书签）。

        :param input_pdf: 输入 PDF 文件路径
        :param output_pdf: 输出 PDF 文件路径
        :param start_page: 起始页（从 1 开始）
        :param end_page: 结束页（从 1 开始，包含该页）
        """
        # 打开输入 PDF 文件
        doc = fitz.open(self.inputFile)
        # 创建一个空的 PDF 文档用于存储选定页
        new_doc = fitz.open()

        # 调整页码为 0 基础
        start_page_index = self.startPage - 1
        end_page_index = self.endPage - 1

        # 提取选定页到新 PDF
        for page_num in range(start_page_index, end_page_index + 1):
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

        # 提取并调整书签
        if self.bookMark == 1:
            bookmarks = []
            for bmk in doc.get_toc():
                # 书签格式：[level, title, page_number]
                level, title, page = bmk
                if self.startPage <= page <= self.endPage:  # 如果书签对应页在范围内
                    bookmarks.append([level, title, page - start_page_index])
            # 添加书签到新 PDF
            if bookmarks:
                new_doc.set_toc(bookmarks)

        # 保存并关闭文件
        new_doc.save(self.outputFile)
        new_doc.close()
        doc.close()
        str = "success split to " +self.outputFile
        self.showInfoLabel.setText(str)
        #print(f"成功提取第 {self.startPage} 到第 {self.endPage} 页，并保留目录，保存为 {self.outputFile}")
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