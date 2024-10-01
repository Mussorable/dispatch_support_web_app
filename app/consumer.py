from confluent_kafka import Consumer
from numpy.f2py.auxfuncs import throw_error


def create_consumer():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'test-consumers',
        'auto.offset.reset': 'earliest',
    })
    return consumer


def consume_messages(topic):
    consumer = create_consumer()
    print('Consumer created successfully')
    consumer.subscribe([topic])
    print('Consumer subscribed')

    try:
        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                print(f'Consumer error: {msg.error()}')
                continue

            print(f'Received message: {msg.value()}')
    except KeyboardInterrupt:
        throw_error('Received keyboard interrupt')
    finally:
        consumer.close()


if __name__ == '__main__':
    consume_messages('test-consumers')
