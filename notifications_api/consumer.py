#!/usr/bin/env python
import asyncio
import json
import os

import pika
import sys

from fastapi_mail import FastMail, MessageSchema, MessageType
import jwt

from src.config.config import conf, settings
from src.models.events import Source, EventType

conn_params = pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME, durable=True)

print("Waiting for messages. To exit press CTRL+C")


def main():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    async def callback(ch, method, properties, body):
        notice = json.loads(body.decode())
        token_data = {
            "id": notice["user"]["id"],
            "login": notice['user']['login']
        }
        token = jwt.encode(token_data, 'secret')
        # token = jwt.encode(token_data, config_credentials["SECRET"])
        print('----------\n', token)
        if notice["source"] == Source.email:
            message = MessageSchema(
                subject="Fastapi-Mail module",
                recipients=[notice["user"]["email"]],
                template_body={"link": f"http://localhost:8000/api/v1/users/verification?token={token}"},
                subtype=MessageType.html,
            )
            fm = FastMail(conf)
            if notice["event_type"] == EventType.welcome_letter:
                await fm.send_message(message, template_name="email_template.html")
                print('sending')

    def receive(ch, method, properties, body):
        loop.run_until_complete(callback(ch, method, properties, body))

    channel.basic_consume(queue='first-queue',
                          auto_ack=True,
                          on_message_callback=receive)
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