import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
import pika

from customs.custom_logger import my_logger
from conn_modd.models import Contact
import conn_modd.connect

def sms_notofocation(task: Contact):
    
    my_logger.log(f"Email successfully delivered to {task.phone_num}")
    return True

def callback(ch, method, properties, body):

    pk = body.decode()
    task = Contact.objects(id=pk, logic_field=False).first()
    if task:
        result = sms_notofocation(task)
        if result:
            # print(datetime().now())
            task.update(set__logic_field=True, set__date_of=datetime.now())
        else:
            my_logger.log('Failed during sms delivery!')
    else:
        my_logger.log("Empty data, I cant proceed further!")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    

def main():

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    queue = 'sms_'
    channel.queue_declare(queue=queue, durable=True)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)