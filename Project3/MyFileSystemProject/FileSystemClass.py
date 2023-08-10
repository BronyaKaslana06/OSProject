from datetime import datetime
from bitarray import bitarray
import pickle
import os

BLOCK_NUM = 2**10   # 块数
BLOCK_SIZE = 4      # 块大小
FAT_FREE = -2  # 表示FAT表中此块未被使用
FAT_END = -1  # 表示为FAT表中链表结尾
SPACE_OCCUPY = 1  # 磁盘空间被占用
SPACE_FREE = 0  # 磁盘空间未被占用


#  文件控制块
class FCB:
    def __init__(self, name, createTime, len, startPos=None):
        self.fileName = name
        self.creatTime = createTime
        self.modifyTime = createTime
        self.length = len
        self.startAddress = startPos

#  FAT
class FAT:
    def __init__(self):
        self.blockNum = BLOCK_NUM
        self.table = []
        for i in range(BLOCK_NUM):
            self.table.append(FAT_FREE)

#  模拟磁盘，记录文件内容
class hardDisk(list):
    def __init__(self):
        super(hardDisk, self).__init__()
        for i in range(BLOCK_NUM):
            self.append("")

#  空闲空间，采用位图方式管理
#  0代表未被占用，1代表被占用
class freeBlock:
    def __init__(self):
        self.bitmap = bitarray(BLOCK_NUM)
        self.bitmap.setall(0)


#  文件夹节点
class folderNode:
    def __init__(self, name, creatTime):
        self.folderName = name
        self.createTime = creatTime
        self.modifyTime = creatTime
        self.folderChildren = []    # 记录作为文件夹的孩子结点
        self.FCBChildren = []       # 记录作为真实文件的孩子结点
        # self.size = len(self.folderChildren) + len(self.FCBChildren)

    def renewSize(self):
        size = len(self.folderChildren) + len(self.FCBChildren)
        return size

#  文件树
class fileTree:
    def __init__(self):
        self.root = folderNode("/", datetime.now())

#  真实文件系统
class fileSystem:
    def __init__(self, system_info_file=None):
        if system_info_file and os.path.exists(system_info_file):
            with open(system_info_file, "rb") as f:
                self._fileTree = pickle.load(f)
                self._freeBlock = pickle.load(f)
                self._hardDisk = pickle.load(f)
                self._fat = pickle.load(f)
        else:  # 否则手动创建
            print("未找到文件")
            self._fileTree = fileTree()
            self._freeBlock = freeBlock()
            self._hardDisk = hardDisk()
            self._fat = FAT()
            self.createDir(self._fileTree.root, "一级文件夹", datetime.now())
            self.createDir(self._fileTree.root.folderChildren[0], "二级文件夹", datetime.now())
            self.createDir(self._fileTree.root.folderChildren[0].folderChildren[0], "三级文件夹", datetime.now())
            self.createFCB("文件1与根文件夹平级", self._fileTree.root)
            self.createFCB("文件2与二级文件夹平级", self._fileTree.root.folderChildren[0])
            self.createFCB("文件3与根文件夹平级", self._fileTree.root)
            print("文件初创完成")

    # 根据bitmap找到空闲块
    def findFreeBlock(self):
        return self._freeBlock.bitmap.find(0)

    # 建立文件目录
    # 传入参数分别为：要建立子文件目录的文件夹节点，建立的子文件目录的名字，建立时间
    # return 0表明创建失败，return 1 表明创建成功
    def createDir(self, folder_node:folderNode, name, creatTime):
        for node in folder_node.folderChildren:
            if node.folderName == name:
                print("文件名已存在，创建失败")
                # return 0

        folder_node.folderChildren.append(folderNode(name, creatTime))
        folder_node.modifyTime = creatTime
        # return 1

    # 创建具体文件FCB
    def createFCB(self, name, dirNode: folderNode):
        if name not in dirNode.FCBChildren:
            dirNode.FCBChildren.append((FCB(name, datetime.now(), 0)))

    def renameFCB(self, fcb : FCB, newName: str, parentFolder:folderNode):
        fcb.fileName = newName
        fcb.modifyTime = datetime.now()
        parentFolder.modifyTime = datetime.now()

    #  清空文件夹内容
    #  传入参数为待清空文件夹节点
    def cleanDir(self, dir:folderNode):
        for node in dir.FCBChildren:
            self.deleteFCB(node)
        for node in dir.folderChildren:
            self.cleanDir(node)     # 递归删除文件夹

    # 删除文件，修改空闲空间标记
    def deleteFCB(self, fcb : FCB):
        ptr = fcb.startAddress
        if ptr is not None:
            while ptr != FAT_END:
                self._hardDisk[ptr] = ""
                self._freeBlock.bitmap[ptr] = 0
                nextPos = self._fat.table[ptr]
                self._fat.table[ptr] = 0
                ptr = nextPos
        self.recursiveDeleteFCB(fcb, self._fileTree.root)

    # 从根节点递归搜索到待删除的FCB并删除
    def recursiveDeleteFCB(self, fcb:FCB, folder_node:folderNode):
        if fcb in folder_node.FCBChildren:
            folder_node.FCBChildren.remove(fcb)
            return
        else:
            for node in folder_node.folderChildren:
                self.recursiveDeleteFCB(fcb, node)

    #  删除文件夹
    def deleteFolder(self, dir:folderNode):
        self.cleanDir(dir)
        ptr = self._fileTree.root
        q = [ptr]
        # 搜索
        while dir not in ptr.folderChildren and q!=[]:
            ptr = q.pop(0)
            q.extend(ptr.folderChildren)

        ptr.folderChildren.remove(dir)

    #  格式化，全部重置
    def format(self):
        print("格式化操作")
        self._fileTree.root.folderChildren = []
        self._fileTree.root.FCBChildren = []
        self._freeBlock = freeBlock()
        self._hardDisk = hardDisk()
        self._fat = FAT()

    # 重命名文件夹
    def renameFolder(self, dirNode: folderNode, name):
        dirNode.folderName = name
        dirNode.modifyTime = datetime.now()

    # 打开文件并返回数据
    def openFCB(self, fcb:FCB):
        if fcb.startAddress is None:
            return ""
        ptr = fcb.startAddress
        content = ""
        while ptr != FAT_END:
            content += self._hardDisk[ptr]
            ptr = self._fat.table[ptr]
        return content

    # 写文件，链接方式
    def writeFCB(self, content, fcb:FCB):
        fcb.length = len(content)
        fcb.modifyTime = datetime.now()
        curBlockIndex = FAT_END
        while content != "":
            nextBlockIndex = self.findFreeBlock()
            if nextBlockIndex == -1:
                print("没有足够空间")
                raise AssertionError("没有足够空间")
            if curBlockIndex == FAT_END:
                fcb.startAddress = nextBlockIndex
            else:
                self._fat.table[curBlockIndex] = nextBlockIndex

            self._hardDisk[nextBlockIndex] = content[:BLOCK_SIZE]
            content = content[BLOCK_SIZE:]
            self._freeBlock.bitmap[nextBlockIndex] = 1

            curBlockIndex = nextBlockIndex
            self._fat.table[curBlockIndex] = FAT_END

    # 将文件保存到本地
    def saveLocally(self, localFile:str):
        print("保存到本地")
        with open(localFile, "wb") as f:
            pickle.dump(self._fileTree, f)
            pickle.dump(self._freeBlock, f)
            pickle.dump(self._hardDisk, f)
            pickle.dump(self._fat, f)




