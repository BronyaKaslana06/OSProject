from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractAnimation, QTimer

INF = 9999
FLOOR_NUM = 20  # 楼层数

#  乘客状态
PASSANGER_UP = 0  # 乘客上行
PASSANGER_DOWN = 1  # 乘客下行
PASSANGER_NONE = 2  # 乘客无动作

#  电梯状态
ELEV_UP = 0  # 电梯上行
ELEV_DOWN = 1  # 电梯下行
ELEV_STILL = 2  # 电梯静止

#  时间
RUN_TIME = 1    # 运行通过一层时间
WAIT_TIME = 3   # 等待接客时间
WAIT_TIME_2 = 4 # 开门后第一次等待（用于手动开门）
WAIT_TIME_3 = 5 # 开门后第二次等待（用于自动开门）

# 警报设置
AVAILABLE = 1   # 电梯可用
INAVAILABLE = 0 # 电梯不可用

# 按钮控制
OPEN_DOOR = 0   # 开门动作
CLOSE_DOOR = 1  # 关门动作

# 门控制
DOOR_OPENED = 1  # 门已开
DOOR_CLOSED = 0  # 门已关

# animation state of elevator
READY_START = 0  # 就绪运行
READY_STOP = 1  # 就绪停止

# 空状态
NOPE = 2  # 空状态

