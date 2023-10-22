"""
My first application
"""
import toga
from toga.style.pack import COLUMN, ROW

import os
from functools import partial


ROOT = os.path.dirname(os.path.abspath(__file__))


class PackUp(toga.App):

    data_path = os.path.join(ROOT, "data.txt")
    
    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        # initialize
        self.datas = self.load_datas()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_page()
        self.main_window.show()

    def load_datas(self):
        datas = {
            "重要物品": [],
            "杂物": []
        }
        if os.path.exists(self.data_path):
            with open(self.data_path, "r") as f:
                metas = f.readlines()
                for meta in metas:
                    mtype, mname = meta.strip().split(" ")
                    datas[mtype].append(mname)
        return datas

    def add_handler(self, widget, type, name):
        type_text = type.value
        name_text = name.value

        if len(name_text) == 0:
            self.main_window.confirm_dialog("错误", "填入物品为空")
        elif name_text in self.datas[type_text]:
            self.main_window.confirm_dialog("错误", "物品已存在")
        else:
            self.datas[type_text].append(name_text)
            self.main_window.confirm_dialog("通过", "添加成功!")
        with open(self.data_path, "w", encoding='utf-8') as f:
            for key in self.datas:
                for item in self.datas[key]:
                    f.write(f"{key} {item}\n")

    def send_mail(self, widget):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.application import MIMEApplication

        # 163 mail url
        mail_host = 'smtp.163.com'
        # 163 username
        mail_user = "hujh960215@163.com"
        # secret
        # 163 auth，WIYIVGRXSZKNIIZM
        mail_pass = 'WIYIVGRXSZKNIIZM'
        # send and recieve mail
        sender = 'hujh960215@163.com'
        receivers = ['hujh960215@163.com']

        message = MIMEMultipart()
        message['Subject'] = 'PackUp text'
        message['From'] = sender
        message['To'] = receivers[0]

        # attachment
        with open(self.data_path, 'rb') as f:
            attachment = MIMEApplication(f.read(), _subtype='txt')
            attachment.add_header('Content-Disposition', 'attachment', filename='data.txt')
            message.attach(attachment)

        #
        try:
            # smtpObj.connect(mail_host,25)
            smtpObj = smtplib.SMTP_SSL(mail_host)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(
                sender,receivers,message.as_string())
            smtpObj.quit()
            self.main_window.confirm_dialog("通过", "邮件发送成功!")
        except smtplib.SMTPException as e:
            self.main_window.confirm_dialog("错误", f"{e}")

    def main_page(self):
        main_box = toga.Box()

        name_input, name_label = toga.TextInput(), toga.Label("名称")
        # 重要物品/杂物
        type_input, type_label = toga.Selection(items=['重要物品', '杂物']), toga.Label("类型")
        button_add = toga.Button("添加",
            on_press=partial(self.add_handler,
                type=type_input,
                name=name_input
            )
        )
        main_box.add(name_label)
        main_box.add(name_input)
        main_box.add(type_label)
        main_box.add(type_input)
        main_box.add(button_add)

        def clean_data(widget):
            try:
                os.remove(self.data_path)
                self.datas = {
                    "重要物品": [],
                    "杂物": []
                }
                self.main_window.confirm_dialog("通过", "删除成功!")
            except:
                self.main_window.confirm_dialog("错误", "删除失败!")

        button = toga.Button("物品列表", on_press=self.list_page)
        button_send = toga.Button("发送邮件", on_press=self.send_mail)
        button_clean = toga.Button("清空", on_press=clean_data)
        # button.style.padding = (0, 50, 0, 50)
        # button.style.flex = 1
        main_box.add(button)
        main_box.add(button_send)
        main_box.add(button_clean)

        main_box.style.update(direction=COLUMN)
        button_clean.style.update(padding=(50, 0, 0, 0))
        return main_box

    def list_page(self, widget):
        # 可滑动的窗口
        scroll_view = toga.ScrollContainer()
        list_box = toga.Box()

        def return_main(widget):
            self.main_window.content = self.main_page()

        button = toga.Button("返回", on_press=return_main)
        list_box.add(button)

        datas = self.load_datas()
        for key in datas:
            items = datas[key]
            key_label = toga.Label(f"{key} {len(items)}项")
            key_label.style.update(font_weight='bold', color='#ff0000')
            list_box.add(key_label)
            for idx in range(len(items)):
                item_label = toga.Label(f"idx {idx}: " + items[idx])
                list_box.add(item_label)
            list_box.add(toga.Label(""))
        list_box.style.update(direction=COLUMN)

        scroll_view.content = list_box
        self.main_window.content = scroll_view


def main():
    return PackUp(icon='resources/PackUp.png')
