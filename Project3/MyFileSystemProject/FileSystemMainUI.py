import sys
from FileSystemClass import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QMainWindow, QMessageBox, QInputDialog, QTreeView, QAbstractItemView, QMenu
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QTextOption, QCursor

localFileName = "localFile"

class FileSystemMainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_system = fileSystem(localFileName)
        self.curDir = []    # 当前文件目录
        self.selectFile = None  # 当前被选择文件
        self.selectDir = None   # 当前被选择文件夹
        self.root = folderNode("", datetime.now())
        self.root.folderChildren.append(self.file_system._fileTree.root)
        self.setupUI()

    def setupUI(self):
        self.resize(800, 600)
        self.setWindowTitle("文件系统")

        # 菜单栏
        menu = self.menuBar()
        menu.setStyleSheet("QMenu::item {padding: 8px 16px;} QMenu::item:selected {background-color: #007bff; color: #fff;")

        fileMenu = menu.addMenu("文件")
        fileMenu.setStyleSheet(
            "QMenu::item {padding: 8px 16px;} QMenu::item:selected {background-color: #007bff; color: #fff;}")
        fileMenu.addAction(QIcon("static/format.png"), "格式化", self.formatting)
        fileMenu.addAction(QIcon("static/save.png"), "保存", self.saveToLocal)

        createMenu = menu.addMenu("创建")
        createMenu.setStyleSheet(
            "QMenu::item {padding: 8px 16px;} QMenu::item:selected {background-color: #007bff; color: #fff;}")
        createMenu.addAction(QIcon("static/createFolder.png"), "创建文件夹", self.createFolder)
        createMenu.addAction(QIcon("static/createFile.png"), "创建文件", self.createFile)

        deleteMenu = menu.addMenu("删除")
        deleteMenu.setStyleSheet(
            "QMenu::item {padding: 8px 16px;} QMenu::item:selected {background-color: #007bff; color: #fff;}")
        deleteMenu.addAction(QIcon("static/deleteFolder.png"), "删除文件夹", self.deleteFolder)
        deleteMenu.addAction(QIcon("static/deleteFile.png"), "删除文件", self.deleteFile)

        renameMenu = menu.addMenu("重命名")
        renameMenu.setStyleSheet(
            "QMenu::item {padding: 8px 16px;} QMenu::item:selected {background-color: #007bff; color: #fff;}")
        renameMenu.addAction(QIcon("static/renameFolder.png"), "重命名文件夹", self.renameFolder)
        renameMenu.addAction(QIcon("static/renameFile.png"), "重命名文件", self.renameFile)
        _widget = QWidget()

        verticalLayout = QVBoxLayout()

        _widget.setLayout(verticalLayout)
        self.setCentralWidget(_widget)

        #  路径栏
        self.pathLable = QLabel("/ ".join(self.curDir))
        self.updatePathLabel()
        self.pathLable.setStyleSheet("font-size: 18px; color: #333; font-weight: bold; border-radius: 1px;")
        verticalLayout.addWidget(self.pathLable)

        horiLayout = QHBoxLayout()
        # 文件树
        self.fileTreeView = QTreeView()
        self.updateFileTree()
        self.fileTreeView.expandAll()
        self.fileTreeView.setStyleSheet(
            "QTreeView::item {padding: 4px 8px;} QTreeView::item:selected {background-color: #007bff; color: #fff;}")
        horiLayout.addWidget(self.fileTreeView)
        verticalLayout.addLayout(horiLayout)

        # 文件名展示
        self.nameLabel = QLabel("打开文件名：未选择文件或打开的是文件夹")
        self.nameLabel.setStyleSheet("font-size: 20px; color: #555; font-weight: bold; margin-bottom: 10px;")

        # 文件内容展示
        ContentLabel = QLabel("当前打开文件内容：")
        ContentLabel.setStyleSheet("font-size: 20px; color: #555; font-weight: bold; margin-bottom: 10px;")
        # ContentLabel.setAlignment(QtCore.Qt.Alignment)

        # 文件文本编辑框
        self.textEdit = QPlainTextEdit()
        self.textEdit.setStyleSheet("font-family: Arial; font-size: 14px;")
        self.textEdit.setWordWrapMode(QTextOption.WrapAnywhere)
        self.textEdit.setStyleSheet("font-size: 14px; color: #333; background-color: #f5f5f5; border: 1px solid #ccc;")


        # 保存按钮
        self.saveButton = QPushButton("保存")
        self.saveButton.setStyleSheet("background-color: #007bff; color: #fff; padding: 6px 12px; border-radius: 4px;")
        self.saveButton.clicked.connect(self.saveFile)

        # 文件信息Layout
        self.fileInfoLabel = QLabel()
        self.fileInfoLabel.setStyleSheet("font-size: 16px; color: #666; border: 1px solid grey;")


        # 文本编辑Layout
        verticalLayout2 = QVBoxLayout()
        verticalLayout2.addWidget(self.nameLabel)
        verticalLayout2.addWidget(ContentLabel)
        verticalLayout2.addWidget(self.textEdit)
        verticalLayout2.addWidget(self.fileInfoLabel)
        verticalLayout2.addWidget(self.saveButton)
        horiLayout.addLayout(verticalLayout2)

    def updateNameLabel(self):
        if self.selectFile is not None:
            self.nameLabel.setText("打开文件名：" + self.selectFile.fileName)
        else:
            self.nameLabel.setText("打开文件名：未选择文件或打开的是文件夹")



    def updatePathLabel(self):
        self.pathLable.setText("> ".join(self.curDir))

    # 构建适用于QTreeView的树模型
    def buildQTreeModel(self) -> QStandardItemModel:
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['名称'])
        rootItem = QStandardItem(self.file_system._fileTree.root.folderName)
        model.appendRow(rootItem)
        self.addItemOnQTree(rootItem, self.file_system._fileTree.root)
        return model

    def addItemOnQTree(self, model, dirNode: folderNode):
        for it in dirNode.folderChildren:
            childItem = QStandardItem(it.folderName)
            self.addItemOnQTree(childItem, it)
            model.appendRow(childItem)
        for it in dirNode.FCBChildren:
            model.appendRow(QStandardItem(it.fileName))

    # 鼠标点击左侧条目，展开选中的文件夹，打开所选的文件
    def clickItem(self, ptr: QModelIndex):
        reverseCurPath = []
        fileOrder = ptr.row()  # 保存原有文件位置索引

        while ptr.data() is not None:
            reverseCurPath.append(ptr.data())
            ptr = ptr.parent()

        self.curDir = list(reversed(reverseCurPath))

        cursor = self.root
        for i in range(len(self.curDir) - 1):
            cursor = next((x for x in cursor.folderChildren if x.folderName == self.curDir[i]))

        # 最后一项可能是文件夹或文件 通过索引判断 位置在前为文件 在后为文件夹
        if len(cursor.folderChildren) - 1 < fileOrder:
            self.selectFile = cursor.FCBChildren[fileOrder - len(cursor.folderChildren)]
            print("file ", self.selectFile.fileName)
            self.selectDir = cursor  # 同时获得所在文件夹
        else:
            self.selectDir = cursor.folderChildren[fileOrder]
            print("dir ", self.selectDir.folderName)
            self.selectFile = None

        self.updatePathLabel()
        self.updateFileInfoLable()
        self.updateTextEdit()
        self.updateNameLabel()

        if self.selectFile is not None:
            self.saveButton.setEnabled(True)
        else:
            self.saveButton.setEnabled(False)

    # 右击动作
    def rightClickItem(self):
        if self.selectDir is None and self.selectFile is None:
            return
        rightClickMenu = QMenu()
        if self.selectFile is not None:
            rightClickMenu.addAction(QIcon('static/deleteFile.png'), "删除文件", self.deleteFile)
            rightClickMenu.addAction(QIcon('static/renameFile.png'), "重命名文件", self.renameFile)
        elif self.selectDir is not None:
            rightClickMenu.addAction(QIcon('static/createFile.png'), "创建文件", self.createFile)
            rightClickMenu.addAction(QIcon('static/createFolder.png'), "创建文件夹", self.createFolder)
            rightClickMenu.addAction(QIcon('static/deleteFolder.png'), "删除文件夹", self.deleteFolder)
            rightClickMenu.addAction(QIcon('static/renameFolder.png'), "重命名文件夹", self.renameFolder)
        rightClickMenu.exec_(QCursor.pos())
        rightClickMenu.show()


    def updateFileInfoLable(self):
        if self.selectDir is not None:
            self.fileInfoLabel.setText("文件夹 " + self.selectDir.folderName + " 含有" + str(self.selectDir.renewSize()) + " 个项目\n创建于 " +
                                str(self.selectDir.createTime) + "，修改于 " + str(self.selectDir.modifyTime))
            if self.selectFile is not None:
                self.fileInfoLabel.setText(self.fileInfoLabel.text() + "\n选择文件 " + self.selectFile.fileName + " 大小为" + str(self.selectFile.length) +
                                    "\n创建于 " + str(self.selectFile.creatTime) + ", 修改于" + str(self.selectFile.modifyTime))
        else:
            self.fileInfoLabel.setText("未选择文件/文件夹对象")

    def updateTextEdit(self):
        if self.selectFile is not None:
            self.textEdit.setEnabled(True)
            self.textEdit.setPlainText(self.file_system.openFCB(self.selectFile))
        else:
            self.textEdit.setPlainText("未选择文件对象")
            self.textEdit.setEnabled(False)

    def updateFileTree(self):
        self.fileTreeView.setModel(self.buildQTreeModel())
        self.fileTreeView.expandAll()
        # 增加点击事件
        self.fileTreeView.selectionModel().currentChanged.connect(self.clickItem)
        # 增加右击点击事件
        self.fileTreeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.fileTreeView.customContextMenuRequested.connect(self.rightClickItem)
        # 设为不可更改
        self.fileTreeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 鼠标滚轮设置
        self.fileTreeView.header().setStretchLastSection(True)
        self.fileTreeView.horizontalScrollBar().setEnabled(True)
        self.fileTreeView.verticalScrollBar().setEnabled(True)
        self.fileTreeView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.fileTreeView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def updateAllComponents(self):
        self.updateFileTree()
        self.updateFileInfoLable()
        self.updatePathLabel()
        self.updateTextEdit()
        self.updateNameLabel()

    # 保存文件
    def saveFile(self):
        content = self.file_system.openFCB(self.selectFile)
        if self.textEdit.toPlainText() == content:
            QMessageBox.warning(self, "警告", "无改动")
            return
        respose = QMessageBox.question(self, "确认", "是否保存？", QMessageBox.Yes | QMessageBox.No)
        if respose == QMessageBox.Yes:
            self.file_system.writeFCB(self.textEdit.toPlainText(), self.selectFile)
            self.updateFileInfoLable()

    # 格式化
    def formatting(self):
        respose = QMessageBox.question(self, '确认', "是否确实要格式化？", QMessageBox.Yes | QMessageBox.No)
        if respose == QMessageBox.Yes:
            self.file_system.format()
            self.selectFile = None
            self.selectDir = self.file_system._fileTree.root
            self.curDir = [self.selectDir.folderName]
            self.updateAllComponents()

    # 保存到本地
    def saveToLocal(self):
        respose = QMessageBox.question(self, "确认", "确定要保存到本地吗？", QMessageBox.Yes | QMessageBox.No)
        if respose == QMessageBox.Yes:
            self.file_system.saveLocally(localFileName)

    # 创建新文件
    def createFile(self):
        newName, res = QInputDialog.getText(self, '创建文件', '输入创建文件名：')
        if res:
            if newName == "":
                QMessageBox.warning(self, "警告", "未输入文件名")
            elif self.selectDir is None:
                QMessageBox.warning(self, "警告", "未选中文件")
            elif len([i for i in self.selectDir.FCBChildren if i.fileName == newName]) > 0:
                QMessageBox.warning(self, "警告", "文件名重复")
            else:
                self.file_system.createFCB(newName, self.selectDir)
                self.updateFileTree()
                self.updateAllComponents()

    # 新建文件夹
    def createFolder(self):
        newName, res = QInputDialog.getText(self, '创建文件', '输入创建文件名：')
        if res:
            if newName == "":
                QMessageBox.warning(self, "警告", "未输入文件夹名")
            elif self.selectDir is None:
                QMessageBox.warning(self, "警告", "未选中父文件夹")
            elif len([i for i in self.selectDir.folderChildren if i.folderName == newName]) > 0:
                QMessageBox.warning(self, "警告", "文件夹名重复")
            else:
                self.file_system.createDir(self.selectDir, newName, datetime.now())
                # self.updateFileTree()
                self.updateAllComponents()

    # 删除文件
    def deleteFile(self):
        if self.selectFile is None:
            QMessageBox.warning(self, "警告", "未选中删除的文件！")
        else:
            res = QMessageBox.question(self, '确认', "确认删除文件" + self.selectFile.fileName + "吗？", QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                self.file_system.deleteFCB(self.selectFile)
                self.selectFile = None
                self.updateAllComponents()

    # 删除文件夹
    def deleteFolder(self):
        if self.selectDir is None:
            QMessageBox.warning(self, "警告", "未选中待删除的文件夹！")
        elif self.selectDir == self.file_system._fileTree.root:
            QMessageBox.warning(self, "警告", "根文件夹不可删除！")
        else:
            res = QMessageBox.question(self, '确认', "确定要删除" + self.selectDir.folderName + "吗？", QMessageBox.Yes | QMessageBox.No)
            if res == QMessageBox.Yes:
                self.file_system.deleteFolder(self.selectDir)
                self.selectDir = None
                self.selectFile = None
                self.updateAllComponents()

    # 重命名文件
    def renameFile(self):
        if self.selectFile is None:
            QMessageBox.warning(self, "警告", "未选中重命名的文件！")
        else:
            newName, res = QInputDialog.getText(self, '重命名文件', '输入新文件名：')
            if res:
                if newName == "":
                    QMessageBox.warning(self, "警告", "未输入文件名")
                elif len([i for i in self.selectDir.FCBChildren if i.fileName == newName]) > 0:
                    QMessageBox.warning(self, "警告", "文件名重复")
                else:
                    self.file_system.renameFCB(self.selectFile, newName, self.selectDir)
                    self.updateAllComponents()

    def renameFolder(self):
        if self.selectDir is None:
            QMessageBox.warning(self, "警告", "未选中重命名的文件夹")
        else:
            newName, res = QInputDialog.getText(self, '重命名文件夹', '输入新文件夹名：')
            if res:
                if newName == "":
                    QMessageBox.warning(self, "警告", "未输入文件夹名")
                elif len([i for i in self.selectDir.folderChildren if i.folderName == newName]) > 0:
                    QMessageBox.warning(self, "警告", "文件夹名重复")
                else:
                    self.file_system.renameFolder(self.selectDir, newName)
                    self.updateAllComponents()

    # 关闭窗口后询问是否要保存
    def closeEvent(self, event):
        self.saveToLocal()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    UI = FileSystemMainUI()
    UI.show()
    sys.exit(app.exec_())



