import asyncio
import json
import os
import pika
import sys

from fastapi_mail import FastMail, MessageSchema, MessageType
import jwt
from config.config import conf, settings


conn_params = pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='admin-mails', durable=True)
channel.queue_declare(queue='welcome-email', durable=True)
print("Waiting for messages. To exit press CTRL+C")


def main():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    async def welcome_callback(ch, method, properties, body):
        notice = json.loads(body.decode())
        token_data = {
            "id": notice["user"]["id"],
            "login": notice['user']['login']
        }

        token = jwt.encode(token_data, 'secret')
        print(token)
        message = MessageSchema(
                subject="Fastapi-Mail module",
                recipients=[notice["user"]["email"]],
                template_body={"link": f"http://localhost:8000/api/v1/users/verification?token={token}"},
                subtype=MessageType.html,
            )
        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
        print('sending')

    async def mailing_callback(ch, method, properties, body):
        notice = json.loads(body.decode())
        print(notice)
        message = MessageSchema(
                subject="Fastapi-Mail module",
                recipients=notice["emails"],
                template_body={
                    "text": notice["text"],
                    "title": notice["title"],
                    "image": "https://mcusercontent.com/597bc5462e8302e1e9db1d857/images/e27b9f2b-08d3-4736-b9b7-96e1c2d387fa.png"
                },
                subtype=MessageType.html,
            )
        fm = FastMail(conf)
        await fm.send_message(message, template_name="mail.html")
        print('sending')

    def receive_welcome(ch, method, properties, body):
        loop.run_until_complete(welcome_callback(ch, method, properties, body))

    def receive_admin_mailing(ch, method, properties, body):
        loop.run_until_complete(mailing_callback(ch, method, properties, body))

    channel.basic_consume(queue='welcome-email',
                          auto_ack=True,
                          on_message_callback=receive_welcome)
    channel.basic_consume(queue='admin-mails',
                          auto_ack=True,
                          on_message_callback=receive_admin_mailing)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        try:
            loop = asyncio.get_event_loop()
            sys.exit(0)
        except SystemExit:
            os._exit(0)