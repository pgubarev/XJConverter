import sys
import json
import os

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog

import mainForm
from XJOptions import XJOptions, XJOptionsEncoder
from XJConverter import XJConverter
from XJUtils import XJUtils


class XJConverterApp(QtWidgets.QMainWindow, mainForm.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.saveOptions.clicked.connect(self.hide_message)
        self.filesButton.clicked.connect(self.hide_message)
        self.dirButton.clicked.connect(self.hide_message)

        self.checkValue.clicked.connect(self.hide_message)
        self.checkLogs.clicked.connect(self.hide_message)
        self.asArray.clicked.connect(self.hide_message)
        self.clearLogs.clicked.connect(self.hide_message)
        self.checkRemove.clicked.connect(self.hide_message)
        self.checkXML.clicked.connect(self.hide_message)
        self.checkZIP.clicked.connect(self.hide_message)

        self.saveOptions.clicked.connect(self.save_convert_options)
        self.filesButton.clicked.connect(self.open_files_dialog)
        self.dirButton.clicked.connect(self.open_dir_dialog)

        self.read_options()
        self.messageText.setText("")

    def open_dir_dialog(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.DontConfirmOverwrite | QFileDialog.ReadOnly
        dir_cur = QtCore.QDir.currentPath()
        directory = QFileDialog.getExistingDirectory(None, "Find Files", dir_cur, options)

        if directory != '':
            parser = XJConverter(self.get_options())
            result = parser.convert_directory(directory + '\\')

            self.set_result_message(result, parser.get_error_message())

    def open_files_dialog(self):
        options = QFileDialog.DontResolveSymlinks | QFileDialog.DontConfirmOverwrite | QFileDialog.ReadOnly
        dir_cur = QtCore.QDir.currentPath()
        files = QFileDialog.getOpenFileNames(None, "Find Files", dir_cur, "", "", options)[0]

        if files:
            parser = XJConverter(self.get_options())
            result = parser.convert_files(files)

            self.set_result_message(result, parser.get_error_message())

    def save_convert_options(self):
        options = self.get_options()
        data = json.dumps(options, cls=XJOptionsEncoder)
        XJUtils.write_data_to_file(data, os.getcwd() + '\\options.json')

    def read_options(self):
        if os.path.isfile(os.getcwd() + '\\options.json'):
            file = open(os.getcwd() + '\\options.json', 'r')
            string = file.read()
            file.close()
            data = json.loads(string)
            self.checkValue.setChecked(data['emptyValue'])
            self.checkLogs.setChecked(data['enabledLogs'])
            self.asArray.setChecked(data['asArray'])
            self.clearLogs.setChecked(data['clearLogs'])
            self.checkRemove.setChecked(data['removeXML'])
            self.checkXML.setChecked(data['parseXML'])
            self.checkZIP.setChecked(data['parseZip'])

    def get_options(self):
        options = XJOptions()
        options.emptyValue = self.checkValue.isChecked()
        options.enabledLogs = self.checkLogs.isChecked()
        options.asArray = self.asArray.isChecked()
        options.clearLogs = self.clearLogs.isChecked()
        options.removeXML = self.checkRemove.isChecked()
        options.parseXML = self.checkXML.isChecked()
        options.parseZip = self.checkZIP.isChecked()
        return options

    def set_result_message(self, result, message=None):
        if result:
            self.messageText.setStyleSheet("color: green")
            self.messageText.setText("Success.")
        else:
            self.messageText.setStyleSheet("color: red")
            self.messageText.setText(message)

    def hide_message(self):
        self.messageText.setText("")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = XJConverterApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
