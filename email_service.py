import sendgrid

from nameko.rpc import rpc


class EmailService(object):
    name = "email_service"

    sg = sendgrid.SendGridClient('')

    @rpc
    def send_email(self, recipient, subject, body):
        message = sendgrid.Mail()
        message.add_to(recipient)
        message.set_from('test@getbellhops.com')
        message.set_subject(subject)
        message.set_html(body)

        self.sg.send(message)
