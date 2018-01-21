import ConfigParser

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import socket
import getpass


config = ConfigParser.ConfigParser()


def init(conf_file):
    global config
    config.readfp(open(conf_file))


def get_host():
    return getpass.getuser() + '@' + socket.gethostname()


def send_mail(exp_name, additional_params=''):
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
              ' next experiment'.format(config.get('info', 'name'), exp_name, get_host(), additional_params)
    msg['Subject'] = "Experiment over"

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.sendmail(email, to, msg.as_string())

    del msg
