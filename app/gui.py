from __init__ import api
from PyQt5.QtWidgets import QLineEdit, QWidget, QApplication, QLabel , QVBoxLayout, QPushButton, QTimeEdit
from PyQt5.QtCore import Qt, QTime, QThread
from PyQt5 import QtGui
import sys
import schedule
import time

#time1 = str(input())
#time2 = str(input())
#id = str(input())
#password = str(input())
ID = ""
PW = ""
Time1 = "16:02"
Time2 = "16:03"
k = 0
log = ""

def api_st():
    global log_dis
    log_dis.setText("작성 중")
    log_dis.setText(api(ID, PW))
    print(ID, PW)


def check():
    global Threading
    schedule.every().day.at(Time1).do(api_st)
    schedule.every().day.at(Time2).do(api_st)

    while Threading:
        schedule.run_pending()
        time.sleep(1)


#schedule.every().day.at(time1).do(check)

#while True:
#    schedule.run_pending()
#    time.sleep(1)
class Timer(QThread):
    def run(self):
        check()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.thread = Timer()
        self.initUI()

    def initUI(self):
        global id, password, btn, btn2, k, log_dis

        if time.localtime().tm_hour < 12:
            k = 0
        if time.localtime().tm_hour >= 12:
            k = 1


        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('양태빈&윤홍민의 합작품')

        lbl1 = QLabel('오전')
        lbl2 = QLabel('오후')
        lbl3 = QLabel('아이디')
        lbl4 = QLabel('비밀번호')
        lbl5 = QLabel("LOG")
        log_dis = QLabel("                                                    ")

        id = QLineEdit(self)
        id.textChanged[str].connect(self.setid)
        password = QLineEdit(self)
        password.setEchoMode(QLineEdit.Password)
        password.textChanged[str].connect(self.setpw)

        #time1 = QTimeEdit(self)
        #time1.setTime(QTime(9,00))
        #time1.setTimeRange(QTime(00, 00), QTime(12, 00))
        #time1.setDisplayFormat('hh:mm')
        #time1.timeChanged.connect(self.settime1)

        #time2 = QTimeEdit(self)
        #time2.setTime(QTime(13,00))
        #time2.setTimeRange(QTime(12, 00), QTime(24, 00))
        #time2.setDisplayFormat('hh:mm')
        #ime2.timeChanged.connect(self.settime2)


        btn = QPushButton('JAGAJINDAN ON', self)
        btn.toggled.connect(self.hongmin)
        #self.btn1.move(100, 150)
        btn.setCheckable(True)

        btn2 = QPushButton('JAGAJINDAN OFF', self)
        btn2.toggled.connect(self.turnoff)
        #self.btn1.move(100, 150)
        btn2.setCheckable(False)


        vbox = QVBoxLayout()
        vbox.addWidget(lbl3)
        vbox.addWidget(id)
        vbox.addWidget(lbl4)
        vbox.addWidget(password)
        vbox.addWidget(lbl1)
        #vbox.addWidget(time1)
        vbox.addWidget(lbl2)
        #vbox.addWidget(time2)
        vbox.addWidget(btn)
        vbox.addWidget(btn2)
        vbox.addWidget(lbl5)
        vbox.addWidget(log_dis)
        vbox.addStretch()

        self.setLayout(vbox)

        self.show()


    def setid(self, text):
        global ID
        ID = text


    def setpw(self, text):
        global PW
        PW = text

    def settime1(self, time):
        global Time1
        Time1 = str(time.toString("hh:mm"))

    def settime2(self, time):
        global Time2
        Time2 = str(time.toString("hh:mm"))


    def hongmin(self):
        global id, password, btn, btn2, Threading, log_dis
        id.setReadOnly(True)
        password.setReadOnly(True)
        btn.setCheckable(False)
        btn2.setCheckable(True)
        Threading = True
        self.thread.start()
        log_dis.setText("Turn On")

    def turnoff(self):
        global id, password, btn, btn2, Threading, log_dis
        id.setReadOnly(False)
        password.setReadOnly(False)
        btn.setCheckable(True)
        btn2.setCheckable(False)
        Threading = False
        self.thread.quit()
        schedule.clear()
        log_dis.setText("Turn Off")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = Window()

    sys.exit(app.exec_())
