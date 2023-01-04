import pika

from src.config.config import settings

conn_params = pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='admin-mails', durable=True)


async def send_msg(notice) -> None:
    channel.basic_publish(exchange='',
                          routing_key='admin-mails',
                          body=notice)
    print('ok')


connection.close()
