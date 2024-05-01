import configparser
import sys
import asyncio
import os
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer

# 引入 ql 类
from ql import QL
from jd_cookie_uploader import get_jd_cookie, update_jd_cookie_to_ql

config_path = './config.ini'

address = "temp"
client_id = "temp"
client_secret = "temp"


def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# 添加用于从配置文件读取数据的函数
def read_config(config_file):
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        address = config.get("app", "address")
        client_id = config.get("app", "client_id")
        client_secret = config.get("app", "client_secret")
    except Exception as e:
        print(f"Error reading config file: {e}")
        address, client_id, client_secret = "temp", "temp", "temp"
    return address, client_id, client_secret


class JDQLApp(QWidget):
    def __init__(self):
        super().__init__()
        self.status_label = None
        # 读取配置文件
        self.address, self.client_id, self.client_secret = read_config(config_path)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 200)  # 设置窗口初始位置和大小
        self.setWindowTitle('JDQL App')  # 设置窗口标题
        self.setWindowIcon(QIcon('app_icon.png'))  # 设置窗口图标

        layout = QGridLayout()

        layout.addWidget(QLabel('Address:'), 0, 0)
        self.address_input = QLineEdit(self)
        self.address_input.setText(self.address)
        layout.addWidget(self.address_input, 0, 1)

        layout.addWidget(QLabel('Client ID:'), 1, 0)
        self.client_id_input = QLineEdit(self)
        self.client_id_input.setText(self.client_id)
        layout.addWidget(self.client_id_input, 1, 1)

        layout.addWidget(QLabel('Client Secret:'), 2, 0)
        self.client_secret_input = QLineEdit(self)
        self.client_secret_input.setText(self.client_secret)
        layout.addWidget(self.client_secret_input, 2, 1)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.onStartClicked)
        layout.addWidget(self.start_button, 3, 0, 1, 2)  # 占据两列空间

        # 添加一个用于显示消息的QLabel
        self.status_label = QLabel(self)
        self.status_label.setFont(QFont("Arial", 12))  # 设置字体和大小
        self.status_label.setAlignment(Qt.AlignCenter)  # 设置文本居中
        layout.addWidget(self.status_label, 4, 0, 1, 2)
        self.update_status("请点击开始按钮。")

        self.setLayout(layout)

    def update_status(self, message, success=True):
        """
        更新状态标签的文本。

        :param message: 要显示的消息。
        :param success: 消息是否表示操作成功。
        """
        if success:
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setStyleSheet("color: red;")
        self.status_label.setText(message)

    def onStartClicked(self):
        # 读取输入框中的内容
        address = self.address_input.text()
        client_id = self.client_id_input.text()
        client_secret = self.client_secret_input.text()

        # 创建QL实例并尝试登录
        ql = QL(address, client_id, client_secret)

        if not ql.valid:
            self.update_status("登录失败，请检查凭据。", success=False)
            # 5秒后退出
            QTimer.singleShot(5000, QApplication.instance().quit)
            return

        # 获取JD Cookie
        success, jd_cookie = asyncio.get_event_loop().run_until_complete(get_jd_cookie())

        if success and "pt_pin=" in jd_cookie:
            remark = jd_cookie[jd_cookie.find("pt_pin=") + 7:jd_cookie.find(";", jd_cookie.find("pt_pin="))]
            # 更新JD Cookie到青龙面板
            if update_jd_cookie_to_ql(ql, jd_cookie, remark):
                self.update_status("JD Cookie更新成功。")
                # 5秒后退出
                QTimer.singleShot(5000, QApplication.instance().quit)
            else:
                self.update_status("JD Cookie更新失败。", success=False)
        else:
            self.update_status("获取JD Cookie失败。", success=False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JDQLApp()
    ex.show()
    sys.exit(app.exec_())
