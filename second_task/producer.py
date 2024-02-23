import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pika
from faker import Faker
from random import choice

from conn_modd.models import Contact
import conn_modd.connect

fake = Faker('uk_UA')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

exchange = "web_08_exch"
queues = ["sms_", "email_"]

channel.exchange_declare(exchange=exchange, exchange_type='topic')
channel.queue_declare(queue=queues[0], durable=True)
channel.queue_bind(exchange=exchange, queue=queues[0], routing_key="sms_")

channel.queue_declare(queue=queues[1], durable=True)
channel.queue_bind(exchange=exchange, queue=queues[1], routing_key="email_")



def create_tasks(numbers: int=0):

    for i in range(numbers):
        task = Contact(fullname=fake.name(), email= fake.email(), phone_num=fake.phone_number()).save()

        channel.basic_publish(
                exchange=exchange,
                routing_key=choice(queues),
                body=str(task.id).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )
    connection.close()


if __name__ == "__main__":
    create_tasks(111)