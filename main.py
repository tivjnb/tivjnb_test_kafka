from flask import Flask, request, jsonify
from confluent_kafka import Producer, Consumer
import json

app = Flask(__name__)

c_config = {
    'bootstrap.servers': 'host.docker.internal:9092',
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
    message = data['data']

    producer.produce('test_topic', key='key', value=message)
    producer.flush()
    return jsonify({"message": "message was sended"}), 200


@app.route('/queue/get_data', methods=['GET'])
def get_data():
    consumer = Consumer(c_config)
    try:
        consumer.subscribe(['test_topic'])
        msg = consumer.poll(timeout=4.0)
        if msg is None:
            return jsonify({"message": "There is no messages"}), 400
        data = json.loads(msg.value().decode('utf-8'))
        return jsonify({"message": data}), 200
    finally:
        consumer.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
