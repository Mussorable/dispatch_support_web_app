import asyncio

from aiokafka import AIOKafkaProducer


def delivery_report(err, msg):
    if err is not None:
        print(f'Delivery failed: {err}')
    else:
        print(f'Delivery successful to {msg.topic()} {msg.partition()}')


async def create_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092',
    )

    await producer.start()

    try:
        await producer.send_and_wait('test-consumers', key=b'key', value=b'hello-kafka')
    finally:
        await producer.stop()
    # return producer

if __name__ == '__main__':
    asyncio.run(create_producer())
# docker stop fervent_elgamal
# docker rm fervent_elgamal
# docker run -d --name fervent_elgamal -p 9092:9092 apache/kafka:3.8.0
