import os
import json

from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from app.config import Config

consumer_config = {
    'bootstrap.servers': f'{Config.KAFKA_HOST}:{Config.KAFKA_PORT}',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

producer_config = {
    'bootstrap.servers': f'{Config.KAFKA_HOST}:{Config.KAFKA_PORT}'
}

class KafkaService:
    @staticmethod
    def send_message(receiver_id, sender_id, data):
        """
        Отправка сообщения в Kafka
        """
        topic = f"asutk_ms_{receiver_id}"
        producer =  Producer(producer_config)
        try:
            producer.produce(topic, key=str(sender_id), value=json.dumps(data))
            producer.flush()
        except Exception as e:
            raise RuntimeError(f"Failed to send message to Kafka: {str(e)}")

    @staticmethod
    def consume_message(receiver_id):
        """
        Получение последнего сообщения из Kafka
        """
        topic = f"asutk_ms_{receiver_id}"
        consumer = Consumer(consumer_config)

        consumer.subscribe([topic])

        try:
            msg = consumer.poll(timeout=5.0)
            if msg is None or msg.error():
                return None

            return json.loads(msg.value().decode('utf-8'))
        except KafkaException as e:
            raise RuntimeError(f"Failed to consume message from Kafka: {str(e)}")
        finally:
            consumer.close()


