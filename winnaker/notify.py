import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from helpers import getScreenshotFiles
import logging
from os.path import join
from winnaker.settings import *


def send_mail(send_from, send_to, subject, text,
              server="localhost"):
    logging.info("Sending email")
    files = getScreenshotFiles()
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    with file(join(cfg_output_files_path, "winnaker.log")) as f:
        log_text = f.read()
    text = text + "\n" + log_text
    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(
                f)
            msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
