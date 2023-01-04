import pika

from src.config.config import settings

conn_params = pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME, durable=True)


async def send_msg(notice):
    channel.basic_publish(exchange='',
                          routing_key='first-queue',
                          body=notice)
    print('ok')


# connection.close()
# docker run -d -p 5672:5672 --name rabbit rabbitmq