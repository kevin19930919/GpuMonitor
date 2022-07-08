# The first step is always the same: import all necessary components:
import smtplib
from os.path import basename
from socket import gaierror
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import config
from cores.models import Record

def get_text_from_records(records):
    text = "Total Warning Items: " + str(len(records)) + " records\n\n\n"

    counter = 0
    for _record in records:
        counter = counter + 1
        
        text += "Item " + str(counter) + ":\n"
        text += "Website: " + _record.website + "\n"
        text += "Location: " + _record.location + "\n"
        text += "Product: " + _record.product.product_name + "\n"
        text += "Standard Price: " + str(_record.standard_price) + "\n"
        text += "Search Result: " + _record.title + "\n"
        text += "Search Price: " + str(_record.price) + "\n"
        text += "Link: <" + _record.url + ">\n"
        text += "Time: " + str(_record.create_time) + "\n\n\n"

    return text


def get_simple_list_text_from_records(records):
    text = ""

    counter = 0
    for _record in records:
        counter = counter + 1
        
        text += "Item " + str(counter) + ":\n"
        text += _record.title + "<" + _record.url + ">\n"
        text += "Searched Price: " + str(_record.price) + "\n\n"

    return text

def get_text_from_crawllogs(_crawllogs):
    text = "Error Logs: \n\n\n"

    for _crawllog in _crawllogs:        
        text += str(_crawllog.log_time) + "\n"
        text += _crawllog.website + "\n"
        text += _crawllog.location + "\n"
        text += _crawllog.message + "\n\n\n"

    return text

def send_mail(send_from, send_to, subject, text):
    # Now you can play with your code. Let’s define the SMTP server separately here:
    port = config.mail_port
    smtp_server = config.smtp_server
    login = config.smtp_login
    password = config.smtp_password

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    try:
        # Send your message with credentials specified above
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            # server.ehlo()
            # server.starttls()
            server.login(login, password)
            server.sendmail(send_from, send_to, msg.as_string())
    except (gaierror, ConnectionRefusedError):
        # tell the script to report if your message was sent or which errors need to be fixed
        print('Failed to connect to the server. Bad connection settings?')
    except smtplib.SMTPServerDisconnected as err:
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        print('SMTP error occurred: ' + str(e))
    else:
        print("Successfully sent to " + send_to)