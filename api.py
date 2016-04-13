from flask import Flask, request
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy


app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}

"""
{
    "body": "This is a test body",
    "recipient": "ablardo@gmail.com",
    "subject": "This is a test subject"
}
"""


@app.route('/email', methods=['POST'])
def email():
    """
    Micro Service Based Mail API
    This API is made with Flask, Flasgger and Nameko
    ---
    parameters:
      - name: email
        in: body
        required: true
        schema:
          id: data
          properties:
            recipient:
              type: string
              required: true
            subject:
              type: string
              required: true
            body:
              type: string
              required: true
    responses:
      200:
        description: A 200 to indicate if the email was sent.
    """
    recipient = request.json.get('recipient')
    subject = request.json.get('subject')
    body = request.json.get('body')

    # Any additional validation code goes here

    with ClusterRpcProxy(CONFIG) as rpc:
        # asynchronously spawning and email notification
        rpc.email_service.send_email.async(recipient, subject, body)
        return "Queued up your email"


@app.route('/text', methods=['POST'])
def text():
    """
    Micro Service Based Text API
    This API is made with Flask, Flasgger and Nameko
    ---
    parameters:
      - name: text
        in: body
        required: true
        schema:
          id: data
          properties:
            recipient:
              type: string
              required: true
            body:
              type: string
              required: true
    responses:
      200:
        description: A 200 to indicate if the text was sent.
    """
    recipient = request.json.get('recipient')
    body = request.json.get('body')

    # Validation code here, can also be a service call or a local
    # implementation.
    with ClusterRpcProxy(CONFIG) as rpc:
        # asynchronously spawning and email notification
        # rpc.twilio_service.send_text.async({"recipient": recipient, "body": body})
        rpc.event_dispatcher.send_event({"type": "send_text", "recipient": recipient, "body": body})

    return "Your text message has been queued."


app.run(debug=True)
