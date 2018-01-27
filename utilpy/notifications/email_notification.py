import ConfigParser

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import socket
import getpass


config = ConfigParser.ConfigParser()


def init(conf_file):
    global config
    config.readfp(open(conf_file))


def get_host():
    return getpass.getuser() + '@' + socket.gethostname()


def plot2img(x, y):
    import StringIO
    import matplotlib.pyplot as plt 
    img = plt.plot(x, y)[0]
    output = StringIO.StringIO()
    plt.savefig(output)
    contents = output.getvalue()
    return contents


def send_mail(exp_name, additional_text='', x=None, y=None):
    global config
    email = config.get('email', 'email')
    password = config.get('email', 'pass')
    host = config.get('email', 'host')
    port = config.get('email', 'port')
    to = config.get('email', 'to')

    s = smtplib.SMTP(host, port)
    s.starttls()
    s.login(email, password)

    msg = MIMEMultipart()
    message = 'Hi {0},\nthe experiment {1} on: {2} is over.\nAdditional parameters: {3}\n\nyou can move on to your' \
              ' next experiment'.format(config.get('info', 'name'), exp_name, get_host(), additional_text)
    msg['Subject'] = "Experiment over"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    if x is not None and y is not None:
        image = MIMEImage(plot2img(x, y))
        msg.attach(image)

    # send the message via the server set up earlier.
    s.sendmail(email, to, msg.as_string())

    del msg
