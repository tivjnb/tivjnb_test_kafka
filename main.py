from flask import Flask, request, jsonify
from confluent_kafka import Producer, Consumer
import json, logging
from os import environ

logger = logging.getLogger(__name__)
app = Flask(__name__)

KAFKA_HOST = environ.get("KAFKA_HOST")
KAFKA_PORT = environ.get("KAFKA_PORT")

c_config = {
    'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

p_config = {
    'bootstrap.servers': 'host.docker.internal:9092'
}

producer = Producer(p_config)

@app.route('/')
def ping():
    return "pong"


@app.route('/queue/set_data', methods=["POST"])
def set_data():
    data = request.json
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message = data['data']

    producer.produce(f"asutk_ms_{receiver_id}", key=sender_id, value=message)
    producer.flush()
    return jsonify({"message": "message was sent"}), 200


@app.route('/queue/get_data', methods=['GET'])
def get_data():
    consumer = Consumer(c_config)
    try:
        receiver_id = request.args.get('receiver_id')
        consumer.subscribe([f"asutk_ms_{receiver_id}"])
        msg = consumer.poll(timeout=4.0)
        if msg is None:
            return jsonify({"message": "There is no messages"}), 400
        data = json.loads(msg.value().decode('utf-8'))
        return jsonify({"message": data}), 200
    finally:
        consumer.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
