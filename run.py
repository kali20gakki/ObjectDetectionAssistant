import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui_oda import *
from analysis import *
from augment import *
import time


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        self.btn_select_path.clicked.connect(self.select_analysis_dir)
        self.pushButton.clicked.connect(self.select_images_dir)
        self.pushButton_3.clicked.connect(self.select_labels_dir)
        self.pushButton_2.clicked.connect(self.select_output_dir)
        self.pushButton_4.clicked.connect(self.gen_dataset)
        self.btn_analysis.clicked.connect(self.start_analysis)

        self.actionhelp.triggered.connect(self.show_help)

    def select_analysis_dir(self):
        label_dir = QFileDialog.getExistingDirectory(
            self, "选取文件夹", "./")  # 起始路径
        self.lineEdit.setText(label_dir)
        print(self.comboBox.currentText())

    def select_images_dir(self):
        label_dir = QFileDialog.getExistingDirectory(
            self, "选取文件夹", "./")  # 起始路径
        self.lineEdit_2.setText(label_dir)

    def select_labels_dir(self):
        label_dir = QFileDialog.getExistingDirectory(
            self, "选取文件夹", "./")  # 起始路径
        self.lineEdit_3.setText(label_dir)

    def select_output_dir(self):
        label_dir = QFileDialog.getExistingDirectory(
            self, "选取文件夹", "./")  # 起始路径
        self.lineEdit_4.setText(label_dir)

    def start_analysis(self):
        if not self.lineEdit.text():
            QMessageBox.critical(self, "严重错误", "文件夹路径为空")
            return
        if self.label_analysis_status.text() != "分析中":
            self.label_analysis_status.setText("分析中")
            QMessageBox.information(self, "消息", "开始分析...")
            analysis(self.lineEdit.text(), self.comboBox.currentText())
            self.label_analysis_status.setText("完 成")

    def gen_dataset(self):
        if not self.lineEdit_2.text():
            QMessageBox.critical(self, "严重错误", "images路径为空")
            return
        elif not self.lineEdit_3.text():
            QMessageBox.critical(self, "严重错误", "labels路径为空")
            return
        elif not self.lineEdit_4.text():
            QMessageBox.critical(self, "严重错误", "output路径为空")
            return

        QMessageBox.information(self, "消息", "点击OK\n开始生成")

        flag_normal = flag_affine = flag_noise = flag_snow = flag_cloud = flag_fog = flag_snowflakes = flag_rain = flag_dropout = False

        if self.checkBox.checkState():
            flag_normal = True
        if self.checkBox_2.checkState():
            flag_affine = True
        if self.checkBox_3.checkState(): 
            flag_noise = True
        
        if self.radioButton_4.isChecked():
            flag_snow = True
        elif self.radioButton_5.isChecked():
            flag_cloud = True
        elif self.radioButton_6.isChecked():
            flag_fog = True
        elif self.radioButton_7.isChecked():
            flag_snowflakes = True
        elif self.radioButton_8.isChecked():
            flag_rain = True
        elif self.radioButton_9.isChecked():
            flag_dropout = True

        seq = get_seq(flag_normal, flag_affine, flag_noise, flag_snow, flag_cloud, flag_fog, flag_snowflakes, flag_rain, flag_dropout)

        start_num = int(self.lineEdit_5.text())

        try :
            if self.comboBox_3.currentText() == "0.5":
                print("0.5倍")
                start_num = augment_half(seq, self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), start_num=start_num, bbox_type=self.comboBox_2.currentText())
            elif self.comboBox_3.currentText() == "1":
                print("1倍")
                start_num = augment_half(seq, self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), start_num=start_num, bbox_type=self.comboBox_2.currentText())
                start_num = augment_half(seq, self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), start_num=start_num, bbox_type=self.comboBox_2.currentText())
            elif self.comboBox_3.currentText() == "2":
                print("2倍")
                start_num = augment_half(seq, self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), start_num=start_num, bbox_type=self.comboBox_2.currentText())
                start_num = augment_half(seq, self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), start_num=start_num, bbox_type=self.comboBox_2.currentText())
                start_num = augment_half(seq, self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), start_num=start_num, bbox_type=self.comboBox_2.currentText())
                start_num = augment_half(seq, self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), start_num=start_num, bbox_type=self.comboBox_2.currentText())

            QMessageBox.information(self, "消息", "生成完成！")
        except:
            QMessageBox.critical(self, "严重错误", "生成过程出错\n请检查报错信息后重试")



    def show_help(self):
        QMessageBox.information(
            self, "消息", "数据集分析：\nhbb(正框): class x y w h\nobb(斜框): class x1 y1 x2 y2 x3 y3 x4 y4")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
