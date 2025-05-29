import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.logger import setup_logger
import os
from dotenv import load_dotenv


class EmailSender:
    def __init__(self):
        self.logger = setup_logger()
        load_dotenv()
        self.sender_authorization_code = os.getenv("AUTHORIZATION_CODE")

    def send_email(self, email_from, email_to, email_subject, email_body):
        print(email_from, email_to, email_subject, email_body)
        message = MIMEMultipart()
        message["From"] = email_from
        message["To"] = email_to
        message["Subject"] = email_subject

        message.attach(MIMEText(email_body, "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.163.com", 465) as server:
                server.login(email_from, self.sender_authorization_code)
                text = message.as_string()
                server.sendmail(email_from, email_to, text)
            self.logger.info(f"邮件发送成功: 从 {email_from} 到 {email_to}, 主题: {email_subject}")
        except Exception as e:
            self.logger.error(f"邮件发送失败: {e}")
            raise e

if __name__ == '__main__':
    emailSender = EmailSender()
    emailSender.send_email("ieyujie@163.com",
                           "yujie@smartcitysz.com",
                           'test',
                           '这是一封测试邮件')