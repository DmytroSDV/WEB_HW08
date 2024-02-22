import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import pika

from conn_modd.models import Contact
import conn_modd.connect

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

exchange = "web_08_exch"
queue = "web_08_qu"

channel.exchange_declare(exchange=exchange, exchange_type='direct')
channel.queue_declare(queue=queue, durable=True)
channel.queue_bind(exchange=exchange, queue=queue)

def create_tasks(nums: int=0):

    task = Contact(fullname="Noname").save()

    channel.basic_publish(
            exchange=exchange,
            routing_key=queue,
            body=str(task.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    connection.close()


if __name__ == "__main__":
    create_tasks()