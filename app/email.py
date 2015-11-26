from flask import render_template, current_app
from flask.ext.mail import Message
from app import mail


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['PATHWAYS_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['PATHWAYS_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
