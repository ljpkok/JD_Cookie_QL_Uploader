import configparser
import sys
import asyncio
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
# 引入 ql 类
from jd_cookie_uploader import QL
from jd_cookie_uploader import get_jd_cookie
from jd_cookie_uploader import update_jd_cookie_to_ql


config_path = 'config.ini'

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
        self.address, self.client_id, self.client_secret = read_config(config_path)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.address_input = QLineEdit(self)
        self.address_input.setText(self.address)
        layout.addWidget(self.address_input)

        self.client_id_input = QLineEdit(self)
        self.client_id_input.setText(self.client_id)
        layout.addWidget(self.client_id_input)

        self.client_secret_input = QLineEdit(self)
        self.client_secret_input.setText(self.client_secret)
        layout.addWidget(self.client_secret_input)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.onStartClicked)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        self.setWindowTitle('JDQL App')

    def onStartClicked(self):
        address = self.address_input.text()
        client_id = self.client_id_input.text()
        client_secret = self.client_secret_input.text()
        # 在这里调用get_jd_cookie函数和更新青龙面板的逻辑
        ql = QL(address, client_id, client_secret)

        # 获取JD Cookie
        jd_cookie = asyncio.get_event_loop().run_until_complete(get_jd_cookie())

        if jd_cookie.find("pt_pin=") != -1:
            remark = jd_cookie[jd_cookie.find("pt_pin=") + 7:jd_cookie.find(";", jd_cookie.find("pt_pin="))]
            print(remark)
        # 更新JD Cookie到青龙面板
        update_jd_cookie_to_ql(ql, jd_cookie, remark)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JDQLApp()
    ex.show()
    sys.exit(app.exec_())
