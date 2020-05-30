# -*- coding: utf-8 -*-
'''
    SSRP推荐平台之自动发送邮件
'''
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import yagmail
from SSRP_recommend import SSRPRecommend


class YagSendMail(object):

    def __init__(self):
        self.csvname = SSRPRecommend().csvname
        self.main_email = 'zhaobowen9876@gmail.com'
        self.back1 = '506513024@qq.com'
        self.group = [self.main_email, self.back1]

    def automatic_send_mail(self):
        yag = yagmail.SMTP(user="841057707@qq.com", password="qviloameyckebfic", host="smtp.qq.com")
        content = ['自动邮件发送测试']
        try:
            yag.send(self.main_email, 'subject', content)
            print("邮件发送成功")
        except Exception as e:
            print(e)

    def automatic_send_group(self):
        yag = yagmail.SMTP(user="841057707@qq.com", password="qviloameyckebfic", host="smtp.qq.com")
        content = ['自动邮件发送测试']
        try:
            yag.send(self.group, 'subject', content)
            print("邮件发送成功")
        except Exception as e:
            print(e)

    def automatic_send_attachment(self):
        yag = yagmail.SMTP(user="841057707@qq.com", password="qviloameyckebfic", host="smtp.qq.com")
        content = ['自动邮件发送测试']
        try:
            yag.send(self.back1, '发送附件', content, [self.csvname])
            print("邮件发送成功")
        except Exception as e:
            print(e)


class SMTPSendMail(object):

    def automatic_send_mail(self):
        # 第三方 SMTP 服务
        mail_host = "smtp.qq.com"  # 设置服务器
        mail_user = "841057707@qq.com"  # 用户名
        mail_pass = "qviloameyckebfic"  # 口令

        sender = '841057707@qq.com'
        receivers = ['zhaobowen9876@gmail.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
        message['From'] = Header("菜鸟教程", 'utf-8')
        message['To'] = Header("测试", 'utf-8')

        subject = 'Python SMTP 邮件测试'
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 465)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print(e)
            print("Error: 无法发送邮件")


if __name__ == '__main__':
    yag = YagSendMail()
    yag.automatic_send_attachment()
    # smtp = SMTPSendMail()
    # smtp.automatic_send_mail()