class Dispatcher:
    # n为电梯数量
    def __init__(self, UI):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateState)
        self.timer.start(1000)
        # 电梯数量
        self.elevNum = 5
        # UI界面
        self.elevUI = UI
        # 顺行列表和逆行列表
        self.comingList = []    # 每部电梯的顺行列表
        for i in range(self.elevNum):
            self.comingList.append([])
        self.reverseList = []   # 每部电梯的逆行列表
        for i in range(self.elevNum):
            self.reverseList.append([])

        # 标识电梯内部开关门按钮的状态
        self.doorButtonState = []
        for i in range(self.elevNum):
            self.doorButtonState.append(NOPE)
        # 每层楼的调度状况
        # 初始默认没有调度
        self.floorCmd = []
        for i in range(FLOOR_NUM):
            self.floorCmd.append(PASSANGER_NONE)

        # 电梯门状态
        self.doorState = []
        for i in range(5):
            self.doorState.append(DOOR_CLOSED)

        # 每个电梯的运行状态
        self.elevState = []
        for i in range(self.elevNum):
            self.elevState.append(ELEV_STILL)

        # 动画状态
        self.animationState = []
        for i in range(self.elevNum):
            self.animationState.append(NOPE)

        # 每个电梯的警报状态
        self.warnState = []
        for i in range(self.elevNum):
            self.warnState.append(AVAILABLE)

        # current floor of each elevator
        self.curFloor = []
        for i in range(self.elevNum):
            self.curFloor.append(0)

    # calculate running time
    # elevNo: the index of elevator
    # targetFloor: the target floor of the elevator
    def runTime(self, elevNo, targetFloor):
        # print("调用运行时间函数计算电梯{}的运行时间".format(elevNo))
        t = INF # 时间
        if self.elevState[elevNo] == ELEV_STILL:
            t = abs(self.curFloor[elevNo] - targetFloor) * RUN_TIME
        # elevator is not still
        else:
            # 顺行方向
            if (self.curFloor[elevNo] > targetFloor and self.elevState[elevNo] ==ELEV_DOWN) or (self.curFloor[elevNo] < targetFloor and self.elevState[elevNo] == ELEV_UP):
                # 记录是否在发出命令的顺行方向还有其他请求
                cnt = 0
                if self.elevState[elevNo] == ELEV_DOWN:
                    for it in self.comingList[elevNo]:
                        # 为了知道在targetFloor之前还有几个楼层需要停
                        if it > targetFloor:
                            cnt = cnt + 1
                        else:
                            break
                else:
                    for it in self.comingList[elevNo]:
                        # 为了知道在targetFloor之前还有几个楼层需要停
                        if it < targetFloor:
                            cnt = cnt + 1
                        else:
                            break
                t = abs(self.curFloor[elevNo] - targetFloor) * RUN_TIME + cnt * WAIT_TIME
            # 非顺行方向
            else:
                FinalFloor = self.comingList[elevNo][-1]    # 正向运行到的最后一层
                # 总时间=正向运行到最后一层的时间+电梯顺行停止时间+最后一层到目标楼层的时间
                t = abs(self.curFloor[elevNo] - FinalFloor) * RUN_TIME + len(self.comingList[elevNo]) * WAIT_TIME + abs(FinalFloor - targetFloor)

        # print("电梯{}运行时间计算结束".format(elevNo))
        return t

    # 外部控制函数
    # targetFloor:目标楼层  direction:电梯方向，上行/下行
    def externalCtrl(self, targetFloor, direction):
        print("调用外部控制函数")
        # 电梯运行时间
        runningTime = []
        for i in range(5):
            runningTime.append(INF)
        # 可用电梯列表
        availableElev = []
        # 向表中添加可用电梯
        for i in range(self.elevNum):
            if self.warnState[i] == AVAILABLE:
                availableElev.append(i)
        print("可用的电梯列表：", availableElev)
        if self.floorCmd[targetFloor] == PASSANGER_NONE:
            self.floorCmd[targetFloor] = direction
            for elevator in availableElev:
                # 计算各个电梯的运行时间
                runningTime[elevator] = self.runTime(elevator, targetFloor)  # 电梯的最小运行时间所对应的电梯索引号
            global minIndex
            minIndex = INF
            minIndex = runningTime.index(min(runningTime))
            print("调度电梯{}响应该命令".format(minIndex))
        # 处理正向逆向队列
        if self.comingList[minIndex]:
            # 反向的情况
            if (targetFloor >= self.curFloor[minIndex] and self.elevState[minIndex] == ELEV_DOWN) or (targetFloor <= self.curFloor[minIndex] and self.elevState[minIndex] == ELEV_UP):
                self.reverseList[minIndex].append(targetFloor)
                # 若电梯上行，则降序排列;反之正序排列
                if self.elevState[minIndex] == ELEV_UP:
                    self.reverseList[minIndex].sort(reverse=True)
                else:
                    self.reverseList[minIndex].sort(reverse=False)
            # 正向的情况
            else:
                self.comingList[minIndex].append(targetFloor)
                if self.elevState[minIndex] == ELEV_UP :
                    self.comingList[minIndex].sort(reverse=False)
                else:
                    self.comingList[minIndex].sort(reverse=True)
        # 需要初始化队列
        else:
            self.comingList[minIndex].append(targetFloor)
        print("外部响应处理结束，已处理完正向逆向队列")

    # 电梯内部控制
    def innerCtrl(self, elevNo, targetFloor):
        curFloor = self.curFloor[elevNo]
        print("内部控制，当前位置{}，目标楼层{}".format(self.curFloor[elevNo], targetFloor))
        # 目标楼层更高
        if targetFloor > curFloor:
            # 电梯为静止或上行状态，加入正向列表
            if self.elevState[elevNo] == ELEV_STILL or self.elevState[elevNo] == ELEV_UP:
                self.comingList[elevNo].append(targetFloor)
                self.comingList[elevNo].sort(reverse=False)
            # 电梯下行，加入逆向列表
            else:
                self.reverseList[elevNo].append(targetFloor)
                self.reverseList[elevNo].sort(reverse=False)
        # 目标楼层更低
        elif targetFloor < curFloor:
            # 电梯静止
            if self.elevState[elevNo] == ELEV_STILL:
                self.comingList[elevNo].append(targetFloor)
                self.comingList[elevNo].sort(reverse=True)
            # 电梯上行，加入逆向列表
            elif self.elevState[elevNo] == ELEV_UP:
                self.reverseList[elevNo].append(targetFloor)
                self.reverseList[elevNo].sort(reverse=True)
            # 电梯下行，加入正向列表，但由于是下行，所以要根据楼层降序排序
            else:
                self.comingList[elevNo].append(targetFloor)
                self.comingList[elevNo].sort(reverse=True)
        # 电梯就在目标楼层
        else:
            # 静止状态，开门
            if self.elevState[elevNo] == ELEV_STILL:
                self.doorCtrl(elevNo, OPEN_DOOR)
                # 模拟电梯内部楼层按钮复原
                self.elevUI.inLevelButtons[elevNo][targetFloor].setEnabled(True)
                self.elevUI.inLevelButtons[elevNo][targetFloor].setStyleSheet("font: 10pt \"AcadEref\";\n"
                                                                             "background-color: rgb(226, 226, 226);")
            # 非静止状态，加入逆向列表
            else:
                self.reverseList[elevNo].append(targetFloor)

    # 门控函数
    def doorCtrl(self, elevNo, cmd):
        # 保证电梯静止
        if self.elevState[elevNo] == ELEV_STILL:
            # 开门
            if cmd == OPEN_DOOR:
                self.warnState[elevNo] = INAVAILABLE    # 开门过程中禁用该电梯
                self.doorButtonState[elevNo] = OPEN_DOOR    # 电梯按钮置为开门状态
                self.doorState[elevNo] = DOOR_OPENED    # 更新门状态
                self.openDoorAnimation(elevNo)  # 调用动画
            # 关门
            else:
                if self.doorState[elevNo] == DOOR_OPENED:
                    self.doorState[elevNo] = DOOR_CLOSED
                    self.closeDoorAnimation(elevNo)
                    self.warnState[elevNo] = AVAILABLE    # 电梯启用

    def openDoorAnimation(self, elevNo):
        print("电梯{}开门".format(elevNo))
        # 两扇门的动画都要设置
        self.elevUI.doorAnims[2 * elevNo].setDirection(QAbstractAnimation.Forward)  # 正向设定动画
        self.elevUI.doorAnims[2 * elevNo + 1].setDirection(QAbstractAnimation.Forward)
        self.elevUI.doorAnims[2 * elevNo].start()  # 开始播放
        self.elevUI.doorAnims[2 * elevNo + 1].start()

    def closeDoorAnimation(self, elevNo):
        print("电梯{}关门".format(elevNo))
        self.elevUI.doorAnims[2 * elevNo].setDirection(QAbstractAnimation.Backward)  # 正向设定动画
        self.elevUI.doorAnims[2 * elevNo + 1].setDirection(QAbstractAnimation.Backward)
        self.elevUI.doorAnims[2 * elevNo].start()  # 开始播放
        self.elevUI.doorAnims[2 * elevNo + 1].start()

    # 警报控制函数
    def warnCtrl(self, elevNo):
        # 电梯此时为静止状态
        if self.elevState[elevNo] == ELEV_STILL and self.warnState[elevNo] == AVAILABLE:
            self.warnState[elevNo] = INAVAILABLE    # 电梯禁用
            self.elevUI.warnButtons[elevNo].setStyleSheet("border-image:url(resources/warn/warning.png)")
            self.MessBox = QtWidgets.QMessageBox.information(self.elevUI, "WARN", "电梯{}报警!".format(elevNo + 1))
            print("电梯{}报警".format(elevNo))

            # 内部电梯按钮禁用
            for btn in self.elevUI.inLevelButtons[elevNo]:
                btn.setEnabled(False)
            self.elevUI.openButtons[elevNo].setEnabled(False)  # 内部开关门按钮禁用
            self.elevUI.closeButtons[elevNo].setEnabled(False)
            self.elevUI.warnButtons[elevNo].setEnabled(False)  # 内部报警按钮禁用
            self.doorButtonState[elevNo] = NOPE  # 电梯按钮置空

    def updateState(self):
        for elevNo in range(self.elevNum):
            # 不可用电梯直接略过
            if self.comingList[elevNo] == INAVAILABLE:
                continue
            # 控制电梯门打开后关闭
            if self.animationState[elevNo] == WAIT_TIME_3:
                self.warnState[elevNo] = AVAILABLE  # 电梯启用
                print("关门")
                self.closeDoorAnimation(elevNo)  # 关门动画
                self.doorState[elevNo] = DOOR_CLOSED
                # 清空标志状态
                self.doorButtonState[elevNo] = NOPE
                self.animationState[elevNo] = NOPE
                continue
            if self.animationState[elevNo] == WAIT_TIME_2:
                # 从等待一到等待二
                print("开门后时间更长的等待")
                self.animationState[elevNo] = WAIT_TIME_3
                continue
            if self.doorButtonState[elevNo] == OPEN_DOOR:
                self.animationState[elevNo] = WAIT_TIME_2
                print("电梯{}等待接客".format(elevNo))
                continue

            # 处理命令队列
            if self.comingList[elevNo]:
                # 开门中，被锁死，略过
                if self.doorState[elevNo] == DOOR_OPENED:
                    continue
                # 静止状态，电梯转化为静止状态说明一些事务结束
                if self.elevState[elevNo] == ELEV_STILL:
                    print("电梯{}由静止状态到开门状态".format(elevNo))
                    self.openDoorAnimation(elevNo)
                    # 处理上下行并更新状态
                    targetFloor = self.comingList[elevNo][0]
                    if targetFloor > self.curFloor[elevNo]:  # 电梯上行
                        self.elevState[elevNo] = ELEV_UP
                        self.elevUI.screenUPLabels[elevNo].setStyleSheet("border-image:url(resources/screen/up.png)")
                    elif targetFloor < self.curFloor[elevNo]:   #电梯下行
                        self.elevState[elevNo] = ELEV_DOWN
                        self.elevUI.screenDWLabels[elevNo].setStyleSheet("border-image:url(resources/screen/down.png)")
                    else:
                        self.elevState[elevNo] = ELEV_UP
                        continue
                    self.animationState[elevNo] = READY_START   # 电梯动画就绪

                # 处理ready_start状态，关门动画
                if self.animationState[elevNo] == READY_START:
                    self.closeDoorAnimation(elevNo)
                    self.animationState[elevNo] = NOPE  # 动画状态置空
                # 结束状态->等待换客
                if self.animationState[elevNo] == READY_STOP:
                    self.animationState[elevNo] = WAIT_TIME
                    continue
                if self.animationState[elevNo] == WAIT_TIME:
                    self.comingList[elevNo].pop(0)  # 弹出当前任务
                    self.floorCmd[elevNo] = PASSANGER_NONE  # 乘客命令清空
                    self.closeDoorAnimation(elevNo)     # 关门动作
                    self.animationState[elevNo] = NOPE  # 动画清空
                    self.elevState[elevNo] = ELEV_STILL # 电梯停止
                    self.elevUI.screenUPLabels[elevNo].setStyleSheet("border-image:url(resources/screen/up_2.png)")
                    self.elevUI.screenDWLabels[elevNo].setStyleSheet("border-image:url(resources/screen/down_2.png)")
                # 电梯可用，处理未完成的命令
                elif self.warnState[elevNo] == AVAILABLE:
                    print("电梯可用，继续处理命令")
                    targetFloor = self.comingList[elevNo][0]
                    if targetFloor > self.curFloor[elevNo]:
                        self.elevState[elevNo] = ELEV_UP
                        self.curFloor[elevNo] += 1
                        self.elevUI.screenLevelLabels[elevNo].setProperty("value", self.curFloor[elevNo] + 1)
                        print("电梯{}显示楼层{},目标指令是{}".format(elevNo, self.curFloor[elevNo] + 1, targetFloor))
                    elif targetFloor < self.curFloor[elevNo]:
                        self.elevState[elevNo] = ELEV_DOWN
                        self.curFloor[elevNo] -= 1
                        self.elevUI.screenLevelLabels[elevNo].setProperty("value", self.curFloor[elevNo] + 1)
                    else:
                        #  内部电梯按钮复原
                        print("内部电梯按钮复原")
                        self.elevUI.inLevelButtons[elevNo][targetFloor].setEnabled(True)
                        self.elevUI.inLevelButtons[elevNo][targetFloor].setStyleSheet("font: 10pt \"AcadEref\";\n"
                                                                             "background-color: rgb(225, 225, 225);")
                        self.openDoorAnimation(elevNo)
                        self.elevUI.levelCmdButtons[2 * targetFloor].setStyleSheet(
                            "border-image:url(resources/btn/up_btn_normal.png)")
                        self.elevUI.levelCmdButtons[2 * targetFloor + 1].setStyleSheet(
                            "border-image:url(resources/btn/down_btn_normal.png)")
                        self.animationState[elevNo] = READY_STOP  # 运行-> 就绪停止

            # 处理反向命令队列
            elif self.reverseList[elevNo]:
                self.comingList[elevNo] = self.reverseList[elevNo].copy()
                self.reverseList[elevNo].clear()


